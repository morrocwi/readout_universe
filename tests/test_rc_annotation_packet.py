"""Regression tests for blinded bilingual RC annotation packets."""

import importlib.util
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "benchmarks"
    / "rc_clinical_th_en"
    / "make_annotation_packet.py"
)


def _load_builder():
    spec = importlib.util.spec_from_file_location("rc_annotation_packet", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_packets_are_100_items_each_and_gold_is_blinded():
    module = _load_builder()
    packets = module.build_packets()
    assert len(packets["en"]) == 100
    assert len(packets["th"]) == 100
    assert len(packets["key"]) == 100

    for packet_name in ("en", "th"):
        for row in packets[packet_name]:
            assert "gold_provisional" not in row
            assert "adjudicated_label" not in row
            assert row["source"]
            assert row["claim"]
            assert row["rival"]


def test_language_packet_orders_are_independent_but_cover_same_items():
    packets = _load_builder().build_packets()
    en_ids = [row["item_id"] for row in packets["en"]]
    th_ids = [row["item_id"] for row in packets["th"]]
    assert set(en_ids) == set(th_ids)
    assert en_ids != th_ids


def test_packet_builder_is_deterministic_for_declared_seeds():
    module = _load_builder()
    p1 = module.build_packets(seed_en=1701, seed_th=2903)
    p2 = module.build_packets(seed_en=1701, seed_th=2903)
    assert p1["en"] == p2["en"]
    assert p1["th"] == p2["th"]
    assert p1["key"] == p2["key"]


def test_adjudication_key_is_separate_and_contains_provisional_labels():
    packets = _load_builder().build_packets()
    assert all(row["gold_provisional"] in {"LICENSED", "NOT_IDENTIFIED", "UNSUPPORTED"}
               for row in packets["key"])
    assert all("source" not in row and "claim" not in row and "rival" not in row
               for row in packets["key"])
