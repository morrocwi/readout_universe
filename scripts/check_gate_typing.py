#!/usr/bin/env python3
"""check_gate_typing.py -- machine gate for docs/GATE_TYPING_LAW.md.

Law, current (two-sided) form: a Type P gate must ship WITH a named
NEGATIVE control that the gate's own predicate derives as NOT passing,
AND a named POSITIVE control that the same predicate derives as
PASSING. Both are recorded as measured values only; the checker derives
both verdicts from the single `gate_passes_when` predicate. A gate is
evidence only if it can be shown to discriminate in BOTH directions --
that is the actual property being certified, not just "has a control
that fails".

WHY TWO-SIDED, NOT ONE-SIDED (history, not decoration -- read this
before assuming the one-sided law was ever adequate):

  The law as first ruled required only a negative control that fails.
  That catches a gate that passes everything (the EGFR disease: a 0.35
  Jaccard threshold that passed all 10 of 10 available pairs, including
  every different-ligand pair -- see docs/GATE_TYPING_LAW.md Case 1). It
  does NOT catch the opposite disease: a gate that fails everything.
  Demonstrated concretely by the chair's own adversarial round:

    description: score must be >= 0.80 to pass, this control genuinely fails
    negative_control_value: 0.95
    gate_passes_when: >= 999999

  0.95 plainly satisfies the gate's REAL condition (score >= 0.80), but
  because the declared predicate is effectively unreachable
  (>= 999999), the one-sided checker derived FAIL and certified the
  record -- exit 0, PASS. Pick any implausible threshold and every
  record self-certifies; a gate that rejects everything is exactly as
  worthless as evidence as a gate that accepts everything, and the
  one-sided law rewarded it.

  The two-sided form closes this STRUCTURALLY, not by judging
  plausibility (a script cannot know whether 999999 is a reasonable
  threshold, and must not pretend to): an unsatisfiable predicate admits
  NO valid positive control (nothing satisfies it, so the required
  positive-control field cannot be filled with anything that actually
  passes); a trivially-satisfiable predicate makes finding a genuine
  negative control require reaching for values outside the plausible
  domain, which is visible in the record rather than hidden by it. The
  checker requires and independently verifies both directions from one
  declared predicate.

This design is round 4 of this law, not round 1. Every earlier round
found a real hole (not cosmetic), each is regression-tested in
scripts/test_check_gate_typing.py, and none were argued away:

  - Round 1: accepted the literal string "FAIL" next to two numbers that
    did not support it (0.70 marked FAIL against a >= 0.35 gate).
  - Round 2: fixed round 1 by requiring an operator + arithmetic
    consistency -- but the operator was still self-declared BY THE SAME
    RECORD, so a record could pick whichever operator made its own
    arithmetic read FAIL, independent of the gate's real meaning.
  - Round 3: removed that degree of freedom -- one predicate
    (gate_passes_when) per GATE, not per control -- but the predicate
    could still be unreachable/vacuous, so a one-sided (negative-only)
    check could be trivially satisfied by an absurd threshold (see the
    999999 example above).
  - Round 4: requires BOTH a negative control (derived NOT passing) and
    a positive control (derived PASSING) from the one predicate. An
    unsatisfiable predicate can no longer self-certify, because it
    admits no valid positive control.
  - Round 5 (this file): fixes a genuine documentation regression --
    docs/AI_READING_GUIDE.md, the one file whose whole purpose is to
    tell an AI reader how to read this repo, had never been updated
    since round 1 and still stated the disproven one-sided rule while
    this file said otherwise (regression-tested by grep below, so it
    cannot silently drift again). Also closes a dressing-up attack: a
    Type U record could carry a full, cleanly-derivable set of Type-P
    control/predicate fields with no per-record complaint, reading as
    evidence to a human skimming the file even though it was typed U.

What this script does NOT enforce, and cannot:
  - Whether either control is a reasonable/representative case (only
    that the arithmetic genuinely discriminates), or whether a Type U
    gate declared honestly here is nonetheless being cited as evidence
    somewhere ELSE (another doc, another repo, a PR description).
    Human/reviewer obligation.
  - RESIDUAL RISKS (named explicitly, not folded into the bullet above --
    each numbered to match the chair's own finding numbers, so the
    numbering is traceable across review rounds; #1, #2, #5 above are
    fixed, these remain open):
    3. The implausible-value gap is TWO-SIDED, not just on the positive
       control: a `negative_control_value: -1000000` against a gate
       whose real domain is `[0, 1]` would satisfy "does not pass
       `>= 0.35`" just as trivially as an absurd positive control
       satisfies an absurd predicate. Neither direction's plausibility
       is checked.
    4. Nothing ties the two controls to the SAME MEASURED QUANTITY. A
       negative control described as "a thermometer reading in degrees
       C" and a positive control described as "a genuine Jaccard
       measurement" would both parse, both derive correctly against a
       shared `gate_passes_when`, and pass -- the checker has no notion
       that they are supposed to be readings of the same thing.
    5. `gate_passes_when` matching the gate's REAL pass condition as
       stated in its own `description` prose is not checked -- only that
       the record is internally self-consistent (both controls' derived
       verdicts match what the declared predicate implies). A script
       cannot know intent and must not pretend to: **a reviewer must
       confirm the declared `gate_passes_when` predicate is the gate's
       real, actual pass condition**, not merely that the record is
       internally consistent and two-sided.
    6. Unknown/extra keys on a record are silently IGNORED, not rejected
       or validated -- e.g. a smuggled `positive_control_result` field
       sitting beside a correctly-spelled, correctly-required set of
       fields parses fine and is never read by anything. A typo'd
       REQUIRED field is still caught (it shows up as "missing"), so this
       is not structural; but given the law's central point is that no
       caller-supplied result is ever trusted, be explicit: an unknown
       key being present in a record is not evidence that anything about
       it was checked.

docs/GATE_TYPING_LAW.md states which part of the law is machine-enforced
and which part is not; do not read a PASS from this script as more than
"this one record's own predicate, applied to its own two controls,
derives one FAIL and one PASS, exactly as declared".

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
  - A Type U record must NOT carry any control or predicate field
    (negative_control_name, negative_control_value,
    positive_control_name, positive_control_value, gate_passes_when) --
    REJECTED if it does, even if those fields would derive a clean
    two-sided pass. There is no legitimate reason for a declared
    convention to carry the same apparatus a Type P record uses to prove
    it can fail; a record with that apparatus reads as evidence to a
    human skimming the file regardless of its declared type.
  - A Type P record additionally requires: negative_control_name,
    negative_control_value, positive_control_name, positive_control_value,
    and gate_passes_when. There is no result field of any kind -- neither
    control carries a caller-supplied verdict; both verdicts are DERIVED.
      * gate_passes_when is the gate's OWN pass predicate, declared once,
        as "<operator> <threshold>", operator one of: >= > <= < == != .
        Example: a gate documented as "same-ligand Jaccard >= 0.35
        passes" declares gate_passes_when: ">= 0.35".
      * negative_control_value, positive_control_value, and the
        threshold inside gate_passes_when must all parse as finite
        numbers (stdlib float(); non-numeric text like
        "banana"/"not-a-number", and non-finite values like
        "nan"/"inf"/"-inf"/"infinity", are all rejected).
      * Both verdicts are DERIVED, never read from the file: the checker
        evaluates gate_passes_when's operator on
        (negative_control_value, threshold) and requires that to be
        False; it separately evaluates it on (positive_control_value,
        threshold) and requires that to be True. Either direction
        failing rejects the record, full stop -- there is no field that
        can override this.
  - Unknown/extra keys on a record (misspellings, or a smuggled field
    like `positive_control_result` that is not part of this format at
    all) are IGNORED, not rejected and not validated. A required field's
    correct name is still checked for presence, so a typo'd REQUIRED key
    is caught (it reads as "missing"); an extra key with no defined
    meaning simply parses into the fields dict and is never read by
    anything. Do not infer from a record parsing cleanly that every key
    in it was checked.
  - A field's value is considered present only after stripping ordinary
    whitespace AND any invisible/blank-rendering characters: Unicode
    category Cf (format, e.g. U+200B ZERO WIDTH SPACE), Cc (control), Mn
    and Me (combining/enclosing marks, which render as zero-width without
    a preceding base character), any character str.isspace() reports as
    whitespace (covers Zs/Zl/Zp separators including U+00A0 NBSP), plus a
    short explicit list of individually-named blank-rendering characters
    that are none of the above: the Hangul filler family (U+115F,
    U+1160, U+3164, U+FFA0) and U+2800 BRAILLE PATTERN BLANK (category
    So -- visually blank, unlike the rest of the Braille block, which is
    why it needs its own entry rather than a category-wide exclusion).
    See _is_blank_char and clean_value below.
  - Gate ids are compared for duplicates after Unicode NFKC
    normalization, a homoglyph substitution pass (see
    _HOMOGLYPH_TO_ASCII), THEN casefold -- in that order (substitution
    must run BEFORE casefold; see the comment on that table for why).
    This table is a deliberately FINITE, hand-picked list and is NOT a
    solved problem: each review round has added entries the previous
    round missed (round 3 added the uppercase Cyrillic IDN set K/M/H/T/B
    after finding the lowercase-only table missed it; round 4 added
    Cyrillic Ѕ/Ј/Ӏ). Treat the list as "known gaps fixed so far", not
    "homoglyph detection is closed" -- it is not, and more gaps almost
    certainly exist outside this table.

Full worked format example lives in docs/GATE_TYPING_LAW.md and in the
comments of gates/GATE_DECLARATIONS.txt.

Usage:
    python3 scripts/check_gate_typing.py [path-to-declarations-file]

Default path: gates/GATE_DECLARATIONS.txt (repo root). Exits 0 if the
file is absent or contains zero live (non-comment) records -- that is
the honest trivial-pass case, and the script SAYS SO explicitly rather
than passing silently. Exits 1 on any malformed, under-evidenced, or
one-sided/arithmetically-inconsistent Type P record, with every problem
listed (not just the first).
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
    "positive_control_name",
    "positive_control_value",
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

# Individually-named characters that render blank but are NOT covered by
# the categories above and are NOT whitespace -- each added after a
# specific finding, not a category-wide sweep (category-wide would catch
# too much: most of category So, for instance, is visible glyphs; only
# U+2800 in the Braille block is blank):
#   - the Hangul filler family (category Lo): U+3164 HANGUL FILLER found
#     missing a round-3 review; U+115F/U+1160/U+FFA0 added alongside it
#     as the same family.
#   - U+2800 BRAILLE PATTERN BLANK (category So): found missing a
#     round-4 review -- "⠀⠀⠀" (three blank Braille cells) survived as a
#     "named" control until this was added.
_EXPLICIT_BLANK_CHARS = {
    "ᅟ",  # U+115F HANGUL CHOSEONG FILLER
    "ᅠ",  # U+1160 HANGUL JUNGSEONG FILLER
    "ㅤ",  # U+3164 HANGUL FILLER
    "ﾠ",  # U+FFA0 HALFWIDTH HANGUL FILLER
    "⠀",  # U+2800 BRAILLE PATTERN BLANK
}


def _is_blank_char(ch: str) -> bool:
    if ch.isspace():
        return True
    if unicodedata.category(ch) in _BLANK_CATEGORIES:
        return True
    if ch in _EXPLICIT_BLANK_CHARS:
        return True
    return False


def clean_value(raw: str) -> str:
    """Strip every character that renders blank -- ordinary whitespace
    (including U+00A0 NBSP), Unicode format/control/combining-mark
    characters, and a short list of individually-named blank-rendering
    characters (Hangul filler family, U+2800 BRAILLE PATTERN BLANK) --
    so a field made only of such characters is correctly treated as
    empty, not present."""
    return "".join(ch for ch in raw if not _is_blank_char(ch)).strip()


# Deliberately FINITE, hand-picked table of common Latin-lookalike
# substitutions from Cyrillic and Greek (the classic IDN homograph-attack
# set), NOT a claim of exhaustive Unicode confusable-skeleton detection
# per UTS #39 (that needs the full confusables.txt data table, which is
# not in the stdlib and is out of scope for a repo whose CI floor is
# numpy/scipy/sympy/pytest only). This list has grown by finding, not by
# design -- round 3 added the uppercase Cyrillic IDN set (К М Н Т В: see
# the comment below on WHY order matters); round 4 added Ѕ/Ј/Ӏ after a
# review found them missing. DO NOT read the presence of this table as
# "the homoglyph problem is solved" -- it enumerates confusables found so
# far, not confusables that could exist.
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
    "Ѕ": "S", "Ј": "J", "Ӏ": "I",
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

    if gate_type == "U":
        # A Type U record must not carry a falsification apparatus at all --
        # no legitimate convention gate has a negative control, a positive
        # control, or a pass predicate. Without this check, a record could
        # dress itself up with a full, cleanly-derivable two-sided pass
        # (both controls genuinely discriminating) while still being typed
        # U, which reads as evidence to any human skimming the file even
        # though the aggregate Type-U reminder at the end is easy to miss.
        # Reject rather than warn: there is no legitimate reason for a
        # declared convention to carry the same fields a Type P record
        # uses to prove it can fail.
        smuggled = [key for key in REQUIRED_TYPE_P if field_present(fields, key)]
        if smuggled:
            errors.append(
                f"gate {label!r}: declared Type U but carries Type-P-only "
                f"field(s) {smuggled} -- a Type U record must not carry "
                f"control or predicate fields at all, regardless of whether "
                f"they would derive a clean two-sided pass if the gate were "
                f"typed P (docs/GATE_TYPING_LAW.md). Either declare "
                f"type: P (and meet every Type P requirement) or remove "
                f"these fields."
            )

    if gate_type != "P":
        return errors

    # --- Type P: paperwork presence ---
    for key in REQUIRED_TYPE_P:
        if not field_present(fields, key):
            errors.append(
                f"gate {label!r}: declared Type P but missing {key!r} -- "
                f"a Type P gate must declare its own pass predicate "
                f"(gate_passes_when) and ship WITH both a negative control "
                f"value that demonstrably fails it AND a positive control "
                f"value that demonstrably satisfies it (docs/GATE_TYPING_LAW.md)"
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

    negative_value = None
    if field_present(fields, "negative_control_value"):
        negative_value = parse_number(fields["negative_control_value"])
        if negative_value is None:
            errors.append(
                f"gate {label!r}: negative_control_value "
                f"{fields['negative_control_value']!r} is not a parseable, "
                f"finite number (non-numeric text and nan/inf are both rejected)"
            )

    positive_value = None
    if field_present(fields, "positive_control_value"):
        positive_value = parse_number(fields["positive_control_value"])
        if positive_value is None:
            errors.append(
                f"gate {label!r}: positive_control_value "
                f"{fields['positive_control_value']!r} is not a parseable, "
                f"finite number (non-numeric text and nan/inf are both rejected)"
            )

    # --- Type P: the actual two-sided arithmetic check (derive both) ---
    # Only run once the predicate parsed AND the respective control value
    # parsed; a missing/unparseable input is already flagged above.
    if parsed_predicate is not None:
        op_token, threshold_num = parsed_predicate

        if negative_value is not None:
            negative_would_pass = OPERATORS[op_token](negative_value, threshold_num)
            if negative_would_pass:
                errors.append(
                    f"gate {label!r}: the recorded negative control "
                    f"(negative_control_value={negative_value!r}) SATISFIES "
                    f"the gate's own declared predicate (gate_passes_when: "
                    f"{op_token} {threshold_num!r}) -- this is not a genuine "
                    f"failing control. See the worked counter-example in "
                    f"gates/GATE_DECLARATIONS.txt "
                    f"(egfr_c797s_contact_jaccard_same_ligand)."
                )

        if positive_value is not None:
            positive_would_pass = OPERATORS[op_token](positive_value, threshold_num)
            if not positive_would_pass:
                errors.append(
                    f"gate {label!r}: the recorded positive control "
                    f"(positive_control_value={positive_value!r}) does NOT "
                    f"satisfy the gate's own declared predicate "
                    f"(gate_passes_when: {op_token} {threshold_num!r}) -- "
                    f"this is not a genuine passing control. An "
                    f"unsatisfiable or implausible predicate (e.g. "
                    f">= 999999 for a gate whose real range never reaches "
                    f"that) will fail here because NO value can be a "
                    f"genuine positive control for it -- see the worked "
                    f"counter-example in gates/GATE_DECLARATIONS.txt "
                    f"(score_gate_unsatisfiable_predicate_attack)."
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
        "value, derives 'does not pass', AND applied to its positive "
        "control's value, derives 'passes' -- i.e. every gate demonstrably "
        "discriminates in both directions. Residual, unfixable risk: this "
        "does not verify gate_passes_when matches the gate's real pass "
        "condition as described in its own prose -- that remains a named "
        "human-review obligation (see module docstring)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
