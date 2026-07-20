#!/usr/bin/env python3
"""check_gate_typing.py -- machine gate for docs/GATE_TYPING_LAW.md.

Law, one line: a gate that cannot fail is not a readout, it is a
convention. Every declared gate is Type P (physical content -- ships WITH
a named negative control that DEMONSTRABLY FAILS the gate, real recorded
value) or Type U (unit/convention -- everything else, never cited as
evidence, never counted in a headline N/N).

What this script enforces (machine-checked, exactly this and no more):
for every record in a declarations file that types itself Type P, the
recorded negative-control value and the recorded threshold are both
parseable numbers, the recorded operator is one of a fixed set, and
APPLYING THE OPERATOR TO THE NUMBERS ACTUALLY EVALUATES TO "gate does not
pass" -- i.e. the arithmetic itself confirms the control fails the gate.
A record that merely writes the word "FAIL" next to two numbers that do
not support that word is REJECTED, not accepted -- literal review-round-1
of this checker accepted exactly that (0.70 against a >= 0.35 gate marked
FAIL) and was wrong to; see `scripts/test_check_gate_typing.py` for the
regression test built from that exact case.

What this script does NOT enforce, and cannot: whether the negative
control is a reasonable/representative case, whether the threshold itself
is well-chosen, or whether a Type U gate declared honestly here is
nonetheless being cited as evidence somewhere ELSE (another doc, another
repo, a PR description). Those remain human/reviewer obligations --
docs/GATE_TYPING_LAW.md states which part of the law is machine-enforced
and which part is not; do not read a PASS from this script as more than
"the paperwork and arithmetic in this one file are self-consistent".

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
    negative_control_value, gate_operator, negative_control_threshold,
    and negative_control_result.
      * gate_operator is the comparison that DEFINES A PASS of the gate
        itself, one of: >= > <= < == != . Example: a gate documented as
        "same-ligand Jaccard >= 0.35 passes" declares
        gate_operator: >= and negative_control_threshold: 0.35.
      * negative_control_value and negative_control_threshold must both
        parse as numbers (int/float, stdlib float()); non-numeric values
        ("banana", "not-a-number") are rejected, not silently accepted.
      * negative_control_result must be exactly the literal string
        "FAIL" -- AND that label must be consistent with the arithmetic:
        evaluating gate_operator(negative_control_value,
        negative_control_threshold) must be False (the control does NOT
        satisfy the gate's own pass condition). If the arithmetic says
        the control actually passes, the record is rejected regardless
        of what its result field claims.
  - A field's value is considered present only after stripping ordinary
    whitespace AND any Unicode "format" characters (category Cf, e.g.
    U+200B ZERO WIDTH SPACE) -- a field containing only such characters
    is treated as empty/missing, not as a real value.
  - Gate ids are compared for duplicates after Unicode NFKC
    normalization + casefold + a small documented table of common
    Cyrillic/Greek Latin-lookalike substitutions (see
    _HOMOGLYPH_TO_ASCII below -- NFKC + casefold alone do NOT catch
    cross-script homographs like Cyrillic 'а' vs Latin 'a', since they
    are canonically distinct letters, not compatibility variants), so
    "G1" / "g1" and the common Latin/Cyrillic/Greek homograph pairs are
    detected as the same id. This is a finite, hand-picked table, not a
    claim of exhaustive UTS #39 confusable-skeleton detection.

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
import sys
import unicodedata
from pathlib import Path

REQUIRED_COMMON = ("gate", "type", "description")
REQUIRED_TYPE_P = (
    "negative_control_name",
    "negative_control_value",
    "gate_operator",
    "negative_control_threshold",
    "negative_control_result",
)
VALID_TYPES = ("P", "U")

# gate_operator -> a two-arg function; OPERATORS[op](value, threshold) is
# True exactly when the gate's own pass condition is satisfied.
OPERATORS = {
    ">=": operator.ge,
    ">": operator.gt,
    "<=": operator.le,
    "<": operator.lt,
    "==": operator.eq,
    "!=": operator.ne,
}

DEFAULT_PATH = Path("gates/GATE_DECLARATIONS.txt")


def clean_value(raw: str) -> str:
    """Strip ordinary whitespace and Unicode format characters (category
    Cf, e.g. U+200B ZERO WIDTH SPACE) so a field made only of such
    characters is correctly treated as empty, not as "present"."""
    without_format_chars = "".join(
        ch for ch in raw if unicodedata.category(ch) != "Cf"
    )
    return without_format_chars.strip()


# NFKC normalization + casefold alone does NOT catch cross-script
# homographs: Cyrillic 'а' (U+0430) has no NFKC decomposition to Latin
# 'a' -- they are canonically distinct letters, not compatibility
# variants of one character, so `unicodedata.normalize("NFKC", "а") ==
# "a"` is False and stays False after casefold. Verified directly before
# writing this table; do not re-introduce the assumption that NFKC alone
# solves this.
#
# This is a deliberately FINITE, hand-picked table of the common
# Latin-lookalike substitutions from Cyrillic and Greek (the same
# characters browsers warn about in IDN homograph attacks), not a claim
# of exhaustive Unicode confusable-skeleton detection per UTS #39 (that
# needs the full confusables.txt data table, which is not in the stdlib
# and is out of scope for a repo whose CI floor is numpy/scipy/sympy/
# pytest only). It is applied AFTER casefold, so only lowercase forms are
# listed -- casefold already lowers e.g. Cyrillic 'А' to 'а'.
_HOMOGLYPH_TO_ASCII = {
    # Cyrillic -> Latin
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y",
    "х": "x", "і": "i", "ј": "j", "ѕ": "s", "һ": "h", "ԁ": "d",
    "ⅰ": "i",
    # Greek -> Latin
    "ο": "o", "ρ": "p", "υ": "u", "ν": "v", "κ": "k",
}


def normalize_id(gate_id: str) -> str:
    """NFKC-normalize, casefold, then map known Cyrillic/Greek
    Latin-lookalike characters to their ASCII equivalents (see
    _HOMOGLYPH_TO_ASCII), so visually/semantically identical ids --
    ASCII-case variants, NFKC compatibility forms, AND the common
    cross-script homographs -- collide for duplicate detection."""
    folded = unicodedata.normalize("NFKC", gate_id).casefold()
    return "".join(_HOMOGLYPH_TO_ASCII.get(ch, ch) for ch in folded)


def parse_number(raw: str) -> float | None:
    """Parse a genuine, finite recorded number. Rejects non-numeric text
    (ValueError from float()) AND rejects 'nan'/'inf'/'-inf'/'infinity',
    which Python's float() otherwise parses without error: a NaN or
    infinite "recorded value" is not a real measurement, and -- found
    while adversarially testing this checker against itself -- 'nan'
    trivially satisfies "fails the gate" for almost any operator/
    threshold (NaN compares False against everything except '!='),
    which would let a fabricated non-value pass as a genuine failing
    control. That is exactly the failure mode this law exists to stop,
    so it is rejected here rather than accepted as "a number"."""
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
                f"a Type P gate must ship WITH a negative control that "
                f"demonstrably fails it (docs/GATE_TYPING_LAW.md)"
            )

    result = fields.get("negative_control_result")
    result_is_fail_literal = result is not None and clean_value(result) == "FAIL"
    if field_present(fields, "negative_control_result") and not result_is_fail_literal:
        errors.append(
            f"gate {label!r}: negative_control_result must be the literal "
            f"string 'FAIL' (got {result!r}) -- a control that does not "
            f"fail is not evidence the gate can discriminate; see the "
            f"contact-residue-Jaccard case in docs/GATE_TYPING_LAW.md, "
            f"where every pair (including different-ligand pairs) passed "
            f"the same threshold"
        )

    op_raw = fields.get("gate_operator")
    op_fn = None
    if field_present(fields, "gate_operator"):
        op_key = clean_value(op_raw)
        if op_key not in OPERATORS:
            errors.append(
                f"gate {label!r}: gate_operator must be one of "
                f"{sorted(OPERATORS)}, got {op_raw!r}"
            )
        else:
            op_fn = OPERATORS[op_key]

    value_num = None
    if field_present(fields, "negative_control_value"):
        value_num = parse_number(fields["negative_control_value"])
        if value_num is None:
            errors.append(
                f"gate {label!r}: negative_control_value "
                f"{fields['negative_control_value']!r} is not a parseable, "
                f"finite number (non-numeric text and nan/inf are both rejected)"
            )

    threshold_num = None
    if field_present(fields, "negative_control_threshold"):
        threshold_num = parse_number(fields["negative_control_threshold"])
        if threshold_num is None:
            errors.append(
                f"gate {label!r}: negative_control_threshold "
                f"{fields['negative_control_threshold']!r} is not a parseable, "
                f"finite number (non-numeric text and nan/inf are both rejected)"
            )

    # --- Type P: the actual arithmetic check (Finding 1) ---
    # Only run once operator + both numbers parsed cleanly; a missing or
    # unparseable input has already been flagged above and would make
    # this check meaningless (and it would raise on op_fn(None, None)).
    if op_fn is not None and value_num is not None and threshold_num is not None:
        gate_would_pass = op_fn(value_num, threshold_num)
        if gate_would_pass:
            errors.append(
                f"gate {label!r}: arithmetic contradicts the FAIL label -- "
                f"negative_control_value={value_num!r} {op_raw.strip()} "
                f"negative_control_threshold={threshold_num!r} evaluates to "
                f"True, i.e. the recorded control ACTUALLY PASSES the gate's "
                f"own pass condition. A record that writes 'FAIL' next to "
                f"numbers that do not support it is exactly the fabricated-"
                f"evidence framing this law exists to stop -- see the worked "
                f"counter-example in gates/GATE_DECLARATIONS.txt "
                f"(egfr_c797s_contact_jaccard_same_ligand, 0.70 >= 0.35)."
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
                    f"casefold) -- records #{prev_index} and #{i} collide"
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
        "gate-typing check: PASS -- every declared Type P gate carries a "
        "negative control whose recorded arithmetic (value, operator, "
        "threshold) actually evaluates to a failed gate, consistent with "
        "its FAIL label."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
