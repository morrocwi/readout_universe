"""Executable distinction-level Separation Eval for Human--AI systems.

This evaluator operationalizes one narrow Readout Condition question:

    Does the stated support separate the asserted claim from a relevant rival?

It is intentionally *not* a fact checker, entailment model, rival generator, or
NLI system.  A caller (human annotation, retrieval evaluator, calibrated model,
tool, etc.) must provide bundle-level compatibility readouts.  The evaluator
then applies the RC separation rule without silently inventing missing evidence.

The key distinction is:

    consistency with the claim != separation from the rival.

If the same support remains compatible with both alternatives, a categorical
assertion is NOT_IDENTIFIED and the recommended runtime behavior is structured
abstention, optionally naming additional access that could resolve the contrast.

Evaluation is deliberately two-sided.  Unauthorized Separation Rate (USR) must
never be reported alone, because a system that abstains on everything trivially
gets USR=0.  The paired error is Missed Separation Rate (MSR): abstaining or
withholding when the source *does* separate the claim from its rival.  Systems
that emit continuous separation scores can be compared across a kappa operating
curve.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set
import argparse
import json
from pathlib import Path
import sys

from .rc_ir import DistinctionToken


SEPARATION_VERDICTS = (
    "LICENSED",
    "NOT_IDENTIFIED",
    "UNSUPPORTED",
    "PROVENANCE_INCOMPLETE",
)


@dataclass(frozen=True)
class BundleSeparationReadout:
    """External readout for one jointly evaluated provenance bundle.

    ``claim_compatible`` and ``rival_compatible`` are deliberately separate.
    A source that is compatible with both alternatives does not license their
    separation.

    The booleans can come from human labels, a domain-specific verifier, a
    calibrated NLI model, a symbolic checker, or another declared instrument.
    RC does not privilege one implementation here; provenance of the verifier
    itself should be recorded in ``evaluator`` / ``metadata``.
    """

    node_ids: Sequence[str]
    claim_compatible: bool
    rival_compatible: bool
    evaluator: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        unique = tuple(dict.fromkeys(self.node_ids))
        if not unique:
            raise ValueError("BundleSeparationReadout.node_ids must be non-empty")
        if len(unique) != len(tuple(self.node_ids)):
            raise ValueError("BundleSeparationReadout.node_ids must not contain duplicates")
        object.__setattr__(self, "node_ids", unique)

    def node_set(self) -> Set[str]:
        return set(self.node_ids)


@dataclass
class SeparationCase:
    token: DistinctionToken
    bundle_readouts: List[BundleSeparationReadout] = field(default_factory=list)
    system_asserted_distinction: bool = True
    system_abstained: bool = False
    system_separation_score: Optional[float] = None

    def __post_init__(self) -> None:
        known = set(self.token.node_map)
        for readout in self.bundle_readouts:
            unknown = readout.node_set() - known
            if unknown:
                raise ValueError(
                    f"bundle readout references unknown provenance nodes: {sorted(unknown)}"
                )


@dataclass(frozen=True)
class SeparationResult:
    distinction_id: str
    verdict: str
    licensed_bundle_node_ids: Sequence[str] = field(default_factory=tuple)
    basis_attribution_ok: bool = False
    should_abstain: bool = False
    required_access: Sequence[str] = field(default_factory=tuple)
    reason: str = ""

    def __post_init__(self) -> None:
        if self.verdict not in SEPARATION_VERDICTS:
            raise ValueError(f"verdict {self.verdict!r} not in SEPARATION_VERDICTS")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def semantic_separable(self) -> bool:
        """Whether the supplied support separates claim from rival.

        This is deliberately independent of whether the system *attributes*
        that support correctly.  MSR is about useful separation; USR additionally
        audits attribution.
        """

        return self.verdict == "LICENSED"

    @property
    def authorized_assertion(self) -> bool:
        """Whether a categorical assertion is both separable and correctly based."""

        return self.semantic_separable and self.basis_attribution_ok


@dataclass(frozen=True)
class SeparationMetrics:
    n_cases: int
    n_assertions: int
    n_licensed_assertions: int
    n_unauthorized_separations: int
    unauthorized_separation_rate: Optional[float]
    n_gold_separable: int
    n_missed_separations: int
    missed_separation_rate: Optional[float]
    n_required_abstentions: int
    n_correct_abstentions: int
    structured_abstention_recall: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OperatingPoint:
    kappa: float
    n_predicted_assert: int
    n_predicted_abstain: int
    unauthorized_separation_rate: Optional[float]
    missed_separation_rate: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _minimal_support_sets(token: DistinctionToken) -> List[Set[str]]:
    return [bundle.as_set() for bundle in token.minimal_support_bundles]


def _matching_readouts(
    token: DistinctionToken, readouts: Iterable[BundleSeparationReadout]
) -> List[BundleSeparationReadout]:
    """Keep readouts that evaluate a stored minimal support bundle exactly.

    Exact matching is intentional.  A readout over a strict superset may hide
    which additional node supplied the separation and therefore cannot certify
    the minimal bundle without a separate ablation/readout.
    """

    support_sets = _minimal_support_sets(token)
    return [r for r in readouts if r.node_set() in support_sets]


def evaluate_case(case: SeparationCase) -> SeparationResult:
    token = case.token

    if not token.minimal_support_bundles:
        return SeparationResult(
            distinction_id=token.id,
            verdict="PROVENANCE_INCOMPLETE",
            basis_attribution_ok=False,
            should_abstain=True,
            required_access=tuple(token.required_access),
            reason="no minimal jointly sufficient support bundle is recorded",
        )

    matching = _matching_readouts(token, case.bundle_readouts)
    if not matching:
        return SeparationResult(
            distinction_id=token.id,
            verdict="PROVENANCE_INCOMPLETE",
            basis_attribution_ok=token.basis_is_jointly_sufficient(),
            should_abstain=True,
            required_access=tuple(token.required_access),
            reason="no separation readout was supplied for a recorded minimal support bundle",
        )

    licensed = [
        r for r in matching if r.claim_compatible and not r.rival_compatible
    ]
    if licensed:
        chosen = licensed[0]
        basis_ok = chosen.node_set() <= token.represented_basis()
        return SeparationResult(
            distinction_id=token.id,
            verdict="LICENSED",
            licensed_bundle_node_ids=tuple(chosen.node_ids),
            basis_attribution_ok=basis_ok,
            should_abstain=False,
            required_access=tuple(),
            reason=(
                "a minimal support bundle separates the claim from the rival"
                if basis_ok
                else "the distinction is supportable, but the represented basis omits a sufficient bundle"
            ),
        )

    unresolved = [
        r for r in matching if r.claim_compatible and r.rival_compatible
    ]
    if unresolved:
        return SeparationResult(
            distinction_id=token.id,
            verdict="NOT_IDENTIFIED",
            basis_attribution_ok=token.basis_is_jointly_sufficient(),
            should_abstain=True,
            required_access=tuple(token.required_access),
            reason="available support is compatible with both the claim and the relevant rival",
        )

    return SeparationResult(
        distinction_id=token.id,
        verdict="UNSUPPORTED",
        basis_attribution_ok=token.basis_is_jointly_sufficient(),
        should_abstain=True,
        required_access=tuple(token.required_access),
        reason="no evaluated minimal support bundle is compatible with the asserted claim",
    )


def evaluate_dataset(cases: Sequence[SeparationCase]) -> Dict[str, Any]:
    """Evaluate one fixed system operating point.

    USR = unauthorized asserted distinctions / asserted distinctions
    MSR = semantically separable distinctions withheld / separable distinctions

    The denominators are intentionally different: USR audits assertion authority,
    including basis attribution; MSR audits useful separation independent of
    whether the system correctly disclosed its basis.
    """

    results = [evaluate_case(case) for case in cases]

    assertions = [
        (case, result)
        for case, result in zip(cases, results)
        if case.system_asserted_distinction and not case.system_abstained
    ]
    unauthorized = [
        (case, result)
        for case, result in assertions
        if not result.authorized_assertion
    ]
    licensed_assertions = [
        (case, result)
        for case, result in assertions
        if result.authorized_assertion
    ]

    gold_separable = [
        (case, result)
        for case, result in zip(cases, results)
        if result.semantic_separable
    ]
    missed = [
        (case, result)
        for case, result in gold_separable
        if case.system_abstained or not case.system_asserted_distinction
    ]

    required_abstentions = [
        (case, result)
        for case, result in zip(cases, results)
        if result.should_abstain
    ]
    correct_abstentions = [
        (case, result)
        for case, result in required_abstentions
        if case.system_abstained
    ]

    n_assertions = len(assertions)
    n_gold_separable = len(gold_separable)
    n_required_abstentions = len(required_abstentions)
    metrics = SeparationMetrics(
        n_cases=len(cases),
        n_assertions=n_assertions,
        n_licensed_assertions=len(licensed_assertions),
        n_unauthorized_separations=len(unauthorized),
        unauthorized_separation_rate=(
            len(unauthorized) / n_assertions if n_assertions else None
        ),
        n_gold_separable=n_gold_separable,
        n_missed_separations=len(missed),
        missed_separation_rate=(
            len(missed) / n_gold_separable if n_gold_separable else None
        ),
        n_required_abstentions=n_required_abstentions,
        n_correct_abstentions=len(correct_abstentions),
        structured_abstention_recall=(
            len(correct_abstentions) / n_required_abstentions
            if n_required_abstentions
            else None
        ),
    )

    return {
        "results": [result.to_dict() for result in results],
        "metrics": metrics.to_dict(),
    }


def evaluate_operating_curve(
    cases: Sequence[SeparationCase], kappas: Sequence[float]
) -> List[OperatingPoint]:
    """Evaluate paired separation errors across score thresholds.

    Every case must carry ``system_separation_score``.  At threshold kappa the
    simulated system asserts iff score >= kappa and abstains otherwise.

    USR at an operating point still treats a semantically separable but
    misattributed assertion as unauthorized.  MSR uses semantic separability
    alone, so disclosure failure cannot erase a gold positive from the
    denominator.
    """

    if any(case.system_separation_score is None for case in cases):
        raise ValueError(
            "evaluate_operating_curve requires system_separation_score for every case"
        )

    results = [evaluate_case(case) for case in cases]
    semantic_gold = [result.semantic_separable for result in results]
    authorized_gold = [result.authorized_assertion for result in results]
    n_semantic_gold = sum(semantic_gold)

    points: List[OperatingPoint] = []
    for kappa in kappas:
        predicted_assert = [
            float(case.system_separation_score) >= float(kappa) for case in cases
        ]
        unauthorized = sum(
            pred and not authorized
            for pred, authorized in zip(predicted_assert, authorized_gold)
        )
        missed = sum(
            (not pred) and semantic
            for pred, semantic in zip(predicted_assert, semantic_gold)
        )
        n_assert = sum(predicted_assert)
        points.append(
            OperatingPoint(
                kappa=float(kappa),
                n_predicted_assert=n_assert,
                n_predicted_abstain=len(cases) - n_assert,
                unauthorized_separation_rate=(
                    unauthorized / n_assert if n_assert else None
                ),
                missed_separation_rate=(
                    missed / n_semantic_gold if n_semantic_gold else None
                ),
            )
        )
    return points


def _case_from_dict(data: Dict[str, Any]) -> SeparationCase:
    return SeparationCase(
        token=DistinctionToken.from_dict(data["token"]),
        bundle_readouts=[
            BundleSeparationReadout(**row) for row in data.get("bundle_readouts", [])
        ],
        system_asserted_distinction=data.get("system_asserted_distinction", True),
        system_abstained=data.get("system_abstained", False),
        system_separation_score=data.get("system_separation_score"),
    )


def _load_cases(path: Optional[str]) -> List[SeparationCase]:
    if path:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    else:
        payload = json.load(sys.stdin)
    rows = payload.get("cases", payload if isinstance(payload, list) else [])
    if not isinstance(rows, list):
        raise ValueError("input must be a list or an object with a 'cases' list")
    return [_case_from_dict(row) for row in rows]


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate distinction-level source separation under RC-IR"
    )
    parser.add_argument(
        "--input",
        help="JSON file containing cases; if omitted, read JSON from stdin",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="pretty-print JSON output",
    )
    parser.add_argument(
        "--kappas",
        nargs="*",
        type=float,
        help="optional operating-curve thresholds; requires system_separation_score on every case",
    )
    args = parser.parse_args(argv)

    cases = _load_cases(args.input)
    out = evaluate_dataset(cases)
    if args.kappas:
        out["operating_curve"] = [
            point.to_dict() for point in evaluate_operating_curve(cases, args.kappas)
        ]
    print(
        json.dumps(
            out,
            ensure_ascii=False,
            indent=2 if args.pretty else None,
            sort_keys=args.pretty,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "SEPARATION_VERDICTS",
    "BundleSeparationReadout",
    "SeparationCase",
    "SeparationResult",
    "SeparationMetrics",
    "OperatingPoint",
    "evaluate_case",
    "evaluate_dataset",
    "evaluate_operating_curve",
]
