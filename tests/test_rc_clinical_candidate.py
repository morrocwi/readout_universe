"""Quality guards for the curated RC clinical annotation candidate.

These are still structural guards, not semantic validation.  Human rival
annotation/adjudication remains mandatory before any benchmark claim.
"""

import importlib.util
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "benchmarks"
    / "rc_clinical_th_en"
    / "curate_seed_100.py"
)


def _load_curator():
    spec = importlib.util.spec_from_file_location("rc_clinical_curator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_curated_candidate_has_100_unique_noncosmetic_triples():
    items = _load_curator().curate()
    assert len(items) == 100

    triples_en = [(x["source_en"], x["claim_en"], x["rival_en"]) for x in items]
    triples_th = [(x["source_th"], x["claim_th"], x["rival_th"]) for x in items]
    assert len(triples_en) == len(set(triples_en))
    assert len(triples_th) == len(set(triples_th))

    assert all("synthetic variant" not in x["source_en"].lower() for x in items)
    assert all("ตัวอย่างสังเคราะห์" not in x["source_th"] for x in items)


def test_curated_candidate_preserves_balance_and_requires_human_adjudication():
    items = _load_curator().curate()
    counts = {
        label: sum(x["gold_provisional"] == label for x in items)
        for label in ("LICENSED", "NOT_IDENTIFIED", "UNSUPPORTED")
    }
    assert counts == {"LICENSED": 40, "NOT_IDENTIFIED": 40, "UNSUPPORTED": 20}
    assert all(x["annotation_status"] == "NEEDS_HUMAN_ADJUDICATION" for x in items)
    assert all(x["adjudicated_label"] is None for x in items)


def test_annotation_fields_are_present_but_not_fabricated():
    items = _load_curator().curate()
    required = {
        "rival_quality_r1",
        "rival_quality_r2",
        "rival_quality_r3",
        "rival_quality_r4",
        "claim_compatible_annotator_1",
        "rival_compatible_annotator_1",
        "claim_compatible_annotator_2",
        "rival_compatible_annotator_2",
        "translation_equivalence",
        "adjudicated_label",
        "adjudication_rationale",
    }
    for item in items:
        assert required <= set(item)
        assert item["adjudicated_label"] is None
