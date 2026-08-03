from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Iterator


class Tier(str, Enum):
    AX = "Ax"
    TH = "Th"
    TH_COQC = "Th_coqc"
    EXACT_ALGEBRA = "exact_algebra"
    FINITE_DIAGNOSTIC = "finite_diagnostic"
    DR = "Dr"
    OPEN = "Open"
    DEFINITION = "definition"


# NOT the same vocabulary as omega.schemas.VERDICT_CLASSES -- must never be
# conflated (Cross-Role Readout Contamination; see
# EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md's EQ-065
# note on two same-named-but-differently-derived quantities for this
# repo's house pattern for this class of warning).
#
# This Verdict is the RAR proof kernel's outcome for ONE proof attempt
# against a single ClaimIR (Gamma, phi) -- it answers "what did
# native_logic.kernel.solve_claim() conclude about this target atom,
# having run the eight RAR gates and the rule chain". It is produced only
# by solve_claim()/failure_proof() in this module.
#
# omega.schemas.VERDICT_CLASSES ("DERIVED", "FORCED", "DEFINITIONAL-RELABEL",
# "POSITED", "BORROWED-SCALE", "OPEN") is the Omega_all translation runner's
# BRIDGE-CLASS taxonomy for a translated term/claim (POSITION.md §3 item 2)
# -- it classifies how a foreign term was imported across the translation
# boundary, before any RAR proof kernel run even starts.
#
# The two enumerations happen to share the literal strings "DERIVED" and
# "OPEN", but a shared string here does NOT mean a shared meaning: a
# VERDICT_CLASSES value of "OPEN" describes an untranslated/unbridged term,
# while a Verdict.OPEN here describes a fully-formed ClaimIR whose gates all
# passed but whose rule chain never reached the target. Comparing or
# substituting one for the other across the omega <-> native_logic boundary
# would silently launder a translation-bridge classification into a proof
# verdict (or vice versa). No declared mapping between them exists, and none
# should be added without a named, reviewed bridge function -- see
# native_logic/from_omega.py, which deliberately carries omega bridge_class
# values through as an opaque string (folded into Fact.source /
# TranslationTerm.bridge_class) rather than ever comparing them against this
# Verdict enum.
class Verdict(str, Enum):
    DERIVED = "DERIVED"
    SUPPORTED_AS_DR = "SUPPORTED_AS_DR"
    UNDERDETERMINED = "UNDERDETERMINED"
    OBSTRUCTED = "OBSTRUCTED"
    DISSOLVED = "DISSOLVED"
    OPEN = "OPEN"


class GateStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"


@dataclass(frozen=True)
class Atom:
    predicate: str
    arguments: tuple[str, ...] = ()
    negated: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Atom":
        return cls(
            predicate=str(data["predicate"]),
            arguments=tuple(str(x) for x in data.get("arguments", [])),
            negated=bool(data.get("negated", False)),
        )

    def instantiate(self, substitution: dict[str, str]) -> "Atom":
        return Atom(
            predicate=self.predicate,
            arguments=tuple(substitution.get(x, x) for x in self.arguments),
            negated=self.negated,
        )

    def opposite(self) -> "Atom":
        return Atom(
            predicate=self.predicate,
            arguments=self.arguments,
            negated=not self.negated,
        )

    def key(self) -> str:
        sign = "¬" if self.negated else ""
        args = ",".join(self.arguments)
        return f"{sign}{self.predicate}({args})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "predicate": self.predicate,
            "arguments": list(self.arguments),
            "negated": self.negated,
        }


@dataclass
class Fact:
    atom: Atom
    tier: Tier
    source: str
    formal_closed: bool = False
    load_bearing: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Fact":
        return cls(
            atom=Atom.from_dict(data["atom"]),
            tier=Tier(data["tier"]),
            source=str(data["source"]),
            formal_closed=bool(data.get("formal_closed", False)),
            load_bearing=bool(data.get("load_bearing", True)),
        )


