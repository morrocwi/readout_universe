"""Claim IR (Intermediate Representation) -- a small, typed layer on top of
one omega/run.py ExtractionResult that turns its translation_table and
posit_ledger rows into a list of `Claim` objects a downstream consumer can
walk (dependencies, tier, bridge_class) without re-parsing the raw
Extraction JSON shape.

This module does NOT invent a second tier system or a second Th_coqc->Dr
downgrade rule. `Claim.tier` for a bridge-derived claim is always produced
by calling gates.py::step4_bridge_audit -- the one place that rule is
implemented -- never by re-deriving "verdict_class != DERIVED/FORCED ->
downgrade Th_coqc -> Dr" a second time in this file. If that rule ever
changes in gates.py, this module changes with it for free.

Similarly, a translation_table row with status "NO_DICTIONARY_ENTRY" (i.e.
the term resisted step1_translate's dictionary lookup) always produces a
Claim tiered "Open" with bridge_class "OPEN" -- an untranslated term is
never silently promoted to a stronger tier just because it appears in a
claim.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from .gates import step4_bridge_audit
from .schemas import Issue, TIER_TAGS, VERDICT_CLASSES

QUANTIFIERS = ("exists", "forall", "none")

# The tier a claim gets when its source term has no dictionary entry at all
# (TRANSLATION_PROTOCOL.md §1's own rule: an untranslated term is [Open]/
# POSITED, not guessed into something stronger).
OPEN_TIER = "Open"
OPEN_BRIDGE_CLASS = "OPEN"


@dataclass
class Claim:
    """One claim in the Claim IR.

    Fields:
      id           -- unique string id for this claim.
      predicate    -- the claim's predicate/status word, e.g. "TRANSLATED",
                       "NO_DICTIONARY_ENTRY", "BRIDGE".
      arguments    -- ordered list of the predicate's arguments (free-form,
                       JSON-serializable values -- term names, our_term
                       strings, etc).
      quantifier   -- one of "exists" | "forall" | "none".
      scope        -- free-text scope/quantifier language (mirrors
                       Quantity.stated_scope in schemas.py), "" if none.
      tier         -- must be one of schemas.TIER_TAGS.
      bridge_class -- must be one of schemas.VERDICT_CLASSES, or None.
      dependencies -- list of other Claim ids this claim relies on.
    """

    id: str
    predicate: str
    arguments: List[Any] = field(default_factory=list)
    quantifier: str = "none"
    scope: str = ""
    tier: str = OPEN_TIER
    bridge_class: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.quantifier not in QUANTIFIERS:
            raise ValueError(
                f"Claim.quantifier {self.quantifier!r} not in {QUANTIFIERS}"
            )
        if self.tier not in TIER_TAGS:
            raise ValueError(f"Claim.tier {self.tier!r} not in schemas.TIER_TAGS {TIER_TAGS}")
        if self.bridge_class is not None and self.bridge_class not in VERDICT_CLASSES:
            raise ValueError(
                f"Claim.bridge_class {self.bridge_class!r} not in "
                f"schemas.VERDICT_CLASSES {VERDICT_CLASSES} (or None)"
            )

    # -- round-trip: dict / JSON -------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Claim":
        return cls(
            id=data["id"],
            predicate=data["predicate"],
            arguments=list(data.get("arguments", [])),
            quantifier=data.get("quantifier", "none"),
            scope=data.get("scope", ""),
            tier=data.get("tier", OPEN_TIER),
            bridge_class=data.get("bridge_class"),
            dependencies=list(data.get("dependencies", [])),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> "Claim":
        return cls.from_dict(json.loads(text))

    # -- construction from an ExtractionResult -----------------------------

    @classmethod
    def from_extraction(cls, extraction_result: Dict[str, Any]) -> List["Claim"]:
        """Build the list of Claims implied by one Extraction dict (the JSON
        shape omega/run.py::run_omega_all / ExtractionResult.to_dict()
        produces -- translation_table + posit_ledger).

        - One Claim per translation_table row. A row with
          status == "NO_DICTIONARY_ENTRY" always gets tier "Open" and
          bridge_class "OPEN" -- never a stronger tier.
        - One Claim per posit_ledger row (declared bridge). Its tier is
          computed by re-running gates.py::step4_bridge_audit on the
          extraction's own posit_ledger rows (the one place the
          Th_coqc -> Dr downgrade rule lives), not by a second copy of
          that rule here.
        - A bridge Claim depends on the translation Claim for the same
          term, when that term also appears in translation_table.
        """

        claims: List[Claim] = []
        term_claim_id: Dict[str, str] = {}

        translation_table = extraction_result.get("translation_table", [])

        # tier for a TRANSLATED row is carried on the step1_translate gate
        # record's raw result (ExtractionResult.translation_table entries
        # themselves drop the "tier" key -- see schemas.TranslationRow),
        # so pull it back from gate_records rather than guessing a tier.
        tier_by_term: Dict[str, Optional[str]] = {}
        for gate_record in extraction_result.get("gate_records", []):
            if gate_record.get("gate") == "step1_translate":
                for row in gate_record.get("result", {}).get("translation_table", []):
                    tier_by_term[row["foreign_term"]] = row.get("tier")

        for row in translation_table:
            foreign_term = row["foreign_term"]
            status = row.get("status", "NO_DICTIONARY_ENTRY")
            claim_id = f"claim:term:{foreign_term}"

            if status == "NO_DICTIONARY_ENTRY":
                claim = cls(
                    id=claim_id,
                    predicate="NO_DICTIONARY_ENTRY",
                    arguments=[foreign_term],
                    quantifier="none",
                    scope="",
                    tier=OPEN_TIER,
                    bridge_class=OPEN_BRIDGE_CLASS,
                    dependencies=[],
                )
            else:
                tier = tier_by_term.get(foreign_term) or "definition"
                if tier not in TIER_TAGS:
                    # Never guess a stronger tag than the corpus stated;
                    # fall back to the weakest honest tag instead of
                    # crashing on an unexpected tier string.
                    tier = "definition"
                claim = cls(
                    id=claim_id,
                    predicate="TRANSLATED",
                    arguments=[foreign_term, row.get("our_term")],
                    quantifier="none",
                    scope="",
                    tier=tier,
                    bridge_class=None,
                    dependencies=[],
                )

            claims.append(claim)
            term_claim_id[foreign_term] = claim_id

        # --- bridge claims: reuse gates.py::step4_bridge_audit verbatim ---
        posit_ledger = extraction_result.get("posit_ledger", [])
        if posit_ledger:
            bridge_issue = Issue(question="", bridges=posit_ledger)
            bridge_out = step4_bridge_audit(bridge_issue)
            for record in bridge_out["result"]["bridges"]:
                term = record.get("term", "<unnamed>")
                resulting_tier = record.get("resulting_tier")
                valid = record.get("valid_verdict_class", False)
                verdict_class = record.get("verdict_class")

                tier = resulting_tier if resulting_tier in TIER_TAGS else OPEN_TIER
                bridge_class = verdict_class if valid and verdict_class in VERDICT_CLASSES else None

                deps = [term_claim_id[term]] if term in term_claim_id else []

                claims.append(
                    cls(
                        id=f"claim:bridge:{term}",
                        predicate="BRIDGE",
                        arguments=[term],
                        quantifier="none",
                        scope="",
                        tier=tier,
                        bridge_class=bridge_class,
                        dependencies=deps,
                    )
                )

        return claims


__all__ = ["Claim", "QUANTIFIERS", "OPEN_TIER", "OPEN_BRIDGE_CLASS"]
