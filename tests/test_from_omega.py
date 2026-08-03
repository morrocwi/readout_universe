"""Tests for native_logic/from_omega.py -- the omega.Claim -> native_logic
ClaimIR adapter.

Run with: python3 -m pytest tests/test_from_omega.py -q
(or: python3 -m pytest -q, if run from repo root)
"""

import pytest

from omega.claim_ir import Claim, OPEN_TIER, OPEN_BRIDGE_CLASS
from native_logic.kernel import Tier
from native_logic.from_omega import omega_claims_to_native_ir


REQUIRED_CONTEXT = {
    "candidate_distinctions": ["a", "b"],
    "grammar_compatible": True,
    "required_retained": [],
    "retained": [],
    "required_accessible": [],
    "accessible": [],
    "metric_nonnegative": True,
    "identity_lock_ok": True,
    "declared_obstruction": False,
    "lens_ok": True,
    "lens_distortion": 0.0,
    "lens_tolerance": 0.1,
}


def _translated_claim() -> Claim:
    return Claim(
        id="claim:term:cause",
        predicate="TRANSLATED",
        arguments=["cause", "a load-bearing retained relation"],
        quantifier="none",
        scope="",
        tier="Dr",
        bridge_class=None,
        dependencies=[],
    )


def _bridge_claim() -> Claim:
    return Claim(
        id="claim:bridge:tension",
        predicate="BRIDGE",
        arguments=["tension"],
        quantifier="none",
        scope="",
        tier="finite_diagnostic",
        bridge_class="POSITED",
        dependencies=["claim:term:cause"],
    )


def _open_claim_from_no_dictionary_entry() -> Claim:
    """An Open-tier claim exactly as omega/claim_ir.py::Claim.from_extraction
    produces for a NO_DICTIONARY_ENTRY translation_table row -- i.e. a term
    that resisted step1_translate's dictionary lookup.
    """

    return Claim(
        id="claim:term:qualia",
        predicate="NO_DICTIONARY_ENTRY",
        arguments=["qualia"],
        quantifier="none",
        scope="",
        tier=OPEN_TIER,
        bridge_class=OPEN_BRIDGE_CLASS,
        dependencies=[],
    )


# ---------------------------------------------------------------------------
# Core conversion: tiers carried over verbatim, never upgraded
# ---------------------------------------------------------------------------

def test_tiers_carried_over_verbatim_no_silent_upgrade():
    claims = [
        _translated_claim(),
        _bridge_claim(),
        _open_claim_from_no_dictionary_entry(),
    ]

    ir = omega_claims_to_native_ir(
        claims,
        question="Is there a load-bearing cause of the tension?",
        target_predicate="resolved",
        context=REQUIRED_CONTEXT,
        falsifier="a retained record showing no such cause exists",
    )

    facts_by_id = {}
    for fact, claim in zip(ir.premises, claims):
        facts_by_id[claim.id] = fact

    # Exact same tier string, mapped 1:1 into the native_logic.kernel.Tier
    # enum -- not weakened, not strengthened.
    assert facts_by_id["claim:term:cause"].tier == Tier.DR
    assert facts_by_id["claim:bridge:tension"].tier == Tier.FINITE_DIAGNOSTIC

    # The Open-tier claim, born from a NO_DICTIONARY_ENTRY case, must land
    # as Tier.OPEN in the kernel -- never silently promoted to something
    # stronger just because it crossed the adapter boundary.
    open_fact = facts_by_id["claim:term:qualia"]
    assert open_fact.tier == Tier.OPEN
    assert open_fact.tier.value == OPEN_TIER

    # bridge_class is carried over verbatim too (into Fact.source, the only
    # free-text field Fact has) -- not dropped, not replaced.
    assert "bridge_class=POSITED" in facts_by_id["claim:bridge:tension"].source
    assert (
        f"bridge_class={OPEN_BRIDGE_CLASS}"
        in facts_by_id["claim:term:qualia"].source
    )
    assert "bridge_class=None" in facts_by_id["claim:term:cause"].source

    # Every input Claim produced exactly one Fact -- no fan-out, no drops.
    assert len(ir.premises) == len(claims)


