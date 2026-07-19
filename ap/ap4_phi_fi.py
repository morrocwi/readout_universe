"""AP4 -- Phi_FI, the Forced-Identification Fraction (first executed run).

    Phi_FI(q; A1, A2, C, pi) = 1 - V*(C \\ pi) / V*(C)

Defined in v2/EQUATION_FI.md (registered there first, 2026-07-19). V is the
LTP1 residual energy of the joint fit; Phi_FI reads off the fraction of an
apparent inter-chain tension whose information lives in the named closure
posit pi rather than in the records.

Honesty header: the ALGEBRAIC form is a nested-model chi-square ratio
(textbook likelihood-ratio kin -- NOT claimed novel); the candidate-novel
layer is the attribution semantics + decision rule + mandatory negative
control [Open, pending literature falsifier]. Interpretive claims: [Dr].
TOY TIER: Gaussian independent errors, fitting-formula grammar from AP1.

Run: pytest ap/ap4_phi_fi.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ap1_hubble_identifiability import theta100  # verified grammar (AP1)

# Hubble toy: records = [100*theta_star, omega_m h^2, h_ladder]
Y_OBS = np.array([1.0411, 0.1424, 0.73])
SIG = np.array([0.0011, 0.0011, 0.01])


def V_hubble(p, w_free):
    h, wm = p[0], p[1]
    w = p[2] if w_free else -1.0
    y = np.array([theta100(h, 0.02237, wm, w), wm, h])
    return float(np.sum(((y - Y_OBS) / SIG) ** 2))


def phi_fi(v_forced, v_relaxed):
    return 1.0 - v_relaxed / v_forced


def _fit(fun, x0):
    return minimize(fun, x0, method="Nelder-Mead", options={"fatol": 1e-8}).fun


def test_hubble_tension_is_closure_borne():
    """Positive case: freeing the single posit w=-1 absorbs the whole
    theta*-vs-ladder tension => Phi_FI ~ 1 (closure-borne, AP1 structure)."""
    vf = _fit(lambda p: V_hubble(p, False), [0.70, 0.142])
    vr = _fit(lambda p: V_hubble(p, True), [0.73, 0.142, -1.2])
    assert vf > 10.0, vf                      # a real (>3 sigma-equiv) forced tension
    phi = phi_fi(vf, vr)
    assert phi > 0.95, phi                    # measured 1.0000


def test_world_side_control_yields_zero():
    """Negative control (mandatory, property 4), NON-TAUTOLOGICAL version
    (review PR #9): two theta*-like records that BOTH genuinely depend on w
    in the same way disagree; freeing w moves both model predictions
    together, so it cannot absorb the split => Phi_FI ~ 0. This tests real
    non-absorption, not parameter non-participation."""
    y2, s2 = np.array([1.0411, 1.0511]), np.array([0.0011, 0.0011])

    def V2(p, w_free):
        h, wm = p[0], p[1]
        w = p[2] if w_free else -1.0
        t = theta100(h, 0.02237, wm, w)      # same prediction feeds BOTH records
        return float(np.sum(((np.array([t, t]) - y2) / s2) ** 2))

    vf = _fit(lambda p: V2(p, False), [0.70, 0.142])
    vr = _fit(lambda p: V2(p, True), [0.70, 0.142, -1.2])
    assert vf > 10.0
    phi = phi_fi(vf, vr)
    assert abs(phi) < 0.05, phi


def test_property_bounds_nested_inclusion():
    """Property 1: V*(relaxed) <= V*(forced) numerically => 0 <= Phi <= 1
    (allow tiny negative from optimizer noise, clamp threshold 1e-6)."""
    vf = _fit(lambda p: V_hubble(p, False), [0.70, 0.142])
    vr = _fit(lambda p: V_hubble(p, True), [0.70, 0.142, -1.0])
    assert vr <= vf + 1e-6
    assert -1e-6 <= phi_fi(vf, vr) <= 1.0 + 1e-6


def test_phi_carries_its_posit():
    """Property 2, NON-TAUTOLOGICAL version (review PR #9): freeing a
    DIFFERENT, genuinely-constrained posit (omega_b, with its real tight
    prior sigma=0.00015) must give low Phi -- the tension is NOT attributable
    to omega_b -- while freeing w gives Phi~1. Also encodes property 5:
    without the prior, ANY third free knob saturates dof=0 and fakes Phi=1,
    so priors representing the posit's true constraint are mandatory."""
    WB0, SWB = 0.02237, 0.00015

    def V_wb(p, wb_free):
        h, wm = p[0], p[1]
        wb = p[2] if wb_free else WB0
        y = np.array([theta100(h, wb, wm, -1.0), wm, h])
        prior = ((wb - WB0) / SWB) ** 2
        return float(np.sum(((y - Y_OBS) / SIG) ** 2)) + prior

    vf = _fit(lambda p: V_wb(p, False), [0.70, 0.142])
    vr_wb = _fit(lambda p: V_wb(p, True), [0.70, 0.142, WB0])
    phi_wb = phi_fi(vf, vr_wb)
    assert phi_wb < 0.10, phi_wb             # measured ~0.025: NOT omega_b's tension
    vr_w = _fit(lambda p: V_hubble(p, True), [0.73, 0.142, -1.2])
    assert phi_fi(vf, vr_w) > 0.95           # ...while it IS w's tension
