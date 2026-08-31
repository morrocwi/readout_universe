"""Derive RC semantic labels from completed human annotations.

This module deliberately separates *annotation* from *adjudication*.
It never resolves human disagreement automatically and never consults the
seed's ``gold_provisional`` field.

Accepted annotation values (case-insensitive):
    yes / no / unclear

Accepted rival-quality values:
    acceptable / weak / invalid

Derived label rule after rival quality is ACCEPTABLE:

    claim=yes, rival=no   -> LICENSED
    claim=yes, rival=yes  -> NOT_IDENTIFIED
    claim=no              -> UNSUPPORTED
    anything with unclear -> NEEDS_ADJUDICATION

A weak/invalid rival is not scored; the item is sent back for rival repair.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional


YES_NO_UNCLEAR = {"yes", "no", "unclear"}
RIVAL_QUALITY = {"acceptable", "weak", "invalid"}


@dataclass(frozen=True)
class DerivedAnnotation:
    item_id: str
    derived_label: str
    rival_status: str
    reason: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


def _norm(value: Optional[str]) -> str:
    return (value or "").strip().lower()


def derive_one(row: Dict[str, str]) -> DerivedAnnotation:
    item_id = row.get("item_id", "").strip()
    if not item_id:
        raise ValueError("annotation row is missing item_id")

    claim = _norm(row.get("claim_compatible_with_source"))
    rival = _norm(row.get("rival_compatible_with_source"))
    quality = _norm(row.get("rival_quality"))

    if quality not in RIVAL_QUALITY:
        return DerivedAnnotation(
            item_id,
            "NEEDS_ADJUDICATION",
            "RIVAL_QUALITY_MISSING",
            "rival_quality must be acceptable, weak, or invalid",
        )

    if quality in {"weak", "invalid"}:
        return DerivedAnnotation(
            item_id,
            "RIVAL_REPAIR_REQUIRED",
            quality.upper(),
            "semantic scoring is blocked until the rival is repaired and re-annotated",
        )

    if claim not in YES_NO_UNCLEAR or rival not in YES_NO_UNCLEAR:
        return DerivedAnnotation(
            item_id,
            "NEEDS_ADJUDICATION",
            "ACCEPTABLE",
            "compatibility judgments must be yes, no, or unclear",
        )

    if "unclear" in {claim, rival}:
        return DerivedAnnotation(
            item_id,
            "NEEDS_ADJUDICATION",
            "ACCEPTABLE",
            "at least one compatibility judgment is unclear",
        )

    if claim == "no":
        return DerivedAnnotation(
            item_id,
            "UNSUPPORTED",
            "ACCEPTABLE",
            "the asserted claim is not compatible with the source",
        )

    if claim == "yes" and rival == "no":
        return DerivedAnnotation(
            item_id,
            "LICENSED",
            "ACCEPTABLE",
            "the source is compatible with the claim and excludes the rival",
        )

    if claim == "yes" and rival == "yes":
        return DerivedAnnotation(
            item_id,
            "NOT_IDENTIFIED",
            "ACCEPTABLE",
            "the source remains compatible with both the claim and the rival",
        )

    # claim=no, rival values are already covered by the claim=no branch.
    raise AssertionError("unreachable annotation state")


def derive_rows(rows: Iterable[Dict[str, str]]) -> List[DerivedAnnotation]:
    return [derive_one(row) for row in rows]


def compare_two_annotators(
    rows_a: Iterable[Dict[str, str]], rows_b: Iterable[Dict[str, str]]
) -> List[Dict[str, str]]:
    """Compare derived labels by item ID; disagreement is never auto-resolved."""

    a = {x.item_id: x for x in derive_rows(rows_a)}
    b = {x.item_id: x for x in derive_rows(rows_b)}
    if set(a) != set(b):
        missing_a = sorted(set(b) - set(a))
        missing_b = sorted(set(a) - set(b))
        raise ValueError(
            f"annotator item sets differ; missing_from_a={missing_a}, missing_from_b={missing_b}"
        )

    out = []
    for item_id in sorted(a):
        la, lb = a[item_id].derived_label, b[item_id].derived_label
        out.append(
            {
                "item_id": item_id,
                "annotator_a_label": la,
                "annotator_b_label": lb,
                "agreement": "yes" if la == lb else "no",
                "adjudication_required": "no" if la == lb else "yes",
            }
        )
    return out


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


__all__ = [
    "DerivedAnnotation",
    "derive_one",
    "derive_rows",
    "compare_two_annotators",
    "read_csv",
]
