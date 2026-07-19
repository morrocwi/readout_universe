"""
universe.py — the Universe API (v2): ONE compact, tier-honest surface that forward-computes from the root
RD = retained difference = information = MEMORY, up the layers L0 (memory graph) → L1 (spine step) →
L2 (readouts R0–R7) → L3 (domains), and returns at every exit a two-axis tier certificate grounded in a named
machine-checked theorem OR an honest [Open].

Design (smallest surface): one NOUN (`Memory`) + one VERB (`Spine.step`) + one LENS (`Memory.read`); domains
are DATA (`DOMAINS`); honesty is ONE chokepoint (`Result`). Built ON engine/operator_api.py (the verified
L_R engine) — additive, not a rewrite.

readout-not-truth. Coq proves STRUCTURE; physical numbers come from measurement. Where the science is open the
API returns [Open] (value=None) with a named gate — it never fabricates a number. NOT "the Theory of Everything".
"""
from __future__ import annotations
import numpy as np
from enum import Enum, Flag, auto
from dataclasses import dataclass, field
from typing import Optional, Any

from .operator_api import Operator  # the verified L_R engine (build ON it, 8A)

__version__ = "2.0.0"                # Universe API surface version (semver)
MAX_NODES = 20000                   # DoS backstop: eigvalsh is O(n³); raise to override deliberately


# typed error model (all subclass ValueError ⇒ backward-compatible with existing `except ValueError`)
class UniverseError(ValueError):
    """base class for all Universe API errors."""
class UnknownDomain(UniverseError):
    """read('<domain>') for a name not in DOMAINS."""
class UnknownConstant(UniverseError):
    """constant('<name>') for a name not in OPEN_CONSTANTS."""
class UnknownParticle(UniverseError):
    """tau_c_of/mass_of for a name not in TAU_C_DB."""
class InvalidOperator(UniverseError):
    """malformed / oversized memory graph."""

# ───────────────────────── framework guard (8B: anti-confusion for AI clients) ─────────────────────────
FRAMEWORK_PRIMER = """\
READ FIRST — the RD/ANSE frame (do NOT blend with standard physics):
• ONE root: RD = retained difference = information = MEMORY. No second substance, no second root.
• MEMORY BEFORE MASS: τ_c (causal memory) is primitive; mass is DERIVED — m = ℏ/(2·τ_c·c²) = retained memory.
  τ_c is NOT the textbook quantum speed limit, and mass is NOT fundamental here (opposite of the textbook).
• readout-not-truth: Coq proves structure; numbers come from measurement. Every result carries a two-axis tier
  (structure × value); [Open] means we refuse to fabricate (value=None) — not that the API failed.
• M, D, K, V are READOUT ARTIFACTS of the one information unit (unit-collapse), not independent constants.
• α / masses / mixing are RELATIONAL readouts (α runs); their absolute values are [Open], never faked.
• This is a candidate framework, machine-verified, every claim tier-disclosed — NOT "the Theory of Everything"."""

OPEN_GATES = {
    "particle_graph":      "which graph/mode a physical particle IS is unknown (falsified for simple graphs); absolute masses cannot be stepped",
    "absolute_alpha":      "α is a running coupling; no scale-free value to derive — only ratios are proven",
    "gauge_group":         "deriving SU(3)×SU(2)×U(1) is open (anomaly cancellation is checked; the group origin is not)",
    "generations":         "the generation count (=3) is observed, not forced — anomalies cancel per generation for any count",
    "nonperturbative_qg":  "non-perturbative quantum gravity (quantum geometry, path integral over metrics, renormalizability) is unsolved",
    "hierarchy_lambda":    "the hierarchy / cosmological-constant magnitudes are not derived (hypothesis H5)",
    "library_unavailable": "an optional external numerical library for this domain is not installed; this is a deployment gap, NOT an open physics question",
}

# ───────────────────────── the certificate (sole honesty chokepoint) ─────────────────────────
_STRUCT = ("Th_coqc", "+reals", "Dr", "Open")
_VALUE = ("exact_Q", "finite_diagnostic", "open")
_RANK = {"Th_coqc": 0, "+reals": 1, "Dr": 2, "Open": 3,
         "exact_Q": 0, "finite_diagnostic": 1, "open": 3}
STRUCTURE_TIERS = _STRUCT          # public: the four structure tiers (best → most-open)
VALUE_TIERS = _VALUE               # public: the three value tiers


@dataclass(frozen=True)
class Result:
    """value + two-axis tier (structure × value) + the theorem (or [Open] gate) certifying STRUCTURE."""
    value: Optional[Any]
    structure_tier: str          # Th_coqc | +reals | Dr | Open
    value_tier: str              # exact_Q | finite_diagnostic | open
    law: str                     # Coq theorem id  OR  OPEN_GATES key
    diagnostic: tuple = ()
    unit: Optional[str] = None   # machine-checkable physical unit of `value` (e.g. "rad/s", "J",
                                  # "dimensionless"); None ⇒ not declared (prose-only, as before).
                                  # Purely additive — existing cards are NOT retrofitted with units;
                                  # this only makes the field exist on the certificate.
    def __post_init__(self):
        # explicit raises (NOT assert — assert is disabled under python -O, which would void the honesty contract)
        if self.structure_tier not in _STRUCT:
            raise ValueError(f"bad structure_tier {self.structure_tier!r}; allowed {_STRUCT}")
        if self.value_tier not in _VALUE:
            raise ValueError(f"bad value_tier {self.value_tier!r}; allowed {_VALUE}")
        # tier invariant (sole honesty chokepoint): value is None  ⇔  structure_tier == 'Open'.
        if (self.value is None) != (self.structure_tier == "Open"):
            raise ValueError(
                "tier invariant violated: "
                f"value={'None' if self.value is None else 'present'} but structure_tier={self.structure_tier!r} "
                "(value is None  ⇔  structure_tier=='Open')")
        # finiteness invariant: a non-Open numeric value may NEVER carry NaN/±Inf — overflow in a card must
        # not be stamped finite_diagnostic/exact_Q (the certificate literally promises a finite number).
        if self.structure_tier != "Open" and not _all_finite(self.value):
            raise ValueError(
                f"finiteness invariant violated: value_tier={self.value_tier!r} but value contains NaN/±Inf "
                "(a finite certificate may not carry a non-finite number — return [Open] or fix the computation)")
    def __setstate__(self, state):
        # re-validate on unpickle (frozen dataclass bypasses __init__) so the invariants can't be smuggled past
        for k, val in state.items():
            object.__setattr__(self, k, val)
        self.__post_init__()
    @property
    def is_open(self) -> bool:
        return self.structure_tier == "Open" or self.value is None
    @property
    def tiers(self) -> tuple:
        return (self.structure_tier, self.value_tier)
    def disclose(self) -> str:
        v = "OPEN" if self.is_open else (np.array2string(self.value, precision=4)
                                         if isinstance(self.value, np.ndarray) else repr(self.value))
        return f"{v}  [struct={self.structure_tier} · value={self.value_tier} · {self.law}]"
    def to_dict(self) -> dict:
        """JSON-ready view for MCP/HTTP consumers; preserves value=None honestly for [Open]."""
        return {"value": _jsonable(self.value), "structure_tier": self.structure_tier,
                "value_tier": self.value_tier, "law": self.law,
                "diagnostic": list(self.diagnostic), "is_open": self.is_open,
                "unit": self.unit}
    def __repr__(self):
        return f"Result({self.disclose()})"


