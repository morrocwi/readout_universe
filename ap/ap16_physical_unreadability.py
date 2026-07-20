#!/usr/bin/env python3
"""AP16 — Physical unreadability classification smoke test.

Runtime tier: finite_diagnostic.
The Schwarzschild/Painleve-Gullstrand calculation is an external Dr adapter.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp


def observability_rank(A: np.ndarray, C: np.ndarray, tol: float = 1e-10) -> int:
    n = A.shape[0]
    O = np.vstack([C @ np.linalg.matrix_power(A, i) for i in range(n)])
    return int(np.linalg.matrix_rank(O, tol=tol))


def output_series(A: np.ndarray, C: np.ndarray, x0: np.ndarray, times: np.ndarray) -> np.ndarray:
    return np.array([float((C @ (expm(A * t) @ x0))[0]) for t in times])


def run() -> dict:
    times = np.linspace(0.0, 20.0, 401)
    C_visible = np.array([[1.0, 0.0]])
    C_hidden = np.array([[0.0, 1.0]])
    x_a = np.array([0.0, 0.0])
    x_b = np.array([0.0, 1.0])

    # Blind sensor.
    A_blind = np.zeros((2, 2))
    sep_blind = np.abs(
        output_series(A_blind, C_visible, x_b, times)
        - output_series(A_blind, C_visible, x_a, times)
    )
    blind_rank = observability_rank(A_blind, C_visible)
    blind_rank_alt = observability_rank(A_blind, np.vstack([C_visible, C_hidden]))

    # Reciprocal thermal memory.
    k = 0.35
    A_thermal = np.array([[-k, k], [k, -k]])
    sep_thermal = np.abs(
        output_series(A_thermal, C_visible, x_b, times)
        - output_series(A_thermal, C_visible, x_a, times)
    )
    thermal_rank = observability_rank(A_thermal, C_visible)

    # One-way retained sink.
    w = 0.35
    A_one_way = np.array([[-w, 0.0], [w, 0.0]])
    sep_one_way = np.abs(
        output_series(A_one_way, C_visible, x_b, times)
        - output_series(A_one_way, C_visible, x_a, times)
    )
    one_way_rank = observability_rank(A_one_way, C_visible)
    transfer = np.array([expm(A_one_way * t) @ np.array([1.0, 0.0]) for t in times])
    retention_error = float(np.max(np.abs(transfer.sum(axis=1) - 1.0)))

    # External GR toy adapter: outgoing radial null ray in PG units c=r_s=1.
    def pg_rhs(_t: float, y: np.ndarray) -> list[float]:
        r = max(float(y[0]), 1e-10)
        return [1.0 - 1.0 / np.sqrt(r)]

    def cutoff(_t: float, y: np.ndarray) -> float:
        return float(y[0] - 0.05)

    cutoff.terminal = True
    cutoff.direction = -1

    def ray(r0: float):
        return solve_ivp(
            pg_rhs,
            (0.0, 4.0),
            [r0],
            rtol=1e-10,
            atol=1e-12,
            max_step=0.002,
            events=cutoff,
        )

    outside = ray(1.2)
    inside = ray(0.8)

    cases = {
        "sensor_blind": {
            "rank": blind_rank,
            "rank_alt_sensor": blind_rank_alt,
            "max_output_separation": float(sep_blind.max()),
            "physical_black_hole": False,
        },
        "thermal_memory": {
            "rank": thermal_rank,
            "max_output_separation": float(sep_thermal.max()),
            "final_output_separation": float(sep_thermal[-1]),
            "physical_black_hole": False,
        },
        "one_way_sink": {
            "rank": one_way_rank,
            "max_output_separation_from_hidden": float(sep_one_way.max()),
            "retention_error": retention_error,
            "final_visible": float(transfer[-1, 0]),
            "final_hidden": float(transfer[-1, 1]),
            "physical_black_hole": False,
        },
        "schwarzschild_pg_toy": {
            "outside_initial_r": 1.2,
            "outside_initial_dr_dt": float(1.0 - 1.0 / np.sqrt(1.2)),
            "outside_final_r": float(outside.y[0, -1]),
            "inside_initial_r": 0.8,
            "inside_initial_dr_dt": float(1.0 - 1.0 / np.sqrt(0.8)),
            "inside_final_r": float(inside.y[0, -1]),
            "hit_cutoff": bool(inside.t_events[0].size > 0),
            "physical_black_hole": True,
        },
    }

    gates = {
        "blind_sensor_counterexample": bool(
            sep_blind.max() < 1e-12 and blind_rank_alt == 2
        ),
        "thermal_hidden_returns": bool(
            thermal_rank == 2 and sep_thermal.max() > 0.1
        ),
        "one_way_sink_counterexample": bool(
            sep_one_way.max() < 1e-12 and retention_error < 1e-12
        ),
        "schwarzschild_inside_outgoing_inward": bool(
            cases["schwarzschild_pg_toy"]["inside_initial_dr_dt"] < 0
            and cases["schwarzschild_pg_toy"]["inside_final_r"] < 0.8
        ),
    }

    return {
        "meta": {
            "artifact": "AP16",
            "tier": "finite_diagnostic",
            "gr_adapter": "Dr",
        },
        "cases": cases,
        "gates": gates,
        "verdict": "PASS" if all(gates.values()) else "FAIL",
        "tested_statement": "unreadable implies physical black hole",
        "result": "FALSIFIED_BY_COUNTEREXAMPLE",
        "replacement": (
            "physical black hole = one-way causal cut AND geometric horizon certificate"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="ap/results/AP16_PHYSICAL_UNREADABILITY_RESULTS.json",
    )
    args = parser.parse_args()
    result = run()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": result["verdict"], "gates": result["gates"]}, indent=2))


if __name__ == "__main__":
    main()
