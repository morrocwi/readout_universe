"""AP9 -- falsifier run for the stance "coupling = 1/k_eff (channel count)".

Origin: the G -> 10^19 -> 1/52 relocation chain (2026-07-19). The lens stance
was: the update rate at the fundamental step reads as an inverse effective
channel count per node, with ROM-3.3's k_max degree gate as the corpus-native
candidate origin. This file puts the NAIVE versions of that stance on the
chopping block against the three measured gauge couplings run to the Planck
step (one-loop SM, no thresholds -- toy tier).

MEASURED (executed below, pinned):
  1/alpha at m_P (one-loop from MZ):  U1_GUT 33.3 | SU2 49.4 | SU3 52.4
  - "single shared k_eff": spread 42% => KILLED at precision, survives ONLY
    as order-of-magnitude (all three ~ 1/(few x 10) at the same step).
  - "k_eff = adjoint dimension (1,3,8)": worst error 76% => KILLED outright.
  - "adjoint+fermion rough count": worst error 12% BUT this is one fitted
    scale + hand-picked integers on THREE data points => NOT evidence;
    recorded only to show how easy 3-point numerology is (anti-numerology
    exhibit, per the corpus's refused-not-faked constants policy).

VERDICT [Dr]: the naive channel-count stance is dead at precision; what
survives is (a) the real, standard fact that the RUNNING slopes b0 are
channel-counting numbers, and (b) an order-of-magnitude shared-budget hint.
A real derivation must produce k_eff from the generation grammar (ROM-3.3)
WITHOUT fitted integers -- that remains [Open]. Kinship: gauge unification
literature (GUT ~1/25 at 2e16 with thresholds; SUSY improves convergence) --
declared, standard, not ours.

Run: pytest ap/ap9_coupling_channels.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
import math

MZ, MP = 91.19, 1.2209e19
LNR = math.log(MP / MZ)
INV0 = {"U1_GUT": 59.01, "SU2": 29.57, "SU3": 1 / 0.1179}
B = {"U1_GUT": 41 / 10, "SU2": -19 / 6, "SU3": -7.0}


def inv_alpha_planck():
    return {k: INV0[k] - B[k] / (2 * math.pi) * LNR for k in INV0}


def best_scale_worst_err(m, vals):
    s = sum(vals[k] * m[k] for k in m) / sum(m[k] ** 2 for k in m)
    return s, max(abs(s * m[k] - vals[k]) / vals[k] for k in m)


def test_running_reproduces_the_52():
    """Grammar sanity: the SU3 value at the Planck step is the ~1/52 quoted
    in the hierarchy chain (same computation as the proton-memory answer)."""
    v = inv_alpha_planck()
    assert abs(v["SU3"] - 52.4) < 0.5
    assert abs(v["SU2"] - 49.4) < 0.5
    assert abs(v["U1_GUT"] - 33.3) < 0.5


def test_shared_keff_killed_at_precision():
    """One shared channel budget at the fundamental step: spread 42% >> any
    reasonable precision claim -- survives ONLY as order-of-magnitude."""
    v = inv_alpha_planck()
    mean = sum(v.values()) / 3
    spread = (max(v.values()) - min(v.values())) / mean
    assert 0.35 < spread < 0.50, spread          # measured 0.42
    assert all(10 < x < 100 for x in v.values())  # the order-of-magnitude part


def test_adjoint_dimension_map_killed():
    """k_eff = dim(adjoint) = (1,3,8): worst relative error ~76% -- dead."""
    v = inv_alpha_planck()
    _, err = best_scale_worst_err({"U1_GUT": 1, "SU2": 3, "SU3": 8}, v)
    assert err > 0.5, err                        # measured 0.76


def test_numerology_exhibit_is_flagged_not_evidence():
    """The hand-picked 'adjoint+fermion' map fits to 12% -- pinned here ONLY
    as an exhibit of how easily 3 data points + 1 fitted scale + chosen
    integers produce a 'good' fit. It must never be quoted as support."""
    v = inv_alpha_planck()
    _, err = best_scale_worst_err({"U1_GUT": 16, "SU2": 19, "SU3": 24}, v)
    assert err < 0.2, err                        # measured 0.12 -- and meaningless