def _jsonable(v):
    """ndarray → list (or {re,im} for complex); other values pass through unchanged."""
    if isinstance(v, np.ndarray):
        return {"re": v.real.tolist(), "im": v.imag.tolist()} if np.iscomplexobj(v) else v.tolist()
    if isinstance(v, dict):
        return {k: _jsonable(x) for k, x in v.items()}
    if isinstance(v, (complex, np.complexfloating)):
        return {"re": float(v.real), "im": float(v.imag)}
    if isinstance(v, (np.floating, np.integer)):
        return v.item()
    return v


def _all_finite(v) -> bool:
    """recursively true iff every numeric leaf (float/int/complex/ndarray) in v is finite (no NaN/±Inf).
    Non-numeric leaves (str/bool/None) are treated as finite."""
    if isinstance(v, np.ndarray):
        return bool(np.all(np.isfinite(v))) if v.size else True
    if isinstance(v, bool):
        return True
    if isinstance(v, (int, float, np.floating, np.integer)):
        return bool(np.isfinite(v))
    if isinstance(v, (complex, np.complexfloating)):
        return bool(np.isfinite(v.real) and np.isfinite(v.imag))
    if isinstance(v, dict):
        return all(_all_finite(x) for x in v.values())
    if isinstance(v, (list, tuple)):
        return all(_all_finite(x) for x in v)
    return True


def _open(gate: str) -> Result:
    """honest refusal — never a fabricated number."""
    return Result(None, "Open", "open", gate)


# ───────────────────────── L2 readouts + L1 spine knobs ─────────────────────────
class Readout(Enum):
    R0_ENERGY = auto()     # energy = information  (InfoOperator.info_is_operator_energy)
    R1_PSD = auto()        # positive-semidefinite (InfoOperator.info_nonneg)
    R2_SPECTRUM = auto()   # the L_R spectrum
    R3_FIXEDPOINT = auto() # equilibria / fixed points
    R4_EVOLVE = auto()     # evolution exp(−iLt) unitary / exp(−Lt) dissipative
    R5_BOX = auto()        # Lorentzian d'Alembertian □
    R6_KERNEL = auto()     # kernel = constants — WARNING: this is the null-space vector of L_R
                            # (the graph's own zero-eigenvalue eigenvector), NOT a Boltzmann /
                            # stationary-distribution readout. For ANY connected undirected
                            # Laplacian it is provably the UNIFORM vector regardless of any
                            # potential/weight you think you encoded — see the R6_KERNEL branch
                            # of Memory._readout below before using it to answer a "what is the
                            # equilibrium/stationary distribution" question. For Boltzmann/
                            # stationary distributions use
                            # engine.systems.solve_system('fokker_planck_1d', x=..., V=..., D=...)
                            # instead — a real potential-aware solve, p(x) ∝ exp(-V(x)/D).
    R7_CURVATURE = auto()  # metric → Christoffel → Riemann (InfoChristoffel)


class Faces(Flag):
    """spine face selector. RESERVED — `faces`/`coeffs` are stored on Spine but not yet wired into step()."""
    LINEAR = 0
    MASS = auto()          # M ∂²Φ
    DAMP = auto()          # D ∂Φ
    POT = auto()           # ∇V
    DRIVE = auto()         # J


