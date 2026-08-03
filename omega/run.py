"""run_omega_all -- executes the implemented gates, in Omega_all's own
8-step order (TRANSLATION_PROTOCOL.md §2), against one Issue and returns a
single JSON Extraction object.

Only steps 1, 2 (G2 half), and 4 have real logic (see gates.py). Every
other step/gate is recorded honestly in the not_checked_ledger, per
POSITION.md §3's own rule: "ทุกอย่างที่ SKIPPED + เหตุผล" (everything
skipped + reason) -- "silent omission reads as coverage = lying by layout."
"""

from __future__ import annotations

import json
from typing import Any, Dict

from .gates import (
    step1_translate,
    step4_bridge_audit,
    g2_omega_infinity,
    STUB_GATES,
)
from .schemas import Issue, ExtractionResult, GateRecord, TranslationRow


def run_omega_all(issue: Issue) -> Dict[str, Any]:
    result = ExtractionResult(issue_question=issue.question)

    # --- Step 1: TRANSLATE ------------------------------------------------
    step1 = step1_translate(issue)
    result.gate_records.append(GateRecord(**step1))
    for row in step1["result"]["translation_table"]:
        result.translation_table.append(
            TranslationRow(
                foreign_term=row["foreign_term"],
                our_term=row["our_term"],
                notes=row["notes"] or "",
                status=row["status"],
            )
        )
    if step1["result"]["residue"]:
        result.not_checked_ledger.append(
            {
                "item": "translation residue",
                "reason": (
                    "terms with no dictionary entry: "
                    f"{step1['result']['residue']} -- flagged [Open]/POSITED, "
                    "not guessed"
                ),
            }
        )

    # --- Step 2 (G2 half): Omega_infinity guard ---------------------------
    g2 = g2_omega_infinity(issue)
    result.gate_records.append(GateRecord(**g2))
    if not g2["result"]["flags"]:
        result.not_checked_ledger.append(
            {
                "item": "G2 injected-infinity semantic judgment",
                "reason": (
                    "keyword guard found no trigger phrase; this is not a "
                    "proof the question is infinity-free (grammar-gate "
                    "well-formedness judgment beyond keyword matching is "
                    "not implemented)"
                ),
            }
        )

    # --- Step 3: Locate -- NOT IMPLEMENTED --------------------------------
    result.not_checked_ledger.append(
        {"item": "Step 3 (Locate: tau_c / step / policy Pi)", "reason": "not implemented"}
    )

    # --- Step 4: Bridge audit ----------------------------------------------
    step4 = step4_bridge_audit(issue)
    result.gate_records.append(GateRecord(**step4))
    result.posit_ledger = step4["result"]["bridges"]
    if not issue.bridges:
        result.not_checked_ledger.append(
            {
                "item": "posit ledger",
                "reason": "issue declared no bridges to audit (empty issue.bridges)",
            }
        )

    # --- Step 5: Residual form -- NOT IMPLEMENTED --------------------------
    result.not_checked_ledger.append(
        {"item": "Step 5 (residual form r, W)", "reason": "not implemented"}
    )

    # --- Step 6: Identifiability gate (G5) -- NOT IMPLEMENTED --------------
    result.not_checked_ledger.append(
        {
            "item": "Step 6 / G5 (identifiability, null-space statement)",
            "reason": "not implemented -- null_space_statement left NOT_CHECKED",
        }
    )

    # --- Step 7: Answer with tag -- NOT IMPLEMENTED -------------------------
    result.not_checked_ledger.append(
        {"item": "Step 7 (tagged answer)", "reason": "not implemented"}
    )

    # --- Step 8: Translate back + falsifier -- NOT IMPLEMENTED --------------
    result.not_checked_ledger.append(
        {
            "item": "Step 8 (translate back + falsifier)",
            "reason": "not implemented -- falsifier left NOT_CHECKED",
        }
    )

    # policy_statement / decisive_record / record_inventory: not computed by
    # any implemented gate (G4, G6, G5 record-inventory half are stubs).
    result.not_checked_ledger.append(
        {
            "item": "policy_statement (Pi / G4)",
            "reason": "G4 (Pi/selection gate) not implemented",
        }
    )
    result.not_checked_ledger.append(
        {
            "item": "decisive_record (G6)",
            "reason": "G6 (load-bearing discard gate) not implemented",
        }
    )
    result.not_checked_ledger.append(
        {
            "item": "record_inventory",
            "reason": "no implemented gate computes a record inventory",
        }
    )

    # --- Run every stub gate too, honestly, so the extraction's gate_records
    # list reflects the full G1-G13 table without fabricating a verdict.
    for name, stub_fn in STUB_GATES.items():
        stub_result = stub_fn(issue)
        result.gate_records.append(GateRecord(**stub_result))
        result.not_checked_ledger.append(
            {"item": f"gate {name}", "reason": "NOT_IMPLEMENTED"}
        )

    return result.to_dict()


def run_omega_all_json(issue: Issue) -> str:
    """Convenience wrapper: run_omega_all, serialized to a JSON string."""

    return json.dumps(run_omega_all(issue), indent=2, ensure_ascii=False)
