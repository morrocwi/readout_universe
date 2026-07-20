#!/usr/bin/env python3
"""check_gate_typing.py -- machine gate for docs/GATE_TYPING_LAW.md.

Law, one line: a gate that cannot fail is not a readout, it is a
convention. Every declared gate is Type P (physical content -- ships WITH
a named negative control that DEMONSTRABLY FAILS the gate, real recorded
value) or Type U (unit/convention -- everything else, never cited as
evidence, never counted in a headline N/N).

What this script enforces (machine-checked, exactly this and no more):
for every record in a declarations file that types itself Type P, the
gate declares its own pass predicate EXACTLY ONCE (`gate_passes_when`,
e.g. ">= 0.80") and the negative control declares ONLY its measured
value (`negative_control_value`); the checker applies the gate's own
predicate to that value and DERIVES whether the control fails the gate --
it does not read a self-declared result as input. A record whose control
value arithmetically satisfies its own gate's predicate is REJECTED
regardless of any FAIL label the record may still carry.

This design is round 3 of this checker, not round 1. Two earlier holes,
both found by adversarial review and both regression-tested below:

  - Round 1 accepted the literal string "FAIL" next to two numbers that
    did not support it (0.70 marked FAIL against a >= 0.35 gate).
  - Round 2 fixed that by requiring the record to state BOTH an operator
    and the arithmetic to be self-consistent -- but the operator was
    still self-declared by the same record, so the record could pick
    WHICHEVER operator made its own arithmetic come out FAIL (e.g.
    declare `gate_operator: <=` for a gate that is actually `>= 0.80`,
    and a control that plainly passes the real gate reads as FAIL).
  - Round 3 (this file) removes that degree of freedom entirely: there
    is exactly one operator per gate (`gate_passes_when`, on the gate,
    not on the control), so the attack above is no longer expressible.
    `negative_control_result` is no longer read as an input at all; see
    "Residual, unfixable risk" below for what remains impossible to
    check by tooling even after this.

What this script does NOT enforce, and cannot:
  - Whether the negative control is a reasonable/representative case, or
    whether a Type U gate declared honestly here is nonetheless being
    cited as evidence somewhere ELSE (another doc, another repo, a PR
    description). Human/reviewer obligation.
  - RESIDUAL, UNFIXABLE RISK (named explicitly, not folded into the
    bullet above): the checker cannot verify that `gate_passes_when`
    matches the gate's REAL pass condition as stated in its own
    `description` prose. Someone can still write a `description` that
    says "score must be >= 0.80 to pass" and a `gate_passes_when: <=
    0.80` that contradicts it -- the arithmetic would be internally
    self-consistent (a control of 0.95 correctly evaluates to FAIL under
    the declared `<= 0.80` predicate) while `gate_passes_when` itself is
    wrong about what the gate actually does. A script cannot know intent
    and must not pretend to; catching this is a NAMED human-review
    obligation: **a reviewer must confirm the declared `gate_passes_when`
    predicate is the gate's real, actual pass condition**, not merely
    that the record is internally consistent.

docs/GATE_TYPING_LAW.md states which part of the law is machine-enforced
and which part is not; do not read a PASS from this script as more than
"the paperwork and arithmetic in this one file are internally
self-consistent, given the predicate as declared".

Declaration format (plain text, stdlib-only parser -- no YAML dependency
so this runs on any interpreter that has numpy/scipy/sympy/pytest and
nothing else, matching the CI runner's floor):

  - Comment lines start with '#' and are stripped before parsing.
  - Records are separated by one or more blank lines.
  - Each record is a block of "key: value" lines (value = rest of line,
    stripped once).
  - Required keys on every record: gate, type, description.
  - type must be exactly "P" or "U" (case-sensitive, no synonyms --
    this is deliberate: no quiet "mostly passes" tier).
  - A Type P record additionally requires: negative_control_name,
    negative_control_value, and gate_passes_when.
      * gate_passes_when is the gate's OWN pass predicate, declared once,
        as "<operator> <threshold>", operator one of: >= > <= < == != .
        Example: a gate documented as "same-ligand Jaccard >= 0.35
        passes" declares gate_passes_when: ">= 0.35". There is no
        separate operator field on the control -- the control has only a
        value, and the gate's own predicate is applied to it.
      * negative_control_value and the threshold inside gate_passes_when
        must both parse as finite numbers (stdlib float(); non-numeric
        text like "banana"/"not-a-number", and non-finite values like
        "nan"/"inf"/"-inf"/"infinity", are all rejected).
      * The result is DERIVED, not read from the file: the checker
        evaluates gate_passes_when's operator on
        (negative_control_value, threshold) and requires that to be
        False (the control does not satisfy the gate's own pass
        condition). A record whose control satisfies its own gate's
        predicate is rejected, full stop -- there is no field that can
        override this.
      * negative_control_result is OPTIONAL and, if present, is treated
        as a human-readable annotation cross-checked against the derived
        result: it must equal the literal string "FAIL" (the only value
        a genuinely valid Type P record can ever derive) or the record is
        rejected for the mismatch. It is never consulted to COMPUTE the
        result -- only gate_passes_when + negative_control_value do that.
  - A field's value is considered present only after stripping ordinary
    whitespace AND any invisible/blank-rendering characters: Unicode
    category Cf (format, e.g. U+200B ZERO WIDTH SPACE), Cc (control), Mn
    and Me (combining/enclosing marks, which render as zero-width without
    a preceding base character), any character str.isspace() reports as
    whitespace (covers Zs/Zl/Zp separators including U+00A0 NBSP), plus a
    short explicit list of blank-rendering Letter-category fillers that
    are none of the above (U+115F, U+1160, U+3164, U+FFA0 -- the Hangul
    filler family). See _is_blank_char and clean_value below.
  - Gate ids are compared for duplicates after Unicode NFKC
    normalization, a homoglyph substitution pass (see
    _HOMOGLYPH_TO_ASCII), THEN casefold -- in that order. The homoglyph
    substitution must run BEFORE casefold: casefold(Cyrillic 'К' U+041A)
    is Cyrillic 'к' U+043A, a different character with no listed Latin
    mapping, so substituting only after casefold silently loses the
    uppercase Cyrillic/Greek confusables (К М Н Т В and their Greek
    counterparts) that visually match Latin uppercase letters but whose
    lowercase forms do not. Running the table first, on the original
    case, catches both directions with one table.

Full worked format example lives in docs/GATE_TYPING_LAW.md and in the
comments of gates/GATE_DECLARATIONS.txt.

Usage:
    python3 scripts/check_gate_typing.py [path-to-declarations-file]

Default path: gates/GATE_DECLARATIONS.txt (repo root). Exits 0 if the
file is absent or contains zero live (non-comment) records -- that is
the honest trivial-pass case, and the script SAYS SO explicitly rather
than passing silently. Exits 1 on any malformed, under-evidenced, or
arithmetically-inconsistent Type P record, with every problem listed
(not just the first).
"""
from __future__ import annotations

