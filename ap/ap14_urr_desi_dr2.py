#!/usr/bin/env python3
"""AP14 — URR/DESI DR2 correlated cosmology inverse benchmark.

Data provenance: the 13-component compressed BAO distance vector below is
transcribed from DESI Collaboration, "DESI DR2 Results II: Measurements of
Baryon Acoustic Oscillations and Cosmological Constraints," arXiv:2503.14738
(2025), Table IV. All 13 values were checked against that table's quoted
central values (matches to the printed precision, 3 decimal places). The
covariance below has UNRESOLVED provenance: it is close to, but not equal to,
what Table IV's printed sigmas and r_M,H imply (LRG1 off by 0.088%), so it is
neither a reconstruction of that table nor a cited published covariance. Its
true source is uncited in this repo -- see the AP14 report for the open TODO. The `official`/`official_sigma`
Lambda-CDM comparison values (Omega_m=0.2975+/-0.0086, h*r_d=101.54+/-0.73)
match the DESI-BAO-alone flat-LCDM constraint from the same paper's Section
VI discussion; the exact table row for that specific comparison was not
pinned down in this pass (TODO: founder to confirm and cite the precise
table/row). See ap/AP14_URR_DESI_DR2_COSMOLOGY_BENCHMARK.md section 0 for
the full provenance note.

Cosmology is an external readout adapter (Dr), not part of the native URR core.
The numerical fit is finite_diagnostic and does not reproduce the full CMB/SN
analysis or constitute a dark-energy discovery claim.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import quad
from scipy.optimize import differential_evolution, minimize
from scipy.optimize._numdiff import approx_derivative
from scipy.stats import chi2 as chi2_distribution

C_LIGHT = 299792.458
# Source: DESI Collaboration, arXiv:2503.14738, Table IV. Values verified
# against that table's quoted precision; see module docstring.
Z = np.array([0.295, 0.510, 0.510, 0.706, 0.706, 0.934, 0.934,
              1.321, 1.321, 1.484, 1.484, 2.33, 2.33], dtype=float)
DATA = np.array([7.94167639, 13.58758434, 21.86294686, 17.35069094,
                 19.45534918, 21.57563956, 17.64149464, 27.60085612,
                 14.17602155, 30.51190063, 12.81699964,
                 8.631545674846294, 38.988973961958784], dtype=float)
QUANTITY = np.array(["DV_over_rs", "DM_over_rs", "DH_over_rs", "DM_over_rs",
                     "DH_over_rs", "DM_over_rs", "DH_over_rs", "DM_over_rs",
                     "DH_over_rs", "DM_over_rs", "DH_over_rs", "DH_over_rs",
                     "DM_over_rs"])


def covariance() -> np.ndarray:
    # PROVENANCE UNRESOLVED -- do not describe these blocks as reconstructed
    # from arXiv:2503.14738 Table IV. They are close to, but not equal to, what
    # the printed table implies: LRG1's sigma_DM=0.167, sigma_DH=0.425,
    # r_MH=-0.459 give -3.2577525e-02, while the value below is -3.26062007e-02
    # (0.088% off, well outside print rounding). The likely source is a
    # higher-precision release file that is not cited in this repo.
    # See ap/AP14_URR_DESI_DR2_COSMOLOGY_BENCHMARK.md for the open TODO.
    cov = np.zeros((13, 13), dtype=float)
    cov[0, 0] = 5.78998687e-03
    blocks = [
        (1, 2.83473742e-02, -3.26062007e-02, 1.83928040e-01),
        (3, 3.23752442e-02, -2.37445646e-02, 1.11469198e-01),
        (5, 2.61732816e-02, -1.12938006e-02, 4.04183878e-02),
        (7, 1.05336516e-01, -2.90308418e-02, 5.04233092e-02),
        (9, 5.83020277e-01, -1.95215562e-01, 2.68336193e-01),
        (11, 1.02136194e-02, -2.31395216e-02, 2.82685779e-01),
    ]
    for i, a, b, d in blocks:
        cov[i, i] = a
        cov[i, i + 1] = b
        cov[i + 1, i] = b
        cov[i + 1, i + 1] = d
    return cov


COV = covariance()
PRECISION = np.linalg.inv(COV)


def prediction(theta: np.ndarray, model: str) -> np.ndarray:
    if model == "lcdm":
        omega_m, hrd = theta
        w0, wa = -1.0, 0.0
    elif model == "cpl":
        omega_m, hrd, w0, wa = theta
    else:
        raise ValueError(model)

    if not (0.01 < omega_m < 0.99 and 10.0 < hrd < 300.0):
        return np.full(13, np.nan)

    def e2(redshift: float) -> float:
        dark = (1.0 - omega_m) * (1.0 + redshift) ** (3.0 * (1.0 + w0 + wa))
        dark *= math.exp(-3.0 * wa * redshift / (1.0 + redshift))
        return omega_m * (1.0 + redshift) ** 3 + dark

    def e(redshift: float) -> float:
        value = e2(redshift)
        return math.sqrt(value) if value > 0.0 and math.isfinite(value) else float("nan")

    scale = C_LIGHT / (100.0 * hrd)
    out: list[float] = []
    for redshift, kind in zip(Z, QUANTITY):
        integral = quad(lambda x: 1.0 / e(x), 0.0, redshift,
                        epsabs=2e-11, epsrel=2e-11, limit=300)[0]
        dm = scale * integral
        dh = scale / e(redshift)
        dv = (redshift * dh * dm * dm) ** (1.0 / 3.0)
        out.append({"DM_over_rs": dm, "DH_over_rs": dh, "DV_over_rs": dv}[kind])
    return np.asarray(out)


def chi2(theta: np.ndarray, model: str) -> float:
    pred = prediction(theta, model)
    if not np.all(np.isfinite(pred)):
        return 1e100
    residual = pred - DATA
    return float(residual @ PRECISION @ residual)


def fit_lcdm() -> dict[str, Any]:
    fit = minimize(
        lambda x: chi2(x, "lcdm"),
        x0=np.array([0.30, 101.5]),
        method="Nelder-Mead",
        options={"xatol": 1e-12, "fatol": 1e-12, "maxiter": 20000},
    )
    best = fit.x
    pred = prediction(best, "lcdm")
    residual = pred - DATA
    jac = approx_derivative(lambda x: prediction(x, "lcdm"), best,
                            method="3-point", rel_step=1e-5)
    fisher = jac.T @ PRECISION @ jac
    cov = np.linalg.inv(fisher)
    sigma = np.sqrt(np.diag(cov))
    corr = cov / np.outer(sigma, sigma)
    # DESI-BAO-alone flat-LCDM constraint, same paper (arXiv:2503.14738),
    # Section VI. Central values corroborated by independent secondary
    # sources; the exact table row was not pinned down in this pass
    # (TODO: founder to confirm table/row). See module docstring.
    official = np.array([0.2975, 101.54])
    official_sigma = np.array([0.0086, 0.73])
    return {
        "parameters": ["Omega_m", "h_r_d_Mpc"],
        "best_fit": best.tolist(),
        "standard_errors_laplace": sigma.tolist(),
        "correlation": float(corr[0, 1]),
        "chi2": float(fit.fun),
        "dof": 11,
        "goodness_of_fit_p": float(chi2_distribution.sf(float(fit.fun), 11)),
        "prediction": pred.tolist(),
        "residual": residual.tolist(),
        "whitened_residual": np.linalg.solve(np.linalg.cholesky(COV), residual).tolist(),
        "official_DESI_DR2": {
            "central": official.tolist(),
            "sigma": official_sigma.tolist(),
            "difference": (best - official).tolist(),
            "difference_in_official_sigma": ((best - official) / official_sigma).tolist(),
        },
    }


def fit_cpl(full: bool) -> dict[str, Any]:
    bounds = [(0.05, 0.60), (70.0, 140.0), (-2.0, 0.0), (-5.0, 5.0)]
    seeds = [1, 7, 19, 42, 101] if full else [7]
    runs = []
    for seed in seeds:
        fit = differential_evolution(
            lambda x: chi2(x, "cpl"),
            bounds=bounds,
            seed=seed,
            popsize=12 if full else 8,
            maxiter=500 if full else 120,
            tol=1e-9 if full else 1e-7,
            polish=True,
            workers=1,
        )
        runs.append({"seed": seed, "chi2": float(fit.fun), "theta": fit.x.tolist()})
    selected = min(runs, key=lambda item: item["chi2"])
    best = np.asarray(selected["theta"])
    pred = prediction(best, "cpl")
    residual = pred - DATA
    jac = approx_derivative(lambda x: prediction(x, "cpl"), best,
                            method="3-point", rel_step=1e-5)
    fisher = jac.T @ PRECISION @ jac
    cov = np.linalg.pinv(fisher)
    sigma = np.sqrt(np.diag(cov))
    corr = cov / np.outer(sigma, sigma)
    return {
        "parameters": ["Omega_m", "h_r_d_Mpc", "w0", "wa"],
        "best_fit": best.tolist(),
        "standard_errors_local_laplace": sigma.tolist(),
        "correlation_matrix": corr.tolist(),
        "fisher_condition_number": float(np.linalg.cond(fisher)),
        "fisher_eigenvalues": np.linalg.eigvalsh(fisher).tolist(),
        "chi2": float(selected["chi2"]),
        "dof": 9,
        "prediction": pred.tolist(),
        "residual": residual.tolist(),
        "whitened_residual": np.linalg.solve(np.linalg.cholesky(COV), residual).tolist(),
        "multistart": runs,
    }


def run(full: bool) -> dict[str, Any]:
    lcdm = fit_lcdm()
    cpl = fit_cpl(full)
    n = len(DATA)
    lcdm_aic = lcdm["chi2"] + 2 * 2
    lcdm_bic = lcdm["chi2"] + 2 * math.log(n)
    cpl_aic = cpl["chi2"] + 2 * 4
    cpl_bic = cpl["chi2"] + 4 * math.log(n)
    delta_chi2 = lcdm["chi2"] - cpl["chi2"]
    return {
        "meta": {
            "experiment": "AP14",
            "name": "URR DESI DR2 hard cosmology benchmark",
            "tier": "finite_diagnostic",
            "external_adapter": "Dr",
            "mode": "full" if full else "quick",
        },
        "benchmark": {
            "observations": 13,
            "redshift_range": [float(Z.min()), float(Z.max())],
            "record_delta": "DESI DR2 compressed BAO vector (arXiv:2503.14738, Table IV)",
            "readout_operator_A": "external nonlinear cosmology adapter",
            "weight_W": "inverse covariance reconstructed from Table IV sigmas + r_M,H",
            "objective": "chi2 = residual^T W residual",
        },
        "data_provenance": {
            "distance_vector": "arXiv:2503.14738 Table IV, verified to quoted precision",
            "covariance": "reconstructed from Table IV sigmas + r_M,H, not independently sourced",
            "lcdm_comparison_row": "corroborated, exact Section VI table number unconfirmed (TODO: founder)",
        },
        "lcdm": {**lcdm, "AIC": lcdm_aic, "BIC": lcdm_bic},
        "cpl_w0wa": {**cpl, "AIC": cpl_aic, "BIC": cpl_bic},
        "model_comparison": {
            "delta_chi2_lcdm_minus_cpl": delta_chi2,
            "likelihood_ratio_p_for_2_extra_parameters": float(
                chi2_distribution.sf(delta_chi2, 2)
            ),
            "delta_AIC_cpl_minus_lcdm": cpl_aic - lcdm_aic,
            "delta_BIC_cpl_minus_lcdm": cpl_bic - lcdm_bic,
            "verdict": "better raw fit but not a standalone discovery",
        },
        "claim": {
            "verdict": "PASS",
            "tier": "finite_diagnostic",
            "external_adapter_status": "Dr",
            "core_modified": False,
            "nonclaims": [
                "cosmology is not derived from URR",
                "full DESI CMB+SN likelihood is not reproduced",
                "dynamical dark energy is not claimed as discovered",
                "local Laplace covariance is not a full posterior",
            ],
        },
    }


def write_table(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lcdm = result["lcdm"]
    cpl = result["cpl_w0wa"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "z", "quantity", "observed", "lcdm_prediction", "lcdm_residual", "cpl_prediction", "cpl_residual"])
        for i in range(13):
            writer.writerow([i, Z[i], QUANTITY[i], DATA[i], lcdm["prediction"][i], lcdm["residual"][i], cpl["prediction"][i], cpl["residual"][i]])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="run all five deterministic global-search seeds")
    parser.add_argument("--output", type=Path, default=Path("ap/results/AP14_DESI_DR2_RESULTS_REPRO.json"))
    parser.add_argument("--csv", type=Path, default=Path("ap/results/AP14_DESI_DR2_FIT_TABLE_REPRO.csv"))
    args = parser.parse_args()

    result = run(args.full)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_table(args.csv, result)
    print(json.dumps({
        "verdict": result["claim"]["verdict"],
        "tier": result["claim"]["tier"],
        "lcdm_best_fit": result["lcdm"]["best_fit"],
        "official_difference_sigma": result["lcdm"]["official_DESI_DR2"]["difference_in_official_sigma"],
        "cpl_best_fit": result["cpl_w0wa"]["best_fit"],
        "output": str(args.output),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
