"""Readout Condition Intermediate Representation (RC-IR).

RC-IR is a typed layer *above* ``omega.claim_ir.Claim``.  Claim IR records
claim-level dependencies, tiers, and bridge classes; RC-IR records the finer
unit needed by the Readout Condition: a distinction asserted against a
relevant rival, together with the provenance bundle(s) that license it.

The module is deliberately non-oracular.  It stores provenance and validates
its shape; it does not infer entailment, relevance, causation, or truth from
text.  Any downstream evaluator must supply those readouts explicitly.

Core design rule:

    no epistemic discrimination without provenance.

A distinction may have more than one minimal jointly sufficient support
bundle.  ``minimal_support_bundles`` therefore forms an antichain: no stored
bundle may strictly contain another stored bundle.  This is the executable
counterpart of the paper's minimal-support-family notation S(d; y, kappa).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set
import json


SOURCE_TYPES = (
    "retrieved",
    "tool",
    "user",
    "episodic_memory",
    "parametric",
    "instruction",
    "background_model",
    "policy",
    "decision_rule",
    "calibration",
    "measurement",
    "testimony",
    "other",
)

RC_STATUSES = (
    "LICENSED",
    "AUGMENTED",
    "PROVENANCE_INCOMPLETE",
    "NOT_IDENTIFIED",
    "ABSTAIN",
    "UNSUPPORTED",
    "OPEN",
)

BASIS_MODES = ("explicit", "implicated", "mixed", "none")


@dataclass(frozen=True)
class ProvenanceNode:
    """One typed node that can contribute to a distinction's support.

    ``node_type`` is epistemic/functional, not ontological.  For example a
    database row may be ``retrieved`` in one pipeline and ``episodic_memory``
    in another if that is the role through which the current claim depends on
    it.
    """

    id: str
    node_type: str
    label: str = ""
    source_ref: str = ""
    version: str = ""
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("ProvenanceNode.id must be non-empty")
        if self.node_type not in SOURCE_TYPES:
            raise ValueError(f"node_type {self.node_type!r} not in SOURCE_TYPES")


@dataclass(frozen=True)
class SupportContribution:
    """Signed contribution of one provenance node to one graded contrast.

    ``value`` has no universal unit.  The caller must name the scale (for
    example ``log_likelihood_ratio``).  Positive and negative contributions
    are both permitted; RC-IR never assumes a monotone support ladder.
    """

    node_id: str
    value: float
    scale: str
    note: str = ""

    def __post_init__(self) -> None:
        if not self.node_id:
            raise ValueError("SupportContribution.node_id must be non-empty")
        if not self.scale:
            raise ValueError("SupportContribution.scale must be non-empty")


@dataclass(frozen=True)
class SupportBundle:
    """One minimal jointly sufficient support bundle for a distinction."""

    node_ids: Sequence[str]
    label: str = ""

    def __post_init__(self) -> None:
        unique = tuple(dict.fromkeys(self.node_ids))
        if not unique:
            raise ValueError("SupportBundle must contain at least one node")
        if len(unique) != len(tuple(self.node_ids)):
            raise ValueError("SupportBundle.node_ids must not contain duplicates")
        object.__setattr__(self, "node_ids", unique)

    def as_set(self) -> Set[str]:
        return set(self.node_ids)


@dataclass
class DistinctionToken:
    """One claim-level distinction against one relevant rival.

    This object separates semantic contrast from response production:

    * ``claim`` / ``rival`` state *what distinction is asserted*.
    * ``response_rule`` records (when known) what process produced the token.

    ``basis_node_ids`` includes both explicitly stated and pragmatically
    implicated bases when the current discourse presents them as supporting
    the distinction.  ``basis_mode`` records how that attribution arose.
    """

    id: str
    claim_id: str
    claim: str
    rival: str
    response_rule: str = ""
    observed_record: str = ""
    kappa: Optional[float] = None
    kappa_scale: str = ""
    provenance_nodes: List[ProvenanceNode] = field(default_factory=list)
    minimal_support_bundles: List[SupportBundle] = field(default_factory=list)
    basis_node_ids: List[str] = field(default_factory=list)
    basis_mode: str = "none"
    contributions: List[SupportContribution] = field(default_factory=list)
    decision_policy_node_ids: List[str] = field(default_factory=list)
    required_access: List[str] = field(default_factory=list)
    status: str = "OPEN"
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("DistinctionToken.id must be non-empty")
        if not self.claim_id:
            raise ValueError("DistinctionToken.claim_id must be non-empty")
        if not self.claim or not self.rival:
            raise ValueError("claim and rival must both be non-empty")
        if self.claim == self.rival:
            raise ValueError("claim and rival must be distinct")
        if self.status not in RC_STATUSES:
            raise ValueError(f"status {self.status!r} not in RC_STATUSES")
        if self.basis_mode not in BASIS_MODES:
            raise ValueError(f"basis_mode {self.basis_mode!r} not in BASIS_MODES")
        if self.kappa is not None and not self.kappa_scale:
            raise ValueError("kappa_scale is required when kappa is set")

        node_ids = [n.id for n in self.provenance_nodes]
        if len(set(node_ids)) != len(node_ids):
            raise ValueError("provenance node ids must be unique")
        node_set = set(node_ids)

        for bundle in self.minimal_support_bundles:
            missing = bundle.as_set() - node_set
            if missing:
                raise ValueError(f"support bundle references unknown nodes: {sorted(missing)}")

        # Minimal support families are stored as an antichain.  If A is a
        # strict subset of B then B is not minimal and must not be recorded.
        bundle_sets = [b.as_set() for b in self.minimal_support_bundles]
        for i, left in enumerate(bundle_sets):
            for j, right in enumerate(bundle_sets):
                if i != j and left < right:
                    raise ValueError(
                        "minimal_support_bundles must form an antichain; "
                        f"bundle {i} is a strict subset of bundle {j}"
                    )

        for name, ids in (
            ("basis_node_ids", self.basis_node_ids),
            ("decision_policy_node_ids", self.decision_policy_node_ids),
        ):
            unknown = set(ids) - node_set
            if unknown:
                raise ValueError(f"{name} references unknown nodes: {sorted(unknown)}")

        contribution_nodes = {c.node_id for c in self.contributions}
        unknown_contrib = contribution_nodes - node_set
        if unknown_contrib:
            raise ValueError(
                f"contributions reference unknown nodes: {sorted(unknown_contrib)}"
            )

    @property
    def node_map(self) -> Dict[str, ProvenanceNode]:
        return {node.id: node for node in self.provenance_nodes}

    def represented_basis(self) -> Set[str]:
        """Return the explicit-or-implicated basis attributed in context."""

        return set(self.basis_node_ids)

    def basis_is_jointly_sufficient(self) -> bool:
        """Whether the represented basis contains at least one support bundle."""

        basis = self.represented_basis()
        return any(bundle.as_set() <= basis for bundle in self.minimal_support_bundles)

    def surviving_support_bundles(self, defeated_node_ids: Iterable[str]) -> List[SupportBundle]:
        """Route node-specific undercutting defeat through the support family.

        This intentionally does not model rebutting defeat or topology-changing
        policy revision; those require a new/updated RC-IR graph.
        """

        defeated = set(defeated_node_ids)
        return [
            bundle
            for bundle in self.minimal_support_bundles
            if bundle.as_set().isdisjoint(defeated)
        ]

    def support_survives(self, defeated_node_ids: Iterable[str]) -> bool:
        return bool(self.surviving_support_bundles(defeated_node_ids))

    def signed_support_total(self, scale: Optional[str] = None) -> float:
        """Sum typed signed contributions on one declared scale.

        If multiple scales are present the caller must select one explicitly.
        This prevents numerically adding unlike epistemic quantities.
        """

        if not self.contributions:
            return 0.0
        scales = {c.scale for c in self.contributions}
        if scale is None:
            if len(scales) != 1:
                raise ValueError(
                    "multiple contribution scales present; select scale explicitly"
                )
            scale = next(iter(scales))
        return sum(c.value for c in self.contributions if c.scale == scale)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DistinctionToken":
        return cls(
            id=data["id"],
            claim_id=data["claim_id"],
            claim=data["claim"],
            rival=data["rival"],
            response_rule=data.get("response_rule", ""),
            observed_record=data.get("observed_record", ""),
            kappa=data.get("kappa"),
            kappa_scale=data.get("kappa_scale", ""),
            provenance_nodes=[ProvenanceNode(**n) for n in data.get("provenance_nodes", [])],
            minimal_support_bundles=[
                SupportBundle(**b) for b in data.get("minimal_support_bundles", [])
            ],
            basis_node_ids=list(data.get("basis_node_ids", [])),
            basis_mode=data.get("basis_mode", "none"),
            contributions=[
                SupportContribution(**c) for c in data.get("contributions", [])
            ],
            decision_policy_node_ids=list(data.get("decision_policy_node_ids", [])),
            required_access=list(data.get("required_access", [])),
            status=data.get("status", "OPEN"),
            notes=data.get("notes", ""),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> "DistinctionToken":
        return cls.from_dict(json.loads(text))


__all__ = [
    "SOURCE_TYPES",
    "RC_STATUSES",
    "BASIS_MODES",
    "ProvenanceNode",
    "SupportContribution",
    "SupportBundle",
    "DistinctionToken",
]
