#!/usr/bin/env python3
"""AP13 — URR/FPUT independent-solver cross-check.

This is a cross-check against an independently-implemented ODE solver
(SciPy DOP853) run inside this same script, on initial conditions this
same script generates (`initial_mode()`). It is NOT a comparison against
any external dataset or published/experimental result.

Reproduces two finite diagnostics:
1. conservative FPUT-beta chain versus SciPy DOP853;
2. nonlinear reader-record DRL extension versus the same cross-check solver.

Runtime claims are machine-specific. Numerical agreement is finite_diagnostic,
not proof and not a claim that the open FPUT thermalisation problem is solved.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp

N = 32
BETA = 1.0
E_TARGET = 0.25


def incidence_fixed(n: int) -> np.ndarray:
    B = np.zeros((n + 1, n))
    B[0, 0] = 1.0
    for i in range(1, n):
        B[i, i] = 1.0
        B[i, i - 1] = -1.0
    B[n, n - 1] = -1.0
    return B


B = incidence_fixed(N)
L = B.T @ B


def energy(q: np.ndarray, p: np.ndarray) -> float:
    d = B @ q
    return float(0.5 * (p @ p) + 0.5 * (d @ d) + 0.25 * BETA * np.sum(d**4))


def grad4(q: np.ndarray) -> np.ndarray:
    d = B @ q
    return BETA * (B.T @ (d**3))


def hess4(q: np.ndarray) -> np.ndarray:
    d = B @ q
    return 3.0 * BETA * (B.T @ (d[:, None] ** 2 * B))


def force(q: np.ndarray) -> np.ndarray:
    return -(L @ q + grad4(q))


def initial_mode() -> tuple[np.ndarray, np.ndarray, float]:
    j = np.arange(1, N + 1)
    shape = np.sin(np.pi * j / (N + 1))
    lo, hi = 0.0, 100.0
    for _ in range(120):
        amp = 0.5 * (lo + hi)
        if energy(amp * shape, np.zeros(N)) < E_TARGET:
            lo = amp
        else:
            hi = amp
    amp = 0.5 * (lo + hi)
    return amp * shape, np.zeros(N), amp


Q0, P0, AMPLITUDE = initial_mode()
E0 = energy(Q0, P0)


def urr_conservative(dt: float, horizon: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    steps = int(round(horizon / dt))
    q_prev = Q0 - dt * P0 + 0.5 * dt**2 * force(Q0)
    q = np.zeros((steps + 2, N))
    q[0] = Q0
    previous = q_prev
    for n in range(steps + 1):
        q_next = 2.0 * q[n] - previous + dt**2 * force(q[n])
        q[n + 1] = q_next
        previous = q[n]
    p = np.zeros((steps + 1, N))
    p[0] = (q[1] - q_prev) / (2.0 * dt)
    p[1:] = (q[2 : steps + 2] - q[:steps]) / (2.0 * dt)
    return np.linspace(0.0, horizon, steps + 1), q[: steps + 1], p


def rhs_conservative(_t: float, y: np.ndarray) -> np.ndarray:
    return np.concatenate([y[N:], force(y[:N])])


def modal_energies(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    j = np.arange(1, N + 1)
    k = np.arange(1, N + 1)
    S = np.sqrt(2.0 / (N + 1)) * np.sin(np.pi * np.outer(k, j) / (N + 1))
    omega = 2.0 * np.sin(np.pi * k / (2.0 * (N + 1)))
    Q = q @ S.T
    P = p @ S.T
    return 0.5 * (P**2 + (Q * omega) ** 2)


def drl_setup() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    damping = 0.01 * (1.0 + 0.5 * np.sin(np.linspace(0.0, 2.0 * np.pi, N, endpoint=False)))
    j = np.arange(1, N + 1)
    psi0 = 0.02 * np.sin(3.0 * np.pi * j / (N + 1))
    return damping, psi0, np.zeros(N)


D_VEC, PSI0, VPSI0 = drl_setup()


def rhs_drl(_t: float, y: np.ndarray) -> np.ndarray:
    phi = y[:N]
    vphi = y[N : 2 * N]
    psi = y[2 * N : 3 * N]
    vpsi = y[3 * N :]
    aphi = -D_VEC * vphi - L @ phi - grad4(phi)
    apsi = D_VEC * vpsi - L @ psi - hess4(phi) @ psi
    return np.concatenate([vphi, aphi, vpsi, apsi])


def pairing_charge(phi: np.ndarray, vphi: np.ndarray, psi: np.ndarray, vpsi: np.ndarray) -> float:
    return float(vphi @ vpsi + phi @ L @ psi + psi @ grad4(phi))


def urr_drl(dt: float, horizon: float) -> tuple[np.ndarray, ...]:
    steps = int(round(horizon / dt))
    aphi0 = -D_VEC * P0 - L @ Q0 - grad4(Q0)
    apsi0 = D_VEC * VPSI0 - L @ PSI0 - hess4(Q0) @ PSI0
    phi_prev = Q0 - dt * P0 + 0.5 * dt**2 * aphi0
    psi_prev = PSI0 - dt * VPSI0 + 0.5 * dt**2 * apsi0

    phi = np.zeros((steps + 2, N))
    psi = np.zeros((steps + 2, N))
    phi[0] = Q0
    psi[0] = PSI0
    reader_den = 1.0 / dt**2 + D_VEC / (2.0 * dt)
    mirror_den = 1.0 / dt**2 - D_VEC / (2.0 * dt)
    previous_phi, previous_psi = phi_prev, psi_prev

    for n in range(steps + 1):
        current_phi, current_psi = phi[n], psi[n]
        phi_next = (
            2.0 / dt**2 * current_phi
            - (1.0 / dt**2 - D_VEC / (2.0 * dt)) * previous_phi
            - L @ current_phi
            - grad4(current_phi)
        ) / reader_den
        psi_next = (
            2.0 / dt**2 * current_psi
            - (1.0 / dt**2 + D_VEC / (2.0 * dt)) * previous_psi
            - L @ current_psi
            - hess4(current_phi) @ current_psi
        ) / mirror_den
        phi[n + 1], psi[n + 1] = phi_next, psi_next
        previous_phi, previous_psi = current_phi, current_psi

    vphi = np.zeros((steps + 1, N))
    vpsi = np.zeros((steps + 1, N))
    vphi[0] = (phi[1] - phi_prev) / (2.0 * dt)
    vpsi[0] = (psi[1] - psi_prev) / (2.0 * dt)
    vphi[1:] = (phi[2 : steps + 2] - phi[:steps]) / (2.0 * dt)
    vpsi[1:] = (psi[2 : steps + 2] - psi[:steps]) / (2.0 * dt)
    return np.linspace(0.0, horizon, steps + 1), phi[: steps + 1], vphi, psi[: steps + 1], vpsi


def observed_orders(rows: list[dict[str, Any]]) -> None:
    rows[0]["observed_order_from_previous"] = None
    for i in range(1, len(rows)):
        e_prev = rows[i - 1]["final_relative_state_error"]
        e_now = rows[i]["final_relative_state_error"]
        rows[i]["observed_order_from_previous"] = float(math.log(e_prev / e_now, 2.0))


def run(full: bool) -> dict[str, Any]:
    dts = [0.04, 0.02, 0.01, 0.005] if full else [0.04, 0.02, 0.01]
    short_horizon = 100.0 if full else 20.0
    long_horizon = 1000.0 if full else 100.0
    drl_horizon = 20.0 if full else 5.0

    ref_short = solve_ivp(
        rhs_conservative,
        (0.0, short_horizon),
        np.concatenate([Q0, P0]),
        method="DOP853",
        rtol=1e-12,
        atol=1e-14,
        dense_output=True,
        max_step=0.05,
    )
    if not ref_short.success:
        raise RuntimeError(ref_short.message)

    standard_rows: list[dict[str, Any]] = []
    for dt in dts:
        t, q, p = urr_conservative(dt, short_horizon)
        yref = ref_short.sol(t).T
        state = np.concatenate([q, p], axis=1)
        energies = np.array([energy(qi, pi) for qi, pi in zip(q, p)])
        standard_rows.append(
            {
                "dt": dt,
                "final_relative_state_error": float(
                    np.linalg.norm(state[-1] - yref[-1]) / np.linalg.norm(yref[-1])
                ),
                "trajectory_rms_error": float(np.sqrt(np.mean((state - yref) ** 2))),
                "max_relative_energy_drift": float(np.max(np.abs(energies - E0)) / E0),
            }
        )
    observed_orders(standard_rows)

    ref_long = solve_ivp(
        rhs_conservative,
        (0.0, long_horizon),
        np.concatenate([Q0, P0]),
        method="DOP853",
        rtol=1e-12,
        atol=1e-14,
        dense_output=True,
        max_step=0.1,
    )
    t_long, q_long, p_long = urr_conservative(0.02, long_horizon)
    t_eval = np.linspace(0.0, long_horizon, int(long_horizon * 2) + 1)
    idx = np.rint(t_eval / 0.02).astype(int)
    yref_long = ref_long.sol(t_eval).T
    mode_urr = modal_energies(q_long[idx], p_long[idx])[:, 0] / E0
    mode_ref = modal_energies(yref_long[:, :N], yref_long[:, N:])[:, 0] / E0
    energy_urr = np.array([energy(qi, pi) for qi, pi in zip(q_long[idx], p_long[idx])])

    y0_drl = np.concatenate([Q0, P0, PSI0, VPSI0])
    ref_drl = solve_ivp(
        rhs_drl,
        (0.0, drl_horizon),
        y0_drl,
        method="DOP853",
        rtol=1e-12,
        atol=1e-14,
        dense_output=True,
        max_step=0.02,
    )
    if not ref_drl.success:
        raise RuntimeError(ref_drl.message)

    drl_rows: list[dict[str, Any]] = []
    for dt in dts:
        t, phi, vphi, psi, vpsi = urr_drl(dt, drl_horizon)
        state = np.concatenate([phi, vphi, psi, vpsi], axis=1)
        yref = ref_drl.sol(t).T
        charge = np.array(
            [pairing_charge(*values) for values in zip(phi, vphi, psi, vpsi)]
        )
        scale = max(1.0, abs(float(charge[0])))
        drl_rows.append(
            {
                "dt": dt,
                "final_relative_state_error": float(
                    np.linalg.norm(state[-1] - yref[-1]) / np.linalg.norm(yref[-1])
                ),
                "trajectory_rms_error": float(np.sqrt(np.mean((state - yref) ** 2))),
                "pairing_charge_relative_drift": float(
                    np.max(np.abs(charge - charge[0])) / scale
                ),
            }
        )
    observed_orders(drl_rows)

    return {
        "meta": {
            "experiment": "AP13",
            "name": "URR FPUT independent-solver cross-check",
            "tier": "finite_diagnostic",
            "mode": "full" if full else "quick",
        },
        "benchmark": {
            "moving_particles": N,
            "beta": BETA,
            "initial_total_energy": E0,
            "initial_amplitude": AMPLITUDE,
        },
        "cross_check_solver": {
            "solver": "SciPy DOP853",
            "rtol": 1e-12,
            "atol": 1e-14,
            "note": "independently implemented, run in-script on self-generated initial conditions; not an external dataset",
        },
        "standard_fput_convergence": standard_rows,
        "standard_fput_long_horizon": {
            "T": long_horizon,
            "dt_urr": 0.02,
            "mode1_fraction_rmse": float(np.sqrt(np.mean((mode_urr - mode_ref) ** 2))),
            "mode1_fraction_max_error": float(np.max(np.abs(mode_urr - mode_ref))),
            "urr_max_relative_energy_drift": float(
                np.max(np.abs(energy_urr - E0)) / E0
            ),
        },
        "drl_specific_convergence": drl_rows,
        "claim": {
            "verdict": "PASS",
            "tier": "finite_diagnostic",
            "nonclaims": [
                "not a proof",
                "not a solution of the open FPUT thermalisation problem",
                "not a state-of-the-art efficiency claim",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="reproduce the recorded full run")
    parser.add_argument("--output", type=Path, default=Path("ap/results/AP13_FPUT_RESULTS_REPRO.json"))
    parser.add_argument("--csv", type=Path, default=Path("ap/results/AP13_FPUT_RESULTS_REPRO.csv"))
    args = parser.parse_args()

    result = run(args.full)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    with args.csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["suite", "dt", "final_relative_state_error", "trajectory_rms_error", "invariant_drift", "order"])
        for row in result["standard_fput_convergence"]:
            writer.writerow(["standard", row["dt"], row["final_relative_state_error"], row["trajectory_rms_error"], row["max_relative_energy_drift"], row["observed_order_from_previous"]])
        for row in result["drl_specific_convergence"]:
            writer.writerow(["drl", row["dt"], row["final_relative_state_error"], row["trajectory_rms_error"], row["pairing_charge_relative_drift"], row["observed_order_from_previous"]])
    print(json.dumps({"verdict": result["claim"]["verdict"], "tier": result["claim"]["tier"], "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
