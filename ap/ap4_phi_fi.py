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
    """Negative control (mandatory, property 4): two records reading h in the
    SAME role differ genuinely; freeing w cannot absorb it => Phi_FI ~ 0."""
    y2, s2 = np.array([0.67, 0.73]), np.array([0.01, 0.01])

    def V2(p, w_free):
        h = p[0]
        return float(np.sum(((np.array([h, h]) - y2) / s2) ** 2))

    vf = _fit(lambda p: V2(p, False), [0.70])
    vr = _fit(lambda p: V2(p, True), [0.70, -1.2])
    assert vf > 10.0
    phi = phi_fi(vf, vr)
    assert abs(phi) < 0.05, phi               # measured 0.000


def test_property_bounds_nested_inclusion():
    """Property 1: V*(relaxed) <= V*(forced) numerically => 0 <= Phi <= 1
    (allow tiny negative from optimizer noise, clamp threshold 1e-6)."""
    vf = _fit(lambda p: V_hubble(p, False), [0.70, 0.142])
    vr = _fit(lambda p: V_hubble(p, True), [0.70, 0.142, -1.0])
    assert vr <= vf + 1e-6
    assert -1e-6 <= phi_fi(vf, vr) <= 1.0 + 1e-6


def test_phi_carries_its_posit():
    """Property 2: Phi_FI is a function OF the freed posit -- freeing an
    IRRELEVANT posit (curvature-like dummy that we keep at zero effect by
    construction: refit with the same forced model twice) must give Phi ~ 0,
    not inherit the w-result."""
    vf = _fit(lambda p: V_hubble(p, False), [0.70, 0.142])
    # "freeing" a posit with no lever on the records = same family
    vr_same = _fit(lambda p: V_hubble(p[:2], False), [0.70, 0.142, 0.0])
    assert abs(phi_fi(vf, vr_same)) < 0.05
