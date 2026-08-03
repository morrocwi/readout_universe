"""Gate implementations for Omega_all.

Only three gates have real logic behind them, per the build brief:

  - step1_translate   -- TRANSLATION_PROTOCOL.md §2 step 1 (dictionary
                          lookup, flags unmapped terms per the corpus's own
                          [Open]/POSITED rule instead of guessing).
  - step4_bridge_audit -- TRANSLATION_PROTOCOL.md §2 step 4 (assigns a
                          verdict class to each imported bridge; downgrades
                          an incoming Th_coqc tag to Dr whenever the verdict
                          class is anything other than DERIVED or FORCED).
  - g2_omega_infinity  -- POSITION.md G2 / philosophy.md §2.5's I1-I4/Z1-Z4
                          dual guard: flags unbounded/completeness-style
                          quantifier language in a claim's stated scope.

Every other named gate (G1, G3-G13) is a stub that returns
{"status": "NOT_IMPLEMENTED"}. This module never fabricates a PASS/verdict
for a gate it has not actually built logic for -- that is the whole point
of this file existing separately from a "looks complete" mock.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

from .dictionary import lookup as dict_lookup, DICTIONARY, I_TAXONOMY, Z_TAXONOMY
from .schemas import Issue, TranslationRow, VERDICT_CLASSES, TIER_PRESERVING_VERDICTS


# ---------------------------------------------------------------------------
# Step 1 -- TRANSLATE
# ---------------------------------------------------------------------------

def _auto_detect_terms(question: str) -> List[str]:
    """Deterministic substring scan of the question against known dictionary
    keys -- longest keys first, so e.g. "time (an entity's own)" is not
    shadowed by the shorter "time" key matching first. This does NOT invent
    any mapping; it only decides which already-known keys are present in
    the text.
    """

    q = question.lower()
    found: List[str] = []
    for key in sorted(DICTIONARY.keys(), key=len, reverse=True):
        # skip the taxonomy/RAR/RD synthetic keys for auto-detection --
        # those are looked up explicitly via issue.terms, not scraped from
        # free text, to avoid false-positive substring hits (e.g. "a1").
        if key.startswith("rar ") or key in ("rd4",) or key.upper() in {**I_TAXONOMY, **Z_TAXONOMY}:
            continue
        if key in q and key not in found:
            found.append(key)
    return found


def step1_translate(issue: Issue) -> Dict[str, Any]:
    """Run TRANSLATION_PROTOCOL.md §2 step 1 on an Issue.

    Returns a JSON-serializable dict with the translation_table (list of
    TranslationRow-shaped dicts) and a residue list of terms that resisted
    translation (per the protocol: "Any residue that resists translation is
    itself a finding -- name it and give it a dictionary row + verdict
    class").
    """

    terms = list(issue.terms) if issue.terms else _auto_detect_terms(issue.question)

    rows: List[Dict[str, Any]] = []
    residue: List[str] = []

    for term in terms:
        result = dict_lookup(term)
        if result["status"] == "translated":
            rows.append(
                {
                    "foreign_term": term,
                    "our_term": result["our_term"],
                    "notes": result.get("notes", ""),
                    "tier": result.get("tier"),
                    "source": result.get("source"),
                    "status": "TRANSLATED",
                }
            )
        else:
            rows.append(
                {
                    "foreign_term": term,
                    "our_term": None,
                    "notes": result["flag"],
                    "tier": None,
                    "source": None,
                    "status": "NO_DICTIONARY_ENTRY",
                }
            )
            residue.append(term)

    return {
        "gate": "step1_translate",
        "status": "RUN",
        "result": {
            "translation_table": rows,
            "residue": residue,
            "terms_checked": terms,
        },
    }


# ---------------------------------------------------------------------------
# Step 4 -- BRIDGE AUDIT
# ---------------------------------------------------------------------------

def step4_bridge_audit(issue: Issue) -> Dict[str, Any]:
    """Run TRANSLATION_PROTOCOL.md §2 step 4 on an Issue's declared bridges.

    Each bridge in issue.bridges is a dict like:
        {"term": "mass", "verdict_class": "DEFINITIONAL-RELABEL",
         "incoming_tier": "Th_coqc"}

    A bridge with an unrecognized verdict_class is itself flagged (not
    silently coerced) since the protocol's verdict-class list is closed.
    Every bridge whose verdict_class is NOT in {DERIVED, FORCED} downgrades
    an incoming Th_coqc tag to Dr, per TRANSLATION_PROTOCOL.md §2 step 4:
    "every bridge assumption downgrades Th -> Dr."
    """

    records: List[Dict[str, Any]] = []
    for bridge in issue.bridges:
        term = bridge.get("term", "<unnamed>")
        verdict_class = bridge.get("verdict_class")
        incoming_tier = bridge.get("incoming_tier")

        if verdict_class not in VERDICT_CLASSES:
            records.append(
                {
                    "term": term,
                    "verdict_class": verdict_class,
                    "valid_verdict_class": False,
                    "note": f"'{verdict_class}' is not one of {VERDICT_CLASSES}",
                    "incoming_tier": incoming_tier,
                    "resulting_tier": incoming_tier,
                    "downgraded": False,
                }
            )
            continue

        preserves_tier = verdict_class in TIER_PRESERVING_VERDICTS
        downgraded = incoming_tier == "Th_coqc" and not preserves_tier
        resulting_tier = "Dr" if downgraded else incoming_tier

        records.append(
            {
                "term": term,
                "verdict_class": verdict_class,
                "valid_verdict_class": True,
                "incoming_tier": incoming_tier,
                "resulting_tier": resulting_tier,
                "downgraded": downgraded,
            }
        )

    return {
        "gate": "step4_bridge_audit",
        "status": "RUN",
        "result": {"bridges": records},
    }


# ---------------------------------------------------------------------------
# G2 -- Omega_infinity guard (dual I1-I4 / Z1-Z4)
# ---------------------------------------------------------------------------

# Trigger phrases per philosophy.md §2.5 / ~lines 645-649. Kept intentionally
# literal (no NLP/ML) -- this is a keyword guard, not a semantic classifier,
# and it says so in its own output rather than pretending otherwise.
_I_TRIGGERS = {
    "I1": ["real completeness", "ℝ-completeness", "r-completeness", "completeness of the reals"],
    "I2": ["h->0", "h→0", "infinitely divisible", "infinite divisibility", "infinitesimal"],
    "I3": ["infinite scale separation", "re,Λ->∞", "re->∞", "Λ->∞"],
    "I4": ["actual infinity", "+∞", "infinity", "infinite", "unbounded", "for all", "for every",
           "complete set", "every possible", "always true", "never fails", "at the limit"],
}
_Z_TRIGGERS = {
    "Z1": ["point of zero size", "zero extent", "r=0", "exact point"],
    "Z2": ["exact-zero spacing", "exactly zero spacing", "reached continuum"],
    "Z3": ["absolute rest", "exact vacuum", "v=0", "t=0", "perfectly still"],
    "Z4": ["true void", "absolute nothing", "the true void"],
}


def g2_omega_infinity(issue: Issue) -> Dict[str, Any]:
    """POSITION.md G2: which infinity/idealized-zero was injected into the
    question itself. Scans issue.question and every quantity's stated_scope
    for I1-I4/Z1-Z4 trigger phrases (philosophy.md §2.5).

    This is a keyword guard: it flags candidate injections for a human/
    downstream gate to confirm, it does not itself decide whether the
    injection is load-bearing. Absence of a match is reported honestly as
    "no trigger phrase found" -- not as a proof the question is infinity-free.
    """

    haystacks = [("question", issue.question)]
    for q in issue.quantities:
        if q.stated_scope:
            haystacks.append((f"quantity:{q.name}", q.stated_scope))

    flags: List[Dict[str, str]] = []
    for source_label, text in haystacks:
        lowered = text.lower()
        for code, phrases in {**_I_TRIGGERS, **_Z_TRIGGERS}.items():
            for phrase in phrases:
                if phrase in lowered:
                    taxonomy = I_TAXONOMY if code in I_TAXONOMY else Z_TAXONOMY
                    flags.append(
                        {
                            "source": source_label,
                            "code": code,
                            "meaning": taxonomy[code],
                            "matched_phrase": phrase,
                        }
                    )

    return {
        "gate": "g2_omega_infinity",
        "status": "RUN",
        "result": {
            "flags": flags,
            "injected": len(flags) > 0,
            "note": "keyword guard only; a flag names a candidate injection, "
            "it does not by itself decide the question is ill-formed",
        },
    }


IMPLEMENTED_GATES = {
    "step1_translate": step1_translate,
    "step4_bridge_audit": step4_bridge_audit,
    "g2_omega_infinity": g2_omega_infinity,
}


# ---------------------------------------------------------------------------
# Stubs -- G1, G3-G13 (POSITION.md's gate table)
# ---------------------------------------------------------------------------
# G1 (Translate, gate-table framing) is intentionally a stub distinct from
# step1_translate above: step1_translate implements the protocol's Step-1
# translate action; G1 as a named gate-table entry (with its own PASS/FAIL
# semantics per POSITION.md) has no logic built yet, so it is honestly
# reported as NOT_IMPLEMENTED rather than aliased to step1_translate's
# result.

_STUB_GATE_NAMES = ["G1", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12", "G13"]


def _make_stub(name: str):
    def _stub(issue: Issue) -> Dict[str, Any]:
        return {
            "gate": name,
            "status": "NOT_IMPLEMENTED",
            "result": {},
        }

    _stub.__name__ = f"gate_{name.lower()}_stub"
    return _stub


STUB_GATES: Dict[str, Any] = {name: _make_stub(name) for name in _STUB_GATE_NAMES}

ALL_GATE_NAMES = list(IMPLEMENTED_GATES.keys()) + _STUB_GATE_NAMES