def test_translation_table_is_minimal_and_derived_from_claims():
    claims = [_translated_claim(), _open_claim_from_no_dictionary_entry()]

    ir = omega_claims_to_native_ir(
        claims,
        question="What does 'cause' mean here?",
        target_predicate="resolved",
        context=REQUIRED_CONTEXT,
        falsifier="a counterexample term with no valid translation",
    )

    assert len(ir.translation) == len(claims)

    by_term = {t.foreign_term: t for t in ir.translation}
    assert by_term["cause"].native_term == "a load-bearing retained relation"
    assert by_term["cause"].tier == Tier.DR

    # NO_DICTIONARY_ENTRY claim: no invented native_term distinct from the
    # foreign term (the claim never asserted a translation).
    assert by_term["qualia"].native_term == "qualia"
    assert by_term["qualia"].tier == Tier.OPEN
    assert by_term["qualia"].bridge_class == OPEN_BRIDGE_CLASS


def test_target_atom_is_built_from_explicit_arguments():
    ir = omega_claims_to_native_ir(
        [_translated_claim()],
        question="q",
        target_predicate="resolved",
        context=REQUIRED_CONTEXT,
        falsifier="f",
        target_arguments=["agent", "t1"],
        target_negated=True,
    )

    assert ir.target.predicate == "resolved"
    assert ir.target.arguments == ("agent", "t1")
    assert ir.target.negated is True


# ---------------------------------------------------------------------------
# Required-argument enforcement -- no fabricated defaults for gate-affecting
# or kernel-scoping fields
# ---------------------------------------------------------------------------

def test_missing_falsifier_raises_instead_of_defaulting():
    with pytest.raises(TypeError):
        # falsifier is keyword-only with no default -- calling without it
        # must fail loudly, not silently default to "".
        omega_claims_to_native_ir(
            [_translated_claim()],
            question="q",
            target_predicate="resolved",
            context=REQUIRED_CONTEXT,
        )  # type: ignore[call-arg]


def test_empty_falsifier_string_raises():
    with pytest.raises(ValueError):
        omega_claims_to_native_ir(
            [_translated_claim()],
            question="q",
            target_predicate="resolved",
            context=REQUIRED_CONTEXT,
            falsifier="   ",
        )


def test_empty_target_predicate_raises():
    with pytest.raises(ValueError):
        omega_claims_to_native_ir(
            [_translated_claim()],
            question="q",
            target_predicate="  ",
            context=REQUIRED_CONTEXT,
            falsifier="f",
        )


def test_empty_question_raises():
    with pytest.raises(ValueError):
        omega_claims_to_native_ir(
            [_translated_claim()],
            question="  ",
            target_predicate="resolved",
            context=REQUIRED_CONTEXT,
            falsifier="f",
        )


def test_unrepresentable_tier_raises_instead_of_guessing():
    """omega.schemas.TIER_TAGS includes 'fit_calibrated', which
    native_logic.kernel.Tier cannot represent. The adapter must refuse to
    guess a mapping rather than coerce it onto some nearby native tier.
    """

    claim = Claim(
        id="claim:term:x",
        predicate="TRANSLATED",
        arguments=["x", "y"],
        quantifier="none",
        scope="",
        tier="fit_calibrated",
        bridge_class=None,
        dependencies=[],
    )

    with pytest.raises(ValueError):
        omega_claims_to_native_ir(
            [claim],
            question="q",
            target_predicate="resolved",
            context=REQUIRED_CONTEXT,
            falsifier="f",
        )


# ---------------------------------------------------------------------------
# End-to-end: the produced ClaimIR is well-formed enough for the kernel
# ---------------------------------------------------------------------------

def test_produced_claim_ir_passes_validate_claim():
    from native_logic.kernel import validate_claim

    ir = omega_claims_to_native_ir(
        [_translated_claim(), _bridge_claim()],
        question="Is there a load-bearing cause of the tension?",
        target_predicate="resolved",
        context=REQUIRED_CONTEXT,
        falsifier="a retained record showing no such cause exists",
        scope="one retained step",
    )

    # Should not raise -- claim_id/question/scope/translation/falsifier/
    # target are all present because the adapter requires them.
    validate_claim(ir)