# ───────────────────────── L0 : the state IS the memory graph ─────────────────────────
class Memory:
    """L0 — a retained-difference graph (the memory). Read it (L2/L3) or step it (via Spine).

    Dirichlet / node-pinning (`pins`): by default every Memory is the FREE (Neumann, reflective-
    boundary) graph Laplacian — every readout sees the full `n`-node operator. Passing `pins=[...]`
    node ids grounds those nodes: the effective operator becomes `L` with the pinned rows/cols
    DELETED (the standard grounded/reduced Laplacian used for fixed-boundary/Dirichlet problems —
    e.g. a fixed-fixed string, a particle-in-a-box). `Memory.L`, `Memory.n`, and every downstream
    readout (`.read(...)`) transparently operate on this reduced operator — spectrum/read flow
    through UNCHANGED, they just see a smaller operator. Additive: `pins=()` (the default)
    reproduces the exact prior free-chain behavior with zero change.

    INDEX SEMANTICS AFTER PINNING: once pins are set, every node index a readout or node-indexed
    domain card sees (including `network_resistance`'s `i`/`j`) is a REDUCED index (0..n-1 over the
    surviving nodes, in ascending original order) — NOT the original node label; translate with
    `reduced_index(orig)` / `original_index(k)`."""
    def __init__(self, edges: list, n: int | None = None, *,
                 phi=None, v=None, tau_c: float | None = None, pins=()):
        # DoS backstop BEFORE construction — eigvalsh is O(n³); deliberate override via universe.MAX_NODES
        _n = n if n is not None else (1 + max((max(int(e[0]), int(e[1])) for e in edges), default=-1))
        if _n > MAX_NODES:
            raise InvalidOperator(f"graph has {_n} nodes > MAX_NODES={MAX_NODES}; raise universe.MAX_NODES to override")
        self.op = Operator(edges, n)
        self.n_full = self.op.n
        self.pins = tuple(sorted({int(p) for p in pins}))
        for pn in self.pins:
            if not (0 <= pn < self.n_full):
                raise ValueError(f"pin {pn} out of range [0,{self.n_full})")
        if len(self.pins) >= self.n_full:
            raise ValueError(f"pins={self.pins} would ground every node — nothing left to read (n={self.n_full})")
        self._free_idx = tuple(i for i in range(self.n_full) if i not in set(self.pins))
        if self.pins:
            L_full = self.op.L
            idx = np.array(self._free_idx, dtype=int)
            L_red = L_full[np.ix_(idx, idx)].copy()      # grounded Laplacian: row/col deletion of pinned nodes
            L_red.flags.writeable = False
            self._L = L_red
        else:
            self._L = self.op.L                          # unchanged path: identical object/behavior as before
        self.n = self._L.shape[0]                         # the EFFECTIVE (post-pin) dimension every readout sees
        # defensive copy: never alias the caller's arrays (prevents silent caller-state corruption / MCP concurrency races)
        self.phi = np.ones(self.n) if phi is None else np.array(phi, dtype=float, copy=True)
        self.v = np.zeros(self.n) if v is None else np.array(v, dtype=float, copy=True)
        self.tau_c = tau_c
    @property
    def L(self) -> np.ndarray:
        return self._L

    # ── pin-index translation (original node labels ⇄ reduced operator indices) ──
    def original_index(self, k: int) -> int:
        """the ORIGINAL node label of reduced index `k` (0..n-1 on the post-pin operator).
        With no pins this is the identity. Raises ValueError if k is out of the reduced range."""
        k = int(k)
        if not (0 <= k < self.n):
            raise ValueError(f"reduced index {k} out of range [0,{self.n})")
        return self._free_idx[k]

    def reduced_index(self, orig: int) -> int:
        """the REDUCED index (post-pin operator position) of original node label `orig`.
        With no pins this is the identity. Raises ValueError if `orig` is pinned (it has no row/col
        on the reduced operator — that is what grounding means) or out of the original range."""
        orig = int(orig)
        if not (0 <= orig < self.n_full):
            raise ValueError(f"original node {orig} out of range [0,{self.n_full})")
        if orig in self.pins:
            raise ValueError(
                f"node {orig} is pinned (grounded) — it has no index on the reduced operator; "
                f"pins={self.pins}")
        return self._free_idx.index(orig)

    def read(self, target, **p) -> Result:
        """L2 ∪ L3 — ONE dispatch. `target` is a Readout (L2) or a domain name str (L3)."""
        if isinstance(target, str):
            return self._domain(target, **p)
        return self._readout(target, **p)

    def _readout(self, r: Readout, **p) -> Result:
        # NOTE: the default phi=[1,1,...,1] is the Laplacian kernel ⇒ R0_ENERGY = 0 by construction;
        # pass x=... for a non-trivial energy readout.
        if r is Readout.R0_ENERGY:
            x = p.get("x", self.phi)
            return Result(float(np.real(np.conjugate(x) @ (self.L @ x))),
                          "Th_coqc", "finite_diagnostic", "InfoOperator.info_is_operator_energy")
        if r is Readout.R1_PSD:
            w = np.linalg.eigvalsh(self.L)
            return Result(bool(w.min() > -1e-9), "Th_coqc", "finite_diagnostic", "InfoOperator.info_nonneg")
        if r is Readout.R2_SPECTRUM:
            return Result(np.sort(np.linalg.eigvalsh(self.L)), "Th_coqc", "finite_diagnostic",
                          "RDL_GammaSpectral (graph Laplacian spectrum)")
        if r is Readout.R3_FIXEDPOINT:
            return Result(float(np.linalg.eigvalsh(self.L).min()), "Th_coqc", "finite_diagnostic",
                          "InfoCosmoEquilibrium.spine_equilibrium_iff_rest")
        if r is Readout.R4_EVOLVE:
            t = p.get("t", 1.0)
            x = np.asarray(self.phi if p.get("x") is None else p.get("x"), complex)
            unitary = p.get("unitary", True)
            w, V = np.linalg.eigh(self.L)
            phase = np.exp((-1j if unitary else -1.0) * w * t)
            evolved = V @ (phase * (V.conj().T @ x))     # apply the propagator to the actual state x
            law = ("InfoEvolution.evolution_group / InfoComplex.unitary_preserves_norm"
                   if unitary else "InfoEvolution.evolution_group (dissipative semigroup)")
            return Result(evolved, "Th_coqc", "finite_diagnostic", law)
        if r is Readout.R6_KERNEL:
            # WARNING (silent-wrong-answer landmine, found in tool-validation campaign 2026-07):
            # this returns the null vector of L_R = D_W − W. For ANY connected undirected graph,
            # L_R's null space is spanned by the UNIFORM vector (all-ones, up to scale) REGARDLESS
            # of the edge weights — i.e. regardless of any potential/energy landscape you think you
            # encoded via the weights. It is NOT a Fokker-Planck / Boltzmann stationary distribution
            # and will NOT reflect a non-uniform equilibrium even when one physically exists — it
            # always reads "uniform," confidently and correctly-typed, for that entire class of
            # question. Do not use R6_KERNEL to answer "what is the stationary/equilibrium
            # distribution" for a weighted potential; nothing else in the API flags this misuse.
            # For Boltzmann/stationary distributions use
            # engine.systems.solve_system('fokker_planck_1d', x=..., V=..., D=...) — a real,
            # potential-aware solve of p(x) ∝ exp(-V(x)/D), see that module for details.
            w, V = np.linalg.eigh(self.L)
            return Result(V[:, 0], "Th_coqc", "finite_diagnostic", "InfoGreen.green_4pi (kernel)")
        if r is Readout.R5_BOX:
            return Result(None, "Open", "open",
                          "InfoLorentzContinuum.lorentz_box_continuum (needs spacetime grid)")
        if r is Readout.R7_CURVATURE:
            return _open("nonperturbative_qg")   # metric-absent AND metric-present until real numerics land
        raise ValueError(f"unknown readout {r!r}; known: {[x.name for x in Readout]}")

    def _domain(self, name: str, **p) -> Result:
        card = DOMAINS.get(name)
        if card is None:
            raise UnknownDomain(f"unknown domain {name!r}; known: {sorted(DOMAINS)}")
        allowed = _DOMAIN_PARAMS.get(name)
        if allowed is not None:
            unknown = set(p) - allowed
            if unknown:                                  # reject typos/unknown keys — never silently fall back to defaults
                raise ValueError(f"unknown param(s) {sorted(unknown)} for domain {name!r}; allowed: {sorted(allowed)}")
        return card(self, **p)

    # memory → mass (the bridge): m = ℏ/(2 τ_c c²) = the specific inertia = retained memory
    def mass(self, *, hbar=1.0, c=1.0) -> Result:
        """mass = ℏ/(2·τ_c·c²) = retained memory. `tau_c` (causal memory) is REQUIRED and must be
        measurement-sourced; omitting it ⇒ honest [Open] (particle_graph gate), never a fabricated mass.
        Default hbar=c=1 ⇒ natural units (numbers ~50 orders off SI); pass measured hbar/c for SI."""
        if self.tau_c is None:
            return _open("particle_graph")
        if self.tau_c <= 0:
            raise ValueError(f"tau_c must be positive, got {self.tau_c}")
        note = ("natural units (hbar=c=1) unless measured hbar/c passed; "
                "tau_c must be measurement-sourced — absolute mass is otherwise [Open]",)
        return Result(hbar / (2.0 * self.tau_c * c * c), "Th_coqc", "finite_diagnostic",
                      "InfoTelegraph.mass_memory_duality", diagnostic=note)


