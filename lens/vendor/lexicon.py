"""
lexicon.py — deterministic World<->Philosophy glossary + honest OPEN_CONSTANTS stance table.

Approach A (chosen): a static .py dict/tuple glossary + deterministic regex substitution translator.
No YAML, no package-data stanza, no new dependency — engine/lexicon.py is just another .py file already
covered by pyproject.toml's `engine*` package glob. Deterministic, byte-for-byte reproducible, trivially
unit-testable (idempotency / longest-match-first / no false positives) — matching the repo's
readout-not-truth discipline: no model call that could hallucinate a stance on an OPEN_CONSTANTS item.

Grafted from Approach B: OPEN_PROBLEM_STANCE entries each carry their own `engine.universe.Result`
(always structure_tier='Open', mirroring `engine.universe.constant()`'s existing contract exactly) so the
stance table never presents itself as more settled than the underlying [Open] readout.

FUTURE EXTENSION POINT (not built in v1): a `MatchStrategy` Protocol could later be introduced to swap the
fixed longest-match-first regex matcher for a fuzzy/embedding-based matcher, e.g.:

    class MatchStrategy(Protocol):
        def find(self, text: str, glossary: tuple[GlossEntry, ...]) -> list[tuple[int, int, GlossEntry]]: ...

This is documented here, deliberately NOT implemented — an unused abstraction is its own maintenance risk,
and v1's only real requirement is a keyword table.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import dataclasses

from .universe import Result, STRUCTURE_TIERS, OPEN_GATES, OPEN_CONSTANTS, UnknownConstant, _open

__all__ = [
    "GlossEntry", "GLOSSARY", "translate_to_philosophy", "translate_to_world",
    "OPEN_PROBLEM_STANCE", "stance_for",
]


# ───────────────────────── glossary entries ─────────────────────────
@dataclass(frozen=True)
class GlossEntry:
    """one bidirectional World<->Philosophy glossary term."""
    world_term: str
    our_term: str
    definition: str
    tier: str                      # one of engine.universe.STRUCTURE_TIERS
    aliases: tuple = field(default_factory=tuple)
    source: str = ""                # doc/code provenance (not a certificate — just a pointer for humans)

    def __post_init__(self):
        if self.tier not in STRUCTURE_TIERS:
            raise ValueError(f"bad tier {self.tier!r} for world_term {self.world_term!r}; allowed {STRUCTURE_TIERS}")


GLOSSARY: tuple = (
    GlossEntry(
        world_term="information",
        our_term="δ_R (retained difference)",
        definition=("The primordial root: a distinction that is drawn AND kept over time. Information is not "
                     "a measure of surprise about pre-existing stuff — it IS the primitive substance the "
                     "universe is made of; everything else is a readout of it."),
        tier="Dr",
        source="docs/GENESIS_DEEP.md:54 (Prologue), engine/universe.py FRAMEWORK_PRIMER line 41",
    ),
    GlossEntry(
        world_term="energy",
        our_term="info(x) = ⟨x, L_R x⟩ (R0_ENERGY)",
        definition=("Energy is identically the information content, computed as the Dirichlet quadratic form "
                     "of the state x against the graph Laplacian/information operator L_R — not a separate "
                     "conserved quantity but the same fact as retained information."),
        tier="Th_coqc",
        source="docs/GENESIS_DEEP.md:74 [Th_coqc: InfoOperator.info_is_operator_energy, R0]; "
               "engine/universe.py:157,204-207 (Readout.R0_ENERGY)",
    ),
    GlossEntry(
        world_term="mass",
        our_term="τ_c (causal memory time), m = ℏ/(2τ_c c²)",
        definition=("Mass is not fundamental; it is a READOUT of causal-memory time — the rate at which a "
                     "piece of the universe forgets. A shorter memory time τ_c pairs with a larger mass "
                     "(mass = inverse memory time), derived from the spine's telegraph substitution."),
        tier="Th_coqc",
        aliases=("rest mass", "particle mass"),
        source="docs/GENESIS_DEEP.md:127-134 [Th_coqc: InfoTelegraph.mass_memory_duality, "
               "InfoSpineMass.spine_memory_mass_product]; engine/universe.py:249-260 (Memory.mass)",
    ),
    GlossEntry(
        world_term="time / arrow of time",
        our_term="causal order ≺, asymmetry of retention",
        definition=("The arrow of time is not assumed; it is what a kept distinction MEANS — retention is "
                     "asymmetric (before-keeping vs after-keeping), and that asymmetry forces a partial "
                     "causal order ≺ over retained states."),
        tier="Th_coqc",
        aliases=("arrow of time",),
        source="docs/GENESIS_DEEP.md:64-70 [Th_coqc: RDL_Distinguishability chain "
               "δ_R→asymmetry→temporal order→discrete clock→discrete-floor]",
    ),
    GlossEntry(
        world_term="measurement confidence / how sure is this claim",
        our_term="two-axis tier certificate (structure_tier × value_tier) on every Result",
        definition=("Every output of the engine is stamped with a structure tier (Th_coqc machine-checked "
                     "axiom-free / +reals / Dr design-narrative / Open honestly unsolved) and a value tier "
                     "(exact_Q / finite_diagnostic / open); a value is never returned without its tier, and "
                     "value=None is enforced to coincide exactly with structure_tier=='Open'."),
        tier="Th_coqc",
        aliases=("how sure is this claim", "measurement confidence"),
        source="engine/universe.py:60-114 (class Result, __post_init__ tier invariant), "
               "docs/GENESIS_DEEP.md:12 (tier legend)",
    ),
    GlossEntry(
        world_term="unsolved problem / open research question",
        our_term="[Open] readout, value=None, OPEN_GATES key",
        definition=("A problem the framework refuses to fabricate an answer for; the API returns "
                     "Result(value=None, structure_tier='Open') tagged with a named OPEN_GATES key describing "
                     "exactly what is missing (e.g. 'particle_graph', 'gauge_group') — an honest refusal, "
                     "not a failure."),
        tier="Open",
        aliases=("open research question",),
        source="engine/universe.py:50-58 (OPEN_GATES dict), :150-152 (_open helper)",
    ),
    GlossEntry(
        world_term="physical constant",
        our_term="OPEN_CONSTANTS / relational readout / RG fixed point",
        definition=("So-called fundamental constants are not free inputs but RELATIONAL readouts of the "
                     "spine's self-consistency (readout/RG) flow — α runs, mass ratios are spectral-gap "
                     "ratios; their absolute IR values are [Open], never fabricated, and constant() always "
                     "returns an [Open] Result for any name in OPEN_CONSTANTS."),
        tier="Open",
        aliases=("fine-structure constant", "fine structure constant", "particle masses"),
        source="engine/universe.py:389-400 (OPEN_CONSTANTS dict, constant()); "
               "docs/OPEN_PROBLEM_HYPOTHESES.md H2 lines 25-34",
    ),
    GlossEntry(
        world_term="space / geometry",
        our_term="the shape of the retained-information form (⟨x,L_R x⟩ as a metric)",
        definition=("Space is not a stage things live in; it is the SHAPE that the bilinear information form "
                     "takes — geometry (Christoffel symbols, Riemann curvature, Bianchi identities) is read "
                     "off the discrete information graph via summation-by-parts, not an arena the graph lives "
                     "inside."),
        tier="Th_coqc",
        aliases=("geometry",),
        source="docs/GENESIS_DEEP.md:148-158 (Tick 5) [Th_coqc: InfoChristoffel.christoffel_lower_symmetric, "
               "metric_compatibility, riemann_antisym_last_pair, first_bianchi]",
    ),
    GlossEntry(
        world_term="gravity",
        our_term="R5 / R7_CURVATURE readout, geometry responding to memory",
        definition=("Gravity is memory curving its own geometry: the Einstein tensor algebra, the 8π factor "
                     "(=2×4π from the Green coefficient), and 8πG emerging from entropy=information via "
                     "Clausius+Unruh are all derived from the one spine — gravity is thermodynamics of "
                     "retained information, not an independent force."),
        tier="Th_coqc",
        source="docs/GENESIS_DEEP.md:176-188 (Tick 7) [Th_coqc: InfoEinsteinEntropy.einstein_factor_from_green, "
               "InfoJacobson.jacobson_8piG_emerges]; engine/universe.py:164,230-234 "
               "(Readout.R7_CURVATURE, currently gated Open in code)",
    ),
    GlossEntry(
        world_term="quantum state / wavefunction evolution",
        our_term="R4_EVOLVE readout, exp(−iLt) unitary branch of the spine",
        definition=("A quantum state is the under-damped (looping) reading of the one spine on the "
                     "oscillatory side of the λ_c threshold; evolution is exp(−iLt) applied via the "
                     "eigendecomposition of L_R, unitary because energy/information is conserved on that "
                     "branch. A CLOSED (periodic) orbit under this evolution — one that returns exactly to "
                     "its own starting readout after finitely many discrete steps — is a root-of-unity "
                     "closure of this same branch, not a separate concept: the crystallographic periods "
                     "already machine-checked here are period 4 (InfoModeRotation_attempt.v's "
                     "step2_period4), period 6 (step1_period6), and period 3 (step3_cubes_to_identity)."),
        tier="Th_coqc",
        aliases=("wavefunction evolution", "orbit", "periodic orbit", "closed orbit"),
        source="docs/GENESIS_DEEP.md:162-172 (Tick 6) [Th_coqc: InfoSchrodinger.spine_mode_dispersion, "
               "InfoDynamics.unitary_preserves_norm]; engine/universe.py:161,217-226 (Readout.R4_EVOLVE); "
               "formal/InfoModeRotation_attempt.v (step2_period4, step1_period6, step3_cubes_to_identity); "
               "causal-quantum-gravity/SUPPLEMENT.md SS12 item 13 postscript (orbit = closed special case "
               "of this entry, not a new coinage)",
    ),
    GlossEntry(
        world_term="probability",
        our_term="energy/information fraction, R1_PSD non-negativity",
        definition=("The Born weight |ψ|² is not a separate axiom; because R0 already says information IS "
                     "the quadratic form, the Born probability is the energy/information fraction "
                     "pᵢ=|ψᵢ|²/Σ|ψⱼ|² — the positive-characterization half of Gleason's theorem, "
                     "machine-checked; full measure-theoretic uniqueness stays Open."),
        tier="Th_coqc",
        aliases=("born rule",),
        source="docs/GENESIS_DEEP.md:168 [Th_coqc: InfoDeepClosings.born_is_energy_fraction]; "
               "docs/TOE_CANDIDACY_ROADMAP.md:56-61 (Gleason remainder marked Open)",
    ),
    GlossEntry(
        world_term="conservation law",
        our_term="dE/dt = −D·v² ≤ 0 (monotone descent), cascade_transfer skew-symmetry",
        definition=("The spine's law of motion is that retained information never increases: energy is "
                     "monotonically non-increasing (the arrow and the second law as one fact), and "
                     "cross-domain transfers conserve the total via a skew-symmetric coupling "
                     "⟨u,B_sk u⟩ = 0."),
        tier="Th_coqc",
        aliases=("energy conservation", "second law"),
        source="docs/GENESIS_DEEP.md:112 [Th_coqc: InfoFrontier.spine_energy_nonincreasing]; "
               "engine/universe.py:299-317 (cascade_transfer, InfoCascade.cascade_conserves_energy)",
    ),
    GlossEntry(
        world_term="atomicity",
        our_term="ℓ₀ (minimal cell), ℏ and ℓ_P as readouts of the atomic floor",
        definition=("Retention cannot be infinitely fine — there is a smallest keepable distinction ℓ₀; "
                     "the Planck constant ℏ and Planck length ℓ_P both drop out as costumes of this one "
                     "atomic floor, not independent quanta."),
        tier="Th_coqc",
        aliases=("planck scale", "smallest unit of nature"),
        source="docs/GENESIS_DEEP.md:80-91 (Tick 1) [Th_coqc: InfoActionQuantum.hbar_from_minimal_cell, "
               "InfoPlanckRel.ell0_is_planck]",
    ),
    GlossEntry(
        world_term="measurement / observation output",
        our_term="readout (R0–R7 enum, Readout class)",
        definition=("A 'readout' is any of the eight defined lenses (R0 energy, R1 positive-semidefiniteness, "
                     "R2 spectrum, R3 fixed-point/equilibrium, R4 evolution, R5 Lorentzian box □, R6 "
                     "kernel/constants, R7 curvature) through which the one memory graph is read; physics "
                     "domains (QM, GR, etc.) are specific readouts, not separate substances."),
        tier="Th_coqc",
        aliases=("observation output",),
        source="engine/universe.py:156-164 (class Readout, R0_ENERGY..R7_CURVATURE)",
    ),
    GlossEntry(
        world_term="physical law / master equation",
        our_term="the spine: M∂²Φ + D∂Φ + K·L_R Φ + ∇V(Φ) = J − η",
        definition=("There is exactly one master equation ('the spine') and every regime of physics "
                     "(classical, quantum, GR, biology, chemistry, economics...) is that same equation read "
                     "in a different basis; M/D/K/V are readout artifacts of one information unit, not "
                     "independently dimensionful."),
        tier="Th_coqc",
        aliases=("master equation",),
        source="docs/GENESIS_DEEP.md:101-119 (Tick 2); engine/universe.py:264-268 (class Spine)",
    ),
    GlossEntry(
        world_term="AI agency / intelligent behavior",
        our_term="agency-like = bounded-info spine in the looping (under-damped) regime",
        definition=("Agency (and agency-like behavior in an AI or a black hole) is modeled as a "
                     "bounded-information spine sitting in the quantum/looping (under-damped) regime past "
                     "λ_c; this is explicitly marked as a design analogy, not a certified identity."),
        tier="Dr",
        aliases=("intelligent behavior",),
        source="engine/universe.py:332-340 (function agency, diagnostic note "
               "'agency≈bounded-info spine (Dr analogy: BH/AI), not a certified identity')",
    ),
    GlossEntry(
        world_term="unified field theory / theory of everything",
        our_term="candidate framework, pre-candidate ToE-bar status",
        definition=("The repo explicitly refuses the label 'Theory of Everything'; it claims only 'a "
                     "candidate framework whose structure is machine-verified and whose every claim is "
                     "tier-disclosed,' and self-assesses as pre-candidate against an 8-point ToE bar (SM "
                     "reproduction, GR, QG, quantitative CODATA agreement, novel prediction, consistency, "
                     "fewer free parameters, background independence)."),
        tier="Dr",
        aliases=("theory of everything",),
        source="docs/TOE_CANDIDACY_ROADMAP.md:1-23 (the bar table, 'We are pre-candidate')",
    ),
    GlossEntry(
        world_term="claim / research finding",
        our_term="finite_diagnostic default tier (CLAIM_BOUNDARY.md)",
        definition=("By default every output of this repo carries claim tier 'finite_diagnostic' — e.g. "
                     "'the spine solver achieves observed convergence order ~X against analytic oracle Y' — "
                     "and forbidden claims (solved GUT/QG, universal truth, production-ready) are explicitly "
                     "firewalled off."),
        tier="Dr",
        aliases=("research finding",),
        source="CLAIM_BOUNDARY.md:1-16",
    ),
    GlossEntry(
        world_term="isometry (of a step map)",
        our_term="info-preserving step, rot_is_isometry",
        definition=("A step map is an isometry when it exactly preserves info(x,y):=x²+y² — the same "
                     "quantity this project's R0_ENERGY entry already calls energy — with no limit taken: "
                     "the i-rotation rot(x,y)=(y,−x) at the mother equation's stability-window center is one "
                     "such step (a one-line ring identity, info(rot(x,y)) == info(x,y), Th_coqc). "
                     "[Dr-tier reading, not itself machine-checked]: this is read as what forces a closed "
                     "orbit's classical action to lock to a fixed multiple of its own info value — an "
                     "isometric step confines every orbit point to one circle (one info level), so the "
                     "phase-space area the orbit encloses has only that one radius to depend on; a "
                     "non-isometric step (the a=1,3 window points) visits different info values and this "
                     "lock breaks. The 'action = enclosed phase-space area' identification and the "
                     "3-orbit example check are not themselves proven as a general Coq theorem here."),
        tier="Th_coqc",
        aliases=("info-preserving step", "energy-conserving automorphism"),
        source="formal/InfoShiftAverage_attempt.v (rot_is_isometry, this branch); "
               "causal-quantum-gravity/SUPPLEMENT.md SS12 item 13 postscript (action=2·info reasoning, "
               "scripts/probe_action_glossary_generalization.py)",
    ),
    GlossEntry(
        world_term="constant-info level-set",
        our_term="orbit_constant_info (finite set of rational points, not a curve)",
        definition=("NOT a continuum 'curve' — that would inject I1 (ℝ-completeness), a non-readout this "
                     "project's philosophy refuses. The honest readout is a FINITE set of discrete rational "
                     "points that all share one exact info(x,y) value: the period-4 i-rotation orbit's four "
                     "points (x,y), rot(x,y), rot(rot(x,y)), rot(rot(rot(x,y))) all evaluate info identically "
                     "(a one-line ring identity, no epsilon, no limit) because each step is the isometry "
                     "above — only these four points are asserted, nothing about points 'between' them."),
        tier="Th_coqc",
        aliases=("constant-energy level set", "info level set"),
        source="formal/InfoShiftAverage_attempt.v (orbit_constant_info); "
               "docs/root/INFINITY_INJECTION_DIAGNOSIS.md (I1 ℝ-completeness refusal); "
               "causal-quantum-gravity/SUPPLEMENT.md SS12 item 13 postscript (four sample points on one "
               "circle, info=541/196)",
    ),
)


def _head(our_term: str) -> str:
    """our_term stripped of its trailing parenthetical, e.g. 'δ_R (retained difference)' -> 'δ_R'."""
    return re.sub(r"\s*\([^)]*\)\s*$", "", our_term).strip()


def _build_indexes():
    world_to_entry: dict = {}
    our_to_entry: dict = {}

    def _put(idx: dict, key: str, entry: GlossEntry):
        key = key.strip().lower()
        if not key:
            return
        existing = idx.get(key)
        if existing is not None and existing is not entry:
            raise ValueError(
                f"lexicon collision: {key!r} maps to both {existing.world_term!r} and {entry.world_term!r}")
        idx[key] = entry

    for entry in GLOSSARY:
        _put(world_to_entry, entry.world_term, entry)
        for alias in entry.aliases:
            _put(world_to_entry, alias, entry)
        _put(our_to_entry, entry.our_term, entry)
        head = _head(entry.our_term)
        if head != entry.our_term:
            _put(our_to_entry, head, entry)
    return world_to_entry, our_to_entry


_WORLD_TO_ENTRY, _OUR_TO_ENTRY = _build_indexes()


def _compile_pattern(terms) -> "re.Pattern | None":
    """one alternation regex over `terms`, longest-first, with lookaround boundaries that stay safe for
    symbol-containing terms (a plain \\b fails on non-word characters like α, ℓ₀, τ_c)."""
    ordered = sorted(set(terms), key=len, reverse=True)
    if not ordered:
        return None
    alt = "|".join(re.escape(t) for t in ordered)
    return re.compile(rf"(?<!\w)(?:{alt})(?!\w)", re.IGNORECASE)


_WORLD_PATTERN = _compile_pattern(_WORLD_TO_ENTRY.keys())
_OUR_PATTERN = _compile_pattern(_OUR_TO_ENTRY.keys())


def translate_to_philosophy(text: str) -> str:
    """deterministic, case-insensitive, longest-match-first substitution of recognized world terms/aliases
    with "our_term (definition) [tier]"; unmatched text passes through unchanged, INCLUDING text inside
    the original input's own parentheses/brackets (an ordinary parenthetical aside is not special-cased —
    only this function's own prior output is). Idempotent: a span that already looks like one of THIS
    function's own annotations ("our_term (definition) [tier]" for a matching GLOSSARY entry) is recognized
    by _match_existing_annotation and skipped whole (including its internal parens), so re-running on
    already-translated text is a no-op without needing any generic paren/bracket-depth tracking."""
    if not text or _WORLD_PATTERN is None:
        return text
    out = []
    i, n = 0, len(text)
    while i < n:
        already = _match_existing_annotation(text, i)
        if already:
            out.append(text[i:already])
            i = already
            continue
        m = _WORLD_PATTERN.match(text, i)
        if m:
            entry = _WORLD_TO_ENTRY[m.group(0).lower()]
            out.append(f"{entry.our_term} ({entry.definition}) [{entry.tier}]")
            i = m.end()
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def _match_existing_annotation(text: str, i: int) -> "int | None":
    """if `text[i:]` starts with one of THIS module's own "our_term (definition) [tier]" annotations
    (as produced by translate_to_philosophy for some GLOSSARY entry), return the end index of that whole
    span; else None. Used to make translate_to_philosophy idempotent even when a GlossEntry.definition
    contains other GLOSSARY world_terms as plain English words."""
    if _OUR_PATTERN is None:
        return None
    m = _OUR_PATTERN.match(text, i)
    if not m:
        return None
    entry = _OUR_TO_ENTRY[m.group(0).lower()]
    tail = f" ({entry.definition}) [{entry.tier}]"
    end = m.end()
    if text[end:end + len(tail)] == tail:
        return end + len(tail)
    return None


def _match_existing_world_annotation(text: str, i: int) -> "int | None":
    """if `text[i:]` starts with one of translate_to_world's own "world_term (definition)" annotations,
    return the end index of that whole span; else None. Mirrors _match_existing_annotation so
    translate_to_world stays idempotent even when a GlossEntry.definition contains other GLOSSARY
    our_term/head-form text as plain English words."""
    if _WORLD_PATTERN is None:
        return None
    m = _WORLD_PATTERN.match(text, i)
    if not m:
        return None
    entry = _WORLD_TO_ENTRY[m.group(0).lower()]
    tail = f" ({entry.definition})"
    end = m.end()
    if text[end:end + len(tail)] == tail:
        return end + len(tail)
    return None


def translate_to_world(text: str) -> str:
    """reverse substitution: our_term (or its head form) -> "world_term (definition)", optionally consuming
    an already-attached "(...) [...]" annotation produced by translate_to_philosophy for that same entry.
    Unmatched text (including the original input's own parentheses/brackets) passes through unchanged —
    an ordinary parenthetical aside is not special-cased. Idempotent: a span that already looks like this
    function's own "world_term (definition)" output is recognized by _match_existing_world_annotation and
    skipped whole, without needing any generic paren/bracket-depth tracking."""
    if not text or _OUR_PATTERN is None:
        return text
    out = []
    i, n = 0, len(text)
    while i < n:
        already = _match_existing_world_annotation(text, i)
        if already:
            out.append(text[i:already])
            i = already
            continue
        m = _OUR_PATTERN.match(text, i)
        if m:
            entry = _OUR_TO_ENTRY[m.group(0).lower()]
            j = m.end()
            annotation = f" ({entry.definition}) [{entry.tier}]"
            if text[j:j + len(annotation)] == annotation:
                j += len(annotation)
            out.append(f"{entry.world_term} ({entry.definition})")
            i = j
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


# ───────────────────────── OPEN_CONSTANTS stance table ─────────────────────────
def _stance(const_id: str, world_gloss: str, our_stance: str) -> dict:
    gate = OPEN_CONSTANTS[const_id]        # KeyError fails loud on drift between lexicon.py and universe.py
    reason = OPEN_GATES[gate]
    # reuse engine.universe._open()'s canonical [Open]-Result construction (same triple used 8+ times
    # in universe.py) rather than duplicating it, then attach the const_id as diagnostic.
    result = dataclasses.replace(_open(gate), diagnostic=(const_id,))
    return {"gate": gate, "world_gloss": world_gloss, "our_stance": our_stance,
            "reason": reason, "result": result}


OPEN_PROBLEM_STANCE: dict = {
    "alpha": _stance(
        "alpha",
        "The fine-structure constant α ≈ 1/137 is treated in physics orthodoxy as a fundamental "
        "dimensionless coupling constant of the electromagnetic interaction, measured to extreme precision "
        "but with no accepted first-principles derivation of its value.",
        "H2: there is no scale-free constant to derive — α RUNS (confirmed via scipy RG flow, "
        "alpha_running_relational.py, 1/137 → ~1/134 at M_Z), and its IR value is hypothesized to be a "
        "FIXED POINT of the spine's self-consistency/RG flow (the same way φ is the fixed point of "
        "x²=x+1, InfoInvariant.golden_is_readout_invariant), with mass ratios = τ_c ratios = spectral-gap "
        "ratios of nonlinear ∇V solitons. The closing condition (deriving the spine β-function and solving "
        "its IR fixed point; computing the nonlinear soliton spectrum) is NOT done — explicitly [Open] "
        "open-research, and the naive particle-graph approach is already falsified for simple graphs "
        "(scripts/falsify_particle_graph.py).",
    ),
    "mass": _stance(
        "mass",
        "Standard Model orthodoxy takes particle rest masses as free parameters fixed by the Higgs Yukawa "
        "couplings, measured experimentally (PDG/CODATA) with no derivation of the specific numerical "
        "values from first principles.",
        "The framework derives the STRUCTURAL relation mass = ℏ/(2τ_c c²) (memory-before-mass duality, "
        "machine-checked Th_coqc) and that mass ratios equal spectral-gap ratios of L_R (relational, "
        "proven). But which graph/mode a given physical particle actually IS — the particle→mode mapping "
        "needed to get an absolute mass — is genuinely open: tested against scipy/networkx simple linear "
        "graphs and failed 80-99% with no fitted graphs allowed; the nonlinear ∇V soliton spectrum is only "
        "a proposed [Dr] route, not a result. Memory.mass() in code always returns [Open] unless a "
        "measurement-sourced τ_c is supplied externally (e.g. from TAU_C_DB, itself PDG-measured input, "
        "not derived).",
    ),
    "mixing": _stance(
        "mixing",
        "The CKM/PMNS quark and neutrino mixing angles are additional free parameters of the Standard "
        "Model, measured but not derived from any deeper symmetry principle.",
        "Grouped under the same H2 hypothesis as α: mixing is proposed to be a relational readout "
        "(mixing = overlap, per InfoRelational's mass ratio = τc ratio = spectral-gap ratio machinery) "
        "whose specific numeric values remain [Open]; no closed derivation of mixing angles is claimed or "
        "attempted beyond this structural analogy.",
    ),
    "generations": _stance(
        "generations",
        "The Standard Model has exactly three generations (families) of fermions; physics has no accepted "
        "derivation of why the count is 3 rather than some other number — it is an empirical input.",
        "H4 (explicitly flagged as 'honestly the weakest hypothesis'): the three generations are "
        "hypothesized to be the three independent readout-modes of the atomicity cell across the causal "
        "order — one per irreducible RD facet (① structure L_R, ② asymmetry ≺, ④ discreteness/atomicity) "
        "— with three being the minimum count that supports a physical CP-violating phase (CKM phase "
        "needs ≥3). The closing condition (proving exactly three modes survive, tying the CKM phase to "
        "causal order) is not met; anomaly cancellation is checked per-generation but does not itself "
        "force the count.",
    ),
    "gauge_group": _stance(
        "gauge_group",
        "The Standard Model gauge group SU(3)×SU(2)×U(1) is taken as given/discovered empirically; "
        "deriving why nature picked exactly this group (and not some other simple group) from first "
        "principles is an open problem in unification physics (cf. GUTs like SU(5), SO(10)).",
        "H1: gauge symmetry is hypothesized as readout-invariance made local — U(1) = phase preserving "
        "|ψ|² (information), SU(2) = rotation of the binary distinction's two retained states, SU(3) = "
        "minimal non-abelian closure over the three RD facets / colour-triality. Only the U(1) piece is "
        "machine-checked (InfoHypothesisSeeds.u1_group_closure + InfoComplex.unitary_preserves_norm: "
        "information-preserving phases close under multiplication and form U(1)). Deriving SU(2) and "
        "SU(3) as automorphism groups of the atomicity cell, and excluding other simple factors, remains "
        "explicitly [Dr]/[Open] — not solved.",
    ),
    "nonperturbative_qg": _stance(
        "nonperturbative_qg",
        "Constructing a consistent, finite, non-perturbative quantum theory of gravity (unifying quantum "
        "mechanics and general relativity beyond perturbative graviton exchange) is one of the deepest "
        "open problems in theoretical physics, pursued by string theory, loop quantum gravity, and other "
        "programs with no consensus solution.",
        "H3: hypothesized to be finite because atomicity provides a built-in UV cutoff — the discrete "
        "floor bounds the spectrum (λ≤Λ) so there is no λ→∞ divergence, machine-checked as a seed "
        "(InfoHypothesisSeeds.energy_uv_bounded, InfoTauFloor.discrete_rate_ceiling) plus the already-"
        "quantized perturbative graviton (InfoGraviton). But the actual closing condition — defining the "
        "measure on graph configurations, proving the path-integral sum converges, and recovering "
        "continuum Einstein dynamics in the IR — is not done. Only co-instantiation/consistency "
        "(InfoQuantumGravity.qg_unification: quantum R4 and GR R5 readouts compose without contradiction "
        "on the shared spine) is proved, explicitly NOT a dynamical quantum=GR claim. Full "
        "non-perturbative QG stays genuinely [Open].",
    ),
    "hierarchy_lambda": _stance(
        "hierarchy_lambda",
        "The mass hierarchy problem (why fermion/boson masses span many orders of magnitude without "
        "fine-tuning) and the cosmological constant problem (why the observed vacuum energy/Λ is ~10^120 "
        "times smaller than naive QFT estimates) are among the most cited unsolved puzzles in particle "
        "physics and cosmology.",
        "H5: hypothesized that the mass hierarchy is the exponential of the τ_c-scale span (modest "
        "action/coupling differences becoming many-order mass ratios via instanton/RG-like structure, cf. "
        "InfoSoliton's exponential separation) — so no fine-tuning is needed, the hierarchy is structural. "
        "Λ is hypothesized as the residual mean damping of a universe still relaxing its kept differences "
        "(dark energy as Ė≤0 equilibrium, InfoCosmoEquilibrium.spine_equilibrium_iff_rest), with its "
        "smallness explained as the deep-IR floor of the spine. The seeds (Ė≤0, soliton exponential "
        "structure) are machine-checked, but the closing condition — actually computing the IR damping "
        "floor to match the observed Λ, and deriving the exponential span from the root — is not done; "
        "explicitly [Dr]/[Open].",
    ),
}

# explicit raise (NOT assert — assert is disabled under python -O, which would silently void this
# drift guard; matches the same discipline engine.universe.Result.__post_init__ documents for its
# own honesty-invariant checks).
if set(OPEN_PROBLEM_STANCE) != set(OPEN_CONSTANTS):
    raise ValueError(
        f"OPEN_PROBLEM_STANCE drift: {set(OPEN_PROBLEM_STANCE) ^ set(OPEN_CONSTANTS)}")


def stance_for(name: str) -> dict:
    """our interpretation of an OPEN_CONSTANTS id — raises UnknownConstant for unknown names (identical
    exception type/message convention to engine.universe.constant)."""
    stance = OPEN_PROBLEM_STANCE.get(name)
    if stance is None:
        raise UnknownConstant(f"unknown constant {name!r}; known: {sorted(OPEN_PROBLEM_STANCE)}")
    return stance