import math
import operator
import re
import sys
import unicodedata
from pathlib import Path

REQUIRED_COMMON = ("gate", "type", "description")
REQUIRED_TYPE_P = (
    "negative_control_name",
    "negative_control_value",
    "gate_passes_when",
)
VALID_TYPES = ("P", "U")

# gate_passes_when's operator token -> a two-arg function; OPERATORS[op]
# (value, threshold) is True exactly when the gate's own pass condition
# is satisfied. Two-character operators are listed, and matched, before
# their single-character prefixes (see GATE_PASSES_WHEN_RE below).
OPERATORS = {
    ">=": operator.ge,
    ">": operator.gt,
    "<=": operator.le,
    "<": operator.lt,
    "==": operator.eq,
    "!=": operator.ne,
}

# Matches "<op> <threshold>", e.g. ">= 0.80", ">=0.80", "== -3". The
# alternation is ordered longest-first so ">=" is not shadowed by ">".
GATE_PASSES_WHEN_RE = re.compile(r"^\s*(>=|<=|==|!=|<|>)\s*(.+?)\s*$")

DEFAULT_PATH = Path("gates/GATE_DECLARATIONS.txt")

# Unicode general categories that render with zero visible width even
# when not otherwise whitespace: Cf (format, e.g. ZERO WIDTH SPACE), Cc
# (control), Mn/Me (nonspacing/enclosing combining marks -- these need a
# preceding base character to be visible at all, so alone in a field they
# render as nothing).
_BLANK_CATEGORIES = {"Cf", "Cc", "Mn", "Me"}

