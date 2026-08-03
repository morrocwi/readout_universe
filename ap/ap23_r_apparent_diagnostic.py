"""AP23 -- a fresh, self-contained finite_diagnostic toy model for
philosophy.md's section 5.2c ("R-ideal and R-apparent"), built to close
the concrete next step that section names but explicitly does not
attempt: a measured signature for when a bounded reader's own residual
starts looking indistinguishable from continuum noise, at a declared
resolution parameter, over a substrate that stays genuinely discrete
throughout. Nothing in this file is copied or adapted from any
proprietary source; every definition and result below was written and
run fresh for this file.

WHAT SECTION 5.2c CLAIMS (restated here in this file's own words, not
quoted verbatim): a genuinely discrete substrate -- no density smuggled
in, tick by tick the whole way down -- can nevertheless APPEAR
continuous to a bounded reader once that reader's own resolution
(tau_c(A), how many ticks they integrate over per reading) exceeds the
substrate's own tick spacing. "R-apparent" names that appearance; it is
agency-relative (two readers with two different tau_c would see two
different degrees of apparent smoothness of the SAME substrate), never
a property of the substrate's own density (which stays provably absent
regardless of scale).

TOY MODEL (entirely fresh, no proprietary reuse): a discrete random-walk
substrate x[n] built from fixed +/-1 ticks (genuinely discrete, no
continuum limit taken). A reader at resolution w integrates over a
window of w ticks (a moving average -- modeling active
integration/interpolation, per this session's own correction to the
TV-pixel analogy in section 5.2c: not mere failure-to-resolve, a real
mechanism doing work). "Roughness" -- mean absolute discrete second
difference -- is the discreteness detector: high roughness means the
individual ticks are still visible in the readout; roughness collapsing
toward zero (relative to the raw substrate's own roughness) means the
readout looks smooth to that reader, even though the substrate itself
never changed.

WHAT IS MEASURED, NOT ASSUMED: (1) that the raw substrate's own
roughness does NOT shrink merely by adding more ticks (N) -- confirming
discreteness is a property of resolution, not of scale, matching this
corpus's own "density is provably absent at the root, at every scale"
claim; (2) that roughness, relative to the raw substrate's own
roughness, monotonically decreases as the reader's window w grows, and
crosses a declared threshold (0.05 of raw) at a measured critical w* --
an actual number, not asserted in advance; (3) that two readers with
different w produce measurably different relative roughness on the
IDENTICAL underlying substrate -- the concrete demonstration of
agency-relativity section 5.2c's own prose argues for narratively.

WHAT THIS DOES NOT SHOW: this is a toy scalar random walk with a linear
moving-average reader, not a claim about real human perceptual
resolution, real tau_c values, or any specific physical system. It does
not formalize "R-ideal" at all (R-ideal is explicitly not a readout of
anything, by section 5.2c's own account -- there is nothing here to
measure). It supplies, at finite_diagnostic tier only, the first
EXECUTED numeric check that section 5.2c's own claimed signature
(discreteness collapsing with resolution, not with scale; agency-
relative outcomes on one substrate) is measurable and internally
coherent in a toy setting -- nothing about real readers or real
continuum illusions is claimed or tested here. Section 5.2c itself
remains Dr; running this file does not upgrade it.

Run: pytest ap/ap23_r_apparent_diagnostic.py -q
"""
import numpy as np

N = 8000
SEED = 7
STEP_SIZE = 1.0
REL_THRESHOLD = 0.05
W_LADDER = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]


def discrete_substrate(n=N, seed=SEED, step_size=STEP_SIZE):
    """A genuinely discrete tick-by-tick substrate: a +/-step_size random
    walk, no continuum limit taken, no density smuggled in."""
    rng = np.random.default_rng(seed)
    steps = rng.choice([-step_size, step_size], size=n)
    return np.cumsum(steps)


def reader_readout(x, w):
    """Reader at resolution w: a moving-average integration over w ticks
    (active integration, not mere failure-to-resolve -- see module
    docstring). w=1 is the substrate itself, unread."""
    if w <= 1:
        return x.copy()
    kernel = np.ones(w) / w
    return np.convolve(x, kernel, mode='valid')


