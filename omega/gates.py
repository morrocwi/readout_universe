"""Gate implementations for Omega_all plus the RC runtime status contract.

Only three legacy Omega gates have real logic behind them:

  - step1_translate
  - step4_bridge_audit
  - g2_omega_infinity

Every other named G1--G13 gate remains an honest ``NOT_IMPLEMENTED`` stub.
Those implementation states are intentionally separate from the new
five-value **RC runtime status** below.  A stub never receives an epistemic
status merely because the enum now exists.

The RC runtime status vocabulary is designed for Human--AI interfaces:

    LICENSED
    AUGMENTED
    PROVENANCE_INCOMPLETE
    NOT_IDENTIFIED
    ABSTAIN

It is a runtime/disposition vocabulary, not a replacement for Claim-IR tiers,
bridge classes, proof verdicts, or the old RUN/NOT_IMPLEMENTED implementation
field.  Conflating those roles would itself be a cross-role readout error.
"""

from __future__ import annotations

from enum import Enum
import re
from typing import Any, Dict, List

from .dictionary import lookup as dict_lookup, DICTIONARY, I_TAXONOMY, Z_TAXONOMY
from .schemas import Issue, TranslationRow, VERDICT_CLASSES, TIER_PRESERVING_VERDICTS


class RCGateStatus(str, Enum):
    """Five runtime statuses exposed by RC-aware Human--AI gates.

    ``LICENSED``
        The asserted distinction is licensed by the represented basis without
        undeclared additional support.
    ``AUGMENTED``
        The distinction is licensed only with additional declared support or
        commitments beyond the focal source.
    ``PROVENANCE_INCOMPLETE``
        A required route, bundle, or attribution is missing/unrecoverable.
    ``NOT_IDENTIFIED``
        Available support leaves the relevant rival compatible.
    ``ABSTAIN``
        Runtime action: withhold a categorical assertion.  This may be the
        correct disposition after NOT_IDENTIFIED, unsupported input, or a
        safety/domain routing rule.

    ABSTAIN is intentionally an action status rather than an epistemic claim.
    The enum is operational: callers should preserve the underlying audit
    record explaining *why* abstention occurred.
    """

    LICENSED = "LICENSED"
    AUGMENTED = "AUGMENTED"
    PROVENANCE_INCOMPLETE = "PROVENANCE_INCOMPLETE"
    NOT_IDENTIFIED = "NOT_IDENTIFIED"
    ABSTAIN = "ABSTAIN"


def rc_runtime_status(
    *,
    separation_verdict: str,
    basis_attribution_ok: bool,
    augmented: bool = False,
    system_abstained: bool = False,
) -> RCGateStatus:
    """Map an RC separation audit to the five-value runtime vocabulary.

    This function does not decide separation itself; ``separation_verdict``
    must come from a real evaluator/gate.  It only converts already-audited
    state into a stable Human--AI runtime status.
    """

    if system_abstained:
        return RCGateStatus.ABSTAIN
    if separation_verdict == "PROVENANCE_INCOMPLETE" or not basis_attribution_ok:
        return RCGateStatus.PROVENANCE_INCOMPLETE
    if separation_verdict in ("NOT_IDENTIFIED", "UNSUPPORTED"):
        return RCGateStatus.NOT_IDENTIFIED
    if separation_verdict == "LICENSED":
        return RCGateStatus.AUGMENTED if augmented else RCGateStatus.LICENSED
    raise ValueError(f"unrecognized separation_verdict: {separation_verdict!r}")


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
        if key.startswith("rar ") or key in ("rd4",) or key.upper() in {**I_TAXONOMY, **Z_TAXONOMY}:
            continue
        if key in q and key not in found:
            found.append(key)
    return found


def step1_translate(issue: Issue) -> Dict[str, Any]:
    """Run TRANSLATION_PROTOCOL.md §2 step 1 on an Issue."""

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
    """Run TRANSLATION_PROTOCOL.md §2 step 4 on declared bridges."""

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
    """Flag candidate infinity/idealized-zero injections; keyword guard only."""

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


__all__ = [
    "RCGateStatus",
    "rc_runtime_status",
    "step1_translate",
    "step4_bridge_audit",
    "g2_omega_infinity",
    "IMPLEMENTED_GATES",
    "STUB_GATES",
    "ALL_GATE_NAMES",
]
