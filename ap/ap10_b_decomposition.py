"""AP10 -- b123 DECOMPOSED (not derived): counting x three kinematic atoms.

Response to "derive b123" (2026-07-19 late). HONESTY HEADER FIRST:
this file does NOT derive the SM one-loop slopes from our grammar -- that
remains the standing falsifier. What it pins (exact rationals, executed):

    b_a  =  (11/3) C2(G_a)  -  (2/3) sum_Weyl T_a(R)  -  (1/3) sum_scalar T_a(S)

i.e. every slope = REPRESENTATION COUNTING (pure channel arithmetic, all
SM content) x THREE UNIVERSAL KINEMATIC WEIGHTS shared by all three groups:

    W_gauge = 11/3 (anti-screening, gauge self-load -- non-abelian only)
    W_weyl  =  2/3 (screening per Weyl channel)
    W_scal  =  1/3 (screening per complex-scalar channel)

KINSHIP (this is textbook, NOT ours): Gross-Wilczek-Politzer 1973;
standard derivation of the weights = one-loop integrals (Peskin ch.16).

LENS TRANSLATION [Dr]: the split maps onto the Degree-Circulation grammar
candidate -- screening matter = DEGREE-like symmetric load (every matter
channel polarizes); anti-screening gauge self-coupling = CIRCULATION-like
oriented load (only non-abelian carriers self-load, sign flips). This is a
structural reading, not a derivation.

FALSIFIER MOVED ONE LEVEL DEEPER: the mystery is no longer (41/10,-19/6,-7)
(those are counting, executed below) but the three atoms (11/3, 2/3, 1/3).
Derive THOSE from the grammar (spin/orientation structure of graph
channels) and b123 -- and hence 52 -- all emerge free. [Open + stance]

Run: pytest ap/ap10_b_decomposition.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
from fractions import Fraction as F

# the three kinematic atoms (universal across groups; NOT derived here)
W_GAUGE, W_WEYL, W_SCAL = F(11, 3), F(2, 3), F(1, 3)

# SM representation content, 3 generations + 1 Higgs doublet (pure counting)
GEN = 3


def b3():
    """SU(3): C2=3; 6 Dirac quarks = 12 Weyl triplets, T=1/2; no scalars."""
    return W_GAUGE * 3 - W_WEYL * (F(1, 2) * 12)


def b2():
    """SU(2): C2=2; per gen 4 Weyl doublet-pairs (3 quark colors + 1 lepton)
    x2 Weyl components... counted as 12 Weyl doublets total, T=1/2; Higgs
    complex doublet T=1/2."""
    return W_GAUGE * 2 - W_WEYL * (F(1, 2) * 12) - W_SCAL * F(1, 2)


def b1():
    """U(1)_GUT (3/5 normalization): no self-load (abelian: zero circulation);
    per-generation sum of Y^2 over Weyl channels = 10/3; Higgs Y=1/2."""
    sum_y2 = GEN * (F(1, 6) + F(4, 3) + F(1, 3) + F(1, 2) + 1)
    return W_WEYL * F(3, 5) * sum_y2 + W_SCAL * F(3, 5) * F(1, 2)


def test_counting_reproduces_all_three_slopes_exactly():
    """Exact rationals, no floats: the SM slopes are counting x atoms."""
    assert b3() == F(7), b3()
    assert b2() == F(19, 6), b2()
    assert b1() == F(41, 10), b1()


def test_abelian_has_zero_gauge_selfload():
    """The anti-screening (circulation-like) term exists ONLY for non-abelian
    groups -- U(1)'s slope is pure screening (degree-like), which is why its
    coupling GROWS toward the UV while SU(2)/SU(3) shrink."""
    assert b1() > 0                       # pure screening: 1/alpha falls toward UV
    assert b2() < W_GAUGE * 2             # screening partially cancels self-load
    assert b3() < W_GAUGE * 3
    assert b2() > 0 and b3() > 0          # self-load wins => asymptotic freedom


def test_atoms_are_the_remaining_mystery():
    """Sensitivity pin: perturbing ANY single atom by 10% breaks at least one
    slope -- the atoms are load-bearing, not decorative; they are exactly
    where the open problem now lives."""
    global W_GAUGE, W_WEYL, W_SCAL
    orig = (W_GAUGE, W_WEYL, W_SCAL)
    targets = (F(7), F(19, 6), F(41, 10))
    for i in range(3):
        vals = list(orig)
        vals[i] = vals[i] * F(11, 10)
        W_GAUGE, W_WEYL, W_SCAL = vals
        broken = (b3(), b2(), b1()) != targets
        W_GAUGE, W_WEYL, W_SCAL = orig
        assert broken, f"atom {i} not load-bearing?"
    assert (b3(), b2(), b1()) == targets  # restored
