"""AP2 -- Einstein Probe FXTs (arXiv:2607.14317) through the RD lens
(toy-tier finite_diagnostic).

Paper's claim: energetic FXTs sit at exceptionally low E_p for their E_iso
(below the Amati locus) and viewing-angle effects of standard Type II GRBs
cannot account for it => new relativistic explosion class.

Lens verdict split (2026-07-19, from ABSTRACT ONLY -- declared limit):
- G7 (readout-vs-readout): WITHIN the assumed single-power-law deboost
  family (E_p ~ delta^1; E_iso ~ delta^p, p in [2,3] -- toy-assumed standard
  beaming scalings: p=3 point-source, p=2 extended jet; ratio = b^(p/2-1)),
  off-axis viewing moves a burst ALONG the Amati locus or ABOVE it; BELOW is
  unreachable IN THIS FAMILY. This supports the paper's refutation direction
  for that family only -- it does NOT bound the real off-axis model space:
  structured/patchy jets with angle-dependent intrinsic E_p (the GRB 170817A
  literature) live outside the family and are not excluded here.
- G4 (Pi/selection): "new low-E_p population" appearing exactly when a
  soft-band low-threshold instrument turns on is the sorites signature; the
  old population must be forward-modeled through the new selection before a
  new class is declared (precedent: X-ray flashes, HETE-2 era). [Dr]
- G5 (identifiability): the paper's three alternatives (lower Gamma / less
  angular momentum / other structures) live in the null space of a
  2-coordinate record (E_p, E_iso) -- undecidable from that plane by
  construction; cheapest null-breaking record: variability/compactness =>
  Gamma bound. [Dr]

Run: pytest ap/ap2_fxt_amati.py -q
"""


def deboosted_position(b, p):
    """Start ON the Amati locus E_p = k*E_iso^0.5 (k=1, E_iso=1 wlog).
    Doppler factor ratio b>1: E_p -> E_p/b, E_iso -> E_iso/b**p.
    Return E_p / (k*E_iso^0.5): >1 above locus, <1 below (FXT territory)."""
    ep, eiso = 1.0/b, 1.0/b**p
    return ep / eiso**0.5


def test_extended_jet_stays_on_locus():
    """E_iso ~ b^-2: deboosting slides EXACTLY along the Amati locus."""
    for b in (2, 5, 10, 30, 100):
        assert abs(deboosted_position(b, 2) - 1.0) < 1e-12


def test_compact_jet_goes_above_locus():
    """E_iso ~ b^-3: deboosting pushes ABOVE the locus, monotonically in b."""
    prev = 1.0
    for b in (2, 5, 10, 30, 100):
        r = deboosted_position(b, 3)
        assert r > prev
        prev = r


def test_below_locus_unreachable_by_viewing_angle():
    """For ANY scaling between the two regimes (2 <= p <= 3) and any b > 1,
    the deboosted point never falls below the locus => within this family,
    low-E_p-at-high-E_iso FXTs cannot be made by viewing angle alone.
    (Family-scoped support for the paper's refutation direction -- structured
    jets with angle-dependent E_p are outside scope; see module docstring.)"""
    for p in (2.0, 2.25, 2.5, 2.75, 3.0):
        for b in (1.5, 2, 5, 10, 30, 100, 1000):
            assert deboosted_position(b, p) >= 1.0 - 1e-12
