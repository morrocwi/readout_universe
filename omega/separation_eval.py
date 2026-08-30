"""Executable distinction-level Separation Eval for Human--AI systems.

This evaluator operationalizes one narrow Readout Condition question:

    Does the stated support separate the asserted claim from a relevant rival?

It is intentionally *not* a fact checker, entailment model, or NLI system.
A caller (human annotation, retrieval evaluator, calibrated model, tool, etc.)
must provide bundle-level compatibility readouts.  The evaluator then applies
the RC separation rule without silently inventing missing evidence.

The key distinction is:

    consistency with the claim != separation from the rival.

If the same support remains compatible with both the claim and its rival, a
categorical assertion is NOT_IDENTIFIED and the recommended runtime behavior
is structured abstention, optionally naming additional access that could
resolve the contrast.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set
import argparse
import json
from pathlib import Path
import sys

from .rc_ir import DistinctionToken, SupportBundle


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


@dataclass(frozen=True)
class SeparationMetrics:
    n_cases: int
    n_assertions: int
    n_licensed_assertions: int
    n_unauthorized_separations: int
    unauthorized_separation_rate: Optional[float]
    n_required_abstentions: int
    n_correct_abstentions: int
    structured_abstention_recall: Optional[float]

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

    # A distinction is licensed if at least one minimal jointly sufficient
    # bundle is compatible with the claim and incompatible with the rival.
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

    # If at least one minimal support bundle is compatible with both, then the
    # current support fails to identify the asserted contrast.  This is the
    # canonical RC abstention case.
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

    # If no evaluated minimal bundle is even compatible with the claim, the
    # problem is not mere under-identification: the asserted side itself is
    # unsupported by the supplied readouts.
    return SeparationResult(
        distinction_id=token.id,
        verdict="UNSUPPORTED",
        basis_attribution_ok=token.basis_is_jointly_sufficient(),
        should_abstain=True,
        required_access=tuple(token.required_access),
        reason="no evaluated minimal support bundle is compatible with the asserted claim",
    )


def evaluate_dataset(cases: Sequence[SeparationCase]) -> Dict[str, Any]:
    results = [evaluate_case(case) for case in cases]

    assertions = [
        (case, result)
        for case, result in zip(cases, results)
        if case.system_asserted_distinction
    ]
    unauthorized = [
        (case, result)
        for case, result in assertions
        if result.verdict != "LICENSED" or not result.basis_attribution_ok
    ]
    licensed_assertions = [
        (case, result)
        for case, result in assertions
        if result.verdict == "LICENSED" and result.basis_attribution_ok
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
    n_required_abstentions = len(required_abstentions)
    metrics = SeparationMetrics(
        n_cases=len(cases),
        n_assertions=n_assertions,
        n_licensed_assertions=len(licensed_assertions),
        n_unauthorized_separations=len(unauthorized),
        unauthorized_separation_rate=(
            len(unauthorized) / n_assertions if n_assertions else None
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


def _case_from_dict(data: Dict[str, Any]) -> SeparationCase:
    return SeparationCase(
        token=DistinctionToken.from_dict(data["token"]),
        bundle_readouts=[
            BundleSeparationReadout(**row) for row in data.get("bundle_readouts", [])
        ],
        system_asserted_distinction=data.get("system_asserted_distinction", True),
        system_abstained=data.get("system_abstained", False),
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
    args = parser.parse_args(argv)

    cases = _load_cases(args.input)
    out = evaluate_dataset(cases)
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
    "evaluate_case",
    "evaluate_dataset",
]
