"""Executable tests for distinction-level RC-IR.

Run with: python3 -m pytest omega/ tests/ -q
"""

import pytest

from omega.rc_ir import (
    DistinctionToken,
    ProvenanceNode,
    SupportBundle,
    SupportContribution,
)


def _nodes():
    return [
        ProvenanceNode(id="test", node_type="measurement", label="lab result"),
        ProvenanceNode(id="model", node_type="calibration", label="calibration model"),
        ProvenanceNode(id="prior", node_type="background_model", label="population prior"),
    ]


def test_rc_ir_round_trip_preserves_distinction_provenance():
    token = DistinctionToken(
        id="d:diagnosis",
        claim_id="claim:diagnosis",
        claim="disease present",
        rival="disease absent",
        response_rule="posterior threshold",
        observed_record="test positive",
        kappa=0.0,
        kappa_scale="log_odds",
        provenance_nodes=_nodes(),
        minimal_support_bundles=[SupportBundle(["test", "model", "prior"])],
        basis_node_ids=["test", "model", "prior"],
        basis_mode="explicit",
        contributions=[
            SupportContribution("test", 2.302585, "log_odds", "LR+=10"),
            SupportContribution("prior", -4.595120, "log_odds", "prior odds 1:99"),
        ],
        status="AUGMENTED",
    )

    rebuilt = DistinctionToken.from_json(token.to_json())
    assert rebuilt.to_dict() == token.to_dict()
    assert rebuilt.claim != rebuilt.rival
    assert rebuilt.basis_is_jointly_sufficient() is True


def test_signed_support_allows_negative_augmentation_and_does_not_assume_monotonicity():
    token = DistinctionToken(
        id="d:posterior",
        claim_id="claim:posterior",
        claim="disease more likely than not",
        rival="disease not more likely than not",
        provenance_nodes=_nodes(),
        minimal_support_bundles=[SupportBundle(["test", "model", "prior"])],
        contributions=[
            SupportContribution("test", 2.302585, "log_odds"),
            SupportContribution("prior", -4.595120, "log_odds"),
        ],
    )

    assert token.signed_support_total("log_odds") == pytest.approx(-2.292535, abs=1e-6)


def test_minimal_support_bundles_must_form_antichain():
    with pytest.raises(ValueError, match="antichain"):
        DistinctionToken(
            id="d:x",
            claim_id="claim:x",
            claim="x",
            rival="not x",
            provenance_nodes=_nodes(),
            minimal_support_bundles=[
                SupportBundle(["test", "model"]),
                SupportBundle(["test", "model", "prior"]),
            ],
        )


def test_node_specific_defeat_removes_only_bundles_that_depend_on_defeated_node():
    nodes = _nodes() + [
        ProvenanceNode(id="independent", node_type="tool", label="independent assay")
    ]
    token = DistinctionToken(
        id="d:x",
        claim_id="claim:x",
        claim="x",
        rival="not x",
        provenance_nodes=nodes,
        minimal_support_bundles=[
            SupportBundle(["test", "model"]),
            SupportBundle(["independent"]),
        ],
    )

    assert token.support_survives(["test"]) is True
    survivors = token.surviving_support_bundles(["test"])
    assert [set(b.node_ids) for b in survivors] == [{"independent"}]
    assert token.support_survives(["test", "independent"]) is False


def test_basis_can_be_implicated_not_only_explicit():
    token = DistinctionToken(
        id="d:x",
        claim_id="claim:x",
        claim="x",
        rival="not x",
        provenance_nodes=_nodes(),
        minimal_support_bundles=[SupportBundle(["test", "model"])],
        basis_node_ids=["test", "model"],
        basis_mode="implicated",
    )

    assert token.basis_is_jointly_sufficient() is True
    assert token.basis_mode == "implicated"


def test_unknown_nodes_are_rejected_in_support_and_basis():
    with pytest.raises(ValueError, match="unknown nodes"):
        DistinctionToken(
            id="d:x",
            claim_id="claim:x",
            claim="x",
            rival="not x",
            provenance_nodes=_nodes(),
            minimal_support_bundles=[SupportBundle(["ghost"])],
        )

    with pytest.raises(ValueError, match="basis_node_ids"):
        DistinctionToken(
            id="d:x",
            claim_id="claim:x",
            claim="x",
            rival="not x",
            provenance_nodes=_nodes(),
            minimal_support_bundles=[SupportBundle(["test"])],
            basis_node_ids=["ghost"],
        )
