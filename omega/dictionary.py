"""The Omega_all translation dictionary, as data.

Every row below is copied (not invented) from what this corpus already
states, with a source citation per row:

  - The main foreign->our-term table is TRANSLATION_PROTOCOL.md §1
    ("The dictionary (foreign term -> our term)"), restated verbatim in
    philosophy.md §3.
  - RD4 is the one Information-DNA axiom (out of RD1-RD9) this corpus
    names explicitly with content ("distinct histories never merge"),
    philosophy.md §5.1.
  - RAR A1-A8 is the ordered 8-item list philosophy.md §5.1 gives right
    after naming "RAR A1-A8" -- read here as an ordered correspondence
    (A1=first item ... A8=last item), which is how the source presents it,
    tiered `Dr` per the source's own "declared (Dr) correspondence, not yet
    a proven formal unification" caveat.
  - The I1-I4 / Z1-Z4 non-readout taxonomy is philosophy.md §2.5 and
    lines ~645-649 (dual guard used by gate G2).

This module does NOT extend the dictionary with new rows beyond what the
corpus states. A lookup for a term with no row must return an explicit
"no_dictionary_entry" result (see lookup()), never a guess -- this is the
corpus's own rule (TRANSLATION_PROTOCOL.md §1: "A term with no row yet must
be given one ... before use").
"""

from __future__ import annotations

from typing import Any, Dict, Optional, TypedDict


class DictEntry(TypedDict, total=False):
    our_term: str
    notes: str
    tier: str
    source: str


# --- TRANSLATION_PROTOCOL.md §1, the foreign -> our-term table -------------
# Key: lower-cased foreign term exactly as the corpus's left column states
# it (comma-separated synonyms in one row are indexed individually, each
# pointing at the same entry).
_TRANSLATION_TABLE_ROWS = [
    (
        ["thing", "object", "entity"],
        "δ_R-entity — a retained distinction",
        "root term",
    ),
    (
        ["property", "state"],
        "ε — the entity's current configuration read by a grammar",
        "",
    ),
    (
        ["law of nature", "constraint", "mechanism"],
        "a row of the grammar A (an edge/relation of L_R)",
        "",
    ),
    (
        ["data", "observation", "evidence"],
        "δ — the record the world returns",
        "",
    ),
    (
        ["theory", "model", "paradigm"],
        "the grammar A itself; paradigm shift = change of A",
        'Ch. "Philosophy of Science"',
    ),
    (
        ["error", "tension", "anomaly", "disease"],
        "residual r = Aε − δ; its energy V = ½ rᵀWr",
        "",
    ),
    (
        ["explanation", "inference", "healing", "learning"],
        "descent of V (residual flow) at the knower's rate",
        "LTP1 `finite_diagnostic`",
    ),
    (
        ["time (an entity's own)", "time"],
        "τ_c — memory time; ordering of retained steps",
        "S1, `Th_coqc` at source",
    ),
    (
        ["measurement", "judgment", "decision", "diagnosis"],
        "readout: binary/graded projection of ε at policy Π",
        "LTP2",
    ),
    (
        ["vague boundary", "paradox of degree"],
        "forced jump of a binary readout on a smooth world; the cut lives in Π",
        "`Th_coqc` (sorites core)",
    ),
    (
        ["infinity", "continuum", "at the limit"],
        "non-readout — run the Ω_∞ check (I1–I4) before admitting the question",
        "Ω_∞",
    ),
    (
        ["unknowable", "hidden variable", "incompleteness"],
        "null-space of A — real difference, identical records (Fisher-singular)",
        "LTP4",
    ),
    (
        ["cause"],
        "a load-bearing retained relation (removing it moves the readout)",
        "LTP3 criterion",
    ),
    (
        ["approximation", "bounded rationality", "heuristic"],
        "inference over a sub-grammar; safe iff the discard is not load-bearing",
        "LTP3",
    ),
    (
        ["mass", "inertia", "habit", "institution"],
        "memory — resistance of a retained configuration to update (τ_c = M/D)",
        "bridge `Dr`",
    ),
    (
        ["horizon", "point of no return", "collapse", "death"],
        "the knife-edge τ_c*, hand-off into the non-readout",
        "bridge `Dr`",
    ),
    (
        ["life", "agency", "mind"],
        "the τ_c > τ_c* regime — memory outlasting one's own oscillation; agency adds observer = observed",
        "bridge `Dr` over `Th_coqc`",
    ),
    (
        ["truth"],
        'tracking — a readout that keeps V low under continued evidence',
        'L-07; never "correspondence to the infinite"',
    ),
    (
        ["ethics", "cooperation", "legitimacy"],
        "preservation of every knower's repair capacity + open correction channels",
        "L-16",
    ),
]