@dataclass
class Rule:
    rule_id: str
    antecedents: tuple[Atom, ...]
    consequent: Atom
    tier: Tier
    source: str
    formal_closed: bool = False
    load_bearing: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Rule":
        return cls(
            rule_id=str(data["id"]),
            antecedents=tuple(
                Atom.from_dict(x) for x in data.get("antecedents", [])
            ),
            consequent=Atom.from_dict(data["consequent"]),
            tier=Tier(data["tier"]),
            source=str(data["source"]),
            formal_closed=bool(data.get("formal_closed", False)),
            load_bearing=bool(data.get("load_bearing", True)),
        )


@dataclass
class TranslationTerm:
    foreign_term: str
    native_term: str
    tier: Tier
    bridge_class: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TranslationTerm":
        return cls(
            foreign_term=str(data["foreign_term"]),
            native_term=str(data["native_term"]),
            tier=Tier(data["tier"]),
            bridge_class=str(data["bridge_class"]),
        )


@dataclass
class GateContext:
    candidate_distinctions: list[str] = field(default_factory=list)

    grammar_compatible: bool = False

    required_retained: list[str] = field(default_factory=list)
    retained: list[str] = field(default_factory=list)

    required_accessible: list[str] = field(default_factory=list)
    accessible: list[str] = field(default_factory=list)

    metric_nonnegative: bool = False
    identity_lock_ok: bool = False
    declared_obstruction: bool = False

    lens_ok: bool = False
    lens_distortion: float = 1.0
    lens_tolerance: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GateContext":
        return cls(
            candidate_distinctions=list(data.get("candidate_distinctions", [])),
            grammar_compatible=bool(data.get("grammar_compatible", False)),
            required_retained=list(data.get("required_retained", [])),
            retained=list(data.get("retained", [])),
            required_accessible=list(data.get("required_accessible", [])),
            accessible=list(data.get("accessible", [])),
            metric_nonnegative=bool(data.get("metric_nonnegative", False)),
            identity_lock_ok=bool(data.get("identity_lock_ok", False)),
            declared_obstruction=bool(
                data.get("declared_obstruction", False)
            ),
            lens_ok=bool(data.get("lens_ok", False)),
            lens_distortion=float(data.get("lens_distortion", 1.0)),
            lens_tolerance=float(data.get("lens_tolerance", 0.0)),
        )


@dataclass(frozen=True)
class GateSpec:
    gate_id: str
    name: str
    positive_control: str
    negative_control: str
    tier: Tier = Tier.DR

    @property
    def type_p(self) -> bool:
        return bool(self.positive_control and self.negative_control)


# RAR A1-A8 are declared philosophical bridges, not machine-checked
# formal steps (see the comment in solve_claim). No matter how
# strongly-tiered the underlying rule chain is, a conclusion reached
# only through these bridges may never be certified above this tier.
# This is an explicit, named ceiling -- not an accident of
# GateSpec.tier's Tier.DR default -- so it stays visible and testable
# rather than silently falling out of cap_tier's branch order.
RAR_BRIDGE_CEILING_TIER: Tier = Tier.DR


GATE_SPECS: tuple[GateSpec, ...] = (
    GateSpec(
        "RAR-A1",
        "Distinguishability",
        "PC-A1-two-distinct-candidates",
        "NC-A1-identical-candidates",
    ),
    GateSpec(
        "RAR-A2",
        "Admissible transport",
        "PC-A2-compatible-types",
        "NC-A2-incompatible-types",
    ),
    GateSpec(
        "RAR-A3",
        "Retention",
        "PC-A3-required-record-retained",
        "NC-A3-required-record-forgotten",
    ),
    GateSpec(
        "RAR-A4",
        "Accessibility",
        "PC-A4-required-record-accessible",
        "NC-A4-existing-but-inaccessible",
    ),
    GateSpec(
        "RAR-A5",
        "Admissible comparison",
        "PC-A5-nonnegative-metric",
        "NC-A5-negative-comparison-metric",
    ),
    GateSpec(
        "RAR-A6",
        "Identity locking",
        "PC-A6-identity-preserved",
        "NC-A6-entity-swapped-mid-proof",
    ),
    GateSpec(
        "RAR-A7",
        "Obstruction",
        "PC-A7-no-contradictory-facts",
        "NC-A7-fact-and-negation",
    ),
    GateSpec(
        "RAR-A8",
        "Non-distorting lens",
        "PC-A8-distortion-under-tolerance",
        "NC-A8-distortion-over-tolerance",
    ),
)