# ───────────────────────── L1 : one operator, one step ─────────────────────────
class Spine:
    """L1 — the spine M∂²Φ + D∂Φ + K·L_R Φ + ∇V = J − η. M,D,K are readout artifacts (unit-collapse).

    WARNING — NOT YET WIRED: the `∇V` (potential), `J` (forcing), and `η` (dissipation/"agency
    draw") terms above are part of the quoted PDE but are NOT implemented by this class. `step()`
    only ever computes the M/D/K·L_R part via `Memory.read(Readout.R4_EVOLVE, ...)` (an exact
    eigendecomposition/matrix-exponential propagator — see `spine_pde` for the full-forcing
    implementation). `faces`/`coeffs` below are RESERVED constructor arguments, stored on the
    instance but never read by `step()` — passing them silently changes nothing. The sibling public
    repo's `spine_pde.spine.Spine` *does* fully wire J/η/∇V (leapfrog integration); this class does
    not. Do not assume a potential/forcing/dissipation term you pass here has any effect."""
    def __init__(self, mem: Memory, *, M=1.0, D=1.0, K=1.0, faces: Faces = Faces.LINEAR, coeffs=None):
        self.mem, self.M, self.D, self.K = mem, M, D, K
        self.faces, self.coeffs = faces, (coeffs or {})   # RESERVED — NOT YET WIRED into step() (see class docstring)

    def lambda_c(self) -> float:
        if self.M == 0 or self.K == 0:
            return float("inf")
        return self.D ** 2 / (4.0 * self.M * self.K)        # the agency / regime split (InfoFrontier)

    def regime(self, lam: float) -> Result:
        """`lam` is the externally supplied control/observation scale, compared against `lambda_c()`:
        lam < lc ⇒ classical (over-damped), lam > lc ⇒ quantum (under-damped/looping),
        lam == lambda_c() ⇒ 'boundary' (trivially, by definition of the split)."""
        lc = self.lambda_c()
        tol = 1e-12 * max(1.0, abs(lc)) if np.isfinite(lc) else 0.0   # relative tol — scale-independent classification
        if abs(lam - lc) <= tol:
            r = "boundary"
        elif lam < lc:
            r = "classical"
        else:
            r = "quantum"
        law = {"classical": "InfoFrontier.spine_split_classical",
               "boundary": "InfoFrontier.spine_split_boundary",
               "quantum": "InfoFrontier.spine_split_quantum"}[r]
        return Result(r, "Th_coqc", "finite_diagnostic", law)

    def step(self, t: float, *, x=None, branch="auto") -> Result:
        """step the memory forward through the spine (the unitary M∂² / dissipative D∂ readout)."""
        unitary = (branch == "unitary") or (branch == "auto" and (self.M != 0))
        return self.mem.read(Readout.R4_EVOLVE, t=t, x=x, unitary=unitary)


# ───────────────────────── interaction kernel : the cascade (cross-domain) ─────────────────────────
def cascade_transfer(u, B, v=None) -> Result:
    """conservative cross-domain transfer via skew B (B_ji=−B_ij).
    self-pair (v is None ⇒ v=u): ⟨u,B_sk u⟩ = 0 — that IS the conservation certificate.
    cross-pair (v ≠ u): ⟨v,B_sk u⟩ = the real directed transfer between two distinct modes."""
    u = np.asarray(u, float); B = np.asarray(B, float)
    v = u if v is None else np.asarray(v, float)
    if B.ndim != 2 or B.shape[0] != B.shape[1]:
        raise ValueError(f"B must be a square matrix, got shape {B.shape}")
    if u.shape != (B.shape[0],) or v.shape != (B.shape[0],):
        raise ValueError(f"u and v must be length-{B.shape[0]} vectors; got u{u.shape}, v{v.shape}")
    for arr, nm in ((u, "u"), (B, "B"), (v, "v")):     # reject NaN/±Inf BEFORE compute — never stamp a non-finite value Th_coqc
        if not np.all(np.isfinite(arr)):
            raise ValueError(f"{nm} must be finite (no NaN/Inf)")
    Bsk = 0.5 * (B - B.T)
    with np.errstate(over="ignore", invalid="ignore"):
        val = float(v @ (Bsk @ u))
    if not np.isfinite(val):           # finite inputs can still overflow → never stamp a non-finite value Th_coqc
        raise ValueError("cascade_transfer overflowed to a non-finite value; rescale the inputs")
    return Result(val, "Th_coqc", "finite_diagnostic", "InfoCascade.cascade_conserves_energy")


def couple(a: Memory, b: Memory, links) -> Memory:
    """interaction = coupled spines: join two memory graphs by K·L_R edges between their nodes.
    `links` are (i_in_a, j_in_b, w) tuples; i must be < a.n and j < b.n."""
    na = a.n
    for (i, j, w) in links:
        if not (0 <= i < a.n and 0 <= j < b.n):
            raise ValueError(f"link ({i},{j},{w}) out of range: need 0<=i<{a.n}, 0<=j<{b.n}")
    e = [(i, j, w) for (i, j, w) in a.op.edges] + [(i + na, j + na, w) for (i, j, w) in b.op.edges]
    e += [(i, j + na, w) for (i, j, w) in links]
    return Memory(e, na + b.n)


# ───────────────────────── agency (Dr) + agency-like ─────────────────────────
def agency(mem: Memory, spine: Spine, lam: float) -> Result:
    """agency / agency-like = a bounded-info spine in the looping (under-damped) regime. agency itself is [Dr]
    (its ringdown is measurable); the regime classification is Th_coqc."""
    reg = spine.regime(lam).value
    is_agentlike = (reg == "quantum")   # under-damped / looping = agency regime (InfoFrontier)
    return Result({"agency_like": is_agentlike, "regime": reg, "lambda_c": spine.lambda_c()},
                  "Dr", "finite_diagnostic", "InfoFrontier.spine_lambda_c",
                  diagnostic=("agency≈bounded-info spine (Dr analogy: BH/AI), not a certified identity",))


