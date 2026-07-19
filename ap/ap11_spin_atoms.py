"""AP11 -- the three atoms COLLAPSE TO ONE FORMULA (executed):

    atom(s) = (-1)^{2s} * [ (2s)^2  -  1/3 ]
              statistics   spin^2     universal orbital screening
              (loop sign)  (paramagnetic)   (diamagnetic)

    s=0   -> -1/3   (scalar screening atom)
    s=1/2 -> -2/3   (Weyl screening atom)
    s=1   -> +11/3  (gauge anti-screening atom)

KINSHIP (this is known deep physics, NOT ours): Nielsen 1981 ("Asymptotic
freedom as a spin effect", Am.J.Phys 49, 1171), R.J. Hughes 1981 (Nucl.Phys
B186, 376) -- asymptotic freedom = vacuum paramagnetism of charged vector
bosons beating universal diamagnetic screening. We pin it exactly and read
it through the lens; we derive NOTHING new here.

WHAT THIS DOES TO THE MYSTERY LADDER: the three atoms (AP10) were the last
stop; they now reduce to TWO structures + a sign:
 (i)  the universal screening constant 1/3 -- whose known origin is the
      ANGULAR AVERAGE <cos^2 theta> = 1/d in d=3 spatial dimensions
      (pinned numerically below for d=3 and d=4) => in lens language the
      diamagnetic atom is a DIMENSION READOUT (ROM-3.7: our graphs carry
      spectral dimension) -- sharp testable stance: on a substrate of
      spectral dimension d_s the screening atom should be 1/d_s [Open];
 (ii) the paramagnetic law (2s)^2 -- spin as channel circulation: a spin-s
      channel carries 2s orientation units, response quadratic [Dr reading;
      derivation from graph channel structure = THE final falsifier];
 (iii) the statistics sign (-1)^{2s} -- fermion loops close odd [Dr].

FINAL-FORM FALSIFIER (supersedes AP10's): derive (2s)^2 and the 1/d_s
screening constant from the generation grammar's channel structure -- then
atoms -> slopes (AP10 counting) -> 52 (AP9 accumulation) -> hierarchy (AP-
chain) ALL emerge from the graph + representation table. [Open + stance]

TOY TIER: Monte-Carlo angular averages (seeded); exact Fractions elsewhere.
Run: pytest ap/ap11_spin_atoms.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
import math
import random
from fractions import Fraction as F

import ap10_b_decomposition as ap10


def atom(two_s: int) -> F:
    """Nielsen-Hughes: (-1)^{2s} [ (2s)^2 - 1/3 ], argument = 2s."""
    return F((-1) ** two_s) * (F(two_s) ** 2 - F(1, 3))


def test_one_formula_yields_all_three_atoms_exactly():
    assert atom(0) == F(-1, 3)      # scalar: pure screening 1/3
    assert atom(1) == F(-2, 3)      # Weyl:   screening 2/3
    assert atom(2) == F(11, 3)      # gauge:  paramagnetism wins -> +11/3


def test_atoms_reconstruct_ap10_weights():
    """The AP10 kinematic weights are exactly |atom(s)| with the statistics
    sign carried separately -- one structure, not three inputs."""
    assert abs(atom(2)) == ap10.W_GAUGE
    assert abs(atom(1)) == ap10.W_WEYL
    assert abs(atom(0)) == ap10.W_SCAL
    # and therefore the full slopes flow from spins + counting alone:
    assert ap10.b3() == F(7) and ap10.b2() == F(19, 6) and ap10.b1() == F(41, 10)


def _mean_cos2(d: int, n: int = 200_000, seed: int = 7) -> float:
    rng = random.Random(seed)
    acc = 0.0
    for _ in range(n):
        v = [rng.gauss(0.0, 1.0) for _ in range(d)]
        r2 = sum(t * t for t in v)
        acc += v[0] * v[0] / r2
    return acc / n


def test_universal_screening_constant_is_one_over_d():
    """The 1/3 is the d=3 angular average <cos^2> = 1/d -- pinned for d=3
    AND d=4 (the d-dependence is the content: the diamagnetic atom reads
    the DIMENSION of the substrate, which in our program is a spectral
    readout of the graph, ROM-3.7)."""
    assert abs(_mean_cos2(3) - 1 / 3) < 3e-3
    assert abs(_mean_cos2(4) - 1 / 4) < 3e-3
    # sanity: they differ (the constant is NOT dimension-blind)
    assert _mean_cos2(3) - _mean_cos2(4) > 0.05


def test_spin_squared_is_the_paramagnetic_axis():
    """Structure pin: across s in {0, 1/2, 1, 3/2, 2}, atom(s) + 1/3 (after
    stripping the statistics sign) is EXACTLY (2s)^2 -- the paramagnetic
    response is purely quadratic in the channel's orientation content."""
    for two_s in range(0, 5):
        stripped = atom(two_s) * F((-1) ** two_s)
        assert stripped + F(1, 3) == F(two_s) ** 2