@dataclass
class GateResult:
    gate_id: str
    name: str
    status: GateStatus
    evidence: list[str]
    positive_control: str
    negative_control: str
    type_p: bool
    failure_verdict: Verdict | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate": self.gate_id,
            "name": self.name,
            "status": self.status.value,
            "evidence": self.evidence,
            "positive_control": self.positive_control,
            "negative_control": self.negative_control,
            "type": "P" if self.type_p else "U",
            "failure_verdict": (
                self.failure_verdict.value
                if self.failure_verdict is not None
                else None
            ),
        }


@dataclass
class ClaimIR:
    claim_id: str
    question: str
    scope: str

    translation: list[TranslationTerm]
    ontology_generable: bool

    premises: list[Fact]
    rules: list[Rule]
    target: Atom

    context: GateContext
    falsifier: str
    not_checked: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClaimIR":
        return cls(
            claim_id=str(data["claim_id"]),
            question=str(data["question"]),
            scope=str(data["scope"]),
            translation=[
                TranslationTerm.from_dict(x)
                for x in data.get("translation", [])
            ],
            ontology_generable=bool(data.get("ontology_generable", False)),
            premises=[
                Fact.from_dict(x) for x in data.get("premises", [])
            ],
            rules=[
                Rule.from_dict(x) for x in data.get("rules", [])
            ],
            target=Atom.from_dict(data["target"]),
            context=GateContext.from_dict(data.get("context", {})),
            falsifier=str(data.get("falsifier", "")),
            not_checked=list(data.get("not_checked", [])),
        )


@dataclass
class ProofNode:
    atom: Atom
    tier: Tier
    source: str
    formal_closed: bool

    via_rule: str | None = None
    parents: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "atom": self.atom.to_dict(),
            "statement": self.atom.key(),
            "tier": self.tier.value,
            "source": self.source,
            "formal_closed": self.formal_closed,
            "via_rule": self.via_rule,
            "parents": list(self.parents),
        }


@dataclass
class ProofObject:
    claim_id: str
    question: str
    verdict: Verdict
    tier: Tier

    target: Atom
    derived: bool

    gates: list[GateResult]
    trace: list[ProofNode]

    falsifier: str
    not_checked: list[str]
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "question": self.question,
            "verdict": self.verdict.value,
            "tier": self.tier.value,
            "target": self.target.to_dict(),
            "derived": self.derived,
            "gates": [x.to_dict() for x in self.gates],
            "proof_trace": [x.to_dict() for x in self.trace],
            "falsifier": self.falsifier,
            "not_checked": self.not_checked,
            "explanation": self.explanation,
        }


class ClaimValidationError(ValueError):
    pass


def validate_claim(claim: ClaimIR) -> None:
    errors: list[str] = []

    if not claim.claim_id.strip():
        errors.append("claim_id is required")

    if not claim.question.strip():
        errors.append("question is required")

    if not claim.scope.strip():
        errors.append("scope is required")

    if not claim.translation:
        errors.append("translation table is required")

    if not claim.falsifier.strip():
        errors.append("falsifier is required")

    if not claim.target.predicate.strip():
        errors.append("target predicate is required")

    rule_ids = [rule.rule_id for rule in claim.rules]
    if len(rule_ids) != len(set(rule_ids)):
        errors.append("rule IDs must be unique")

    for rule in claim.rules:
        antecedent_vars = {
            arg
            for atom in rule.antecedents
            for arg in atom.arguments
            if is_variable(arg)
        }
        consequent_vars = {
            arg
            for arg in rule.consequent.arguments
            if is_variable(arg)
        }
        unbound = sorted(consequent_vars - antecedent_vars)

        if unbound:
            errors.append(
                f"rule {rule.rule_id} consequent references variable(s) "
                f"{unbound} not bound by any antecedent"
            )

    for spec in GATE_SPECS:
        if not spec.type_p:
            errors.append(
                f"{spec.gate_id} is Type-U: positive and negative "
                "controls are both required"
            )

    if errors:
        raise ClaimValidationError("; ".join(errors))


