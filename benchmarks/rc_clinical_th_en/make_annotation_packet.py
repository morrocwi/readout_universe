"""Build blinded human-annotation packets from the curated RC clinical seed.

The annotator-facing files intentionally OMIT ``gold_provisional`` and all
internal author labels.  Annotators judge compatibility and rival quality
first; RC labels are derived only after adjudication.

Outputs (all local/generated; do not treat as validated data):

    annotation_en.csv
    annotation_th.csv
    adjudication_key.csv

The two language packets use independently shuffled item order under declared
seeds so annotators do not mechanically align rows across languages.  The
adjudication key is for project owners/adjudicators, not annotators.
"""

from __future__ import annotations

import csv
import importlib.util
import random
from pathlib import Path
from typing import Dict, Iterable, List

HERE = Path(__file__).resolve().parent
CURATOR = HERE / "curate_seed_100.py"

ANNOTATOR_FIELDS = [
    "item_id",
    "domain",
    "source",
    "claim",
    "rival",
    "rival_type",
    "r1_semantically_distinct",
    "r2_materially_relevant",
    "r3_rival_compatible_with_source",
    "r4_epistemically_material_distinction",
    "claim_compatible_with_source",
    "rival_compatible_with_source",
    "rival_quality",
    "translation_equivalence",
    "annotator_id",
    "annotator_rationale",
]

KEY_FIELDS = [
    "item_id",
    "domain",
    "rival_type",
    "gold_provisional",
    "construction_status",
    "annotation_status",
]


def _load_curator():
    spec = importlib.util.spec_from_file_location("rc_curator", CURATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _packet_rows(items: Iterable[Dict], lang: str, seed: int) -> List[Dict]:
    if lang not in {"en", "th"}:
        raise ValueError("lang must be 'en' or 'th'")

    rows = []
    for item in items:
        rows.append(
            {
                "item_id": item["id"],
                "domain": item["domain"],
                "source": item[f"source_{lang}"],
                "claim": item[f"claim_{lang}"],
                "rival": item[f"rival_{lang}"],
                "rival_type": item["rival_type"],
                "r1_semantically_distinct": "",
                "r2_materially_relevant": "",
                "r3_rival_compatible_with_source": "",
                "r4_epistemically_material_distinction": "",
                "claim_compatible_with_source": "",
                "rival_compatible_with_source": "",
                "rival_quality": "",
                "translation_equivalence": "",
                "annotator_id": "",
                "annotator_rationale": "",
            }
        )

    rng = random.Random(seed)
    rng.shuffle(rows)
    return rows


def _write_csv(path: Path, fieldnames: List[str], rows: Iterable[Dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_packets(seed_en: int = 1701, seed_th: int = 2903) -> Dict[str, List[Dict]]:
    items = _load_curator().curate()
    en = _packet_rows(items, "en", seed_en)
    th = _packet_rows(items, "th", seed_th)
    key = [
        {field: item[field if field != "item_id" else "id"] for field in KEY_FIELDS}
        for item in items
    ]

    # Guard against accidental gold leakage into annotator packets.
    forbidden = {"gold_provisional", "adjudicated_label"}
    assert not (forbidden & set(ANNOTATOR_FIELDS))
    assert all(not (forbidden & set(row)) for row in en)
    assert all(not (forbidden & set(row)) for row in th)

    return {"en": en, "th": th, "key": key}


def main() -> None:
    packets = build_packets()
    _write_csv(HERE / "annotation_en.csv", ANNOTATOR_FIELDS, packets["en"])
    _write_csv(HERE / "annotation_th.csv", ANNOTATOR_FIELDS, packets["th"])
    _write_csv(HERE / "adjudication_key.csv", KEY_FIELDS, packets["key"])
    print("wrote blinded EN/TH annotation packets and separate adjudication key")


if __name__ == "__main__":
    main()