# A field made ONLY of these renders blank but is not covered by the
# categories above and is not whitespace: the Hangul filler family.
# Finding (round-3 review): U+3164 HANGUL FILLER (category Lo) and
# U+00A0 NBSP (whitespace, but confirm it's actually caught) both need to
# be rejected as "no real value" -- verified with a regression test
# below rather than assumed.
_BLANK_LO_CHARS = {
    "ᅟ",  # HANGUL CHOSEONG FILLER
    "ᅠ",  # HANGUL JUNGSEONG FILLER
    "ㅤ",  # HANGUL FILLER
    "ﾠ",  # HALFWIDTH HANGUL FILLER
}


def _is_blank_char(ch: str) -> bool:
    if ch.isspace():
        return True
    if unicodedata.category(ch) in _BLANK_CATEGORIES:
        return True
    if ch in _BLANK_LO_CHARS:
        return True
    return False


def clean_value(raw: str) -> str:
    """Strip every character that renders blank -- ordinary whitespace
    (including U+00A0 NBSP), Unicode format/control/combining-mark
    characters, and the Hangul filler family (U+3164 etc., which are
    Letter-category and so survive a Cf-only filter) -- so a field made
    only of such characters is correctly treated as empty, not present."""
    return "".join(ch for ch in raw if not _is_blank_char(ch)).strip()


# Deliberately FINITE, hand-picked table of the common Latin-lookalike
# substitutions from Cyrillic and Greek (the classic IDN homograph-attack
# set), not a claim of exhaustive Unicode confusable-skeleton detection
# per UTS #39 (that needs the full confusables.txt data table, which is
# not in the stdlib and is out of scope for a repo whose CI floor is
# numpy/scipy/sympy/pytest only).
#
# Both upper- and lower-case forms are listed EXPLICITLY, and the table
# is applied BEFORE casefold (see normalize_id) -- applying it only after
# casefold was round-2's bug: casefold(Cyrillic 'К' U+041A) yields
# Cyrillic 'к' U+043A, and a lowercase-only table has no entry for that,
# so the classic uppercase confusable set (К М Н Т В and their Greek
# counterparts, which visually match Latin UPPERCASE letters; their
# lowercase Cyrillic/Greek forms do NOT resemble the Latin lowercase
# letters) silently passed through unmapped. Verified directly:
# 'К'.casefold() == 'к', which is absent from a lowercase-only
# table -- do not reintroduce a lowercase-only table.
_HOMOGLYPH_TO_ASCII = {
    # Cyrillic uppercase -> Latin uppercase (classic IDN confusable set)
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H",
    "О": "O", "Р": "P", "С": "C", "Т": "T", "У": "Y", "Х": "X",
    # Cyrillic lowercase -> Latin lowercase
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y",
    "х": "x", "і": "i", "ј": "j", "ѕ": "s", "һ": "h", "ԁ": "d",
    "ӏ": "l",
    # Greek uppercase -> Latin uppercase
    "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H", "Ι": "I",
    "Κ": "K", "Μ": "M", "Ν": "N", "Ο": "O", "Ρ": "P", "Τ": "T",
    "Υ": "Y", "Χ": "X",
    # Greek lowercase -> Latin lowercase
    "ο": "o", "ρ": "p", "υ": "u", "ν": "v", "κ": "k",
}


def normalize_id(gate_id: str) -> str:
    """NFKC-normalize, apply the homoglyph substitution table (BEFORE
    casefold -- see _HOMOGLYPH_TO_ASCII for why order matters), then
    casefold, so visually/semantically identical ids -- ASCII-case
    variants, NFKC compatibility forms, and the common cross-script
    homographs in EITHER case -- collide for duplicate detection."""
    nfkc = unicodedata.normalize("NFKC", gate_id)
    substituted = "".join(_HOMOGLYPH_TO_ASCII.get(ch, ch) for ch in nfkc)
    return substituted.casefold()