DICTIONARY: Dict[str, DictEntry] = {}

for _synonyms, _our_term, _notes in _TRANSLATION_TABLE_ROWS:
    for _term in _synonyms:
        DICTIONARY[_term.lower()] = DictEntry(
            our_term=_our_term,
            notes=_notes,
            tier="Dr",
            source="v2/TRANSLATION_PROTOCOL.md §1",
        )

# --- RD4 (Information DNA), philosophy.md §5.1 ------------------------------
DICTIONARY["rd4"] = DictEntry(
    our_term="retention/memory — distinct histories never merge",
    notes="the axiom the DRL equation is forced by",
    tier="Th_coqc",
    source="philosophy.md §5.1 (evidence/RD.v, evidence/URCF_RD_All.v)",
)

# --- RAR A1-A8, philosophy.md §5.1 ------------------------------------------
_RAR_ITEMS = [
    "distinguishability",
    "transport",
    "retention threshold",
    "accessibility",
    "admissibility",
    "identity-locking",
    "obstruction-not-explosion",
    "lens-validation",
]
for _i, _name in enumerate(_RAR_ITEMS, start=1):
    DICTIONARY[f"rar a{_i}"] = DictEntry(
        our_term=_name,
        notes="RAR A1-A8: a logic of retention built on the RD genome; "
        "declared (Dr) correspondence to the book's own machinery, "
        "not yet a proven formal unification",
        tier="Dr",
        source="philosophy.md §5.1",
    )

# --- I1-I4 / Z1-Z4 non-readout taxonomy (dual guard used by G2) ------------
I_TAXONOMY = {
    "I1": "ℝ-completeness",
    "I2": "infinite divisibility (h→0)",
    "I3": "infinite scale separation (Re,Λ→∞)",
    "I4": "actual +∞",
}
Z_TAXONOMY = {
    "Z1": "the point r=0 (zero extent)",
    "Z2": "exact-zero spacing (a reached continuum)",
    "Z3": "absolute rest / exact vacuum (v=0, T=0)",
    "Z4": "the true void",
}
for _code, _desc in {**I_TAXONOMY, **Z_TAXONOMY}.items():
    DICTIONARY[_code.lower()] = DictEntry(
        our_term=_desc,
        notes="injected non-readout in the I1-I4/Z1-Z4 dual guard used by gate G2",
        tier="Dr",
        source="philosophy.md §2.5, ~lines 645-649",
    )

NO_ENTRY_STATUS = "no_dictionary_entry"


def lookup(term: str) -> Dict[str, Any]:
    """Look up one foreign term. Never guesses.

    Returns either:
      {"status": "translated", "foreign_term": ..., **DictEntry}
    or, for an unmapped term, the honest:
      {"status": "no_dictionary_entry", "foreign_term": term,
       "flag": "[Open]/POSITED — extend the dictionary before use"}
    per TRANSLATION_PROTOCOL.md §1's own rule.
    """

    key = term.strip().lower()
    entry: Optional[DictEntry] = DICTIONARY.get(key)
    if entry is None:
        return {
            "status": NO_ENTRY_STATUS,
            "foreign_term": term,
            "flag": "[Open]/POSITED — extend the dictionary before use",
        }
    return {"status": "translated", "foreign_term": term, **entry}