def is_variable(arg: str) -> bool:
    """
    True iff ``arg`` is a unification variable rather than a literal.

    A variable is a single, unescaped leading '?' (e.g. "?a"). A fact
    or pattern argument whose literal value must itself begin with
    '?' cannot be written as-is -- it would be indistinguishable from
    a variable -- so it is escaped by doubling the leading character
    at construction time ("??foo" means the literal "?foo").

    The escaped form ("??foo") is the canonical representation used
    throughout this module -- in facts, in pattern arguments, and in
    bound substitution values alike -- so that comparison, storage,
    and re-instantiation (``Atom.instantiate``) never need to decode
    it: two atoms that were built with the same escaping convention
    compare equal by plain string equality. See ``unescape_literal``
    for recovering the original, human-readable value; it is a
    display-only utility and is never called internally by
    ``atom_unifies`` or ``Atom.instantiate``.
    """
    return arg.startswith("?") and not arg.startswith("??")


def unescape_literal(arg: str) -> str:
    """
    Recover the original literal value from its '??'-escaped form.

    This is a DISPLAY utility only -- for a caller that wants to show
    a matched or bound literal's real value to a human. It is not, and
    must not be, used internally for matching or substitution: the
    escaped form is the canonical representation everywhere data flows
    through this module (facts, patterns, bound substitutions,
    instantiated atoms), so two correctly-escaped values already
    compare equal without decoding. Decoding only at the boundary
    keeps that round-trip symmetric -- decoding mid-pipeline (e.g. at
    bind time) would produce a value that no longer round-trips back
    through ``is_variable``/``Atom.instantiate`` consistently.

    Only meaningful on an argument that is not a variable. A literal
    with no leading '?' at all is returned unchanged.
    """
    if arg.startswith("??"):
        return arg[1:]

    return arg


def cap_tier(
    tiers: Iterable[Tier],
    *,
    formal_closed: bool,
) -> Tier:
    """
    Calculate the strongest tier the conclusion may honestly carry.

    This is deliberately not a simple numeric minimum.
    """
    values = list(tiers)

    if not values:
        return Tier.OPEN

    if Tier.OPEN in values:
        return Tier.OPEN

    if Tier.DR in values:
        return Tier.DR

    if Tier.FINITE_DIAGNOSTIC in values:
        return Tier.FINITE_DIAGNOSTIC

    if Tier.TH in values:
        return Tier.TH

    if Tier.EXACT_ALGEBRA in values:
        return Tier.EXACT_ALGEBRA

    meaningful = [
        tier
        for tier in values
        if tier not in {Tier.AX, Tier.DEFINITION}
    ]

    if formal_closed and (
        Tier.TH_COQC in meaningful
        or not meaningful
    ):
        return Tier.TH_COQC

    if not meaningful:
        return Tier.DEFINITION

    # A purported formal result that is not closed is downgraded.
    return Tier.DR


def atom_unifies(
    pattern: Atom,
    fact: Atom,
    substitution: dict[str, str],
) -> dict[str, str] | None:
    if pattern.predicate != fact.predicate:
        return None

    if pattern.negated != fact.negated:
        return None

    if len(pattern.arguments) != len(fact.arguments):
        return None

    result = dict(substitution)

    for expected, actual in zip(pattern.arguments, fact.arguments):
        if is_variable(expected):
            existing = result.get(expected)

            if existing is not None and existing != actual:
                return None

            result[expected] = actual
            continue

        if expected != actual:
            return None

    return result


def matching_substitutions(
    antecedents: tuple[Atom, ...],
    facts: dict[str, ProofNode],
) -> Iterator[tuple[dict[str, str], tuple[ProofNode, ...]]]:
    fact_nodes = list(facts.values())

    def recurse(
        index: int,
        substitution: dict[str, str],
        selected: list[ProofNode],
    ) -> Iterator[
        tuple[dict[str, str], tuple[ProofNode, ...]]
    ]:
        if index >= len(antecedents):
            yield substitution, tuple(selected)
            return

        pattern = antecedents[index].instantiate(substitution)

        for node in fact_nodes:
            unified = atom_unifies(
                pattern,
                node.atom,
                substitution,
            )

            if unified is None:
                continue

            selected.append(node)
            yield from recurse(index + 1, unified, selected)
            selected.pop()

    yield from recurse(0, {}, [])


