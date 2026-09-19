"""Integration tests: Separation Eval -> five-state Human-AI runtime status."""

from omega.rc_ir import DistinctionToken, ProvenanceNode, SupportBundle
from omega.separation_eval import BundleSeparationReadout, SeparationCase, evaluate_dataset


def _token(status="OPEN", basis=True):
    return DistinctionToken(
        id="d:x",
        claim_id="claim:x",
        claim="x",
        rival="not-x",
        provenance_nodes=[ProvenanceNode(id="s", node_type="retrieved")],
        minimal_support_bundles=[SupportBundle(["s"])],
        basis_node_ids=["s"] if basis else [],
        basis_mode="explicit" if basis else "none",
        status=status,
    )


def test_licensed_case_compiles_to_licensed_runtime_status():
    case = SeparationCase(
        token=_token(),
        bundle_readouts=[BundleSeparationReadout(["s"], True, False)],
    )
    out = evaluate_dataset([case])
    assert out["results"][0]["runtime_status"] == "LICENSED"


def test_declared_augmentation_compiles_to_augmented_runtime_status():
    case = SeparationCase(
        token=_token(status="AUGMENTED"),
        bundle_readouts=[BundleSeparationReadout(["s"], True, False)],
    )
    out = evaluate_dataset([case])
    assert out["results"][0]["runtime_status"] == "AUGMENTED"


def test_missing_basis_compiles_to_provenance_incomplete():
    case = SeparationCase(
        token=_token(basis=False),
        bundle_readouts=[BundleSeparationReadout(["s"], True, False)],
    )
    out = evaluate_dataset([case])
    assert out["results"][0]["runtime_status"] == "PROVENANCE_INCOMPLETE"


def test_unresolved_rival_compiles_to_not_identified():
    case = SeparationCase(
        token=_token(),
        bundle_readouts=[BundleSeparationReadout(["s"], True, True)],
    )
    out = evaluate_dataset([case])
    assert out["results"][0]["runtime_status"] == "NOT_IDENTIFIED"


def test_actual_abstention_compiles_to_abstain_while_audit_is_retained():
    case = SeparationCase(
        token=_token(),
        bundle_readouts=[BundleSeparationReadout(["s"], True, True)],
        system_asserted_distinction=False,
        system_abstained=True,
    )
    out = evaluate_dataset([case])
    assert out["results"][0]["runtime_status"] == "ABSTAIN"
    assert out["results"][0]["verdict"] == "NOT_IDENTIFIED"