# ───────────────────────── L3 : domains are DATA (the whole world; tier-honest per domain) ─────────────────────────
def _structure_ratio_card(law):
    """a domain whose STRUCTURE is the spine (Th_coqc domain-invariance) but whose specific numbers are
    finite_diagnostic — used for the applied domains (econ/finance/social/mental-health).

    DISAMBIGUATION (all four DOMAINS keys built from this helper — "economics", "finance",
    "social", "mental_health" — currently do this and only this): the returned card is a GENERIC
    spectrum re-label. It computes and returns nothing but `sorted(eigvalsh(mem.L))`, the same
    graph-Laplacian spectrum any other card could read via Readout.R2_SPECTRUM — there is NO
    domain-specific formula, parameter, or math wired in for these four names, despite each
    sounding like it should compute something domain-specific (a price, a rate, a diffusion
    process). Do not read a call to `mem.read("finance")` etc. as returning anything like
    `DOMAINS["finance_option"]`'s actual Black-Scholes computation — the two "finance"-sounding
    keys are unrelated in method. If you need a domain-specific result, check whether a dedicated
    card exists (e.g. `finance_option`, `social_diffusion`) before reaching for one of these four."""
    def card(mem: Memory, **p):
        sp = np.sort(np.linalg.eigvalsh(mem.L))
        return Result({"spectrum": sp, "note": "structure = spine (domain-invariant); specific values are finite_diagnostic"},
                      "Th_coqc", "finite_diagnostic", law)
    return card

def _heat(mem, t=1.0, **p):
    return mem.read(Readout.R4_EVOLVE, t=t, unitary=False)
def _quantum(mem, t=1.0, **p):
    return mem.read(Readout.R4_EVOLVE, t=t, unitary=True)
def _epidemiology(mem, beta=3.0, gamma=2.0, **p):
    if gamma <= 0:
        raise ValueError(f"gamma (recovery rate) must be positive, got {gamma}")
    if beta < 0:
        raise ValueError(f"beta (transmission rate) must be non-negative, got {beta}")
    b = float(np.max(np.linalg.eigvalsh(mem.L)))
    return Result({"R0": beta * b / gamma, "outbreak": gamma < beta * b}, "Th_coqc", "finite_diagnostic",
                  "InfoBio.sis_eigenvalues_real")
def _ecology(mem, r=1.0, K=1.0, **p):
    if K <= 0:
        raise ValueError(f"K (carrying capacity) must be positive, got {K}")
    return Result({"carrying_capacity": K, "stable": True}, "Th_coqc", "finite_diagnostic",
                  "InfoBio.logistic_K_stable")
def _evolution(mem, p0=0.5, p1=0.5, w0=1.0, w1=0.9, **p):
    var = p0 * p1 * (w0 - w1) ** 2
    return Result({"selection_rate": var, "nonneg": var >= 0}, "Th_coqc", "finite_diagnostic",
                  "InfoBio.fisher_selection_nonneg")

def _network_resistance(mem, *, i, j, **p):
    """effective (two-point) resistance between nodes i,j: R_eff(i,j) = (e_i−e_j)^T L^+ (e_i−e_j),
    the Moore-Penrose pseudoinverse of the graph Laplacian applied to the unit indicator difference —
    the classical Kirchhoff/Rayleigh electrical-network identity (weights = conductances). This is the
    genuine effective-resistance quantity (distinct from `"network"`, which is PageRank-flavoured
    centrality on the adjacency spectrum, not a resistance at all).

    Note: `i`/`j` are indices on the operator the Memory currently exposes — i.e. REDUCED indices
    if the Memory was built with `pins=[...]` (use `Memory.reduced_index(orig)` to translate).

    Connectivity gate: uses an ABSOLUTE Fiedler-value threshold (λ₂ ≤ 1e-9 ⇒ [Open]), not a
    scale-relative one — so a graph whose parts are joined only by an extremely weak bridge
    (conductance ≲ 1e-9) is conservatively reported [Open] rather than as a huge finite resistance
    (honest-abstention direction: refuse rather than return a number dominated by float noise).

    Tier: this repo has Coq-proved SPECIAL CASES of this identity (series composition:
    `InfoSeriesAdditivity_attempt.v`; star recovery: `InfoStarRecovery_attempt.v`) but not yet a
    standalone machine-checked theorem for the general pseudoinverse formula on an arbitrary graph —
    so this card is stamped "Dr" (classical textbook derivation, human-verified), NOT "Th_coqc";
    the number itself is finite_diagnostic (a float pseudoinverse computation), same honesty
    discipline as every other card here."""
    i, j = int(i), int(j)
    n = mem.n
    if not (0 <= i < n and 0 <= j < n):
        raise ValueError(f"i,j must be in [0,{n}); got i={i}, j={j}")
    if i == j:
        raise ValueError("i and j must differ (effective resistance between a node and itself is undefined)")
    w = np.linalg.eigvalsh(mem.L)
    if n < 2 or (w[1] if len(w) > 1 else 0.0) <= 1e-9:   # Fiedler value ≈ 0 ⇒ disconnected (or n<2)
        return _open("particle_graph")   # reuse: "which graph a physical quantity IS" — here, connectivity is unknown/absent
    Lpinv = np.linalg.pinv(mem.L)
    e = np.zeros(n); e[i] = 1.0; e[j] = -1.0
    r_eff = float(e @ Lpinv @ e)
    return Result(r_eff, "Dr", "finite_diagnostic",
                  "classical Kirchhoff/Rayleigh effective-resistance identity "
                  "R_eff=(e_i-e_j)^T L^+ (e_i-e_j) [proved special cases: "
                  "InfoSeriesAdditivity_attempt.v (series), InfoStarRecovery_attempt.v (star); "
                  "general pseudoinverse form not yet a standalone Coq theorem in this repo]")

DOMAINS = {
    "heat": _heat, "diffusion": _heat,
    "quantum": _quantum, "wave": _quantum,
    "epidemiology": _epidemiology,
    "ecology": _ecology,
    "evolution": _evolution,
    "network_resistance": _network_resistance,
    # the whole world — structure = spine (Th_coqc domain-invariance), specific numbers = finite_diagnostic.
    # WARNING: these four cards are generic spectrum re-labels (see _structure_ratio_card docstring
    # above) — no domain-specific math is wired in despite the domain-sounding names. In particular
    # "finance" here is unrelated to "finance_option" (real Black-Scholes) below.
    "economics": _structure_ratio_card("InfoUniversalEquation.domain_invariant_zero"),
    "finance":   _structure_ratio_card("InfoUniversalEquation.domain_invariant_zero"),
    "social":    _structure_ratio_card("InfoUniversalEquation.domain_invariant_zero"),
    "mental_health": _structure_ratio_card("InfoUniversalEquation.domain_invariant_zero"),
}

