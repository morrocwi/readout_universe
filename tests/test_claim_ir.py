"""Real, executable tests for the Claim IR (omega/claim_ir.py).

Run with: python3 -m pytest omega/ tests/ -q
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from omega.claim_ir import Claim, OPEN_TIER, OPEN_BRIDGE_CLASS
from omega.gates import step4_bridge_audit
from omega.schemas import Issue
from omega.run import run_omega_all


# ---------------------------------------------------------------------------
# (a) building a Claim from an extraction with a DERIVED bridge preserves
#     Th_coqc
# ---------------------------------------------------------------------------

def test_derived_bridge_preserves_th_coqc():
    issue = Issue(
        question="irrelevant",
        bridges=[{"term": "L_R", "verdict_class": "DERIVED", "incoming_tier": "Th_coqc"}],
    )
    extraction = run_omega_all(issue)
    claims = Claim.from_extraction(extraction)

    bridge_claims = [c for c in claims if c.predicate == "BRIDGE"]
    assert len(bridge_claims) == 1
    claim = bridge_claims[0]
    assert claim.tier == "Th_coqc"
    assert claim.bridge_class == "DERIVED"


# ---------------------------------------------------------------------------
# (b) building one from a DEFINITIONAL-RELABEL bridge downgrades to Dr --
#     verified by calling gates.py's own logic directly and checking the
#     Claim IR agrees with it, not just checking the Claim IR in isolation.
# ---------------------------------------------------------------------------

def test_definitional_relabel_bridge_downgrades_to_dr_agrees_with_gates_py():
    issue = Issue(
        question="irrelevant",
        bridges=[
            {"term": "mass", "verdict_class": "DEFINITIONAL-RELABEL", "incoming_tier": "Th_coqc"}
        ],
    )
    extraction = run_omega_all(issue)

    # Ground truth: call gates.py's own bridge-audit logic directly.
    direct = step4_bridge_audit(issue)
    direct_record = direct["result"]["bridges"][0]
    assert direct_record["resulting_tier"] == "Dr"
    assert direct_record["downgraded"] is True

    # Claim IR must agree with that ground truth, not diverge from it.
    claims = Claim.from_extraction(extraction)
    bridge_claims = [c for c in claims if c.predicate == "BRIDGE"]
    assert len(bridge_claims) == 1
    claim = bridge_claims[0]

    assert claim.tier == direct_record["resulting_tier"]
    assert claim.tier == "Dr"
    assert claim.bridge_class == direct_record["verdict_class"]
    assert claim.bridge_class == "DEFINITIONAL-RELABEL"


# ---------------------------------------------------------------------------
# (c) an extraction with NO_DICTIONARY_ENTRY residue produces a Claim
#     tiered Open -- never silently promoted to a stronger tier.
# ---------------------------------------------------------------------------

def test_no_dictionary_entry_term_produces_open_claim():
    issue = Issue(question="irrelevant", terms=["quantum_flapdoodle"])
    extraction = run_omega_all(issue)

    claims = Claim.from_extraction(extraction)
    term_claims = [c for c in claims if c.predicate == "NO_DICTIONARY_ENTRY"]
    assert len(term_claims) == 1
    claim = term_claims[0]
    assert claim.tier == OPEN_TIER
    assert claim.bridge_class == OPEN_BRIDGE_CLASS
    assert claim.tier == "Open"  # exact tag, no stronger tier silently applied


# ---------------------------------------------------------------------------
# (d) round-trip: a Claim serializes to dict/JSON and back without data
#     loss.
# ---------------------------------------------------------------------------

def test_claim_round_trips_through_dict_and_json():
    original = Claim(
        id="claim:term:cause",
        predicate="TRANSLATED",
        arguments=["cause", "a load-bearing retained relation"],
        quantifier="forall",
        scope="for all r",
        tier="finite_diagnostic",
        bridge_class="DERIVED",
        dependencies=["claim:term:tension"],
    )

    # dict round-trip
    as_dict = original.to_dict()
    rebuilt_from_dict = Claim.from_dict(as_dict)
    assert rebuilt_from_dict == original

    # JSON round-trip
    as_json = original.to_json()
    rebuilt_from_json = Claim.from_json(as_json)
    assert rebuilt_from_json == original
    assert rebuilt_from_json.to_dict() == as_dict


def test_claim_rejects_invalid_tier_and_bridge_class_and_quantifier():
    import pytest

    with pytest.raises(ValueError):
        Claim(id="x", predicate="p", tier="NOT_A_REAL_TIER")

    with pytest.raises(ValueError):
        Claim(id="x", predicate="p", tier="Open", bridge_class="NOT_A_REAL_VERDICT_CLASS")

    with pytest.raises(ValueError):
        Claim(id="x", predicate="p", tier="Open", quantifier="maybe")


# ---------------------------------------------------------------------------
# (e) the free-will smoke test: run_omega_all on "does free will exist",
#     terms=["free will"] produces a Claim IR whose tier is Open, not a
#     stronger tier -- the regression case this module exists to get right.
# ---------------------------------------------------------------------------

def test_free_will_smoke_produces_open_claim_not_stronger():
    issue = Issue(question="does free will exist", terms=["free will"])
    extraction = run_omega_all(issue)

    # Sanity: "free will" really has no dictionary entry in this corpus,
    # so this test is exercising the residue path, not a lucky hit.
    residue_terms = [
        row["foreign_term"]
        for row in extraction["translation_table"]
        if row["status"] == "NO_DICTIONARY_ENTRY"
    ]
    assert "free will" in residue_terms

    claims = Claim.from_extraction(extraction)
    free_will_claims = [c for c in claims if "free will" in c.arguments]
    assert len(free_will_claims) == 1
    claim = free_will_claims[0]

    assert claim.tier == "Open"
    assert claim.bridge_class == "OPEN"
    # Regression guard: must never be silently promoted to a stronger tag.
    assert claim.tier not in ("Th_coqc", "finite_diagnostic", "Dr", "fit_calibrated", "definition")