def contains_contradiction(nodes: Iterable[ProofNode]) -> bool:
    atoms = {node.atom for node in nodes}
    return any(atom.opposite() in atoms for atom in atoms)


def gate_result(
    spec: GateSpec,
    passed: bool,
    evidence: list[str],
    failure_verdict: Verdict,
) -> GateResult:
    return GateResult(
        gate_id=spec.gate_id,
        name=spec.name,
        status=GateStatus.PASS if passed else GateStatus.FAIL,
        evidence=evidence,
        positive_control=spec.positive_control,
        negative_control=spec.negative_control,
        type_p=spec.type_p,
        failure_verdict=None if passed else failure_verdict,
    )


def run_rar_gates(
    claim: ClaimIR,
    nodes: dict[str, ProofNode],
) -> list[GateResult]:
    c = claim.context
    specs = {spec.gate_id: spec for spec in GATE_SPECS}

    distinct = set(c.candidate_distinctions)

    a1 = gate_result(
        specs["RAR-A1"],
        passed=len(distinct) >= 2,
        evidence=sorted(distinct),
        failure_verdict=Verdict.DISSOLVED,
    )

    a2 = gate_result(
        specs["RAR-A2"],
        passed=c.grammar_compatible,
        evidence=[
            "grammar-compatible"
            if c.grammar_compatible
            else "grammar/type mismatch"
        ],
        failure_verdict=Verdict.OBSTRUCTED,
    )

    missing_retained = sorted(
        set(c.required_retained) - set(c.retained)
    )

    a3 = gate_result(
        specs["RAR-A3"],
        passed=not missing_retained,
        evidence=(
            sorted(c.retained)
            if not missing_retained
            else [f"missing:{x}" for x in missing_retained]
        ),
        failure_verdict=Verdict.UNDERDETERMINED,
    )

    missing_accessible = sorted(
        set(c.required_accessible) - set(c.accessible)
    )

    a4 = gate_result(
        specs["RAR-A4"],
        passed=not missing_accessible,
        evidence=(
            sorted(c.accessible)
            if not missing_accessible
            else [f"inaccessible:{x}" for x in missing_accessible]
        ),
        failure_verdict=Verdict.UNDERDETERMINED,
    )

    a5 = gate_result(
        specs["RAR-A5"],
        passed=c.metric_nonnegative,
        evidence=[
            "metric_nonnegative="
            f"{str(c.metric_nonnegative).lower()}"
        ],
        failure_verdict=Verdict.OBSTRUCTED,
    )

    a6 = gate_result(
        specs["RAR-A6"],
        passed=c.identity_lock_ok,
        evidence=[
            "identity_lock_ok="
            f"{str(c.identity_lock_ok).lower()}"
        ],
        failure_verdict=Verdict.OBSTRUCTED,
    )

    contradiction = contains_contradiction(nodes.values())

    a7_passed = (
        not c.declared_obstruction
        and not contradiction
    )

    a7_evidence: list[str] = []

    if c.declared_obstruction:
        a7_evidence.append("declared obstruction")

    if contradiction:
        a7_evidence.append("fact and negation both retained")

    if not a7_evidence:
        a7_evidence.append("O(Gamma,phi)=0")

    a7 = gate_result(
        specs["RAR-A7"],
        passed=a7_passed,
        evidence=a7_evidence,
        failure_verdict=Verdict.OBSTRUCTED,
    )

    lens_passed = (
        c.lens_ok
        and c.lens_distortion <= c.lens_tolerance
    )

    a8 = gate_result(
        specs["RAR-A8"],
        passed=lens_passed,
        evidence=[
            f"lens_ok={str(c.lens_ok).lower()}",
            f"distortion={c.lens_distortion}",
            f"tolerance={c.lens_tolerance}",
        ],
        failure_verdict=Verdict.OBSTRUCTED,
    )

    return [a1, a2, a3, a4, a5, a6, a7, a8]


