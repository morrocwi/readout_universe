"""Structural tests for the bilingual RC clinical seed builder.

These tests validate count/balance/status only.  They do NOT validate semantic
quality or rival validity; those require independent human annotation.
"""

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "benchmarks" / "rc_clinical_th_en" / "build_seed_100.py"


def _load_builder():
    spec = importlib.util.spec_from_file_location("rc_clinical_seed_builder", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_seed_builder_returns_exactly_100_bilingual_draft_items():
    items = _load_builder().build()
    assert len(items) == 100
    assert all(item["source_en"] and item["source_th"] for item in items)
    assert all(item["claim_en"] and item["claim_th"] for item in items)
    assert all(item["rival_en"] and item["rival_th"] for item in items)
    assert all(item["construction_status"] == "DRAFT_SYNTHETIC" for item in items)
    assert all(item["annotation_status"] == "NEEDS_HUMAN_ADJUDICATION" for item in items)


def test_seed_balance_is_40_licensed_40_not_identified_20_unsupported():
    items = _load_builder().build()
    counts = {
        label: sum(item["gold_provisional"] == label for item in items)
        for label in ("LICENSED", "NOT_IDENTIFIED", "UNSUPPORTED")
    }
    assert counts == {
        "LICENSED": 40,
        "NOT_IDENTIFIED": 40,
        "UNSUPPORTED": 20,
    }


def test_seed_ids_are_unique_and_rivals_are_not_empty_or_identical_to_claims():
    items = _load_builder().build()
    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids))
    for item in items:
        assert item["claim_en"] != item["rival_en"]
        assert item["claim_th"] != item["rival_th"]
        assert item["rival_type"]
