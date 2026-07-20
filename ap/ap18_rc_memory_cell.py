#!/usr/bin/env python3
"""AP18 — Two-Capacitor RC Memory Cell.

A reproducible ideal-circuit test of:
- analytic vs numerical dynamics;
- declared charge retention;
- resistor energy accounting;
- exact linear hidden-sector elimination;
- hidden-state readability through a visible-only time trace;
- two-state observability.

This is a finite diagnostic. It is not a hardware validation and does not test
the inertial DRL term or an ontic interpretation of Psi.
"""
from pathlib import Path
import argparse
import json
import math
import platform

import numpy as np
import scipy
from scipy.integrate import solve_ivp, trapezoid
from scipy.linalg import expm


def run() -> dict:
    R_ohm = 10_000.0
    C1 = 100e-6
    C2 = 100e-6
    V10 = 5.0
    V20 = 0.0
    t_end = 5.0
    n_samples = 10_001
    times = np.linspace(0.0, t_end, n_samples)

    A = np.array([
        [-1.0 / (R_ohm * C1), 1.0 / (R_ohm * C1)],
        [1.0 / (R_ohm * C2), -1.0 / (R_ohm * C2)],
    ])
    x0 = np.array([V10, V20])

    solution = solve_ivp(
        lambda _t, x: A @ x,
        (0.0, t_end),
        x0,
        t_eval=times,
        rtol=1e-12,
        atol=1e-14,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    x_num = solution.y.T
    x_exact = np.array([expm(A * t) @ x0 for t in times])

    tau_diff = R_ohm * C1 / 2.0
    v_avg = (C1 * V10 + C2 * V20) / (C1 + C2)
    delta0 = V10 - V20
    x_closed = np.column_stack([
        v_avg + 0.5 * delta0 * np.exp(-times / tau_diff),
        v_avg - 0.5 * delta0 * np.exp(-times / tau_diff),
    ])

    max_num_vs_matrix = float(np.max(np.abs(x_num - x_exact)))
    max_matrix_vs_closed = float(np.max(np.abs(x_exact - x_closed)))

    charge = C1 * x_num[:, 0] + C2 * x_num[:, 1]
    charge0 = float(charge[0])
    charge_abs = float(np.max(np.abs(charge - charge0)))
    charge_rel = float(charge_abs / abs(charge0))

    energy_caps = 0.5 * C1 * x_num[:, 0] ** 2 + 0.5 * C2 * x_num[:, 1] ** 2
    power_R = (x_num[:, 0] - x_num[:, 1]) ** 2 / R_ohm
    energy_R = np.zeros_like(times)
    energy_R[1:] = np.cumsum(
        0.5 * (power_R[1:] + power_R[:-1]) * np.diff(times)
    )
    energy_accounted = energy_caps + energy_R
    energy_abs = float(np.max(np.abs(energy_accounted - energy_caps[0])))
    energy_rel = float(energy_abs / energy_caps[0])

    F_OO = -1.0 / (R_ohm * C1)
    R_return = 1.0 / (R_ohm * C1)
    W_write = 1.0 / (R_ohm * C2)
    F_H = -1.0 / (R_ohm * C2)

    check_indices = np.linspace(0, len(times) - 1, 201, dtype=int)
    residuals = []
    for index in check_indices:
        t = float(times[index])
        lhs = float((A @ x_num[index])[0])
        hidden_initial = R_return * math.exp(F_H * t) * V20
        if index == 0:
            convolution = 0.0
        else:
            history_times = times[:index + 1]
            integrand = (
                R_return
                * np.exp(F_H * (t - history_times))
                * W_write
                * x_num[:index + 1, 0]
            )
            convolution = float(trapezoid(integrand, history_times))
        rhs_reduced = (
            F_OO * float(x_num[index, 0])
            + hidden_initial
            + convolution
        )
        residuals.append(abs(lhs - rhs_reduced))
    hidden_residual = float(max(residuals))

    x_a0 = np.array([0.0, 0.0])
    x_b0 = np.array([0.0, 1.0])
    x_a = np.array([expm(A * t) @ x_a0 for t in times])
    x_b = np.array([expm(A * t) @ x_b0 for t in times])
    delta_y = x_b[:, 0] - x_a[:, 0]
    max_hidden_signal = float(np.max(np.abs(delta_y)))

    C_read = np.array([[1.0, 0.0]])
    observation = np.vstack([C_read, C_read @ A])
    observation_rank = int(np.linalg.matrix_rank(observation))
    observation_determinant = float(np.linalg.det(observation))

    initial_energy = float(energy_caps[0])
    final_energy_exact = float(0.5 * (C1 + C2) * v_avg ** 2)
    resistor_loss_exact = float(initial_energy - final_energy_exact)

    sample_times = [0.0, 0.25, 0.5, 1.0, 2.0, 5.0]
    samples = []
    for sample_time in sample_times:
        index = int(np.argmin(np.abs(times - sample_time)))
        samples.append({
            "t_s": float(sample_time),
            "V1_V": float(x_num[index, 0]),
            "V2_V": float(x_num[index, 1]),
            "charge_C": float(charge[index]),
            "capacitor_energy_J": float(energy_caps[index]),
            "resistor_energy_J": float(energy_R[index]),
            "hidden_history_signal_V": float(delta_y[index]),
        })

    gates = {
        "numerical_matches_matrix_exponential":
            bool(max_num_vs_matrix < 1e-9),
        "matrix_exponential_matches_closed_form":
            bool(max_matrix_vs_closed < 1e-12),
        "total_charge_conserved":
            bool(charge_rel < 1e-10),
        "capacitor_plus_resistor_energy_balanced":
            bool(energy_rel < 5e-7),
        "hidden_elimination_matches_full_system":
            bool(hidden_residual < 2e-7),
        "hidden_initial_state_becomes_visible":
            bool(abs(float(delta_y[0])) < 1e-12 and max_hidden_signal > 0.49),
        "two_sample_observability_full_rank":
            bool(observation_rank == 2),
    }

    return {
        "meta": {
            "artifact": "AP18",
            "title": "Two-Capacitor RC Memory Cell",
            "version": "0.1.1",
            "tier": "finite_diagnostic",
            "verdict": "PASS" if all(gates.values()) else "FAIL",
            "runtime": {
                "python": platform.python_version(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
            },
        },
        "parameters": {
            "R_ohm": R_ohm,
            "C1_F": C1,
            "C2_F": C2,
            "V1_initial_V": V10,
            "V2_initial_V": V20,
            "simulation_end_s": t_end,
            "samples": n_samples,
        },
        "equations": {
            "state_matrix": A.tolist(),
            "full_system": [
                "C1 dV1/dt = -(V1-V2)/R",
                "C2 dV2/dt = +(V1-V2)/R",
            ],
            "equal_C_closed_form": [
                "V1(t)=Vavg+(DeltaV0/2) exp(-2t/(RC))",
                "V2(t)=Vavg-(DeltaV0/2) exp(-2t/(RC))",
            ],
            "memory_kernel":
                "K_mem(tau)=(1/(R C1))(1/(R C2)) exp(-tau/(R C2))",
            "charge_retention": "C1 V1 + C2 V2 = constant",
            "energy_balance":
                "E_caps(t)+integral_0^t ((V1-V2)^2/R) ds=E_caps(0)",
        },
        "derived": {
            "difference_time_constant_s": tau_diff,
            "initial_charge_C": charge0,
            "initial_capacitor_energy_J": initial_energy,
            "final_capacitor_energy_exact_J": final_energy_exact,
            "resistor_loss_exact_J": resistor_loss_exact,
        },
        "errors": {
            "max_numerical_vs_matrix_V": max_num_vs_matrix,
            "max_matrix_vs_closed_form_V": max_matrix_vs_closed,
            "max_charge_absolute_C": charge_abs,
            "max_charge_relative": charge_rel,
            "max_energy_balance_absolute_J": energy_abs,
            "max_energy_balance_relative": energy_rel,
            "max_hidden_elimination_residual_V_per_s": hidden_residual,
        },
        "readability": {
            "observation_matrix": observation.tolist(),
            "observability_rank": observation_rank,
            "observability_determinant": observation_determinant,
            "hidden_initial_difference_visible_at_t0_V": float(delta_y[0]),
            "max_hidden_to_visible_signal_V": max_hidden_signal,
            "hidden_to_visible_signal_at_end_V": float(delta_y[-1]),
        },
        "samples": samples,
        "gates": gates,
        "claim_boundary": {
            "linear_circuit_solution":
                "exact_algebra_in_declared_ideal_model",
            "runtime": "finite_diagnostic",
            "hardware_validation": "not_yet_executed",
            "drl_inertial_term": "not_tested",
            "ontic_Psi_record": "not_tested",
            "unified_DRL_cut_tape_action": "Open",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="ap/results/AP18_RC_MEMORY_CELL_RESULTS.json",
    )
    args = parser.parse_args()
    result = run()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "verdict": result["meta"]["verdict"],
        "charge_relative_error": result["errors"]["max_charge_relative"],
        "energy_relative_error": result["errors"]["max_energy_balance_relative"],
        "hidden_elimination_residual":
            result["errors"]["max_hidden_elimination_residual_V_per_s"],
        "observability_rank": result["readability"]["observability_rank"],
    }, indent=2))


if __name__ == "__main__":
    main()
