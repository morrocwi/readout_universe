"""AP12 -- THE GRAPH SPITS OUT THE ATOM: 1/d_s computed from L_R alone.

Closes (at finite_diagnostic, torus scope) the geometric half of AP11's
final falsifier: the universal screening atom 1/d is a DIRECTION-PARTITION
READOUT of the graph -- on Z_n^d torus substrates, the fraction of a random
low-pass field's Dirichlet energy carried by ONE axis equals 1/d, and the
same graphs' heat-kernel spectral dimension reads d. Both computed from the
Laplacian alone; no continuum, no QFT input.

    d=1: partition 1.0000 (exact)   spectral-dim ~1.1
    d=2: partition ~0.486           spectral-dim ~2.3
    d=3: partition ~0.342           spectral-dim ~3.3

EXACT-BY-SYMMETRY note: for axis-symmetric mode ensembles the partition is
exactly 1/d (d identical per-axis terms summing to the total); the sampled
values approach it with ensemble size -- MC is illustration, symmetry is
the proof (same epistemic split as AP11's <cos^2> test).

HONEST SCOPE: this closes the GEOMETRIC content ("the 1/3 is a dimension
readout, and our graphs compute their own dimension") on REGULAR TORI. It
is NOT a QFT derivation of the diamagnetic loop term on a graph (gauge
field + vacuum polarization on the graph = still open), and irregular /
non-integer-d_s substrates are untested [Open -- sharp next probe: does an
irregular graph with fractal d_s give partition 1/d_s?].

TERMINAL FRONTIER after this file (the two remaining atoms-of-atoms):
 (1) the paramagnetic law (2s)^2 from graph channel structure (g=2 of the
     gauge channel) -- [Open]
 (2) the statistics sign (-1)^{2s} (spin-statistics on the graph) -- [Open]

Run: pytest ap/ap12_dimension_readout.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
import numpy as np

RNG_SEED = 7


def ring_L(n: int) -> np.ndarray:
    return 2 * np.eye(n) - np.roll(np.eye(n), 1, 0) - np.roll(np.eye(n), -1, 0)


def torus_axis_laplacians(n: int, d: int) -> list[np.ndarray]:
    """Per-axis Laplacians of Z_n^d; the full L_R is their sum."""
    eye = np.eye(n)
    mats = []
    for ax in range(d):
        m = None
        for k in range(d):
            f = ring_L(n) if k == ax else eye
            m = f if m is None else np.kron(m, f)
        mats.append(m)
    return mats


def direction_partition(n: int, d: int, draws: int = 40) -> float:
    """Fraction of Dirichlet energy on axis 0 for random low-pass fields."""
    axes = torus_axis_laplacians(n, d)
    L = sum(axes)
    lam, V = np.linalg.eigh(L)
    k = max(4, L.shape[0] // 8)
    rng = np.random.default_rng(RNG_SEED)
    ratios = []
    for _ in range(draws):
        f = V[:, 1:k + 1] @ rng.normal(size=k)
        ratios.append(float(f @ axes[0] @ f) / float(f @ L @ f))
    return float(np.mean(ratios))


def spectral_dimension(n: int, d: int) -> float:
    """Heat-kernel log-slope estimate: P(t) = Tr e^{-tL}/N ~ t^{-ds/2}."""
    L = sum(torus_axis_laplacians(n, d))
    lam = np.linalg.eigvalsh(L)
    ts = np.geomspace(0.5, 4.0, 8)
    P = [np.exp(-t * lam).sum() / len(lam) for t in ts]
    slope = np.polyfit(np.log(ts), np.log(P), 1)[0]
    return float(-2 * slope)


def test_partition_reads_one_over_d():
    """The atom, from the graph: axis energy fraction = 1/d on d=1,2,3."""
    assert abs(direction_partition(64, 1) - 1.0) < 1e-9   # d=1 exact
    assert abs(direction_partition(16, 2) - 0.5) < 0.05   # measured 0.486
    assert abs(direction_partition(8, 3) - 1 / 3) < 0.05  # measured 0.342


def test_graph_reads_its_own_dimension():
    """Spectral dimension from the heat kernel orders and brackets d
    (coarse window on small tori -- ballpark tier, declared)."""
    d1, d2, d3 = spectral_dimension(64, 1), spectral_dimension(16, 2), spectral_dimension(8, 3)
    assert 0.8 < d1 < 1.5
    assert 1.8 < d2 < 2.7
    assert 2.7 < d3 < 3.8
    assert d1 < d2 < d3


def test_partition_tracks_dimension_not_size():
    """Control: changing torus SIZE at fixed d must not move the partition
    (it reads dimension, not node count). Ensemble 160 draws per size
    (40 was under-sampled: caught red on first run -- honest fix is MORE
    statistics, not a looser bound; measured 0.4813 vs 0.5061)."""
    a = direction_partition(12, 2, draws=160)
    b = direction_partition(20, 2, draws=160)
    assert abs(a - b) < 0.04                      # measured |diff| = 0.0248
    assert abs(a - 0.5) < 0.05 and abs(b - 0.5) < 0.05
