#!/usr/bin/env python3
"""check_gate_typing.py -- machine gate for docs/GATE_TYPING_LAW.md.

Law, one line: a gate that cannot fail is not a readout, it is a
convention. Every declared gate is Type P (physical content -- ships WITH
a named negative control that DEMONSTRABLY FAILS the gate, real recorded
value) or Type U (unit/convention -- everything else, never cited as
evidence, never counted in a headline N/N).

This script does NOT judge whether a gate's science is correct. It only
checks the paperwork: every gate that DECLARES ITSELF Type P must carry a
negative-control record with an actual failing value attached. If it
doesn't, that is exactly the failure mode this law exists to catch (see
the EGFR C797S and PSII cases in docs/GATE_TYPING_LAW.md), so the check
fails loudly rather than trusting the self-declared type.

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
    negative_control_value, negative_control_threshold, and
    negative_control_result. negative_control_result must be exactly
    the literal string "FAIL" -- a control that does not fail is not a
    negative control, no matter what the record calls it.

Full worked format example lives in docs/GATE_TYPING_LAW.md.

Usage:
    python3 scripts/check_gate_typing.py [path-to-declarations-file]

Default path: gates/GATE_DECLARATIONS.txt (repo root). Exits 0 if the
file is absent or contains zero live (non-comment) records -- that is
the honest trivial-pass case, and the script SAYS SO explicitly rather
than passing silently. Exits 1 on any malformed or under-evidenced
Type P record, with every problem listed (not just the first).
"""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_COMMON = ("gate", "type", "description")
REQUIRED_TYPE_P = (
    "negative_control_name",
    "negative_control_value",
    "negative_control_threshold",
    "negative_control_result",
)
VALID_TYPES = ("P", "U")

DEFAULT_PATH = Path("gates/GATE_DECLARATIONS.txt")


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


def check_record(fields: dict, record_index: int) -> list[str]:
    errors: list[str] = []
    label = fields.get("gate", f"<record #{record_index}, no 'gate' key>")

    for key in REQUIRED_COMMON:
        if not fields.get(key):
            errors.append(f"gate {label!r}: missing required field {key!r}")

    gate_type = fields.get("type")
    if gate_type is not None and gate_type not in VALID_TYPES:
        errors.append(
            f"gate {label!r}: type must be exactly 'P' or 'U', got {gate_type!r}"
        )

    if gate_type == "P":
        for key in REQUIRED_TYPE_P:
            if not fields.get(key):
                errors.append(
                    f"gate {label!r}: declared Type P but missing {key!r} -- "
                    f"a Type P gate must ship WITH a negative control that "
                    f"demonstrably fails it (docs/GATE_TYPING_LAW.md)"
                )
        result = fields.get("negative_control_result")
        if result is not None and result != "FAIL":
            errors.append(
                f"gate {label!r}: negative_control_result must be the literal "
                f"string 'FAIL' (got {result!r}) -- a control that does not "
                f"fail is not evidence the gate can discriminate; see the "
                f"contact-residue-Jaccard case in docs/GATE_TYPING_LAW.md, "
                f"where every pair (including different-ligand pairs) passed "
                f"the same threshold"
            )
        value = fields.get("negative_control_value")
        if value is not None and not value:
            errors.append(f"gate {label!r}: negative_control_value is empty")

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
    seen_ids: dict[str, int] = {}
    type_p_count = 0
    type_u_count = 0

    for i, record_lines in enumerate(records, start=1):
        fields, parse_errors = parse_record(record_lines, i)
        all_errors.extend(parse_errors)
        record_errors = check_record(fields, i)
        all_errors.extend(record_errors)

        gate_id = fields.get("gate")
        if gate_id:
            if gate_id in seen_ids:
                all_errors.append(
                    f"gate {gate_id!r}: declared more than once "
                    f"(records #{seen_ids[gate_id]} and #{i})"
                )
            else:
                seen_ids[gate_id] = i

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
            f"(docs/GATE_TYPING_LAW.md)."
        )

    if all_errors:
        print(f"gate-typing check: FAIL -- {len(all_errors)} problem(s):")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("gate-typing check: PASS -- every declared Type P gate carries a "
          "negative control recorded as FAIL.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