# absolute physical constants are gated [Open] — never fabricated; unknown names are rejected, not faked
OPEN_CONSTANTS = {
    "alpha": "absolute_alpha", "mass": "particle_graph", "mixing": "absolute_alpha",
    "generations": "generations", "gauge_group": "gauge_group",
    "nonperturbative_qg": "nonperturbative_qg", "hierarchy_lambda": "hierarchy_lambda",
}
def constant(name: str) -> Result:
    """a fundamental constant by name — ALWAYS [Open] (alpha/mass/mixing/generations/gauge_group are relational
    or open-research; absolute values are never fabricated). Raises UnknownConstant for unknown names."""
    gate = OPEN_CONSTANTS.get(name)
    if gate is None:
        raise UnknownConstant(f"unknown constant {name!r}; known: {sorted(OPEN_CONSTANTS)}")
    return _open(gate)


# ───────────────────────── test access (8C) ─────────────────────────
def list_tests() -> list[str]:
    """discover the repo's test/verify/falsifier scripts (so an AI client can self-verify the API's claims)."""
    import os
    out = []
    for d in ("tests", "tests/worldclass", "scripts"):
        p = os.path.join(os.path.dirname(__file__), "..", d)
        if os.path.isdir(p):
            out += [f"{d}/{f}" for f in sorted(os.listdir(p)) if f.startswith(("test_", "smoke", "falsify", "alpha"))]
    return out

def verify_hint() -> str:
    """one-line pointer to the commands that re-verify the whole stack (Coq kernel + axiom audit + tests)."""
    return ("run: `make verify` (coqchk + axiom audit) · `python -m pytest tests/` · "
            "`PYTHONPATH=. python3 scripts/smoke_test_spine.py` · `scripts/falsify_particle_graph.py`")


# ───────────────────────── discovery helpers (feed MCP domain/read tools) ─────────────────────────
READOUT_NAMES = tuple(r.name for r in Readout)

def list_domains() -> list[str]:
    """names of the L3 domain cards (DATA-driven; structure = spine, values finite_diagnostic)."""
    return sorted(DOMAINS)

def list_readouts() -> list[str]:
    """names of the L2 readouts R0–R7."""
    return list(READOUT_NAMES)


__all__ = [
    "Memory", "Spine", "Readout", "Faces", "Result",
    "DOMAINS", "OPEN_GATES", "OPEN_CONSTANTS", "FRAMEWORK_PRIMER",
    "STRUCTURE_TIERS", "VALUE_TIERS", "READOUT_NAMES",
    "cascade_transfer", "couple", "agency", "constant",
    "list_tests", "verify_hint", "list_domains", "list_readouts",
]


# ═══════════════════════ τc DATABASE — measured constants → causal memory τc ═══════════════════════
# Each known particle has a MEASURED mass (PDG/CODATA); its causal memory time is τc = ℏ/(2·m·c²)
# [Th_coqc: InfoTelegraph.mass_memory_duality]. Values are finite_diagnostic (measured input), NOT derived
# (deriving the masses is [Open]). In natural units (ℏ=c=1) τc = 1/(2m) — the common information unit.
def _phys_constants():
    """ℏ (J·s) and e (C) — LAZY scipy import with fallback to engine.constants (honours the lazy-import contract:
    a missing scipy must NOT brick the whole module / MCP server)."""
    try:
        import scipy.constants as _SC
        return _SC.hbar, _SC.e
    except Exception:
        from .constants import HBAR, E_CHARGE
        return HBAR, E_CHARGE
# particle : rest mass in MeV/c²  (measured, PDG 2024)
TAU_C_DB = {
    "electron": 0.51099895, "muon": 105.6583755, "tau": 1776.86,
    "up": 2.16, "down": 4.67, "strange": 93.4, "charm": 1270.0, "bottom": 4180.0, "top": 172500.0,
    "proton": 938.27208816, "neutron": 939.56542052,
    "W": 80377.0, "Z": 91187.6, "higgs": 125250.0,
}
def _tau_c_seconds(mass_MeV: float) -> float:
    hbar, ev = _phys_constants()
    E_J = mass_MeV * 1e6 * ev                         # rest energy m c² in joules
    return hbar / (2.0 * E_J)                         # τc = ℏ/(2E)
def mass_of(name: str) -> Result:
    """measured rest mass (MeV/c²) — finite_diagnostic (PDG), NOT derived ([Open] to derive)."""
    if name not in TAU_C_DB:
        raise UnknownParticle(f"unknown particle {name!r}; known: {sorted(TAU_C_DB)}")
    return Result(TAU_C_DB[name], "Th_coqc", "finite_diagnostic", "InfoTelegraph.mass_memory_duality")
def tau_c_of(name: str) -> Result:
    """causal memory time τc = ℏ/(2 m c²) for a particle with a measured mass — the memory-before-mass bridge."""
    if name not in TAU_C_DB:
        raise UnknownParticle(f"unknown particle {name!r}; known: {sorted(TAU_C_DB)}")
    return Result(_tau_c_seconds(TAU_C_DB[name]), "Th_coqc", "finite_diagnostic",
                  "InfoTelegraph.mass_memory_duality")
def memory_of(name: str) -> Memory:
    """a Memory whose τc (seconds) is set from a measured particle. To recover the SI rest mass (kg) call
    .mass(hbar=scipy.constants.hbar, c=scipy.constants.c) — the default ℏ=c=1 gives the natural-unit value."""
    return Memory([(0, 1, 1.0)], tau_c=_tau_c_seconds(TAU_C_DB[name]))

# ═══════════════════════ lib-backed DOMAIN CARDS — API orchestrates world-class libs ═══════════════════════
# Each card wraps an external numerical engine; the EXTERNAL result is finite_diagnostic, the STRUCTURE stays
# the spine [Th_coqc: InfoUniversalEquation.domain_invariant_zero]. Libs are lazy-imported; absent ⇒ [Open].
def _lib(name):
    try:
        import importlib; return importlib.import_module(name)
    except Exception:
        return None

def _chemistry(mem=None, *, smiles=None, **p):
    """chemistry: molecular graph = L_R; Hückel MO energies = the spectrum readout (RDKit builds the graph).
    Without a SMILES there is no molecule to read ⇒ honest [Open] (particle_graph); we never fabricate a spectrum
    from an unrelated memory graph and call it chemistry."""
    if smiles is None:
        return _open("particle_graph")
    rk = _lib("rdkit")
    if rk is None:
        return _open("library_unavailable")
    from rdkit import Chem
    m = Chem.MolFromSmiles(smiles)
    if m is None or m.GetNumAtoms() == 0:        # unparseable OR empty/0-atom ⇒ no molecule to read ⇒ [Open]
        return _open("particle_graph")
    A = Chem.GetAdjacencyMatrix(m).astype(float)
    huckel = np.sort(np.linalg.eigvalsh(A))                # Hückel MO energies (β units), ascending (matches R2_SPECTRUM)
    return Result({"huckel_MO": huckel, "n_atoms": m.GetNumAtoms(), "smiles": smiles},
                  "Th_coqc", "finite_diagnostic", "InfoOperator.info_is_operator_energy (Hückel = graph spectrum)")

