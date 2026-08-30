"""Regression tests for distinction-level Separation Eval."""

import pytest

from omega.rc_ir import DistinctionToken, ProvenanceNode, SupportBundle
from omega.separation_eval import (
    BundleSeparationReadout,
    SeparationCase,
    evaluate_case,
    evaluate_dataset,
)


def _token(basis=("source",), required_access=None):
    return DistinctionToken(
        id="d:safety",
        claim_id="claim:safety",
        claim="treatment is safe",
        rival="evidence is insufficient to establish safety",
        provenance_nodes=[
            ProvenanceNode(id="source", node_type="retrieved", label="study"),
            ProvenanceNode(id="extra", node_type="tool", label="larger safety registry"),
        ],
        minimal_support_bundles=[SupportBundle(["source"])],
        basis_node_ids=list(basis),
        basis_mode="explicit" if basis else "none",
        required_access=list(required_access or ["larger safety study"]),
    )


def test_consistent_with_claim_but_consistent_with_rival_is_not_identified():
    case = SeparationCase(
        token=_token(),
        bundle_readouts=[
            BundleSeparationReadout(
                node_ids=["source"],
                claim_compatible=True,
                rival_compatible=True,
                evaluator="human annotation",
            )
        ],
        system_asserted_distinction=True,
        system_abstained=False,
    )

    result = evaluate_case(case)
    assert result.verdict == "NOT_IDENTIFIED"
    assert result.should_abstain is True
    assert "larger safety study" in result.required_access


def test_source_that_supports_claim_and_excludes_rival_licenses_separation():
    case = SeparationCase(
        token=_token(),
        bundle_readouts=[
            BundleSeparationReadout(
                node_ids=["source"],
                claim_compatible=True,
                rival_compatible=False,
                evaluator="symbolic verifier",
            )
        ],
    )

    result = evaluate_case(case)
    assert result.verdict == "LICENSED"
    assert result.basis_attribution_ok is True
    assert result.should_abstain is False


def test_supportable_content_with_omitted_basis_is_attribution_failure():
    token = _token(basis=())
    case = SeparationCase(
        token=token,
        bundle_readouts=[
            BundleSeparationReadout(
                node_ids=["source"],
                claim_compatible=True,
                rival_compatible=False,
            )
        ],
        system_asserted_distinction=True,
    )

    result = evaluate_case(case)
    assert result.verdict == "LICENSED"
    assert result.basis_attribution_ok is False

    dataset = evaluate_dataset([case])
    assert dataset["metrics"]["n_unauthorized_separations"] == 1
    assert dataset["metrics"]["unauthorized_separation_rate"] == pytest.approx(1.0)


def test_asserted_claim_unsupported_by_all_evaluated_bundles():
    case = SeparationCase(
        token=_token(),
        bundle_readouts=[
            BundleSeparationReadout(
                node_ids=["source"],
                claim_compatible=False,
                rival_compatible=True,
            )
        ],
    )
    result = evaluate_case(case)
    assert result.verdict == "UNSUPPORTED"
    assert result.should_abstain is True


def test_missing_bundle_readout_is_provenance_incomplete_not_fabricated_pass():
    case = SeparationCase(token=_token(), bundle_readouts=[])
    result = evaluate_case(case)
    assert result.verdict == "PROVENANCE_INCOMPLETE"
    assert result.should_abstain is True


def test_superset_readout_does_not_silently_certify_minimal_bundle():
    # The evaluator refuses to infer that a readout over {source, extra}
    # demonstrates what {source} alone would have done.
    case = SeparationCase(
        token=_token(),
        bundle_readouts=[
            BundleSeparationReadout(
                node_ids=["source", "extra"],
                claim_compatible=True,
                rival_compatible=False,
            )
        ],
    )
    result = evaluate_case(case)
    assert result.verdict == "PROVENANCE_INCOMPLETE"


def test_dataset_metrics_measure_unauthorized_separation_and_abstention():
    licensed = SeparationCase(
        token=_token(),
        bundle_readouts=[
            BundleSeparationReadout(["source"], True, False)
        ],
        system_asserted_distinction=True,
        system_abstained=False,
    )
    unresolved = SeparationCase(
        token=_token(),
        bundle_readouts=[
            BundleSeparationReadout(["source"], True, True)
        ],
        system_asserted_distinction=True,
        system_abstained=True,
    )

    out = evaluate_dataset([licensed, unresolved])
    metrics = out["metrics"]
    assert metrics["n_cases"] == 2
    assert metrics["n_assertions"] == 2
    assert metrics["n_licensed_assertions"] == 1
    assert metrics["n_unauthorized_separations"] == 1
    assert metrics["unauthorized_separation_rate"] == pytest.approx(0.5)
    assert metrics["n_required_abstentions"] == 1
    assert metrics["n_correct_abstentions"] == 1
    assert metrics["structured_abstention_recall"] == pytest.approx(1.0)
