"""lens.gates -- Omega_all as a callable API: forcing gates G1-G7 + G9-G11
(G8 = the Extraction assembly in run_gates).

The NEW layer developed in THIS repo (2026-07-19) on top of the vendored
verified engine (lens/vendor/, snapshot of research_universal_solver/engine).
Doc contract: v2/POSITION.md section 2 (gates) + section 3 (7-piece extraction).

Design rule (readout-not-truth): a gate that can COMPUTE, computes and tags
`finite_diagnostic`; a gate that requires judgment returns verdict `PROMPT`
with the exact question the operator (human/AI) must answer -- it never fakes
an answer. Every Extraction states its overall tier as the WEAKEST tier used.

PRIVATE / PROPRIETARY -- not under the repo's CC BY 4.0 grant (see LICENSE
EXCEPTIONS + lens/vendor/LICENSE). Do not publish.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import numpy as np

from .vendor.lexicon import translate_to_philosophy
from . import solver_link

# The FULL Zero-Infinity Dual Guard (ZERO_INFINITY_DUAL_DIAGNOSIS.md):
# an injected exact ZERO is the same disease as an injected INFINITY --
# both are non-readouts. Heuristic screens; the operator confirms each hit.
_INF_MARKERS = {
    "I1_R_completeness": r"\breal number|continuum|\bR-complete|infinitely precise|exact value\b",
    "I2_infinite_divisibility": r"h\s*->\s*0|infinitely divisible|limit of zero step|supertask",
    "I3_infinite_scale": r"infinite (universe|volume|extent|scale)|unbounded domain|Re\s*->\s*inf",
    "I4_actual_infinity": r"actual infinity|infinitely many steps completed|\binfinite set\b",
}
_ZERO_MARKERS = {
    "Z1_exact_point": r"\bpoint (particle|mass|charge)\b|exactly zero size|\bsingularity\b",
    "Z2_zero_step": r"\bh\s*=\s*0\b|zero step size|instantaneous(ly)? exact",
    "Z3_absolute_rest": r"\babsolute (rest|zero)\b|\bT\s*=\s*0\b|perfectly isolated",
    "Z4_true_void": r"\btrue void\b|absolute nothing|empty of all difference",
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
    cited_theorems: list[str] = field(default_factory=list)   # names claimed as machine-checked
    limit_series: tuple[list[float], list[float]] | None = None  # (samples, limit_vars)
    limit_side: str = "zero"                   # 'zero' | 'infinity' (which limit is claimed)
    formula_pair: tuple[str, str] | None = None  # two closure ids claimed (in)equivalent
    claimed_tau_s: float | None = None         # a timescale the issue asserts (seconds)


@dataclass
class GateResult:
    gate: str
    verdict: str        # PASS | FLAG | PROMPT
    tier: str           # Open | Dr | finite_diagnostic | Th_coqc (weakest..strongest)
    detail: str


@dataclass
class Extraction:
    """The 8-piece maximal extraction (v2/POSITION.md section 3).
    Piece 8 (not_checked) imports the PDEBench discipline: every bound of the
    analysis is declared RUN / SKIPPED-with-reason -- silent omission reads as
    coverage, which is a lie by layout."""
    translation: str
    posit_ledger: str
    record_inventory: str
    null_space: str
    pi_statement: str
    decisive_record: str
    falsifier: str
    not_checked: str = ""
    gates: list[GateResult] = field(default_factory=list)
    tier: str = "Dr"

    def complete(self) -> bool:
        """Complete = every piece filled AND no 'operator fills' placeholder
        left. A placeholder counting as done would let a fake extraction pass
        -- the exact failure this class exists to prevent."""
        pieces = [self.translation, self.posit_ledger, self.record_inventory,
                  self.null_space, self.pi_statement, self.decisive_record,
                  self.falsifier, self.not_checked]
        return all(p.strip() and not p.startswith("operator fills") for p in pieces)


def g1_translate(issue: Issue) -> GateResult:
    """G1: translate via the REAL lexicon (never paraphrase from memory).
    If no glossary term matched (echo-back), say so -- the Lens Law needs the
    operator to add dictionary rows, not to mistake an echo for a translation."""
    phil = translate_to_philosophy(issue.statement)
    if phil.strip() == issue.statement.strip():
        return GateResult("G1_translate", "PROMPT", "Open",
                          "no glossary term matched -- statement echoed back; "
                          "add dictionary rows (TRANSLATION_PROTOCOL step 1) "
                          "before proceeding")
    return GateResult("G1_translate", "PASS", "Dr", phil)


def g2_infinity(text: str) -> GateResult:
    """The dual Guard: screen for injected INFINITY (I1-I4) AND injected
    exact ZERO (Z1-Z4) -- both are non-readouts; a verdict benchmarked on
    either side is inadmissible (readout-vs-readout only)."""
    hits = [k for k, pat in _INF_MARKERS.items() if re.search(pat, text, re.I)]
    hits += [k for k, pat in _ZERO_MARKERS.items() if re.search(pat, text, re.I)]
    if hits:
        return GateResult("G2_omega_inf", "FLAG", "Dr",
                          f"injected: {', '.join(hits)} -- dissolve or restate "
                          "as finite readout before answering (heuristic screen; "
                          "false positives possible -- operator confirms)")
    return GateResult("G2_omega_inf", "PASS", "Dr", "no zero/infinity marker "
                      "detected (heuristic screen -- operator confirms)")


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
        return GateResult("G5_identifiability", "PASS", "Dr",
                          f"{issue.hypothesis_dims} hypothesis directions <= "
                          f"{rec}-coordinate record: no structural obstruction "
                          "(counting argument only -- a grammar run is stronger)")
    return GateResult("G5_identifiability", "PROMPT", "Open",
                      "supply the grammar A (or record/hypothesis dims) to run this gate")


def g6_load_bearing(issue: Issue) -> GateResult:
    """LTP3 executable: does dropping the declared rows move the query answer?

    Method note: uses unit evidence d=1 + lstsq, NOT the canonical battery's
    damped-descent settle() with d=[1.0,0.5,-0.3] (code/LTP2_3_4_battery.py).
    The idle/load-bearing dichotomy is a structural property of which query
    overlaps the dropped row -- verified invariant across evidence vectors --
    but keep the canonical battery as the citable LTP3 anchor."""
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


def g9_theorem_check(issue: Issue) -> GateResult:
    """G9: every claimed machine-checked theorem must resolve against the
    live solver arc (THEOREM_INDEX.md + formal/*.v). Miss => the claim's
    Th_coqc tag is UNBACKED: auto-downgrade to Dr. This turns tier discipline
    from manual habit into mechanism."""
    if not issue.cited_theorems:
        return GateResult("G9_theorem_check", "PASS", "Dr", "no Th_coqc citation to verify")
    lines, misses, unavailable = [], [], False
    for name in issue.cited_theorems:
        r = solver_link.theorem_lookup(name)
        if r["found"] is None:
            unavailable = True
            lines.append(f"{name}: UNVERIFIED ({r['note']})")
        elif r["found"]:
            lines.append(f"{name}: FOUND ({', '.join(r['v_files'] or r['index_hits'])})")
        else:
            misses.append(name)
            lines.append(f"{name}: MISS -- auto-downgrade Th_coqc -> Dr")
    note = (" [grep-level check: FOUND = referenced in the arc, not re-verified"
            " -- for verified status run coq_verify/coqc on the file]")
    if unavailable:
        return GateResult("G9_theorem_check", "PROMPT", "Open", "; ".join(lines))
    if misses:
        return GateResult("G9_theorem_check", "FLAG", "Dr", "; ".join(lines) + note)
    return GateResult("G9_theorem_check", "PASS", "Dr", "; ".join(lines) + note)


def g10_limit(issue: Issue) -> GateResult:
    """G10: a convergence/divergence claim gets a fitted-law verdict from the
    live solver's limits engine (LimitCertificate; refuses on thin data) --
    never an eyeballed 'it clearly goes to zero'."""
    if issue.limit_series is None:
        return GateResult("G10_limit", "PASS", "Dr", "no limit claim to certify")
    limits = solver_link.import_engine("limits")
    if limits is None:
        return GateResult("G10_limit", "PROMPT", "Open",
                          "SKIPPED: solver unavailable -- limit claim stays uncertified")
    samples, lvars = issue.limit_series
    fn = limits.classify_zero_limit if issue.limit_side == "zero" else limits.classify_infinity_limit
    try:
        cert = fn(list(samples), list(lvars))
    except Exception as e:  # thin/invalid data: refuse honestly, never fabricate
        return GateResult("G10_limit", "PROMPT", "Open", f"BLOCKED_NOT_CLAIMED: {e}")
    return GateResult("G10_limit", "FLAG" if "BLOCKED" in str(cert.verdict) else "PASS",
                      "finite_diagnostic", f"verdict={cert.verdict} law={getattr(cert, 'law', '?')} "
                      f"(LimitCertificate from engine.limits)")


def g11_equivalence(issue: Issue) -> GateResult:
    """G11: 'these two formulas are (not) the same' is adjudicated by the
    solver's equivalence registry (documented mapping + numeric re-proof),
    not by argument. Quantity-by-role at the formula level."""
    if issue.formula_pair is None:
        return GateResult("G11_equivalence", "PASS", "Dr", "no formula-pair dispute")
    eq = solver_link.import_engine("equivalence")
    formulas = solver_link.import_engine("formulas")
    if eq is None or formulas is None:
        return GateResult("G11_equivalence", "PROMPT", "Open",
                          "SKIPPED: solver unavailable -- equivalence undecided")
    a, b = issue.formula_pair
    unknown = [n for n in (a, b) if n not in getattr(formulas, "REGISTRY", {})]
    if unknown:
        return GateResult("G11_equivalence", "PROMPT", "Open",
                          f"unknown closure(s) {unknown} -- not in the formulas "
                          "REGISTRY; nothing was adjudicated")
    if a == b:
        return GateResult("G11_equivalence", "PASS", "finite_diagnostic",
                          f"'{a}' == '{b}': identical closure, trivially equivalent")
    same = b in eq.equivalent_closures(a)
    if same:
        return GateResult("G11_equivalence", "PASS", "finite_diagnostic",
                          f"'{a}' ~ '{b}': EQUIVALENT under registered mapping")
    return GateResult("G11_equivalence", "FLAG", "Dr",
                      f"'{a}' vs '{b}': NO registered equivalence mapping -- "
                      "UNDECIDED. Absence of registration is NOT proof of "
                      "inequivalence; register the mapping to adjudicate")


def g12_triage(issue: Issue) -> GateResult:
    """G12: structural intake triage via the solver's murg operators -- names
    which of the 14 cross-domain reasoning operators (Repair, Cost, Boundary,
    Persistence, ...) the issue is made of, BEFORE the gates argue anything.
    Informational (Dr): a triage is a reading aid, never a verdict."""
    murg = solver_link.import_engine("murg")
    if murg is None:
        return GateResult("G12_triage", "PROMPT", "Open",
                          "SKIPPED: solver unavailable -- triage by hand")
    r = murg.route(issue.statement)
    return GateResult("G12_triage", "PASS", "Dr",
                      f"domain~{r.domain}, operators={r.operators}, "
                      f"confidence={r.confidence:.2f} (keyword router -- reading aid, "
                      "not a verdict; low confidence => triage by hand)")


def g13_timescale(issue: Issue) -> GateResult:
    """G13: a claimed timescale is checked against the solver's tau_c atlas
    (220 entries / 36 disciplines, ~85 orders of magnitude) -- naming the
    regime it lands in and its nearest measured neighbours, so an issue
    cannot silently conflate regimes."""
    if issue.claimed_tau_s is None:
        return GateResult("G13_timescale", "PASS", "Dr", "no timescale claim")
    if issue.claimed_tau_s <= 0:
        return GateResult("G13_timescale", "PROMPT", "Open",
                          "non-positive timescale -- restate as a finite readout")
    tc = solver_link.import_engine("tau_c")
    if tc is None:
        return GateResult("G13_timescale", "PROMPT", "Open",
                          "SKIPPED: solver unavailable -- timescale unchecked")
    import math
    tau = issue.claimed_tau_s
    neighbours = []
    for cat, entries in tc.ATLAS.items():
        for (nm, t, _kind, _src) in entries:
            if t > 0:
                neighbours.append((abs(math.log10(tau / t)), f"{nm} [{cat}] {t:.3g}s"))
    neighbours.sort()
    near = "; ".join(n for _, n in neighbours[:3])
    floor = getattr(tc, "TAU_C_FLOOR_S", None)
    below = floor is not None and tau < floor
    return GateResult("G13_timescale", "FLAG" if below else "PASS",
                      "finite_diagnostic",
                      (f"BELOW the tau_c floor ({floor:.3g}s) -- non-readout territory; "
                       if below else "") + f"nearest atlas neighbours: {near}")


def run_gates(issue: Issue) -> Extraction:
    """Walk G1-G7 + G9-G13; assemble the 8-piece extraction (= G8)."""
    g = [g1_translate(issue), g2_infinity(issue.statement), g3_quantity_role(issue),
         g4_pi_selection(issue), g5_identifiability(issue), g6_load_bearing(issue),
         g7_readout_vs_readout(issue), g9_theorem_check(issue), g10_limit(issue),
         g11_equivalence(issue), g12_triage(issue), g13_timescale(issue)]
    # weakest-tier-wins over the ordering Open < Dr < finite_diagnostic < Th_coqc
    _ORDER = ["Open", "Dr", "finite_diagnostic", "Th_coqc"]
    tiers = [r.tier for r in g]
    overall = _ORDER[min(_ORDER.index(t) for t in tiers)]
    overall = "Dr" if overall in ("finite_diagnostic", "Th_coqc") else overall
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
        not_checked="operator fills: every SKIPPED check + why (resource/data/"
                    "scope) -- silent omission is banned",
        gates=g, tier=overall)
    return ex
