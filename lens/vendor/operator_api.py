"""
operator_api.py — the public compute interface for the information operator 𝓘  (API v1.1.0)

ONE operator, six readouts: `info`/R0_ENERGY, `is_psd`/R1_PSD, `spectrum`/R2_SPECTRUM,
`evolve`/R4_EVOLVE, `box`/R5_BOX, `kernel_has_constants`/R6_KERNEL. Build once from a weighted
graph; every domain is a readout.

Note: this module does NOT itself define an R3 (fixed-point) or R7 (curvature) readout — the
higher-level `engine.universe.Readout` enum ships EIGHT members (R0–R7), adding
`R3_FIXEDPOINT` and `R7_CURVATURE` (the latter permanently `[Open]`, gated on
`nonperturbative_qg`). "Six readouts" here describes this file's own `Operator` surface only;
it is not a claim that the wider Universe API also has only six.

READOUT-NOT-TRUTH, made operational with a TWO-AXIS tier on every result:
  • structure_tier — the tier of the LAW (machine-checked in formal/URCF_RD_All.v): "Th_coqc" (axiom-free)
    or "+reals" (continuum, +reals axioms).
  • value_tier — how THIS number was produced: "exact_Q" (an exact rational matching Coq vm_compute) or
    "finite_diagnostic" (a float / eigensolver / tolerance verdict — a measurement).
A float verdict (eigvalsh, np.allclose, any IEEE float) is ALWAYS value_tier="finite_diagnostic" even when
its structural law is axiom-free. A tier is only ever lowered, never raised. Out-of-hypothesis inputs raise
typed errors BEFORE any tier is attached. Certified against the kernel by scripts/bridge_engine_vs_kernel.py.
Spec: docs/root/OPERATOR_API.md · cards: docs/root/INTERPRETATION_CARDS.md.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Generic, NamedTuple, TypeVar, Any, Callable
import math
import numpy as np

# Optional scipy.sparse backend (large graphs). Guarded: fall back to dense numpy if unavailable.
try:  # pragma: no cover - import guard
    import scipy.sparse as _sp
    import scipy.sparse.linalg as _spla
    _HAS_SCIPY = True
except Exception:  # pragma: no cover - scipy missing ⇒ dense everywhere
    _sp = None
    _spla = None
    _HAS_SCIPY = False

__api_version__ = "1.1.0"
MAX_N = 512          # eigh is O(n³); cap dense allocation/compute (override via Operator(..., max_n=))
MAX_EDGES = 4096
SPARSE_N = 128       # n ≥ SPARSE_N routes lambda_max / principal-vector / evolve via scipy.sparse (if present)

STRUCTURE_TIERS = ("Th_coqc", "+reals")
VALUE_TIERS = ("exact_Q", "finite_diagnostic")
_RANK = {"Th_coqc": 0, "+reals": 1, "exact_Q": 0, "finite_diagnostic": 2}

__all__ = ["Operator", "Result", "Eigen", "list_domains", "domain_signature",
           "self_check", "MAX_N", "MAX_EDGES", "SPARSE_N", "__api_version__"]

T = TypeVar("T")


@dataclass(frozen=True, slots=True, eq=False)
class Result(Generic[T]):
    """A readout certificate: the value + the two-axis tier + the Coq theorem certifying its structure."""
    value: T
    structure_tier: str   # ∈ STRUCTURE_TIERS — tier of `law`
    value_tier: str       # ∈ VALUE_TIERS — how this number was produced
    law: str              # Coq theorem id (formal/*.v) certifying the readout's STRUCTURE
    unit: "str | None" = None   # machine-checkable physical unit of `value` (e.g. "s", "J");
                                 # None ⇒ not declared (as before) — purely additive, no card is
                                 # retrofitted with units by this change.
    def __post_init__(self):
        if self.structure_tier not in STRUCTURE_TIERS:
            raise ValueError(f"bad structure_tier {self.structure_tier!r}")
        if self.value_tier not in VALUE_TIERS:
            raise ValueError(f"bad value_tier {self.value_tier!r}")

    @property
    def tier(self) -> str:
        """Back-compat single tier = the weaker of structure/value."""
        return self.value_tier if _RANK[self.value_tier] >= _RANK[self.structure_tier] else self.structure_tier

    def __repr__(self):
        v = self.value
        vs = (f"{v:.6g}" if isinstance(v, (int, float)) else
              (f"ndarray{tuple(v.shape)}" if isinstance(v, np.ndarray) else
               ("None(abstain)" if v is None else type(v).__name__)))
        return f"Result({vs}  [struct={self.structure_tier} · value={self.value_tier} · {self.law}])"

    def to_dict(self):
        v = self.value
        if isinstance(v, np.ndarray):
            v = ({"re": v.real.tolist(), "im": v.imag.tolist()} if np.iscomplexobj(v) else v.tolist())
        return {"value": v, "structure_tier": self.structure_tier,
                "value_tier": self.value_tier, "law": self.law, "unit": self.unit}

    @classmethod
    def from_dict(cls, d) -> "Result":
        """Inverse of to_dict: rebuild a Result, reviving ndarray / complex-ndarray values."""
        v = d["value"]
        if isinstance(v, dict) and "re" in v and "im" in v:        # complex ndarray round-trip
            v = np.asarray(v["re"], float) + 1j * np.asarray(v["im"], float)
        elif isinstance(v, list):                                  # real ndarray round-trip
            v = np.asarray(v)
        return cls(v, d["structure_tier"], d["value_tier"], d["law"], d.get("unit"))

    def __eq__(self, other) -> bool:
        if other.__class__ is not self.__class__:
            return NotImplemented
        if (self.structure_tier, self.value_tier, self.law) != \
           (other.structure_tier, other.value_tier, other.law):
            return False
        a, b = self.value, other.value
        if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
            return np.array_equal(a, b)
        if isinstance(a, Eigen) and isinstance(b, Eigen):
            return (np.array_equal(a.eigenvalues, b.eigenvalues) and
                    np.array_equal(a.eigenvectors, b.eigenvectors))
        return bool(a == b)

    def __hash__(self):          # consistent with __eq__ (equal Results hash equal); ndarray-safe
        return hash((self.structure_tier, self.value_tier, self.law))

    def _repr_html_(self) -> str:
        v = self.value
        if isinstance(v, np.ndarray):
            vs = f"ndarray&nbsp;{tuple(v.shape)}"
        elif v is None:
            vs = "None&nbsp;(abstain)"
        elif isinstance(v, (int, float)):
            vs = f"{v:.6g}"
        else:
            vs = str(v).replace("<", "&lt;").replace(">", "&gt;")
        rows = (("value", vs), ("structure_tier", self.structure_tier),
                ("value_tier", self.value_tier), ("law", self.law))
        body = "".join(
            f"<tr><th style='text-align:left;padding:2px 8px'>{k}</th>"
            f"<td style='padding:2px 8px'><code>{val}</code></td></tr>" for k, val in rows)
        return ("<table style='border-collapse:collapse;font-family:monospace'>"
                "<caption style='text-align:left;font-weight:bold'>Result (readout-not-truth)</caption>"
                f"{body}</table>")


class Eigen(NamedTuple):
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray


def _finite(x) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(x)


class Operator:
    """The graph operator L_R = 𝓘 (weighted graph Laplacian). Immutable; build once, read out many domains."""

    def __init__(self, edges, n: int | None = None, *, exact: bool = False,
                 max_n: int = MAX_N, max_edges: int = MAX_EDGES):
        edges = list(edges)
        if len(edges) > max_edges:
            raise ValueError(f"too many edges ({len(edges)} > MAX_EDGES={max_edges})")
        norm = []
        for e in edges:
            if len(e) != 3:
                raise ValueError(f"edge must be (u, v, w), got {e!r}")
            u, v, w = int(e[0]), int(e[1]), float(e[2])
            if u == v:
                raise ValueError(f"self-loop not allowed: ({u},{v})")
            if not (math.isfinite(w) and w > 0):
                raise ValueError(f"edge weight must be finite and > 0 (info_nonneg/PSD hypothesis): {w}")
            norm.append((u, v, w))
        nn = n if n is not None else (1 + max((max(u, v) for u, v, _ in norm), default=-1))
        if nn <= 0:
            raise ValueError("empty graph (n must be ≥ 1) — there is nothing to certify")
        if nn > max_n:
            raise ValueError(f"n={nn} exceeds MAX_N={max_n} (O(n³) guard); raise max_n explicitly if intended")
        for u, v, _ in norm:
            if not (0 <= u < nn and 0 <= v < nn):
                raise ValueError(f"node id out of range [0,{nn}): edge ({u},{v})")
        self._n = nn
        self._edges = tuple(norm)
        self._exact = bool(exact)
        L = np.zeros((nn, nn))
        for u, v, w in norm:
            L[u, u] += w; L[v, v] += w; L[u, v] -= w; L[v, u] -= w
        L.flags.writeable = False
        self._L = L
        self._eig: Eigen | None = None
        self._eigA: Eigen | None = None
        # Optional sparse CSR copy for large graphs (routes lambda_max / principal-vector / evolve).
        # MAX_N semantics unchanged: this is an *additional* representation, not a different cap.
        self._csr = _sp.csr_matrix(L) if (_HAS_SCIPY and nn >= SPARSE_N) else None
        self._csrA = None   # adjacency CSR, built lazily

    # ── immutable accessors ──
    @property
    def n(self) -> int: return self._n
    @property
    def edges(self) -> tuple: return self._edges
    @property
    def L(self) -> np.ndarray: return self._L

    def adjacency(self) -> np.ndarray:
        A = np.zeros((self._n, self._n))
        for u, v, w in self._edges:
            A[u, v] += w; A[v, u] += w
        A.flags.writeable = False
        return A

    def _eigL(self) -> Eigen:
        if self._eig is None:
            w, V = np.linalg.eigh(self._L)
            self._eig = Eigen(w, V)
        return self._eig

    def _eigAdj(self) -> Eigen:
        if self._eigA is None:
            w, V = np.linalg.eigh(self.adjacency())
            self._eigA = Eigen(w, V)
        return self._eigA

    def _csr_adj(self):
        """Sparse CSR adjacency for large graphs (None ⇒ use dense). Same float values as adjacency()."""
        if self._csrA is None and _HAS_SCIPY and self._n >= SPARSE_N:
            self._csrA = _sp.csr_matrix(self.adjacency())
        return self._csrA

    def _adj_top(self, k: int):
        """k largest-algebraic (value, vector) of adjacency, sparse path when large; (None ⇒ dense).
        Returns (w, V) ascending like numpy.linalg.eigh, or None to signal the dense fallback."""
        csrA = self._csr_adj()
        if csrA is None or k >= self._n:
            return None
        try:
            w, V = _spla.eigsh(csrA, k=k, which="LA")
            order = np.argsort(w)
            return w[order], V[:, order]
        except Exception:   # pragma: no cover - eigsh convergence ⇒ fall back to dense
            return None

    def _check_x(self, x, allow_complex: bool = False) -> np.ndarray:
        a = np.asarray(x, complex) if allow_complex else np.asarray(x, float)  # complex: keep imaginary part
        if a.shape[-1] != self._n:
            raise ValueError(f"DIM_MISMATCH: x last axis {a.shape[-1]} != n={self._n}")
        if not np.all(np.isfinite(a)):
            raise ValueError("x contains non-finite values")
        return a

    # ── OP2 / R0 — energy = retained information ──
    def info(self, x) -> Result:
        a = self._check_x(x)
        if self._exact and a.ndim == 1:
            xf = [Fraction(str(float(t))) for t in a]
            val = sum(Fraction(str(w)) * (xf[u] - xf[v]) ** 2 for u, v, w in self._edges)
            return Result(val, "Th_coqc", "exact_Q", "InfoOperator.info_is_operator_energy")
        val = float(np.einsum("...i,ij,...j->...", a, self._L, a)) if a.ndim == 1 else \
              np.einsum("...i,ij,...j->...", a, self._L, a)
        return Result(val, "Th_coqc", "finite_diagnostic", "InfoOperator.info_is_operator_energy")

    # ── R1 — PSD (tolerance-gated float verdict) ──
    def is_psd(self, tol=1e-9) -> Result:
        return Result(bool(np.all(self._eigL().eigenvalues >= -tol)),
                      "Th_coqc", "finite_diagnostic", "InfoOperator.info_nonneg")

    # ── R6 — kernel ⊇ constants ──
    def kernel_has_constants(self, tol=1e-9) -> Result:
        return Result(bool(np.allclose(self._L @ np.ones(self._n), 0.0, atol=tol)),
                      "Th_coqc", "finite_diagnostic", "InfoDtN.nodeLap_const")

    # ── OP3 / R2 — spectrum ──
    def spectrum(self) -> Result:
        e = self._eigL()
        return Result(Eigen(e.eigenvalues.copy(), e.eigenvectors.copy()),
                      "Th_coqc", "finite_diagnostic", "InfoSpectral2")

    def lambda_max(self) -> Result:
        if self._csr is not None:                       # large-N: principal value via sparse eigsh(k=1)
            try:
                lam = float(_spla.eigsh(self._csr, k=1, which="LA",
                                        return_eigenvectors=False)[0])
                return Result(lam, "Th_coqc", "finite_diagnostic",
                              "InfoSpectral2.sym2_disc_nonneg")
            except Exception:                           # pragma: no cover - fall back to dense
                pass
        return Result(float(self._eigL().eigenvalues[-1]),
                      "Th_coqc", "finite_diagnostic", "InfoSpectral2.sym2_disc_nonneg")

    # ── OP4 / R4 — evolution ──
    def evolve(self, x, t: float, unitary: bool = True) -> Result:
        if not _finite(t):
            raise ValueError("t must be finite")
        a = self._check_x(x, allow_complex=unitary)     # unitary states may be complex (keep imaginary part)
        if self._csr is not None and a.ndim == 1:       # large-N: sparse matrix exponential action
            try:
                if unitary:
                    res = _spla.expm_multiply(-1j * t * self._csr, a.astype(complex))
                    return Result(np.asarray(res), "+reals", "finite_diagnostic",
                                  "InfoHilbertBridge.multimode_preserves_norm")
                res = _spla.expm_multiply(-t * self._csr, a.astype(float))
                return Result(np.asarray(res), "+reals", "finite_diagnostic",
                              "RDL_SpineGraphEnergy.total_energy_nonincreasing")
            except Exception:                           # pragma: no cover - fall back to dense
                pass
        w, V = self._eigL()
        if unitary:
            c = (V.T @ a.astype(complex)) * np.exp(-1j * w * t)
            return Result(V @ c, "+reals", "finite_diagnostic",
                          "InfoHilbertBridge.multimode_preserves_norm")
        c = (V.T @ a) * np.exp(-w * t)
        return Result(V @ c, "+reals", "finite_diagnostic",
                      "RDL_SpineGraphEnergy.total_energy_nonincreasing")

    # ── OP5 / R5 — Lorentzian d'Alembertian □ = sign·∂tt + ∂xx on a sampled field f[t,x] ──
    @staticmethod
    def box(f, ht: float, hx: float, sign: int = -1) -> Result:
        if sign not in (-1, 1):
            raise ValueError("sign must be -1 (timelike/Lorentzian) or +1 (spacelike)")
        if not (_finite(ht) and ht > 0 and _finite(hx) and hx > 0):
            raise ValueError("ht, hx must be finite and > 0")
        f = np.asarray(f, float)
        if f.ndim != 2 or f.shape[0] < 3 or f.shape[1] < 3:
            raise ValueError("f must be a 2-D grid with each axis ≥ 3")
        if not np.all(np.isfinite(f)):
            raise ValueError("f contains non-finite values")
        d2t = (f[2:, 1:-1] - 2 * f[1:-1, 1:-1] + f[:-2, 1:-1]) / ht ** 2   # interior (T-2, X-2)
        d2x = (f[1:-1, 2:] - 2 * f[1:-1, 1:-1] + f[1:-1, :-2]) / hx ** 2
        return Result(sign * d2t + d2x, "+reals", "finite_diagnostic",
                      "InfoLorentzContinuum.lorentz_box_continuum")

    # ── OP6 — domain dispatch (declarative card registry) ──
    def readout(self, domain: str, **params) -> Result:
        card = _resolve_card(domain)
        missing = [p for p in card.required if p not in params]
        if missing:
            raise TypeError(f"readout({domain!r}) missing required params: {missing}")
        return card.fn(self, params)


# ── domain cards: each maps a domain to a readout; tier copied verbatim, never relabeled ──
class _Card(NamedTuple):
    name: str
    aliases: tuple
    required: tuple
    structure_tier: str
    value_tier: str
    law: str
    fn: Callable[["Operator", dict], Result]

def _bio(op, p):
    top = op._adj_top(1)                            # large-N: spectral radius via sparse eigsh(k=1)
    lam = float(top[0][-1]) if top is not None else float(op._eigAdj().eigenvalues[-1])
    return Result(p["gamma"] < p["beta"] * lam, "Th_coqc", "finite_diagnostic", "InfoBio.sis_outbreak (R2)")

def _network(op, p):
    top = op._adj_top(2)                            # large-N: principal vector via sparse eigsh(k=2)
    w, V = top if top is not None else op._eigAdj()
    gap = w[-1] - w[-2] if len(w) >= 2 else w[-1]
    if not (w[-1] > 1e-9 and gap > 1e-9):          # honest abstention on degenerate/disconnected top
        return Result(None, "Th_coqc", "finite_diagnostic",
                      "InfoDomains.network (R2) [ABSTAIN: degenerate/disconnected top eigenvalue]")
    pv = np.abs(V[:, -1]); pv = pv / pv.sum()
    return Result(pv, "Th_coqc", "finite_diagnostic", "InfoDomains.network (R2)")

def _finance(op, p):
    terms = p["terms"]
    if len(terms) > MAX_EDGES:
        raise ValueError("too many portfolio terms")
    if op._exact:
        val = sum(Fraction(str(float(w))) ** 2 * Fraction(str(float(s))) ** 2 for w, s in terms)
        return Result(val, "Th_coqc", "exact_Q", "InfoFinance.risk_nonneg (R1)")
    return Result(float(sum((w ** 2) * (s ** 2) for w, s in terms)),
                  "Th_coqc", "finite_diagnostic", "InfoFinance.risk_nonneg (R1)")

def _econ_micro(op, p):
    a, b, g = p["a"], p["b"], p["g"]
    if a + g == 0:
        raise ValueError("a+g must be nonzero (no equilibrium)")
    if op._exact:
        return Result(Fraction(str(float(b))) / (Fraction(str(float(a))) + Fraction(str(float(g)))),
                      "Th_coqc", "exact_Q", "InfoEcon.market_clears (R3)")
    return Result(b / (a + g), "Th_coqc", "finite_diagnostic", "InfoEcon.market_clears (R3)")

def _econ_macro(op, p):
    A, c = p["A"], p["c"]
    if c == 1:
        raise ValueError("c must be ≠ 1 (multiplier diverges)")
    if op._exact:
        return Result(Fraction(str(float(A))) / (1 - Fraction(str(float(c)))),
                      "Th_coqc", "exact_Q", "InfoEcon.income_fixed_point (R3)")
    return Result(A / (1 - c), "Th_coqc", "finite_diagnostic", "InfoEcon.income_fixed_point (R3)")

def _thermo(op, p):
    D, v = p["D"], np.asarray(p["v"], float)
    if not (math.isfinite(D) and D >= 0):
        raise ValueError("D must be finite and ≥ 0")
    return Result(float(D * (v @ v)), "Th_coqc", "finite_diagnostic",
                  "InfoDomains.thermo_dissipation_nonneg (R1)")

def _electrical(op, p):
    return Result(float(p["R"] * p["C"]), "+reals", "finite_diagnostic",
                  "InfoDomains.electrical_tau_RC (R4)")

def _Q(x):  # exact rational from a value (str route avoids binary-float noise)
    return Fraction(str(float(x)))

def _chem(op, p):                              # Turing dispersion s = a − D·μ
    a, D, mu = p["a"], p["D"], p["mu"]
    if op._exact:
        return Result(_Q(a) - _Q(D) * _Q(mu), "Th_coqc", "exact_Q", "InfoDomains.chem_dominant_growth (R2)")
    return Result(float(a - D * mu), "Th_coqc", "finite_diagnostic", "InfoDomains.chem_dominant_growth (R2)")

def _cognitive(op, p):                         # symmetric DDM hitting probability = x0 / a
    x0, a = p["x0"], p["a"]
    if a == 0:
        raise ValueError("a (barrier) must be nonzero")
    if op._exact:
        return Result(_Q(x0) / _Q(a), "Th_coqc", "exact_Q", "InfoDomains.cognitive_hitting (R0/R4)")
    return Result(x0 / a, "Th_coqc", "finite_diagnostic", "InfoDomains.cognitive_hitting (R0/R4)")

def _navier_stokes(op, p):                     # Reynolds number Re = ρ·v·L/μ
    rho, v, Lc, mu = p["rho"], p["v"], p["Lc"], p["mu"]
    if mu == 0:
        raise ValueError("mu (viscosity) must be nonzero")
    if op._exact:
        return Result(_Q(rho) * _Q(v) * _Q(Lc) / _Q(mu), "Th_coqc", "exact_Q", "InfoDomains.reynolds (R0/R4)")
    return Result(rho * v * Lc / mu, "Th_coqc", "finite_diagnostic", "InfoDomains.reynolds (R0/R4)")

def _magnetism(op, p):                         # magnetic energy density B²/(2μ) ≥ 0 (PSD)
    B, mu = p["B"], p["mu"]
    if not (math.isfinite(mu) and mu > 0):
        raise ValueError("mu (permeability) must be finite and > 0")
    if op._exact:
        return Result(_Q(B) * _Q(B) / (2 * _Q(mu)), "Th_coqc", "exact_Q", "InfoDomains.mhd_energy_nonneg (R1)")
    return Result((B * B) / (2 * mu), "Th_coqc", "finite_diagnostic", "InfoDomains.mhd_energy_nonneg (R1)")

def _nuclear(op, p):                           # binding energy per nucleon B/A
    B, A = p["B"], p["A"]
    if A == 0:
        raise ValueError("A (nucleon number) must be nonzero")
    if op._exact:
        return Result(_Q(B) / _Q(A), "Th_coqc", "exact_Q", "InfoDomains.nuclear_binding_per_nucleon (R2)")
    return Result(B / A, "Th_coqc", "finite_diagnostic", "InfoDomains.nuclear_binding_per_nucleon (R2)")

def _cosmology(op, p):                         # critical-density scaling ρ_c ∝ H² → ratio (H2/H1)²
    H1, H2 = p["H1"], p["H2"]
    if H1 == 0:
        raise ValueError("H1 must be nonzero")
    if op._exact:
        return Result(_Q(H2) * _Q(H2) / (_Q(H1) * _Q(H1)), "Th_coqc", "exact_Q", "InfoDomains.cosmo_density_scaling (R5/R6)")
    return Result((H2 * H2) / (H1 * H1), "Th_coqc", "finite_diagnostic", "InfoDomains.cosmo_density_scaling (R5/R6)")

# ── operator-native cards (data / AI / social): DIRECT readouts of L_R, citing the core proved theorem.
#    These are not new formulas — the domain quantity IS the Dirichlet energy / spectrum / diffusion of L_R. ──
def _energy_card(op, p, law):
    r = op.info(p["x"])                                 # ⟨x, L_R x⟩ ; tier flows from info (exact_Q in exact mode)
    return Result(r.value, r.structure_tier, r.value_tier, law)

def _data(op, p):       return _energy_card(op, p, "InfoOperator.info_is_operator_energy (R0) [graph-signal smoothness / total variation]")
def _ai(op, p):         return _energy_card(op, p, "InfoOperator.info_nonneg (R1) [Laplacian regularization / GNN smoothness penalty]")
def _social(op, p):     return _energy_card(op, p, "InfoOperator.info_is_operator_energy (R0) [opinion disagreement energy]")

def _connectivity(op, p):
    w = op.spectrum().value.eigenvalues                 # Fiedler value λ₂ = algebraic connectivity
    return Result(float(w[1]) if len(w) > 1 else 0.0, "Th_coqc", "finite_diagnostic",
                  "InfoSpectral2 (R2) [Fiedler λ₂ / algebraic connectivity / spectral clustering]")

def _consensus(op, p):                                  # opinion dynamics ẋ=−Lx → everyone → the mean (kernel=constants)
    r = op.evolve(p["x"], float(p.get("t", 20.0)), unitary=False)
    return Result(r.value, r.structure_tier, r.value_tier,
                  "InfoDtN.nodeLap_const (R6) [opinion dynamics / distributed averaging → consensus]")

def _diffusion(op, p):                                  # heat-kernel diffusion exp(−Lt) (label spread, embeddings, random walk)
    r = op.evolve(p["x"], float(p.get("t", 1.0)), unitary=False)
    return Result(r.value, r.structure_tier, r.value_tier,
                  "RDL_SpineGraphEnergy.total_energy_nonincreasing (R4) [heat-kernel diffusion / random walk]")

# ── unified force (InfoForce): the root-force law + the one-operator force converter ──
def _force(op, p):                              # F_root = −K·Lx − ∇V  (geometry + potential term)
    K, Lx, gradV = p["K"], p["Lx"], p.get("gradV", 0)
    if op._exact:
        return Result(-_Q(K)*_Q(Lx) - _Q(gradV), "Th_coqc", "exact_Q", "InfoForce.geometry_force_conservative")
    return Result(float(-K*Lx - gradV), "Th_coqc", "finite_diagnostic", "InfoForce.geometry_force_conservative")

def _force_transform(op, p):                    # ONE operator: convert a force from unit ki to unit kj
    ki, kj, Fi = p["ki"], p["kj"], p["Fi"]
    if ki == 0:
        raise ValueError("ki (source coupling) must be nonzero")
    if op._exact:
        return Result(_Q(kj)/_Q(ki)*_Q(Fi), "Th_coqc", "exact_Q", "InfoForce.transform_force_eq")
    return Result(float(kj/ki*Fi), "Th_coqc", "finite_diagnostic", "InfoForce.transform_force_eq")

DOMAINS: dict[str, _Card] = {c.name: c for c in [
    _Card("bio", ("sis", "epidemic"), ("beta", "gamma"), "Th_coqc", "finite_diagnostic", "InfoBio.sis_outbreak (R2)", _bio),
    _Card("network", ("pagerank", "centrality"), (), "Th_coqc", "finite_diagnostic", "InfoDomains.network (R2)", _network),
    _Card("finance", (), ("terms",), "Th_coqc", "finite_diagnostic", "InfoFinance.risk_nonneg (R1)", _finance),
    _Card("economics_micro", ("market",), ("a", "b", "g"), "Th_coqc", "finite_diagnostic", "InfoEcon.market_clears (R3)", _econ_micro),
    _Card("economics_macro", ("multiplier",), ("A", "c"), "Th_coqc", "finite_diagnostic", "InfoEcon.income_fixed_point (R3)", _econ_macro),
    _Card("thermo", ("thermodynamics", "dissipation"), ("D", "v"), "Th_coqc", "finite_diagnostic", "InfoDomains.thermo_dissipation_nonneg (R1)", _thermo),
    _Card("electrical", ("rc",), ("R", "C"), "+reals", "finite_diagnostic", "InfoDomains.electrical_tau_RC (R4)", _electrical),
    _Card("chem", ("turing", "chemistry"), ("a", "D", "mu"), "Th_coqc", "finite_diagnostic", "InfoDomains.chem_dominant_growth (R2)", _chem),
    _Card("cognitive", ("ddm", "decision"), ("x0", "a"), "Th_coqc", "finite_diagnostic", "InfoDomains.cognitive_hitting (R0/R4)", _cognitive),
    _Card("navier_stokes", ("fluid", "reynolds"), ("rho", "v", "Lc", "mu"), "Th_coqc", "finite_diagnostic", "InfoDomains.reynolds (R0/R4)", _navier_stokes),
    _Card("magnetism", ("mhd", "magnetic"), ("B", "mu"), "Th_coqc", "finite_diagnostic", "InfoDomains.mhd_energy_nonneg (R1)", _magnetism),
    _Card("nuclear", ("binding",), ("B", "A"), "Th_coqc", "finite_diagnostic", "InfoDomains.nuclear_binding_per_nucleon (R2)", _nuclear),
    _Card("cosmology", ("cosmo", "density"), ("H1", "H2"), "Th_coqc", "finite_diagnostic", "InfoDomains.cosmo_density_scaling (R5/R6)", _cosmology),
    # operator-native data/AI/social cards (direct readouts of L_R)
    _Card("data", ("smoothness", "signal"), ("x",), "Th_coqc", "finite_diagnostic", "InfoOperator.info_is_operator_energy (R0) [graph-signal smoothness]", _data),
    _Card("ai", ("ml", "gnn"), ("x",), "Th_coqc", "finite_diagnostic", "InfoOperator.info_nonneg (R1) [Laplacian regularization]", _ai),
    _Card("social", ("opinion", "polarization"), ("x",), "Th_coqc", "finite_diagnostic", "InfoOperator.info_is_operator_energy (R0) [disagreement energy]", _social),
    _Card("connectivity", ("fiedler", "clustering"), (), "Th_coqc", "finite_diagnostic", "InfoSpectral2 (R2) [algebraic connectivity λ₂]", _connectivity),
    _Card("consensus", ("averaging",), ("x",), "+reals", "finite_diagnostic", "InfoDtN.nodeLap_const (R6) [opinion dynamics → mean]", _consensus),
    _Card("diffusion", ("heat", "randomwalk"), ("x",), "+reals", "finite_diagnostic", "RDL_SpineGraphEnergy.total_energy_nonincreasing (R4) [heat kernel]", _diffusion),
    # unified force: the root-force law + the one-operator force converter (new native unit)
    _Card("force", ("rootforce",), ("K", "Lx"), "Th_coqc", "finite_diagnostic", "InfoForce.geometry_force_conservative [F=−K·Lx−∇V]", _force),
    _Card("force_transform", ("forceconvert", "unify_force"), ("ki", "kj", "Fi"), "Th_coqc", "finite_diagnostic", "InfoForce.transform_force_eq [one operator converts forces ki→kj]", _force_transform),
]}
_ALIAS = {a: c.name for c in DOMAINS.values() for a in (c.name, *c.aliases)}

def _resolve_card(domain: str) -> _Card:
    key = _ALIAS.get(domain.lower())
    if key is None:
        raise ValueError(f"unknown domain {domain!r}; known: {sorted(DOMAINS)}")
    return DOMAINS[key]

def list_domains() -> list[str]:
    return sorted(DOMAINS)

def domain_signature(domain: str) -> dict:
    c = _resolve_card(domain)
    return {"domain": c.name, "aliases": list(c.aliases), "required_params": list(c.required),
            "structure_tier": c.structure_tier, "value_tier": c.value_tier, "law": c.law}


def self_check() -> bool:
    """The API reproduces the Coq vm_compute values (same as the L2 bridge) — exact mode = exact ℚ."""
    op = Operator([(0, 1, 1), (1, 2, 1), (2, 0, 1)])                      # triangle K3
    ok = op.readout("bio", beta=2.0, gamma=3.0).value is True            # λmax=2 → 3<4 → outbreak
    ok &= float(op.readout("finance", terms=[(0.5, 2), (0.5, 4)]).value) == 5.0
    ok &= float(op.readout("economics_macro", A=10, c=0.6).value) == 25.0
    ok &= float(op.readout("thermo", D=2, v=[1, 2]).value) == 10.0
    ok &= op.is_psd().value and op.kernel_has_constants().value
    # exact-ℚ backend: value_tier must be exact_Q and exactly right
    ope = Operator([(0, 1, 1), (1, 2, 1), (2, 0, 1)], exact=True)
    r = ope.readout("finance", terms=[(0.5, 2), (0.5, 4)])
    ok &= r.value == Fraction(5) and r.value_tier == "exact_Q"
    # honesty: a float verdict must NOT claim exact_Q
    ok &= op.is_psd().value_tier == "finite_diagnostic"
    return bool(ok)


if __name__ == "__main__":
    print(f"operator_api v{__api_version__} — information operator 𝓘, six readouts (two-axis tier)")
    op = Operator([(0, 1, 1.0), (1, 2, 1.0), (2, 0, 1.0)])
    print("  info([1,2,3])     :", op.info([1, 2, 3]))
    print("  is_psd            :", op.is_psd())
    print("  bio outbreak      :", op.readout("bio", beta=2.0, gamma=3.0))
    print("  finance variance  :", op.readout("finance", terms=[(0.5, 2), (0.5, 4)]))
    print("  finance (exact)   :", Operator([(0,1,1),(1,2,1),(2,0,1)], exact=True).readout("finance", terms=[(0.5,2),(0.5,4)]))
    print("  domains           :", list_domains())
    print("  SELF-CHECK        :", "PASS" if self_check() else "FAIL")
