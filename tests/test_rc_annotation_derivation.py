"""Tests for deterministic RC label derivation and disagreement routing."""

import importlib.util
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "benchmarks"
    / "rc_clinical_th_en"
    / "derive_annotation_labels.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location("rc_annotation_labels", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _row(item_id="x", claim="yes", rival="no", quality="acceptable"):
    return {
        "item_id": item_id,
        "claim_compatible_with_source": claim,
        "rival_compatible_with_source": rival,
        "rival_quality": quality,
    }


def test_label_derivation_matches_rc_semantic_rule():
    m = _load_module()
    assert m.derive_one(_row(claim="yes", rival="no")).derived_label == "LICENSED"
    assert m.derive_one(_row(claim="yes", rival="yes")).derived_label == "NOT_IDENTIFIED"
    assert m.derive_one(_row(claim="no", rival="yes")).derived_label == "UNSUPPORTED"
    assert m.derive_one(_row(claim="no", rival="no")).derived_label == "UNSUPPORTED"


def test_unclear_or_missing_judgment_goes_to_adjudication_not_guessing():
    m = _load_module()
    assert m.derive_one(_row(claim="unclear", rival="yes")).derived_label == "NEEDS_ADJUDICATION"
    assert m.derive_one(_row(claim="yes", rival="unclear")).derived_label == "NEEDS_ADJUDICATION"
    assert m.derive_one(_row(claim="", rival="no")).derived_label == "NEEDS_ADJUDICATION"


def test_weak_or_invalid_rival_blocks_scoring():
    m = _load_module()
    assert m.derive_one(_row(quality="weak")).derived_label == "RIVAL_REPAIR_REQUIRED"
    assert m.derive_one(_row(quality="invalid")).derived_label == "RIVAL_REPAIR_REQUIRED"


def test_two_annotator_disagreement_is_never_auto_resolved():
    m = _load_module()
    a = [_row("item-1", claim="yes", rival="no")]
    b = [_row("item-1", claim="yes", rival="yes")]
    comparison = m.compare_two_annotators(a, b)
    assert comparison == [
        {
            "item_id": "item-1",
            "annotator_a_label": "LICENSED",
            "annotator_b_label": "NOT_IDENTIFIED",
            "agreement": "no",
            "adjudication_required": "yes",
        }
    ]