def parse_number(raw: str) -> float | None:
    """Parse a genuine, finite recorded number. Rejects non-numeric text
    (ValueError from float()) AND rejects 'nan'/'inf'/'-inf'/'infinity',
    which Python's float() otherwise parses without error: a NaN or
    infinite "recorded value" is not a real measurement, and 'nan' in
    particular trivially satisfies "fails the gate" against almost any
    operator (NaN compares False against everything except '!='), which
    would let a fabricated non-value pass as a genuine failing control."""
    cleaned = clean_value(raw)
    if not cleaned:
        return None
    try:
        value = float(cleaned)
    except ValueError:
        return None
    if not math.isfinite(value):
        return None
    return value


def parse_gate_passes_when(raw: str) -> tuple[str, float] | None:
    """Parse "<op> <threshold>" into (operator_token, threshold_float).
    Returns None if the operator token isn't recognized or the threshold
    isn't a parseable finite number."""
    cleaned = clean_value(raw)
    match = GATE_PASSES_WHEN_RE.match(cleaned)
    if not match:
        return None
    op_token, threshold_raw = match.group(1), match.group(2)
    if op_token not in OPERATORS:
        return None
    threshold = parse_number(threshold_raw)
    if threshold is None:
        return None
    return op_token, threshold


def strip_comments(text: str) -> str:
    kept = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            continue
        kept.append(line)
    return "\n".join(kept)


def split_records(text: str) -> list[list[str]]:
    records: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.strip() == "":
            if current:
                records.append(current)
                current = []
            continue
        current.append(line)
    if current:
        records.append(current)
    return records


def parse_record(lines: list[str], record_index: int) -> tuple[dict, list[str]]:
    """Parse one record's lines into a dict. Returns (fields, parse_errors)."""
    fields: dict[str, str] = {}
    errors: list[str] = []
    for line in lines:
        if ":" not in line:
            errors.append(
                f"record #{record_index}: malformed line (no 'key: value'): {line!r}"
            )
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if key in fields:
            errors.append(
                f"record #{record_index}: duplicate key {key!r} "
                f"(first value {fields[key]!r}, second {value!r})"
            )
            continue
        fields[key] = value
    return fields, errors


def field_present(fields: dict, key: str) -> bool:
    value = fields.get(key)
    if value is None:
        return False
    return bool(clean_value(value))


