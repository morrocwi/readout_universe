"""Real, executable tests for the Omega_all runner (omega/).

Run with: python3 -m pytest omega/ tests/test_omega_all.py -q
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from omega.dictionary import lookup, NO_ENTRY_STATUS
from omega.gates import step1_translate, step4_bridge_audit, g2_omega_infinity, STUB_GATES
from omega.schemas import Issue, Quantity
from omega.run import run_omega_all


# ---------------------------------------------------------------------------
# (a) a term WITH a dictionary entry translates correctly
# ---------------------------------------------------------------------------

def test_dictionary_hit_translates_correctly():
    result = lookup("cause")
    assert result["status"] == "translated"
    assert result["our_term"] == (
        "a load-bearing retained relation (removing it moves the readout)"
    )
    assert result["source"] == "v2/TRANSLATION_PROTOCOL.md §1"


def test_step1_translate_gate_on_mapped_term():
    issue = Issue(question="What is the cause of this tension?", terms=["cause", "tension"])
    out = step1_translate(issue)
    assert out["status"] == "RUN"
    rows = {r["foreign_term"]: r for r in out["result"]["translation_table"]}
    assert rows["cause"]["status"] == "TRANSLATED"
    assert rows["cause"]["our_term"].startswith("a load-bearing retained relation")
    assert rows["tension"]["status"] == "TRANSLATED"
    assert out["result"]["residue"] == []


# ---------------------------------------------------------------------------
# (b) a term WITHOUT a dictionary entry returns the honest no-entry result
# ---------------------------------------------------------------------------

def test_dictionary_miss_is_honest_not_a_guess():
    result = lookup("quantum_flapdoodle")
    assert result["status"] == NO_ENTRY_STATUS
    assert "flag" in result
    assert "our_term" not in result  # never fabricated


def test_step1_translate_gate_flags_unmapped_term():
    issue = Issue(question="irrelevant", terms=["quantum_flapdoodle"])
    out = step1_translate(issue)
    rows = out["result"]["translation_table"]
    assert len(rows) == 1
    assert rows[0]["status"] == "NO_DICTIONARY_ENTRY"
    assert rows[0]["our_term"] is None
    assert out["result"]["residue"] == ["quantum_flapdoodle"]


# ---------------------------------------------------------------------------
# (c) bridge-audit gate downgrades a DEFINITIONAL-RELABEL bridge Th -> Dr
# ---------------------------------------------------------------------------

def test_bridge_audit_downgrades_definitional_relabel():
    issue = Issue(
        question="irrelevant",
        bridges=[
            {"term": "mass", "verdict_class": "DEFINITIONAL-RELABEL", "incoming_tier": "Th_coqc"}
        ],
    )
    out = step4_bridge_audit(issue)
    record = out["result"]["bridges"][0]
    assert record["verdict_class"] == "DEFINITIONAL-RELABEL"
    assert record["incoming_tier"] == "Th_coqc"
    assert record["downgraded"] is True
    assert record["resulting_tier"] == "Dr"


def test_bridge_audit_preserves_tier_for_derived_or_forced():
    issue = Issue(
        question="irrelevant",
        bridges=[
            {"term": "L_R", "verdict_class": "FORCED", "incoming_tier": "Th_coqc"},
            {"term": "space", "verdict_class": "DERIVED", "incoming_tier": "Th_coqc"},
        ],
    )
    out = step4_bridge_audit(issue)
    for record in out["result"]["bridges"]:
        assert record["downgraded"] is False
        assert record["resulting_tier"] == "Th_coqc"


# ---------------------------------------------------------------------------
# (d) unbounded/I1-I4-style language is correctly flagged by G2
# ---------------------------------------------------------------------------

def test_g2_flags_unbounded_language():
    issue = Issue(
        question="Does this hold for all possible values, unbounded, at the limit?",
    )
    out = g2_omega_infinity(issue)
    assert out["status"] == "RUN"
    assert out["result"]["injected"] is True
    codes = {f["code"] for f in out["result"]["flags"]}
    assert "I4" in codes


def test_g2_flags_scope_on_quantity():
    issue = Issue(
        question="Compare two rates.",
        quantities=[Quantity(name="rate", stated_scope="infinitely divisible, h->0")],
    )
    out = g2_omega_infinity(issue)
    codes = {f["code"] for f in out["result"]["flags"]}
    assert "I2" in codes


def test_g2_no_false_positive_on_bounded_language():
    issue = Issue(question="What is the mass of this specific object measured today?")
    out = g2_omega_infinity(issue)
    assert out["result"]["injected"] is False
    assert out["result"]["flags"] == []


# ---------------------------------------------------------------------------
# (e) run_omega_all returns valid JSON matching the schema, not-checked
#     ledger populated for un-implemented gates
# ---------------------------------------------------------------------------

def test_run_omega_all_returns_valid_json_with_not_checked_ledger():
    issue = Issue(
        question="Why do two rival measurements disagree, for all datasets, unbounded?",
        terms=["error", "tension"],
        bridges=[
            {"term": "mass", "verdict_class": "POSITED", "incoming_tier": "Th_coqc"},
        ],
    )
    extraction = run_omega_all(issue)

    # Must be JSON-serializable (this IS the schema check: round-trip it).
    serialized = json.dumps(extraction)
    reloaded = json.loads(serialized)
    assert reloaded["issue_question"] == issue.question

    # Required top-level fields (POSITION.md §3's 8 items).
    for field_name in [
        "translation_table",
        "posit_ledger",
        "record_inventory",
        "null_space_statement",
        "policy_statement",
        "decisive_record",
        "falsifier",
        "not_checked_ledger",
        "gate_records",
    ]:
        assert field_name in extraction, f"missing field: {field_name}"

    # Translation table populated from implemented step1 gate.
    assert len(extraction["translation_table"]) == 2

    # Posit ledger populated from implemented step4 gate, and shows the
    # Th->Dr downgrade for the POSITED bridge.
    assert extraction["posit_ledger"][0]["downgraded"] is True
    assert extraction["posit_ledger"][0]["resulting_tier"] == "Dr"

    # Un-implemented items are explicitly NOT_CHECKED, never guessed.
    assert extraction["null_space_statement"] == "NOT_CHECKED"
    assert extraction["policy_statement"] == "NOT_CHECKED"
    assert extraction["decisive_record"] == "NOT_CHECKED"
    assert extraction["falsifier"] == "NOT_CHECKED"

    # not_checked_ledger must name every stub gate (G1, G3-G13).
    ledger_items = " ".join(entry["item"] for entry in extraction["not_checked_ledger"])
    for stub_name in STUB_GATES.keys():
        assert f"gate {stub_name}" in ledger_items

    # gate_records must include every implemented + stub gate, and no stub
    # gate is fabricating a RUN/PASS status.
    statuses_by_gate = {g["gate"]: g["status"] for g in extraction["gate_records"]}
    assert statuses_by_gate["step1_translate"] == "RUN"
    assert statuses_by_gate["step4_bridge_audit"] == "RUN"
    assert statuses_by_gate["g2_omega_infinity"] == "RUN"
    for stub_name in STUB_GATES.keys():
        assert statuses_by_gate[stub_name] == "NOT_IMPLEMENTED"


def test_run_omega_all_no_bridges_no_fabricated_posit_ledger():
    issue = Issue(question="A question with no declared bridges.")
    extraction = run_omega_all(issue)
    assert extraction["posit_ledger"] == []
    reasons = [e["reason"] for e in extraction["not_checked_ledger"]]
    assert any("no bridges to audit" in r for r in reasons)