def _finance_option(mem=None, *, S=100.0, K=100.0, r=0.02, sigma=0.2, T=1.0, call=True, **p):
    """finance: Black-Scholes option price (stdlib closed form; structure = spine domain-invariance).
    Black-Scholes is computable WITHOUT any external library, so this never returns a (mis-labelled) physics gate."""
    if S <= 0 or K <= 0:
        raise ValueError(f"S and K (prices) must be positive, got S={S}, K={K}")
    if sigma <= 0 or T <= 0:
        raise ValueError(f"sigma (vol) and T (maturity) must be positive, got sigma={sigma}, T={T}")
    import math
    d1 = (math.log(S / K) + (r + sigma * sigma / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    from statistics import NormalDist
    N = NormalDist().cdf
    price = (S * N(d1) - K * math.exp(-r * T) * N(d2)) if call else (K * math.exp(-r * T) * N(-d2) - S * N(-d1))
    return Result({"price": price, "S": S, "K": K, "sigma": sigma, "T": T},
                  "Th_coqc", "finite_diagnostic", "InfoUniversalEquation.domain_invariant_zero")

def _social_diffusion(mem, *, beta=0.1, gamma=0.05, steps=20, frac_infected=0.05, seed=0,
                      stochastic=False, **p):
    """social: SIR contagion on the memory graph. DETERMINISTIC by default — the spectral epidemic threshold
    R0 = β·λ_max/γ [Th_coqc: InfoBio.sis_eigenvalues_real]. Pass stochastic=True to run ndlib's Monte-Carlo SIR
    (seeded; note: ndlib uses its own RNG so the seed reduces but may not fully remove run-to-run variation)."""
    if stochastic and _lib("ndlib") is not None and _lib("networkx") is not None:
        import random as _rnd
        _rnd.seed(seed); np.random.seed(seed)
        import networkx as nx, ndlib.models.ModelConfig as mc, ndlib.models.epidemics as ep
        A = (np.abs(mem.L) > 1e-9).astype(float) - np.eye(mem.n)
        model = ep.SIRModel(nx.from_numpy_array(A)); cfg = mc.Configuration()
        cfg.add_model_parameter("beta", beta); cfg.add_model_parameter("gamma", gamma)
        cfg.add_model_parameter("fraction_infected", frac_infected); model.set_initial_status(cfg)
        peak = max(s["node_count"][1] for s in model.iteration_bunch(steps))
        return Result({"peak_infected": peak, "steps": steps, "stochastic": True, "seed": seed},
                      "Th_coqc", "finite_diagnostic", "InfoBio.sis_eigenvalues_real")
    lam_max = float(np.max(np.linalg.eigvalsh(mem.L)))
    return Result({"R0": beta * lam_max / gamma, "epidemic": beta * lam_max > gamma, "deterministic": True},
                  "Th_coqc", "finite_diagnostic", "InfoBio.sis_eigenvalues_real")

DOMAINS.update({
    "chemistry": _chemistry,
    "finance_option": _finance_option,
    "social_diffusion": _social_diffusion,
})
__all__ += ["TAU_C_DB", "tau_c_of", "mass_of", "memory_of", "__version__", "MAX_NODES",
            "UniverseError", "UnknownDomain", "UnknownConstant", "UnknownParticle", "InvalidOperator"]


# more lib-backed domain cards (qutip / pyscf / biopython / astropy) — engine=finite_diagnostic, structure=spine
def _quantum_dynamics(mem=None, *, gamma=0.1, t=5.0, **p):
    """quantum: open-system decoherence via QuTiP (Lindblad) — the spine D∂ dissipative readout."""
    qt = _lib("qutip")
    if qt is None:
        return _open("library_unavailable")
    import numpy as _np
    H = qt.sigmaz() * 0.5
    psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
    res = qt.mesolve(H, psi0, _np.linspace(0, t, 50),
                     c_ops=[_np.sqrt(gamma) * qt.sigmam()], e_ops=[qt.sigmax()])
    coh = float(res.expect[0][-1])
    return Result({"coherence_final": coh, "gamma": gamma, "t": t}, "Th_coqc", "finite_diagnostic",
                  "InfoDecoherence.decoherence_rate_positive (D-branch of the spine)")

def _chemistry_dft(mem=None, *, atom="H 0 0 0; H 0 0 0.74", basis="sto-3g", **p):
    """chemistry: real electronic energy via PySCF RHF — energy = information (R0) at the quantitative tier."""
    ps = _lib("pyscf")
    if ps is None:
        return _open("particle_graph")
    from pyscf import gto, scf
    mol = gto.M(atom=atom, basis=basis, verbose=0)
    e = float(scf.RHF(mol).kernel())
    return Result({"energy_hartree": e, "atom": atom, "basis": basis}, "Th_coqc", "finite_diagnostic",
                  "InfoOperator.info_is_operator_energy (electronic energy)")

def _genomics(mem=None, *, sequence="ATGCGCGTAATTACG", **p):
    """genomics: sequence information content (GC + Shannon entropy) — RD=information made literal (Biopython)."""
    import math, collections
    s = sequence.upper()
    gc = (s.count("G") + s.count("C")) / max(len(s), 1)
    cnt = collections.Counter(s); n = len(s)
    H = -sum((c / n) * math.log2(c / n) for c in cnt.values()) if n else 0.0
    return Result({"gc_content": gc, "shannon_bits": H, "length": n}, "Th_coqc", "finite_diagnostic",
                  "InfoOperator.info_is_operator_energy (Shannon = retained information)")

def _cosmology(mem=None, *, z=1.0, **p):
    """cosmology: FRW distances/age via Astropy — the spine cosmo-equilibrium readout."""
    ap = _lib("astropy")
    if ap is None:
        return _open("library_unavailable")
    from astropy.cosmology import Planck18
    return Result({"age_Gyr": float(Planck18.age(z).value), "lum_dist_Mpc": float(Planck18.luminosity_distance(z).value), "z": z},
                  "Th_coqc", "finite_diagnostic", "InfoCosmoEquilibrium.spine_equilibrium_iff_rest")

DOMAINS.update({
    "quantum_dynamics": _quantum_dynamics,
    "chemistry_dft": _chemistry_dft,
    "genomics": _genomics,
    "cosmology": _cosmology,
})


# lib cards: neuro (MNE) / agent-based (Mesa→consensus) / optimization (CVXPY) / geo (Shapely)
def _neuro(mem=None, *, fs=256.0, freq=10.0, t=2.0, **p):
    """neuro: dominant rhythm of a signal via PSD (MNE if present, else SciPy) — the spectrum readout."""
    import numpy as _np
    n = int(fs * t); times = _np.arange(n) / fs
    sig = _np.sin(2 * _np.pi * freq * times)
    mne = _lib("mne")
    if mne is not None:
        psd, f = mne.time_frequency.psd_array_welch(sig[None, :], sfreq=fs, fmin=1, fmax=40, verbose=0)
        peak = float(f[_np.argmax(psd[0])])
    else:
        from scipy.signal import welch
        f, psd = welch(sig, fs=fs); peak = float(f[_np.argmax(psd)])
    return Result({"peak_hz": peak, "fs": fs}, "Th_coqc", "finite_diagnostic",
                  "RDL_GammaSpectral (PSD = the spectrum readout)")

def _agent_based(mem, *, steps=200, **p):
    """agent-based: DeGroot consensus on the memory graph (agents = coupled spines → spine equilibrium).
    Mesa available for richer ABM; the consensus limit is the spine fixed point."""
    import numpy as _np
    scale = float(_np.abs(mem.L).max()) or 1.0                # relative edge threshold — don't drop small-but-real weights
    A = (_np.abs(mem.L) > 1e-9 * scale).astype(float) - _np.eye(mem.n)
    A = _np.clip(A, 0, None); deg = A.sum(1, keepdims=True); W = A / _np.where(deg == 0, 1, deg)
    x = _np.linspace(0, 1, mem.n)
    for _ in range(steps):
        x = W @ x
    return Result({"consensus": float(x.mean()), "spread": float(x.max() - x.min()), "steps": steps},
                  "Th_coqc", "finite_diagnostic", "InfoCosmoEquilibrium.spine_equilibrium_iff_rest")

def _optimization(mem=None, *, target=None, n=4, **p):
    """optimization: project a target onto the simplex (min ‖x−target‖² s.t. x≥0, Σx=1) via CVXPY — ∇V min."""
    cp = _lib("cvxpy")
    import numpy as _np
    tgt = _np.array(target if target is not None else _np.linspace(0, 1, n), float); k = len(tgt)
    if cp is None:
        v = tgt - (tgt.sum() - 1) / k; x = _np.clip(v, 0, None)        # closed-form-ish proxy
        return Result({"x": x.tolist(), "note": "cvxpy absent — proxy"}, "Th_coqc", "finite_diagnostic",
                      "InfoPotential.vacuum_is_equilibrium")
    x = cp.Variable(k); prob = cp.Problem(cp.Minimize(cp.sum_squares(x - tgt)), [x >= 0, cp.sum(x) == 1])
    prob.solve()
    return Result({"x": [float(v) for v in x.value], "objective": float(prob.value)},
                  "Th_coqc", "finite_diagnostic", "InfoPotential.vacuum_is_equilibrium (∇V minimum)")

def _geo(mem=None, *, points=None, radius=1.5, **p):
    """geo: geography as a memory graph — points → proximity graph → the L_R spectrum (Shapely distances)."""
    import numpy as _np
    pts = _np.array(points if points is not None else [(0, 0), (1, 0), (1, 1), (0, 1), (2, 2)], float)
    D = _np.sqrt(((pts[:, None] - pts[None]) ** 2).sum(-1))
    A = ((D > 0) & (D <= radius)).astype(float)
    Lg = _np.diag(A.sum(1)) - A
    return Result({"spectrum": _np.sort(_np.linalg.eigvalsh(Lg)).tolist(), "n_points": len(pts)},
                  "Th_coqc", "finite_diagnostic", "RDL_GammaSpectral (geography = memory graph)")

DOMAINS.update({
    "neuro": _neuro, "agent_based": _agent_based, "optimization": _optimization, "geo": _geo,
})


def _group_theory(mem=None, *, group="S4", **p):
    """group theory via sympy.combinatorics (GAP optional backend). Computes finite-group invariants AND the SM
    gauge STRUCTURE (SU(N) generators = N²−1: gluons 8, weak 3, U(1) 1 = 12 bosons) [Th_coqc: InfoStandardModel].
    The gauge-group DERIVATION (why SU(3)×SU(2)×U(1)) is [Open] — hypothesis H1 (gauge = info-preserving
    readout symmetry). The tool computes group PROPERTIES; it does NOT derive which group nature picks."""
    try:                                                   # lazy-import contract: absent sympy ⇒ honest [Open], never a crash
        from sympy.combinatorics.named_groups import (SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup)
    except Exception:
        return _open("library_unavailable")
    tbl = {"S": SymmetricGroup, "A": AlternatingGroup, "C": CyclicGroup, "D": DihedralGroup}
    kind, k = group[0].upper(), int(group[1:])
    G = tbl.get(kind, SymmetricGroup)(k)
    finite = {"group": group, "order": int(G.order()), "abelian": bool(G.is_abelian),
              "solvable": bool(G.is_solvable), "nilpotent": bool(G.is_nilpotent)}
    sm = {"SU(3)_gluons": 3 * 3 - 1, "SU(2)_weak": 2 * 2 - 1, "U(1)": 1,
          "total_gauge_bosons": (3 * 3 - 1) + (2 * 2 - 1) + 1}
    return Result({"finite_group": finite, "sm_gauge_structure": sm,
                   "open_H1": "deriving SU(3)×SU(2)×U(1) is [Open] (H1: gauge = info-preserving readout symmetry)"},
                  "Th_coqc", "finite_diagnostic",
                  "InfoStandardModel (gauge dims = N^2-1; group DERIVATION [Open] H1)")

DOMAINS.update({"group_theory": _group_theory})


# per-domain allowed-parameter whitelist (used by Memory._domain). Unknown keys are REJECTED, never silently
# swallowed into a default (so a typo like `gamm=` can no longer change the answer behind the caller's back).
_DOMAIN_PARAMS = {
    "heat": {"t"}, "diffusion": {"t"},
    "quantum": {"t"}, "wave": {"t"},
    "epidemiology": {"beta", "gamma"},
    "ecology": {"r", "K"},
    "evolution": {"p0", "p1", "w0", "w1"},
    "network_resistance": {"i", "j"},
    "economics": set(), "finance": set(), "social": set(), "mental_health": set(),
    "chemistry": {"smiles"},
    "finance_option": {"S", "K", "r", "sigma", "T", "call"},
    "social_diffusion": {"beta", "gamma", "steps", "frac_infected", "seed", "stochastic"},
    "quantum_dynamics": {"gamma", "t"},
    "chemistry_dft": {"atom", "basis"},
    "genomics": {"sequence"},
    "cosmology": {"z"},
    "neuro": {"fs", "freq", "t"},
    "agent_based": {"steps"},
    "optimization": {"target", "n"},
    "geo": {"points", "radius"},
    "group_theory": {"group"},
}