def initial_nodes(claim: ClaimIR) -> dict[str, ProofNode]:
    nodes: dict[str, ProofNode] = {}

    for fact in claim.premises:
        node = ProofNode(
            atom=fact.atom,
            tier=fact.tier,
            source=fact.source,
            formal_closed=fact.formal_closed,
        )
        nodes[node.atom.key()] = node

    return nodes


def forward_chain(
    claim: ClaimIR,
    nodes: dict[str, ProofNode],
    *,
    max_rounds: int = 64,
) -> dict[str, ProofNode]:
    for _ in range(max_rounds):
        changed = False

        for rule in claim.rules:
            for substitution, parents in matching_substitutions(
                rule.antecedents,
                nodes,
            ):
                consequent = rule.consequent.instantiate(
                    substitution
                )
                key = consequent.key()

                if key in nodes:
                    continue

                parent_tiers = [parent.tier for parent in parents]
                parent_closed = all(
                    parent.formal_closed for parent in parents
                )

                formal_closed = (
                    rule.formal_closed
                    and parent_closed
                    and rule.tier
                    not in {
                        Tier.DR,
                        Tier.OPEN,
                        Tier.FINITE_DIAGNOSTIC,
                    }
                )

                conclusion_tier = cap_tier(
                    [*parent_tiers, rule.tier],
                    formal_closed=formal_closed,
                )

                nodes[key] = ProofNode(
                    atom=consequent,
                    tier=conclusion_tier,
                    source=rule.source,
                    formal_closed=formal_closed,
                    via_rule=rule.rule_id,
                    parents=tuple(
                        parent.atom.key()
                        for parent in parents
                    ),
                )

                changed = True

        if not changed:
            break

    return nodes


def proof_trace(
    target_key: str,
    nodes: dict[str, ProofNode],
) -> list[ProofNode]:
    ordered: list[ProofNode] = []
    visited: set[str] = set()

    def visit(key: str) -> None:
        if key in visited:
            return

        visited.add(key)

        node = nodes[key]

        for parent in node.parents:
            visit(parent)

        ordered.append(node)

    visit(target_key)
    return ordered


def failure_proof(
    claim: ClaimIR,
    gates: list[GateResult],
    verdict: Verdict,
    explanation: str,
) -> ProofObject:
    return ProofObject(
        claim_id=claim.claim_id,
        question=claim.question,
        verdict=verdict,
        tier=Tier.DR,
        target=claim.target,
        derived=False,
        gates=gates,
        trace=[],
        falsifier=claim.falsifier,
        not_checked=claim.not_checked,
        explanation=explanation,
    )


