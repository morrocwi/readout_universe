"""Typed records for the Omega_all runner.

Field names track TRANSLATION_PROTOCOL.md and POSITION.md's own vocabulary
wherever those documents name a field explicitly:

  - "translation table"        -> TRANSLATION_PROTOCOL.md §1 / §2 step 1
  - "posit ledger"              -> POSITION.md §3 item 2 (verdict classes:
                                    DERIVED/FORCED/DEFINITIONAL-RELABEL/
                                    POSITED/BORROWED-SCALE/OPEN)
  - "record inventory"          -> POSITION.md §3 item 3
  - "null-space statement"      -> POSITION.md §3 item 4 / TRANSLATION_PROTOCOL.md
                                    step 6 (identifiability gate)
  - "policy statement" (Pi)     -> POSITION.md §3 item 5
  - "decisive record"           -> POSITION.md §3 item 6
  - "falsifier"                 -> TRANSLATION_PROTOCOL.md step 8 /
                                    POSITION.md §3 item 7
  - "not-checked ledger"        -> POSITION.md §3 item 8

No numeric/factual claim in this module is asserted as settled; every
dataclass below is a container, not a verdict-producer. Verdicts are
produced only by omega/gates.py, and only for the gates that module
actually implements.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


VERDICT_CLASSES = (
    "DERIVED",
    "FORCED",
    "DEFINITIONAL-RELABEL",
    "POSITED",
    "BORROWED-SCALE",
    "OPEN",
)

TIER_TAGS = ("Th_coqc", "finite_diagnostic", "Dr", "Open", "fit_calibrated", "definition")

# Th -> Dr collapse set (TRANSLATION_PROTOCOL.md §2 step 4: "each bridge
# assumption downgrades Th -> Dr"). Any verdict class other than DERIVED or
# FORCED is a bridge assumption and must downgrade an incoming Th_coqc tag.
TIER_PRESERVING_VERDICTS = ("DERIVED", "FORCED")


@dataclass
class Quantity:
    """One named quantity inside an Issue -- the thing a gate reasons about."""

    name: str
    # Free-text description of what this quantity denotes in the foreign
    # (non-translated) vocabulary, e.g. "the universe's expansion rate".
    description: str = ""
    # Optional stated quantifier/scope language attached to a claim about
    # this quantity, e.g. "for all r", "in the limit h->0", "unbounded".
    # This is what gates.py's G2 guard inspects for I1-I4-style language.
    stated_scope: str = ""


@dataclass
class Issue:
    """A question plus its quantities -- the unit of work Omega_all runs on."""

    question: str
    quantities: List[Quantity] = field(default_factory=list)
    # Free terms the asker used, to be looked up in the dictionary at Step 1.
    # If empty, terms are auto-extracted (naively) from `question`.
    terms: List[str] = field(default_factory=list)
    # Optional: a claimed bridge/import for the bridge-audit gate (Step 4),
    # e.g. {"term": "mass", "verdict_class": "DEFINITIONAL-RELABEL",
    #        "incoming_tier": "Th_coqc"}
    bridges: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TranslationRow:
    """One row of the translation table produced at Step 1."""

    foreign_term: str
    our_term: Optional[str]
    notes: str = ""
    status: str = "TRANSLATED"  # or "NO_DICTIONARY_ENTRY"


@dataclass
class GateRecord:
    """The JSON record a single gate returns."""

    gate: str
    status: str  # "RUN" | "NOT_IMPLEMENTED"
    result: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractionResult:
    """The one JSON Extraction object run_omega_all returns.

    Populates the 8 items POSITION.md §3 names as "maximal extraction" for
    one issue, using only the gates that are actually implemented; every
    item this runner cannot compute is filled from the not-checked ledger
    instead of guessed.
    """

    issue_question: str
    translation_table: List[TranslationRow] = field(default_factory=list)
    posit_ledger: List[Dict[str, Any]] = field(default_factory=list)
    record_inventory: Dict[str, Any] = field(default_factory=dict)
    null_space_statement: str = "NOT_CHECKED"
    policy_statement: str = "NOT_CHECKED"
    decisive_record: str = "NOT_CHECKED"
    falsifier: str = "NOT_CHECKED"
    not_checked_ledger: List[Dict[str, str]] = field(default_factory=list)
    gate_records: List[GateRecord] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issue_question": self.issue_question,
            "translation_table": [vars(r) for r in self.translation_table],
            "posit_ledger": self.posit_ledger,
            "record_inventory": self.record_inventory,
            "null_space_statement": self.null_space_statement,
            "policy_statement": self.policy_statement,
            "decisive_record": self.decisive_record,
            "falsifier": self.falsifier,
            "not_checked_ledger": self.not_checked_ledger,
            "gate_records": [
                {"gate": g.gate, "status": g.status, "result": g.result}
                for g in self.gate_records
            ],
        }