def check_record(fields: dict, record_index: int) -> list[str]:
    errors: list[str] = []
    label = fields.get("gate", f"<record #{record_index}, no 'gate' key>")

    for key in REQUIRED_COMMON:
        if not field_present(fields, key):
            errors.append(f"gate {label!r}: missing required field {key!r}")

    gate_type = fields.get("type")
    if gate_type is not None and gate_type not in VALID_TYPES:
        errors.append(
            f"gate {label!r}: type must be exactly 'P' or 'U', got {gate_type!r}"
        )

    if gate_type != "P":
        return errors

    # --- Type P: paperwork presence ---
    for key in REQUIRED_TYPE_P:
        if not field_present(fields, key):
            errors.append(
                f"gate {label!r}: declared Type P but missing {key!r} -- "
                f"a Type P gate must declare its own pass predicate "
                f"(gate_passes_when) and ship WITH a negative control "
                f"value that demonstrably fails it (docs/GATE_TYPING_LAW.md)"
            )

    parsed_predicate = None
    if field_present(fields, "gate_passes_when"):
        parsed_predicate = parse_gate_passes_when(fields["gate_passes_when"])
        if parsed_predicate is None:
            errors.append(
                f"gate {label!r}: gate_passes_when {fields['gate_passes_when']!r} "
                f"must be formatted as one operator ({', '.join(sorted(OPERATORS))}) "
                f"followed by a finite number, e.g. '>= 0.80'"
            )

    value_num = None
    if field_present(fields, "negative_control_value"):
        value_num = parse_number(fields["negative_control_value"])
        if value_num is None:
            errors.append(
                f"gate {label!r}: negative_control_value "
                f"{fields['negative_control_value']!r} is not a parseable, "
                f"finite number (non-numeric text and nan/inf are both rejected)"
            )

    # --- Type P: the actual arithmetic check (derive, don't trust) ---
    # Only run once the predicate parsed AND the control value parsed; a
    # missing/unparseable input is already flagged above.
    if parsed_predicate is not None and value_num is not None:
        op_token, threshold_num = parsed_predicate
        gate_would_pass = OPERATORS[op_token](value_num, threshold_num)
        if gate_would_pass:
            errors.append(
                f"gate {label!r}: the recorded negative control "
                f"(negative_control_value={value_num!r}) SATISFIES the "
                f"gate's own declared predicate (gate_passes_when: "
                f"{op_token} {threshold_num!r}) -- this is not a genuine "
                f"failing control, regardless of any negative_control_result "
                f"label the record carries. See the worked counter-example "
                f"in gates/GATE_DECLARATIONS.txt "
                f"(egfr_c797s_contact_jaccard_same_ligand)."
            )

    # negative_control_result is OPTIONAL, never read to COMPUTE the
    # result -- only cross-checked against the derived value, if present.
    # (If the control actually passes the gate, that is already reported
    # above as the primary error regardless of what this field says.)
    if field_present(fields, "negative_control_result"):
        result_raw = fields["negative_control_result"]
        if clean_value(result_raw) != "FAIL":
            errors.append(
                f"gate {label!r}: negative_control_result, if present, must "
                f"be the literal string 'FAIL' (got {result_raw!r}) -- it is "
                f"an optional human-readable annotation cross-checked "
                f"against the DERIVED result (gate_passes_when applied to "
                f"negative_control_value), not an input the checker trusts"
            )

    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT_PATH

    print(f"gate-typing check: reading {path}")

    if not path.exists():
        print(
            f"gate-typing check: {path} does not exist -- 0 gates declared. "
            f"TRIVIAL PASS (nothing to check yet). This is not the same as "
            f"'all gates verified'; it means the declarations file has not "
            f"been created. See docs/GATE_TYPING_LAW.md."
        )
        return 0

    raw = path.read_text()
    stripped = strip_comments(raw)
    records = split_records(stripped)

    if not records:
        print(
            f"gate-typing check: {path} exists but declares 0 live gates "
            f"(comments only). TRIVIAL PASS. See docs/GATE_TYPING_LAW.md."
        )
        return 0

    all_errors: list[str] = []
    seen_ids: dict[str, tuple[int, str]] = {}
    type_p_count = 0
    type_u_count = 0

    for i, record_lines in enumerate(records, start=1):
        fields, parse_errors = parse_record(record_lines, i)
        all_errors.extend(parse_errors)
        record_errors = check_record(fields, i)
        all_errors.extend(record_errors)

        gate_id = fields.get("gate")
        if gate_id and clean_value(gate_id):
            norm = normalize_id(clean_value(gate_id))
            if norm in seen_ids:
                prev_index, prev_id = seen_ids[norm]
                all_errors.append(
                    f"gate {gate_id!r}: same id as gate {prev_id!r} in record "
                    f"#{prev_index} after Unicode normalization (NFKC + "
                    f"homoglyph substitution + casefold) -- records "
                    f"#{prev_index} and #{i} collide"
                )
            else:
                seen_ids[norm] = (i, gate_id)

        gate_type = fields.get("type")
        if gate_type == "P":
            type_p_count += 1
        elif gate_type == "U":
            type_u_count += 1

    print(
        f"gate-typing check: {len(records)} gate(s) declared "
        f"({type_p_count} Type P, {type_u_count} Type U, "
        f"{len(records) - type_p_count - type_u_count} malformed)"
    )
    if type_u_count:
        print(
            f"gate-typing check: reminder -- the {type_u_count} Type U "
            f"gate(s) above must NOT be counted in any 'N/N checks passed' "
            f"evidence claim and must not appear in a headline verdict "
            f"(docs/GATE_TYPING_LAW.md). This script cannot detect a "
            f"headline-verdict misuse elsewhere; that is a human review "
            f"obligation."
        )

    if all_errors:
        print(f"gate-typing check: FAIL -- {len(all_errors)} problem(s):")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print(
        "gate-typing check: PASS -- every declared Type P gate's own "
        "predicate (gate_passes_when), applied to its negative control's "
        "recorded value, derives to 'gate does not pass' -- i.e. every "
        "control genuinely fails its gate. Residual, unfixable risk: this "
        "does not verify gate_passes_when matches the gate's real pass "
        "condition as described in its own prose -- that remains a named "
        "human-review obligation (see module docstring)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