def roughness(y):
    """Discreteness detector: mean absolute discrete second difference.
    High roughness = individual ticks still visible; near-zero relative
    roughness = looks smooth to this reader."""
    d2 = y[2:] - 2 * y[1:-1] + y[:-2]
    return float(np.mean(np.abs(d2)))


def test_raw_roughness_is_scale_invariant_not_size_invariant():
    """Discreteness is a property of resolution, not of how much data a
    reader has -- the raw substrate (w=1) should NOT get smoother just
    because N grows. Matches this corpus's own claim that density is
    provably absent at the root at every scale, not just small ones."""
    roughnesses = [roughness(discrete_substrate(n=n)) for n in (1000, 5000, 20000)]
    # MEASURED this run: all three within a narrow band around 1.0
    # (expected: E|step_i - 2*step_{i+1} + step_{i+2}| for +/-1 iid steps).
    assert max(roughnesses) / min(roughnesses) < 1.2, (
        f"unexpected: raw roughness varied by more than 20% across N -- "
        f"got {roughnesses}; section 5.2c's own claim that discreteness "
        f"doesn't disappear with scale would need to be reported as NOT "
        f"confirmed in this toy setting if this assertion fails"
    )


def test_relative_roughness_decreases_monotonically_with_resolution():
    """The core falsifiable signature: as a reader's resolution window w
    grows, their readout of the SAME substrate should look monotonically
    smoother (relative roughness shrinking toward 0), and cross a
    declared threshold at a measurable, reported critical w*."""
    x = discrete_substrate()
    raw_r = roughness(reader_readout(x, 1))
    rel_roughnesses = [roughness(reader_readout(x, w)) / raw_r for w in W_LADDER]

    # MEASURED this run (fixed seed): monotonically decreasing, crossing
    # 0.05 at w*=21 (see ladder above; reported for the record).
    assert all(rel_roughnesses[i] > rel_roughnesses[i + 1] for i in range(len(rel_roughnesses) - 1)), (
        f"unexpected: relative roughness was not monotonically decreasing "
        f"in w -- got {rel_roughnesses}; section 5.2c's own falsifier "
        f"would need to be reported as NOT confirmed in this toy setting "
        f"if this assertion fails"
    )

    crit_w = next((w for w, r in zip(W_LADDER, rel_roughnesses) if r < REL_THRESHOLD), None)
    assert crit_w is not None, (
        f"unexpected: relative roughness never dropped below "
        f"{REL_THRESHOLD} across the tested window ladder {W_LADDER} -- "
        f"got {rel_roughnesses}"
    )
    # MEASURED this run: crit_w == 21 at REL_THRESHOLD=0.05, fixed seed=7.


def test_agency_relativity_two_readers_one_substrate():
    """Two readers with different resolution windows, reading the exact
    same discrete substrate, should measurably disagree on how smooth it
    looks -- the concrete demonstration of R-apparent's agency-relativity,
    not a claim about any specific reader's real value of tau_c."""
    x = discrete_substrate()
    raw_r = roughness(reader_readout(x, 1))
    rel_A = roughness(reader_readout(x, 5)) / raw_r
    rel_B = roughness(reader_readout(x, 200)) / raw_r

    # MEASURED this run: rel_A ~ 0.200 (w=5), rel_B ~ 0.005 (w=200) --
    # same substrate, two different apparent smoothnesses.
    assert rel_B < rel_A, (
        f"unexpected: the higher-resolution reader (w=200) did not see a "
        f"smoother readout than the lower-resolution reader (w=5) on the "
        f"identical substrate -- rel_A={rel_A:.4f}, rel_B={rel_B:.4f}; "
        f"agency-relativity would need to be reported as NOT confirmed "
        f"in this toy setting if this assertion fails"
    )
    assert rel_A > 5 * rel_B, (
        f"unexpected: the two readers' apparent smoothness was not "
        f"substantially different (rel_A={rel_A:.4f}, rel_B={rel_B:.4f}) "
        f"-- the toy model's agency-relativity signature would be too "
        f"weak to call a genuine demonstration"
    )
