#!/usr/bin/env python3
"""AP17 — Return Transformation and Physical Readability Smoke Test.

Claim tier:
- linear identities: exact algebra in the declared finite model
- runtime outputs: finite_diagnostic
- physical interpretation: Dr
- universal nonlinear return: Open
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad


def matrix_rank(a: np.ndarray, tol: float = 1e-10) -> int:
    return int(np.linalg.matrix_rank(a, tol=tol))


def json_default(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def gaussian_mutual_information(
    K: np.ndarray, Sigma_x: np.ndarray, Sigma_eta: np.ndarray
) -> float:
    """I(x;y) in bits for y=Kx+eta with independent Gaussian x and eta."""
    sx_half = np.linalg.cholesky(Sigma_x)
    middle = sx_half.T @ K.T @ np.linalg.solve(Sigma_eta, K @ sx_half)
    sign, logdet = np.linalg.slogdet(np.eye(middle.shape[0]) + middle)
    if sign <= 0:
        raise ValueError("Non-positive determinant in mutual information")
    return float(0.5 * logdet / np.log(2.0))


def gls_decoder(K: np.ndarray, Sigma_eta: np.ndarray, tol: float = 1e-12):
    fisher = K.T @ np.linalg.solve(Sigma_eta, K)
    if matrix_rank(fisher, tol) < fisher.shape[0]:
        return None, fisher
    decoder = np.linalg.solve(fisher, K.T @ np.linalg.inv(Sigma_eta))
    return decoder, fisher


def stacked_observation_operator(F: np.ndarray, C: np.ndarray, L: int) -> np.ndarray:
    return np.vstack([C @ np.linalg.matrix_power(F, i) for i in range(L + 1)])


def run() -> dict:
    gamma = 0.12
    omega = 1.7
    F_H = np.array([[-gamma, -omega], [omega, -gamma]])

    # Full-rank transformed return.
    tau = 0.8
    W = np.array([[1.0, 0.25], [0.15, 0.9]])
    R = np.array([[0.75, -0.10], [0.20, 0.65]])
    K = R @ expm(F_H * tau) @ W
    Sigma_x = np.eye(2)
    Sigma_eta = (0.04**2) * np.eye(2)
    decoder, fisher = gls_decoder(K, Sigma_eta)
    decode_error = float(np.linalg.norm(decoder @ K - np.eye(2), ord=2))
    rank_full = matrix_rank(K)
    distance_identity = float(np.linalg.norm(K - np.eye(2), ord=2))
    info_full = gaussian_mutual_information(K, Sigma_x, Sigma_eta)
    whitened = np.linalg.solve(
        np.linalg.cholesky(Sigma_eta),
        K @ np.linalg.cholesky(Sigma_x),
    )
    svals = np.linalg.svd(whitened, compute_uv=False)

    # Partial return.
    R_partial = np.array([[1.0, 0.0], [0.0, 0.0]])
    K_partial = R_partial @ expm(F_H * tau) @ W
    rank_partial = matrix_rank(K_partial)
    info_partial = gaussian_mutual_information(K_partial, Sigma_x, Sigma_eta)
    partial_decoder, _ = gls_decoder(K_partial, Sigma_eta)

    # No direct return.
    K_zero = np.zeros_like(K)
    rank_zero = matrix_rank(K_zero)
    info_zero = gaussian_mutual_information(K_zero, Sigma_x, Sigma_eta)

    # Delayed echo.
    W_echo = np.array([[1.0], [0.0]])
    R_echo = np.array([[0.0, 1.0]])
    taus = np.linspace(0.0, 8.0, 1601)
    echo_kernel = np.array(
        [float((R_echo @ expm(F_H * t) @ W_echo)[0, 0]) for t in taus]
    )
    idx = int(np.argmax(np.abs(echo_kernel)))
    tau_echo = float(taus[idx])
    echo_amplitude = float(echo_kernel[idx])

    # Hidden-sector elimination.
    lambda_o = 0.4
    W_scalar = np.array([[0.7], [-0.2]])
    R_scalar = np.array([[0.3, 0.5]])
    A_full = np.block(
        [[np.array([[-lambda_o]]), R_scalar], [W_scalar, F_H]]
    )
    x0 = np.array([1.0, 0.25, -0.10])

    def full_state(t: float) -> np.ndarray:
        return expm(A_full * t) @ x0

    errors = []
    for t in np.linspace(0.0, 4.0, 81):
        x = full_state(float(t))
        o = float(x[0])
        lhs = float((A_full @ x)[0])
        hidden_initial = float((R_scalar @ expm(F_H * t) @ x0[1:])[0])

        def integrand(s: float) -> float:
            o_s = float(full_state(s)[0])
            kernel = float(
                (R_scalar @ expm(F_H * (t - s)) @ W_scalar)[0, 0]
            )
            return kernel * o_s

        convolution = quad(
            integrand, 0.0, float(t), epsabs=1e-11, epsrel=1e-11, limit=200
        )[0]
        rhs = -lambda_o * o + hidden_initial + convolution
        errors.append(abs(lhs - rhs))

    elimination_error = float(max(errors))

    # Finite-window readability.
    dt = 0.25
    F_sample = expm(A_full * dt)
    C_sample = np.array([[1.0, 0.0, 0.0]])
    Sigma_x3 = np.eye(3)
    sigma_y = 0.05
    windows = []
    for L in [0, 1, 2, 4, 8, 16]:
        G_L = stacked_observation_operator(F_sample, C_sample, L)
        Sigma_N = (sigma_y**2) * np.eye(G_L.shape[0])
        windows.append(
            {
                "samples": L + 1,
                "rank": matrix_rank(G_L),
                "nullity": int(3 - matrix_rank(G_L)),
                "information_bits": gaussian_mutual_information(
                    G_L, Sigma_x3, Sigma_N
                ),
            }
        )

    gates = {
        "transformed_return_is_not_identity": distance_identity > 0.1,
        "transformed_return_is_full_rank": rank_full == 2,
        "known_decoder_recovers_noiseless_input": decode_error < 1e-10,
        "partial_return_is_rank_deficient": rank_partial == 1,
        "zero_return_has_zero_information": abs(info_zero) < 1e-12
        and rank_zero == 0,
        "echo_is_delayed": tau_echo > 0.1
        and abs(echo_amplitude) > 0.1
        and abs(echo_kernel[0]) < 1e-12,
        "hidden_elimination_identity_matches_full_system": elimination_error < 1e-9,
        "longer_window_improves_rank": windows[0]["rank"] < windows[-1]["rank"],
    }

    return {
        "meta": {
            "artifact": "AP17",
            "title": "Return Transformation and Physical Readability Smoke Test",
            "version": "0.4.0-return",
            "tier": "finite_diagnostic",
        },
        "equations": {
            "return_kernel": (
                "K_{alpha<-beta}(tau)=A_alpha O_alpha R_alpha "
                "U_H(tau) H_beta W_beta O_beta E_beta"
            ),
            "linear_hidden_propagator": "U_H(tau)=exp(F_H tau)",
            "gaussian_readability": (
                "I=1/2 log2 det(I+Sigma_x^(1/2) K^T "
                "Sigma_eta^(-1) K Sigma_x^(1/2))"
            ),
            "finite_window_operator": "G_L=stack(C,CF,...,CF^L)",
            "hidden_elimination_kernel": "K_mem(t)=R exp(F_H t) W",
        },
        "transformed_return": {
            "tau": tau,
            "kernel": K.tolist(),
            "rank": rank_full,
            "singular_values_noise_whitened": svals.tolist(),
            "distance_from_identity_operator_norm": distance_identity,
            "noiseless_decode_identity_error": decode_error,
            "gaussian_readable_information_bits": info_full,
        },
        "partial_return": {
            "rank": rank_partial,
            "nullity": int(2 - rank_partial),
            "gaussian_readable_information_bits": info_partial,
            "full_decoder_exists": partial_decoder is not None,
        },
        "no_direct_return": {
            "rank": rank_zero,
            "gaussian_readable_information_bits": info_zero,
        },
        "echo": {
            "tau_echo": tau_echo,
            "amplitude": echo_amplitude,
            "kernel_at_zero": float(echo_kernel[0]),
        },
        "hidden_elimination": {"max_absolute_residual": elimination_error},
        "finite_window_readability": windows,
        "gates": gates,
        "verdict": "PASS" if all(gates.values()) else "FAIL",
        "claim_boundary": {
            "linear_return_kernel": "exact_algebra_in_declared_scope",
            "gaussian_mutual_information": (
                "exact_for_declared_linear_Gaussian_channel"
            ),
            "runtime": "finite_diagnostic",
            "nonlinear_universal_return": "Open",
            "all_retained_states_eventually_return": "not_claimed",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="ap/results/AP17_RETURN_TRANSFORMATION_RESULTS.json",
    )
    args = parser.parse_args()
    result = run()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, default=json_default), encoding="utf-8")
    print(json.dumps({
        "verdict": result["verdict"],
        "decode_error": result["transformed_return"][
            "noiseless_decode_identity_error"
        ],
        "echo_time": result["echo"]["tau_echo"],
        "hidden_elimination_error": result["hidden_elimination"][
            "max_absolute_residual"
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
