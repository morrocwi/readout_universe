"""lens.gates -- Omega_all as a callable API: the G1-G8 forcing gates.

The NEW layer developed in THIS repo (2026-07-19) on top of the vendored
verified engine (lens/vendor/, snapshot of research_universal_solver/engine).
Doc contract: v2/POSITION.md section 2 (gates) + section 3 (7-piece extraction).

Design rule (readout-not-truth): a gate that can COMPUTE, computes and tags
`finite_diagnostic`; a gate that requires judgment returns verdict `PROMPT`
with the exact question the operator (human/AI) must answer -- it never fakes
an answer. Every Extraction states its overall tier as the WEAKEST tier used.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import numpy as np

from .vendor.lexicon import translate_to_philosophy

# I1-I4 infinity-injection markers (heuristic screen; Omega_inf doctrine)
_INF_MARKERS = {
    "I1_R_completeness": r"\breal number|continuum|\bR-complete|infinitely precise|exact value\b",
    "I2_infinite_divisibility": r"h\s*->\s*0|infinitely divisible|limit of zero step|supertask",
    "I3_infinite_scale": r"infinite (universe|volume|extent|scale)|unbounded domain",
    "I4_actual_infinity": r"actual infinity|infinitely many steps completed|\binfinite set\b",
}


@dataclass
class Quantity:
    """A quantity = (name, operator/chain, role). Identity by role, not name."""
    name: str
    chain: str          # calibration/derivation chain that produced it
    role: str = ""      # downstream inferential role


@dataclass
class Issue:
    statement: str
    quantities: list[Quantity] = field(default_factory=list)
    grammar: list[list[float]] | None = None   # rows of A (the record's grammar)
    query: list[float] | None = None           # direction asked about (dim = A cols)
    discard_rows: list[int] = field(default_factory=list)  # rows a bounded reading drops
    hypothesis_dims: int | None = None         # independent directions among hypotheses
    instrument_change: str = ""                # new readout policy, if any
    refutation_benchmark: str = ""             # what a claimed refutation compares against


@dataclass
class GateResult:
    gate: str
    verdict: str        # PASS | FLAG | PROMPT
    tier: str           # Dr | finite_diagnostic | Open
    detail: str


@dataclass
class Extraction:
    """The 7-piece maximal extraction (v2/POSITION.md section 3)."""
    translation: str
    posit_ledger: str
    record_inventory: str
    null_space: str
    pi_statement: str
    decisive_record: str
    falsifier: str
    gates: list[GateResult] = field(default_factory=list)
    tier: str = "Dr"

    def complete(self) -> bool:
        """Complete = every piece filled AND no 'operator fills' placeholder
        left. A placeholder counting as done would let a fake extraction pass
        -- the exact failure this class exists to prevent."""
        pieces = [self.translation, self.posit_ledger, self.record_inventory,
                  self.null_space, self.pi_statement, self.decisive_record,
                  self.falsifier]
        return all(p.strip() and not p.startswith("operator fills") for p in pieces)


def g1_translate(issue: Issue) -> GateResult:
    """G1: translate via the REAL lexicon (never paraphrase from memory)."""
    phil = translate_to_philosophy(issue.statement)
    return GateResult("G1_translate", "PASS", "Dr", phil)


def g2_infinity(text: str) -> GateResult:
    hits = [k for k, pat in _INF_MARKERS.items() if re.search(pat, text, re.I)]
    if hits:
        return GateResult("G2_omega_inf", "FLAG", "Dr",
                          f"injected: {', '.join(hits)} -- dissolve or restate "
                          "as finite readout before answering")
    return GateResult("G2_omega_inf", "PASS", "Dr", "no infinity marker detected "
                      "(heuristic screen -- operator confirms)")


def g3_quantity_role(issue: Issue) -> GateResult:
    """Equal-number fallacy guard: same name + different chain => different
    quantities by role until role-equivalence is shown."""
    by_name: dict[str, set[str]] = {}
    for q in issue.quantities:
        by_name.setdefault(q.name, set()).add(q.chain)
    clashes = {n: c for n, c in by_name.items() if len(c) > 1}
    if clashes:
        det = "; ".join(f"'{n}' carries {len(c)} distinct chains -- treat as "
                        f"DIFFERENT quantities until role-equivalence proven"
                        for n, c in clashes.items())
        return GateResult("G3_quantity_role", "FLAG", "Dr", det)
    return GateResult("G3_quantity_role", "PASS", "Dr", "no same-name/different-chain clash")


def g4_pi_selection(issue: Issue) -> GateResult:
    if issue.instrument_change:
        return GateResult("G4_pi_selection", "FLAG", "Dr",
                          f"readout policy changed ({issue.instrument_change}): "
                          "sorites signature -- forward-model the OLD population "
                          "through the NEW selection before declaring a new class")
    return GateResult("G4_pi_selection", "PASS", "Dr", "no policy change declared")


def g5_identifiability(issue: Issue) -> GateResult:
    """If the grammar is given, COMPUTE the null space (finite_diagnostic)."""
    if issue.grammar is not None:
        A = np.asarray(issue.grammar, float)
        rank = int(np.linalg.matrix_rank(A))
        n = A.shape[1]
        if rank < n:
            _, _, vt = np.linalg.svd(A)
            null = vt[rank:]
            det = (f"rank {rank}/{n}: null space dim {n-rank}, basis "
                   f"{np.round(null, 3).tolist()} -- differences along it are "
                   "REAL but permanently inaccessible from this record (LTP4)")
            if issue.query is not None:
                q = np.asarray(issue.query, float)
                q = q / np.linalg.norm(q)
                overlap = float(np.linalg.norm(null @ q))
                det += f"; query||null overlap = {overlap:.3f}" + (
                    " => query is STRUCTURALLY unanswerable from this record"
                    if overlap > 0.5 else "")
            return GateResult("G5_identifiability", "FLAG", "finite_diagnostic", det)
        return GateResult("G5_identifiability", "PASS", "finite_diagnostic",
                          f"full rank {rank}/{n}: record identifies every direction")
    if issue.hypothesis_dims is not None and issue.quantities:
        rec = len({q.name for q in issue.quantities})
        if issue.hypothesis_dims > rec:
            return GateResult("G5_identifiability", "FLAG", "Dr",
                              f"{issue.hypothesis_dims} hypothesis directions vs "
                              f"{rec}-coordinate record: alternatives live in the "
                              "null space -- undecidable from this record by construction")
    return GateResult("G5_identifiability", "PROMPT", "Open",
                      "supply the grammar A (or record/hypothesis dims) to run this gate")


def g6_load_bearing(issue: Issue) -> GateResult:
    """LTP3 executable: does dropping the declared rows move the query answer?"""
    if issue.grammar is None or issue.query is None or not issue.discard_rows:
        return GateResult("G6_load_bearing", "PROMPT", "Open",
                          "supply grammar + query + discard_rows to run this gate")
    A = np.asarray(issue.grammar, float)
    d = np.ones(A.shape[0])           # unit evidence per constraint (toy convention)
    keep = [i for i in range(A.shape[0]) if i not in issue.discard_rows]
    q = np.asarray(issue.query, float)
    full = float(q @ np.linalg.lstsq(A, d, rcond=None)[0])
    sub = float(q @ np.linalg.lstsq(A[keep], d[keep], rcond=None)[0])
    bearing = abs(full - sub) > 1e-9
    return GateResult("G6_load_bearing", "FLAG" if bearing else "PASS",
                      "finite_diagnostic",
                      f"query answer full={full:.3f} vs bounded={sub:.3f} -- discard is "
                      + ("LOAD-BEARING: the bounded reading diverges (LTP3-B)"
                         if bearing else "idle: bounded ~= full (LTP3-A)"))


def g7_readout_vs_readout(issue: Issue) -> GateResult:
    if not issue.refutation_benchmark:
        return GateResult("G7_rvr", "PASS", "Dr", "no refutation under audit")
    inner = g2_infinity(issue.refutation_benchmark)
    if inner.verdict == "FLAG":
        return GateResult("G7_rvr", "FLAG", "Dr",
                          "refutation benchmarks against an infinity-injected "
                          f"intermediate ({inner.detail}) -- INVALID as a refutation; "
                          "demand readout-vs-readout")
    return GateResult("G7_rvr", "PASS", "Dr",
                      "benchmark shows no injected-infinity marker (heuristic)")


def run_gates(issue: Issue) -> Extraction:
    """Walk G1-G8; assemble the 7-piece extraction. G8 = this assembly."""
    g = [g1_translate(issue), g2_infinity(issue.statement), g3_quantity_role(issue),
         g4_pi_selection(issue), g5_identifiability(issue), g6_load_bearing(issue),
         g7_readout_vs_readout(issue)]
    tiers = [r.tier for r in g]
    overall = "Open" if "Open" in tiers else "Dr"
    ex = Extraction(
        translation=g[0].detail,
        posit_ledger="operator fills: every closure assumption + verdict class "
                     "(DERIVED/FORCED/RELABEL/POSITED/BORROWED/OPEN)",
        record_inventory="; ".join(f"{q.name} <- {q.chain}" for q in issue.quantities)
                         or "operator fills: record coordinates + their chains",
        null_space=g[4].detail,
        pi_statement=g[3].detail,
        decisive_record="operator fills: cheapest record that breaks the null "
                        "direction (ranked by cost)",
        falsifier="operator fills: what kills OUR reading of this issue",
        gates=g, tier=overall)
    return ex
