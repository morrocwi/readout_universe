"""AP8 -- H_quartic FOUND: the nonlinear distinction charge of the DRL.

AP6's honest finding was that the QUADRATIC-form charge drifts (0.119) once
V gains a quartic term. Continuum Legendre transform of the generalized DRL
Lagrangian L = M dPhi dPsi + (D/2)(Phi dPsi - Psi dPhi) - K Phi.Lw.Psi
              - Psi.gradV(Phi) + J.Psi
gives (D-terms cancel exactly as in the linear case):

    H_nl = sum_i M_i vPhi_i vPsi_i + K Phi.Lw.Psi + Psi.gradV(Phi) - J.Psi

i.e. the quartic correction is simply k2*Phi.Psi -> Psi.V'(Phi)
(= k2 Phi.Psi + k4 Phi^3.Psi per node), plus -J.Psi for constant forcing.
The AP6 drift was a WRONG-CHARGE artifact, not a missing conservation law.

Tier: hand Legendre derivation [Dr] + executed drift checks below
[finite_diagnostic, toy: same N=8 weighted graph as ap6]. Coq lift of the
nonlinear cancellation queued with the general-N work.

Run: pytest ap/ap8_h_quartic.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ap6_drl_general as g6


def h_quartic(Phi, Psi, n_idx, dt, M, K, Lw, k2, k4, J):
    """The corrected nonlinear charge: quadratic term promoted to
    Psi.gradV(Phi), plus the constant-forcing term."""
    vp = (Phi[n_idx + 1] - Phi[n_idx - 1]) / (2 * dt)
    vs = (Psi[n_idx + 1] - Psi[n_idx - 1]) / (2 * dt)
    gradV = k2 * Phi[n_idx] + k4 * Phi[n_idx] ** 3
    return (np.sum(M * vp * vs) + K * Phi[n_idx] @ Lw @ Psi[n_idx]
            + float(Psi[n_idx] @ gradV) - float(J @ Psi[n_idx]))


def _drift(charge_vals):
    h = np.array(charge_vals)
    return (h.max() - h.min()) / abs(h.mean())


def _run(k4, J_amp, steps=4000):
    J = J_amp * g6.J_FORCE if np.ndim(g6.J_FORCE) else np.full(g6.N, J_amp)
    Phi, Psi = g6.el_trajectories(g6.N, g6.DT, steps, g6.M_HET, g6.D_HET,
                                  g6.LW, g6.K, g6.K2, k4, J, seed=7)
    return Phi, Psi, J


def test_quartic_charge_now_conserved():
    """THE resolution of AP6's open finding: with the corrected H_nl, the
    quartic (k4>0, J=0) case conserves to <2e-3 -- same O(dt^2) class as the
    linear case -- vs 0.119 for the wrong (quadratic-form) charge."""
    k4 = g6.K4
    Phi, Psi, J = _run(k4, 0.0)
    good = [h_quartic(Phi, Psi, n, g6.DT, g6.M_HET, g6.K, g6.LW, g6.K2, k4, J)
            for n in range(1, len(Phi) - 1, 10)]
    bad = [g6.distinction_charge(Phi, Psi, n, g6.DT, g6.M_HET, g6.K, g6.LW, g6.K2)
           for n in range(1, len(Phi) - 1, 10)]
    assert _drift(good) < 2e-3, _drift(good)
    assert _drift(bad) > 1e-2                  # the old charge really does fail here


def test_forced_case_also_conserved():
    """Constant J: L has no explicit time dependence, so H_nl (with the -J.Psi
    term) stays conserved."""
    Phi, Psi, J = _run(g6.K4, 0.5)
    good = [h_quartic(Phi, Psi, n, g6.DT, g6.M_HET, g6.K, g6.LW, g6.K2, g6.K4, J)
            for n in range(1, len(Phi) - 1, 10)]
    assert _drift(good) < 5e-3, _drift(good)


def test_reduces_to_old_charge_when_linear():
    """k4=0, J=0: H_nl == the ap6 quadratic charge identically."""
    Phi, Psi, J = _run(0.0, 0.0, steps=500)
    for n in (5, 100, 400):
        a = h_quartic(Phi, Psi, n, g6.DT, g6.M_HET, g6.K, g6.LW, g6.K2, 0.0, J)
        b = g6.distinction_charge(Phi, Psi, n, g6.DT, g6.M_HET, g6.K, g6.LW, g6.K2)
        assert abs(a - b) < 1e-12


def test_drift_scales_as_dt_squared():
    """The residual drift of H_nl is O(dt^2) discretization error, not a
    broken law: halving dt shrinks drift ~4x."""
    def drift_at(dt, steps):
        J = np.zeros(g6.N)
        Phi, Psi = g6.el_trajectories(g6.N, dt, steps, g6.M_HET, g6.D_HET,
                                      g6.LW, g6.K, g6.K2, g6.K4, J, seed=7)
        vals = [h_quartic(Phi, Psi, n, dt, g6.M_HET, g6.K, g6.LW, g6.K2, g6.K4, J)
                for n in range(1, steps - 1, 10)]
        return _drift(vals)
    d1, d2 = drift_at(g6.DT, 4000), drift_at(g6.DT / 2, 8000)
    assert 2.5 < d1 / d2 < 6.0, (d1, d2)
