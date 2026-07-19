"""graph_structure.py — cheap structure detection + EXACT transform-diagonalization routes for the
router (engine/router.py).

Three graph families have a CLOSED-FORM diagonalization of their (unit-weight) Laplacian, so
exp(-tL)v can be computed via a fast transform instead of any iterative/eigh numerics:

  * path (chain), uniform weight w        -> DCT-II/III pair          (Neumann discrete Laplacian)
  * cycle, uniform weight w                -> DFT (circulant matrix)
  * 2D rectangular grid, uniform weight w  -> separable DCT-II/III on each axis
                                               (L = L_rows ⊕ L_cols, a Kronecker SUM, so
                                               exp(-tL) = exp(-tL_rows) ⊗ exp(-tL_cols) — apply
                                               axis-by-axis on the reshaped (rows, cols) array)

These formulas are registered in docs/root/EQUATION_REGISTRY.md (discrete Laplacian eigenbases via
DCT/DFT — standard spectral graph theory / discrete Fourier analysis).

Detection is O(n) or O(E): compute the degree sequence + edge multiset for the candidate structure
and compare it EXACTLY against the given edge list (a cheap, honest verifier) before trusting the
detection — never a probabilistic guess. If verification fails, `detect(...)` reports no match and
the router falls back to the generic sparse/dense routes.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.fft import dct, idct, dctn, idctn


@dataclass
class StructureMatch:
    kind: str            # "path" | "cycle" | "grid2d"
    params: dict          # e.g. {"n": N, "w": weight} or {"rows": r, "cols": c, "w": weight}
    verified: bool
    reason: str


def _edge_multiset(edges):
    """canonical (unordered-pair, weight) multiset for exact comparison."""
    return sorted((min(u, v), max(u, v), round(float(w), 12)) for u, v, w in edges)


def _expected_path_edges(n, w):
    return [(i, i + 1, w) for i in range(n - 1)]


def _expected_cycle_edges(n, w):
    return [(i, (i + 1) % n, w) for i in range(n)]


def _expected_grid2d_edges(rows, cols, w):
    e = []
    def idx(r, c): return r * cols + c
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols:
                e.append((idx(r, c), idx(r, c + 1), w))
            if r + 1 < rows:
                e.append((idx(r, c), idx(r + 1, c), w))
    return e


def detect(edges, n: int) -> StructureMatch | None:
    """Cheap detector + exact verifier. edges: iterable of (u, v, w). Returns None if no registered
    exact structure matches (router should fall back to generic sparse/dense routes)."""
    edges = list(edges)
    if not edges:
        return None
    weights = {round(float(w), 12) for _, _, w in edges}
    if len(weights) != 1:
        return None   # non-uniform weight -> no closed form here (honest bail-out)
    w = next(iter(weights))
    actual = _edge_multiset(edges)

    # path: n-1 edges, degree sequence [1,1,2,2,...]
    if len(edges) == n - 1:
        expected = _edge_multiset(_expected_path_edges(n, w))
        if actual == expected:
            return StructureMatch("path", {"n": n, "w": w}, True,
                                   "edge multiset exactly matches a unit-weight path graph on n nodes")

    # cycle: n edges, all degree 2
    if len(edges) == n:
        expected = _edge_multiset(_expected_cycle_edges(n, w))
        if actual == expected:
            return StructureMatch("cycle", {"n": n, "w": w}, True,
                                   "edge multiset exactly matches a unit-weight cycle graph on n nodes")

    # 2D grid: try small factor pairs of n only (cheap: divisors of n, capped)
    for rows in range(2, int(n ** 0.5) + 2):
        if n % rows != 0:
            continue
        cols = n // rows
        if rows > cols:
            continue
        expected_edges = _expected_grid2d_edges(rows, cols, w)
        if len(expected_edges) != len(edges):
            continue
        expected = _edge_multiset(expected_edges)
        if actual == expected:
            return StructureMatch("grid2d", {"rows": rows, "cols": cols, "w": w}, True,
                                   f"edge multiset exactly matches a unit-weight {rows}x{cols} grid graph")
    return None


def laplacian_matches_edges(L, edges, n: int, *, rtol: float = 1e-12) -> bool:
    """FULL O(nnz) verification that the operator L actually IS the free/Neumann graph Laplacian
    implied by `edges` — diagonal (weighted degrees), every off-diagonal entry, and no extra
    entries. This gate prevents the exact-transform routes from being applied to a MODIFIED
    operator (e.g. a Dirichlet pin L[i,i]+=c added without touching the edge list): the closed
    forms diagonalize the edge-implied Laplacian, not whatever matrix the caller handed in, so a
    mismatch here must refuse the exact route (the router then falls back to L-based numerics)."""
    import scipy.sparse as _sp
    exp_diag = np.zeros(n)
    exp_off: dict = {}
    for u, v, w in edges:
        u, v, w = int(u), int(v), float(w)
        exp_diag[u] += w
        exp_diag[v] += w
        exp_off[(u, v)] = exp_off.get((u, v), 0.0) - w
        exp_off[(v, u)] = exp_off.get((v, u), 0.0) - w
    scale = max(float(np.max(np.abs(exp_diag))), 1e-300)
    atol = rtol * scale
    if _sp.issparse(L):
        C = L.tocoo()
        got_diag = np.zeros(n)
        got_off: dict = {}
        for i, j, val in zip(C.row, C.col, C.data):
            if i == j:
                got_diag[i] += val
            else:
                got_off[(int(i), int(j))] = got_off.get((int(i), int(j)), 0.0) + float(val)
    else:
        Ld = np.asarray(L)
        got_diag = np.diag(Ld).copy()
        got_off = {}
        off = Ld - np.diag(np.diag(Ld))
        ii, jj = np.nonzero(off)
        for i, j in zip(ii, jj):
            got_off[(int(i), int(j))] = float(Ld[i, j])
    if not np.allclose(got_diag, exp_diag, rtol=0, atol=atol):
        return False
    got_off = {k: v for k, v in got_off.items() if abs(v) > atol}
    exp_off = {k: v for k, v in exp_off.items() if abs(v) > atol}
    if set(got_off) != set(exp_off):
        return False
    return all(abs(got_off[k] - exp_off[k]) <= atol for k in exp_off)


# ───────────────────────── exact fast-transform routes ─────────────────────────
def path_eigenvalues(n: int, w: float) -> np.ndarray:
    k = np.arange(n)
    return 2.0 * w * (1.0 - np.cos(k * np.pi / n))


def cycle_eigenvalues(n: int, w: float) -> np.ndarray:
    k = np.arange(n)
    return 2.0 * w * (1.0 - np.cos(2.0 * np.pi * k / n))


def path_heat_apply(t: float, v: np.ndarray, n: int, w: float) -> np.ndarray:
    """exp(-tL)v for the unit-weight (scaled by w) path graph Laplacian, via DCT-II/III (O(n log n))."""
    lam = path_eigenvalues(n, w)
    axis = 0
    c = dct(v, type=2, norm="ortho", axis=axis)
    damp = np.exp(-t * lam)
    c = (damp[:, None] * c) if v.ndim == 2 else (damp * c)
    return idct(c, type=2, norm="ortho", axis=axis)


def cycle_heat_apply(t: float, v: np.ndarray, n: int, w: float) -> np.ndarray:
    """exp(-tL)v for the unit-weight cycle graph Laplacian, via FFT (O(n log n))."""
    lam = cycle_eigenvalues(n, w)
    axis = 0
    c = np.fft.fft(v, axis=axis)
    damp = np.exp(-t * lam)
    c = (damp[:, None] * c) if v.ndim == 2 else (damp * c)
    out = np.fft.ifft(c, axis=axis)
    return np.real(out) if not np.iscomplexobj(v) else out


def grid2d_heat_apply(t: float, v: np.ndarray, rows: int, cols: int, w: float) -> np.ndarray:
    """exp(-tL)v for the unit-weight rows x cols grid graph Laplacian, L = L_rows (+) L_cols
    (Kronecker SUM) -> exp(-tL) = exp(-tL_rows) kron exp(-tL_cols), applied as a separable 2D DCT
    (O(n log n), n = rows*cols). v is (n,) or (n, q); reshaped to (rows, cols[, q])."""
    lam_r = path_eigenvalues(rows, w)
    lam_c = path_eigenvalues(cols, w)
    q = v.shape[1] if v.ndim == 2 else None
    shape = (rows, cols, q) if q is not None else (rows, cols)
    V = v.reshape(shape, order="C")
    C = dctn(V, type=2, norm="ortho", axes=(0, 1))
    damp = lam_r[:, None] + lam_c[None, :]
    damp = np.exp(-t * damp)
    if q is not None:
        damp = damp[:, :, None]
    C = damp * C
    out = idctn(C, type=2, norm="ortho", axes=(0, 1))
    return out.reshape(v.shape, order="C")
