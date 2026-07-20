#!/usr/bin/env python3
"""AP15 — finite smoke test for the URR-C Read–Write Cut.

Runtime tier: finite_diagnostic.
Interpretation of the cut: Dr.
Unified derivation from the DRL action: Open.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm

EPS = 1e-15


def build_generator(W: np.ndarray, R: np.ndarray, leak: np.ndarray) -> np.ndarray:
    W = np.asarray(W, dtype=float)
    R = np.asarray(R, dtype=float)
    leak = np.asarray(leak, dtype=float).reshape(-1)
    nh, no = W.shape
    if R.shape != (no, nh):
        raise ValueError(f"R shape {R.shape}; expected {(no, nh)}")
    if leak.size != nh:
        raise ValueError(f"leak length {leak.size}; expected {nh}")
    if np.any(W < 0) or np.any(R < 0) or np.any(leak < 0):
        raise ValueError("W, R and leak must be nonnegative")

    A = np.zeros((no + nh + 1, no + nh + 1), dtype=float)
    A[:no, :no] = -np.diag(W.sum(axis=0))
    A[:no, no:no + nh] = R
    A[no:no + nh, :no] = W
    A[no:no + nh, no:no + nh] = -np.diag(R.sum(axis=0) + leak)
    A[-1, no:no + nh] = leak
    return A


def observability_rank(A: np.ndarray, C: np.ndarray, tol: float = 1e-10) -> int:
    blocks = []
    power = np.eye(A.shape[0])
    for _ in range(A.shape[0]):
        blocks.append(C @ power)
        power = power @ A
    return int(np.linalg.matrix_rank(np.vstack(blocks), tol=tol))


def simulate(name, W, R, leak, y0, times):
    A = build_generator(W, R, leak)
    nh, no = W.shape
    states = np.array([expm(A * t) @ y0 for t in times])
    visible = states[:, :no].sum(axis=1)
    hidden = states[:, no:no + nh].sum(axis=1)
    tape = states[:, -1]
    total = states.sum(axis=1)

    C = np.zeros((no, A.shape[0]))
    C[:, :no] = np.eye(no)
    rank = observability_rank(A, C)

    wn = float(np.linalg.norm(W))
    rn = float(np.linalg.norm(R))
    return {
        "name": name,
        "horizon_index": wn / (wn + rn + EPS),
        "observability_rank": rank,
        "observability_nullity": int(A.shape[0] - rank),
        "total_retention_error": float(np.max(np.abs(total - total[0]))),
        "generator_column_sum_error": float(np.max(np.abs(A.sum(axis=0)))),
        "max_generator_eigenvalue_real_part": float(np.max(np.real(np.linalg.eigvals(A)))),
        "initial": {"visible": float(visible[0]), "hidden": float(hidden[0]), "tape": float(tape[0])},
        "final": {"visible": float(visible[-1]), "hidden": float(hidden[-1]), "tape": float(tape[-1])},
        "visible_monotone_nonincreasing": bool(np.all(np.diff(visible) <= 1e-12)),
        "hidden_monotone_nondecreasing": bool(np.all(np.diff(hidden) >= -1e-12)),
        "tape_monotone_nondecreasing": bool(np.all(np.diff(tape) >= -1e-12)),
    }


def run(output: Path) -> dict:
    W = np.diag([0.30, 0.20, 0.10])
    R_equal = W.T
    R_leaky = 0.05 * W.T
    R_zero = np.zeros_like(R_equal)
    leak_zero = np.zeros(3)
    leak_tape = np.array([0.02, 0.01, 0.005])

    y_visible = np.array([0.50, 0.30, 0.20, 0.0, 0.0, 0.0, 0.0])
    y_hidden = np.array([0.0, 0.0, 0.0, 0.50, 0.30, 0.20, 0.0])
    times = np.linspace(0.0, 30.0, 301)

    cases = [
        simulate("closed_control", np.zeros_like(W), np.zeros_like(R_equal), leak_zero, y_visible, times),
        simulate("reciprocal_cut", W, R_equal, leak_zero, y_visible, times),
        simulate("one_way_horizon", W, R_zero, leak_zero, y_visible, times),
        simulate("leaky_horizon", W, R_leaky, leak_zero, y_visible, times),
        simulate("one_way_with_tape", W, R_zero, leak_tape, y_visible, times),
        simulate("source_like_reverse", np.zeros_like(W), R_equal, leak_zero, y_hidden, times),
    ]
    by_name = {c["name"]: c for c in cases}

    gates = {
        "all_total_retention": all(c["total_retention_error"] < 1e-12 for c in cases),
        "all_generator_column_sums": all(c["generator_column_sum_error"] < 1e-14 for c in cases),
        "closed_control_static": abs(by_name["closed_control"]["final"]["visible"] - 1.0) < 1e-12,
        "one_way_horizon_index": by_name["one_way_horizon"]["horizon_index"] > 1.0 - 1e-12,
        "reciprocal_index_half": abs(by_name["reciprocal_cut"]["horizon_index"] - 0.5) < 1e-12,
        "leaky_index_between": 0.5 < by_name["leaky_horizon"]["horizon_index"] < 1.0,
        "one_way_visible_decays": by_name["one_way_horizon"]["visible_monotone_nonincreasing"] and by_name["one_way_horizon"]["final"]["visible"] < 0.06,
        "one_way_hidden_accumulates": by_name["one_way_horizon"]["hidden_monotone_nondecreasing"] and by_name["one_way_horizon"]["final"]["hidden"] > 0.94,
        "tape_append_only": by_name["one_way_with_tape"]["tape_monotone_nondecreasing"] and by_name["one_way_with_tape"]["final"]["tape"] > 0.10,
        "return_restores_observability": by_name["reciprocal_cut"]["observability_nullity"] == 1 and by_name["one_way_horizon"]["observability_nullity"] == 4,
        "stable_generators": all(c["max_generator_eigenvalue_real_part"] < 1e-12 for c in cases),
    }
    verdict = "PASS" if all(gates.values()) else "FAIL"
    report = {
        "meta": {
            "artifact": "AP15",
            "title": "Universal Retention–Cut smoke test",
            "tier": "finite_diagnostic",
            "cut_interpretation": "Dr",
            "unified_mechanism": "Open",
        },
        "model": {
            "visible_dimension": 3,
            "hidden_dimension": 3,
            "tape_dimension": 1,
            "write_matrix_W": W.tolist(),
            "reciprocal_return_R": R_equal.tolist(),
            "leaky_return_R": R_leaky.tolist(),
            "one_way_return_R": R_zero.tolist(),
            "tape_leak": leak_tape.tolist(),
            "equations": {
                "visible": "dq_O/dt = -diag(1^T W) q_O + R q_H",
                "hidden": "dq_H/dt = W q_O - diag(1^T R + ell) q_H",
                "tape": "dq_T/dt = ell^T q_H",
            },
        },
        "cases": cases,
        "gates": gates,
        "claim": {
            "verdict": verdict,
            "derived_in_this_finite_model": [
                "total retained quantity is conserved because generator columns sum to zero",
                "R=0 gives exact visible-sector damping with no return term",
                "R>0 creates delayed return and improves dynamical observability",
                "append-only tape is monotone when ell>=0",
            ],
            "not_claimed": [
                "all real systems are linear retained-flow systems",
                "black-hole dynamics are derived",
                "the cut term is derived from the DRL action",
                "the read-write interpretation is externally peer reviewed",
            ],
        },
    }
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("AP15_READ_WRITE_CUT_RESULTS.json"))
    args = parser.parse_args()
    report = run(args.output)
    cases = {c["name"]: c for c in report["cases"]}
    print(json.dumps({
        "verdict": report["claim"]["verdict"],
        "one_way_horizon_index": cases["one_way_horizon"]["horizon_index"],
        "reciprocal_horizon_index": cases["reciprocal_cut"]["horizon_index"],
        "leaky_horizon_index": cases["leaky_horizon"]["horizon_index"],
        "one_way_observability_nullity": cases["one_way_horizon"]["observability_nullity"],
        "reciprocal_observability_nullity": cases["reciprocal_cut"]["observability_nullity"],
        "one_way_final_visible": cases["one_way_horizon"]["final"]["visible"],
        "one_way_final_hidden": cases["one_way_horizon"]["final"]["hidden"],
        "tape_final": cases["one_way_with_tape"]["final"]["tape"],
        "max_total_retention_error": max(c["total_retention_error"] for c in report["cases"]),
    }, indent=2))
    return 0 if report["claim"]["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