def solve_claim(claim: ClaimIR) -> ProofObject:
    validate_claim(claim)

    if not claim.ontology_generable:
        return ProofObject(
            claim_id=claim.claim_id,
            question=claim.question,
            verdict=Verdict.DISSOLVED,
            tier=Tier.DR,
            target=claim.target,
            derived=False,
            gates=[],
            trace=[],
            falsifier=claim.falsifier,
            not_checked=claim.not_checked,
            explanation=(
                "The target depends on a referent that the declared "
                "RD-generated ontology does not admit."
            ),
        )

    nodes = initial_nodes(claim)
    gates = run_rar_gates(claim, nodes)

    for result in gates:
        if result.status == GateStatus.FAIL:
            assert result.failure_verdict is not None

            return failure_proof(
                claim,
                gates,
                result.failure_verdict,
                (
                    f"Inference stopped at {result.gate_id} "
                    f"({result.name}): "
                    f"{'; '.join(result.evidence)}"
                ),
            )

    nodes = forward_chain(claim, nodes)

    # A7 (Obstruction) was checked once above, against the raw
    # premises only, before any rule fired. A rule chain can derive
    # an atom and its negation purely through rules with no
    # contradiction present in the initial premises; if that
    # happens, ex falso quodlibet lets a later rule take both as
    # antecedents and "derive" anything. Re-check the full closure
    # here and refuse to certify past it, exactly as the initial
    # pre-chain A7 gate would have if the contradiction had been a
    # premise.
    if contains_contradiction(nodes.values()):
        specs = {spec.gate_id: spec for spec in GATE_SPECS}
        gates = [
            gate_result(
                specs["RAR-A7"],
                passed=False,
                evidence=[
                    "fact and negation both retained "
                    "(derived via rule chain, not a raw premise)"
                ],
                failure_verdict=Verdict.OBSTRUCTED,
            )
            if result.gate_id == "RAR-A7"
            else result
            for result in gates
        ]

        return failure_proof(
            claim,
            gates,
            Verdict.OBSTRUCTED,
            (
                "Inference stopped at RAR-A7 (Obstruction): the "
                "declared rule chain derived both an atom and its "
                "negation; ex falso quodlibet is refused even "
                "though no contradiction was present in the raw "
                "premises."
            ),
        )

    target_key = claim.target.key()
    target_node = nodes.get(target_key)

    if target_node is None:
        return ProofObject(
            claim_id=claim.claim_id,
            question=claim.question,
            verdict=Verdict.OPEN,
            tier=Tier.OPEN,
            target=claim.target,
            derived=False,
            gates=gates,
            trace=[],
            falsifier=claim.falsifier,
            not_checked=claim.not_checked,
            explanation=(
                "All RAR gates passed, but no declared rule chain "
                "derives the target."
            ),
        )

    trace = proof_trace(target_key, nodes)

    # RAR A1-A8 are presently declared philosophical bridges, not
    # machine-checked formal steps. Therefore a native philosophical
    # conclusion can never silently inherit Th_coqc (or any tier
    # stronger than Dr) merely because a lower-level premise/rule
    # chain happens to be formally closed -- it is explicitly ceiled
    # at Dr here. This is intentional (matches philosophy.md's "a
    # miss auto-downgrades Th_coqc -> Dr" rule), not an accident of
    # GATE_SPECS defaults -- see RAR_BRIDGE_CEILING_TIER below and
    # tests/test_native_logic.py::test_rar_bridge_ceiling_caps_a_
    # formally_closed_chain_at_dr for the regression that pins it.
    intrinsic_tier = cap_tier(
        [target_node.tier],
        formal_closed=target_node.formal_closed,
    )

    final_tier = cap_tier(
        [intrinsic_tier, RAR_BRIDGE_CEILING_TIER],
        formal_closed=target_node.formal_closed,
    )

    if final_tier == Tier.OPEN:
        verdict = Verdict.OPEN
    elif final_tier == Tier.DR:
        verdict = Verdict.SUPPORTED_AS_DR
    else:
        verdict = Verdict.DERIVED

    bridge_capped = (
        final_tier == RAR_BRIDGE_CEILING_TIER
        and intrinsic_tier != final_tier
    )

    explanation = (
        "The target was derived through declared rules and all "
        "eight RAR gates passed. The underlying rule chain itself "
        f"reached {intrinsic_tier.value}, but the conclusion is "
        f"ceiled at {RAR_BRIDGE_CEILING_TIER.value} because the RAR "
        "gates (A1-A8) are declared philosophical bridges, not "
        "machine-checked steps, and cannot lend a stronger tier "
        "than that to a philosophical conclusion."
        if bridge_capped
        else (
            "The target was derived through declared rules, all "
            "eight RAR gates passed, and the conclusion was capped "
            "at the weakest load-bearing tier."
        )
    )

    return ProofObject(
        claim_id=claim.claim_id,
        question=claim.question,
        verdict=verdict,
        tier=final_tier,
        target=claim.target,
        derived=True,
        gates=gates,
        trace=trace,
        falsifier=claim.falsifier,
        not_checked=claim.not_checked,
        explanation=explanation,
    )


def load_claim(path: str | Path) -> ClaimIR:
    raw = json.loads(
        Path(path).read_text(encoding="utf-8")
    )
    return ClaimIR.from_dict(raw)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run Claim IR through the Readout Universe "
            "RAR proof kernel."
        )
    )
    parser.add_argument("claim", help="Path to Claim IR JSON")
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print proof object JSON",
    )
    args = parser.parse_args()

    claim = load_claim(args.claim)
    proof = solve_claim(claim)

    print(
        json.dumps(
            proof.to_dict(),
            ensure_ascii=False,
            indent=2 if args.pretty else None,
        )
    )


if __name__ == "__main__":
    main()
