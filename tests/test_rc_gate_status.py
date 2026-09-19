"""Tests for the five-value RC runtime status contract in omega.gates."""

import pytest

from omega.gates import RCGateStatus, rc_runtime_status, STUB_GATES
from omega.schemas import Issue


def test_rc_gate_status_has_exactly_five_runtime_values():
    assert {s.value for s in RCGateStatus} == {
        "LICENSED",
        "AUGMENTED",
        "PROVENANCE_INCOMPLETE",
        "NOT_IDENTIFIED",
        "ABSTAIN",
    }


def test_runtime_mapping_keeps_licensed_and_augmented_distinct():
    assert rc_runtime_status(
        separation_verdict="LICENSED",
        basis_attribution_ok=True,
        augmented=False,
    ) is RCGateStatus.LICENSED
    assert rc_runtime_status(
        separation_verdict="LICENSED",
        basis_attribution_ok=True,
        augmented=True,
    ) is RCGateStatus.AUGMENTED


def test_missing_basis_is_provenance_incomplete_even_if_content_is_supportable():
    assert rc_runtime_status(
        separation_verdict="LICENSED",
        basis_attribution_ok=False,
    ) is RCGateStatus.PROVENANCE_INCOMPLETE


def test_not_identified_and_unsupported_do_not_become_licensed():
    assert rc_runtime_status(
        separation_verdict="NOT_IDENTIFIED",
        basis_attribution_ok=True,
    ) is RCGateStatus.NOT_IDENTIFIED
    assert rc_runtime_status(
        separation_verdict="UNSUPPORTED",
        basis_attribution_ok=True,
    ) is RCGateStatus.NOT_IDENTIFIED


def test_abstain_is_an_explicit_runtime_disposition():
    assert rc_runtime_status(
        separation_verdict="NOT_IDENTIFIED",
        basis_attribution_ok=True,
        system_abstained=True,
    ) is RCGateStatus.ABSTAIN


def test_old_stubs_remain_not_implemented_and_receive_no_fake_rc_status():
    issue = Issue(question="test")
    out = STUB_GATES["G5"](issue)
    assert out["status"] == "NOT_IMPLEMENTED"
    assert "rc_status" not in out


def test_unrecognized_separation_verdict_is_rejected():
    with pytest.raises(ValueError):
        rc_runtime_status(
            separation_verdict="MAGIC_PASS",
            basis_attribution_ok=True,
        )
