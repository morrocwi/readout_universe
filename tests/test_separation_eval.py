"""Regression tests for distinction-level Separation Eval."""

import pytest

from omega.rc_ir import DistinctionToken, ProvenanceNode, SupportBundle
from omega.separation_eval import (
    BundleSeparationReadout,
    SeparationCase,
    evaluate_case,
    evaluate_dataset,
    evaluate_operating_curve,
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


def test_dataset_reports_usr_and_msr_together():
    licensed_asserted = SeparationCase(
        token=_token(),
        bundle_readouts=[BundleSeparationReadout(["source"], True, False)],
        system_asserted_distinction=True,
        system_abstained=False,
    )
    unresolved_asserted = SeparationCase(
        token=_token(),
        bundle_readouts=[BundleSeparationReadout(["source"], True, True)],
        system_asserted_distinction=True,
        system_abstained=False,
    )
    licensed_but_abstained = SeparationCase(
        token=_token(),
        bundle_readouts=[BundleSeparationReadout(["source"], True, False)],
        system_asserted_distinction=False,
        system_abstained=True,
    )

    out = evaluate_dataset([licensed_asserted, unresolved_asserted, licensed_but_abstained])
    metrics = out["metrics"]
    assert metrics["n_cases"] == 3
    assert metrics["n_assertions"] == 2
    assert metrics["n_licensed_assertions"] == 1
    assert metrics["n_unauthorized_separations"] == 1
    assert metrics["unauthorized_separation_rate"] == pytest.approx(0.5)
    assert metrics["n_gold_separable"] == 2
    assert metrics["n_missed_separations"] == 1
    assert metrics["missed_separation_rate"] == pytest.approx(0.5)


def test_always_abstain_has_zero_assertions_but_bad_missed_separation_rate():
    cases = [
        SeparationCase(
            token=_token(),
            bundle_readouts=[BundleSeparationReadout(["source"], True, False)],
            system_asserted_distinction=False,
            system_abstained=True,
        )
        for _ in range(3)
    ]
    metrics = evaluate_dataset(cases)["metrics"]
    assert metrics["n_assertions"] == 0
    assert metrics["unauthorized_separation_rate"] is None
    assert metrics["missed_separation_rate"] == pytest.approx(1.0)


def test_operating_curve_trades_unauthorized_against_missed_separation():
    licensed = SeparationCase(
        token=_token(),
        bundle_readouts=[BundleSeparationReadout(["source"], True, False)],
        system_separation_score=0.8,
    )
    unresolved = SeparationCase(
        token=_token(),
        bundle_readouts=[BundleSeparationReadout(["source"], True, True)],
        system_separation_score=0.6,
    )

    points = evaluate_operating_curve([licensed, unresolved], [0.5, 0.7, 0.9])
    # kappa .5: assert both => one unauthorized, no missed licensed distinction
    assert points[0].unauthorized_separation_rate == pytest.approx(0.5)
    assert points[0].missed_separation_rate == pytest.approx(0.0)
    # kappa .7: assert only the licensed case => ideal point for this toy set
    assert points[1].unauthorized_separation_rate == pytest.approx(0.0)
    assert points[1].missed_separation_rate == pytest.approx(0.0)
    # kappa .9: assert none => miss the licensed separation
    assert points[2].unauthorized_separation_rate is None
    assert points[2].missed_separation_rate == pytest.approx(1.0)
