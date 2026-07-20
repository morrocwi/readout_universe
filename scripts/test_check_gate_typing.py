#!/usr/bin/env python3
"""test_check_gate_typing.py -- self-test for scripts/check_gate_typing.py.

Not part of the ap/ pytest suite on purpose (pytest.ini scopes testpaths
to ap/ deliberately -- see the comment there). This is a standalone
stdlib-only script, invoked directly by scripts/ci_verify.sh, that drives
the checker as a subprocess against small fixture files and asserts exit
codes and, where it matters, that the right problem is actually named in
the output (not just "it failed for some reason").

Every case here traces to a real finding from an independent-review round
on this checker. Three rounds so far:

  Round 1 (accepted a self-declared "FAIL" literal next to unrelated
  numbers):
  - test_egfr_arithmetic_contradiction_is_rejected
  - test_non_numeric_values_rejected

  Round 2 fix of round 1 (self-testing this checker found more holes
  before round 2 was even reported):
  - test_nan_and_inf_values_rejected

  Round 3 (round 2's fix still let the record pick WHICHEVER operator
  made its own arithmetic read FAIL, since operator was still declared
  on the control, not the gate; also found the homoglyph table and the
  blank-field stripping both had real coverage gaps):
  - test_operator_choice_attack_is_impossible: the chair's own worked
    counter-example -- a >= 0.80 gate with a control of 0.95 (which
    obviously PASSES the real gate) cannot be smuggled through by
    declaring a self-serving operator, because there is no longer a
    place in the record to declare one; the gate's own
    gate_passes_when is the only predicate that exists.
  - test_negative_control_result_is_derived_not_trusted: a record that
    lies in its (optional) negative_control_result field is still
    rejected, because that field is never read to compute the result.
  - test_uppercase_cyrillic_homoglyph_duplicate: the chair's exact
    SOME_KEY_GATE / SOME_КEY_GATE pair (Cyrillic U+041A), which the
    round-2 lowercase-only table (applied after casefold) missed.
  - test_widened_invisible_chars_rejected: U+3164 HANGUL FILLER and
    U+00A0 NBSP, neither of which is Unicode category Cf, both of which
    must still count as "no real value".

  Carried forward from round 2 (still valid under the new format):
  - test_duplicate_ids_case_and_homograph: ASCII case + lowercase
    Cyrillic homograph.
  - test_zero_width_space_field_rejected: U+200B specifically (Cf).
  - test_genuine_failing_control_accepted / test_type_u_still_accepted:
    the checker isn't just rejecting everything.
  - test_missing_declarations_file_is_trivial_pass.

Run directly: python3 scripts/test_check_gate_typing.py
Exits 0 if all assertions pass, 1 (with the failing assertion named) if
not -- so it is a normal CI gate step, not a pytest-only artifact.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKER = REPO_ROOT / "scripts" / "check_gate_typing.py"

FAILURES: list[str] = []


def run_checker(contents: str) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    ) as f:
        f.write(contents)
        path = Path(f.name)
    try:
        return subprocess.run(
            [sys.executable, str(CHECKER), str(path)],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
    finally:
        path.unlink(missing_ok=True)


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  [PASS] {name}")
    else:
        print(f"  [FAIL] {name}  {detail}")
        FAILURES.append(name)


def test_egfr_arithmetic_contradiction_is_rejected() -> None:
    """The exact record from docs/GATE_TYPING_LAW.md's Case 1: 0.70 does
    NOT satisfy the gate's own ">= 0.35" predicate as a failing value --
    it satisfies it as a PASSING value. Round-1 of this checker accepted
    this record (exit 0) merely because a result field said "FAIL"; it
    must not."""
    record = """
gate: egfr_c797s_contact_jaccard_same_ligand
type: P
description: same-ligand co-crystal pairs show contact-residue Jaccard >= 0.35
negative_control_name: different-ligand pair, osimertinib vs brigatinib
negative_control_value: 0.70
gate_passes_when: >= 0.35
negative_control_result: FAIL
"""
    result = run_checker(record)
    check(
        "test_egfr_arithmetic_contradiction_is_rejected: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_egfr_arithmetic_contradiction_is_rejected: names the contradiction",
        "SATISFIES the gate's own declared predicate" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def test_operator_choice_attack_is_impossible() -> None:
    """The chair's round-3 worked counter-example: a gate documented as
    ">= 0.80 passes", with a control of 0.95 (which obviously PASSES the
    real gate) -- round 2 of this checker let the record declare its OWN
    operator (e.g. '<=') to make the arithmetic read FAIL regardless of
    what the gate actually does. Under this format there is no field on
    the record where a self-serving operator could even be written --
    gate_passes_when is the gate's own predicate, declared once, and
    0.95 correctly fails it (>= 0.80 is True for 0.95, so the control
    does not fail the gate)."""
    record = """
gate: score_gate_attack
type: P
description: score must be >= 0.80 to pass this gate (high score = pass)
negative_control_name: attempted round-2-style attack
negative_control_value: 0.95
gate_passes_when: >= 0.80
negative_control_result: FAIL
"""
    result = run_checker(record)
    check(
        "test_operator_choice_attack_is_impossible: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_operator_choice_attack_is_impossible: names the contradiction",
        "SATISFIES the gate's own declared predicate" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def test_negative_control_result_is_derived_not_trusted() -> None:
    """negative_control_result must never be read as an input. A record
    with a genuinely failing control (0.10 does not satisfy >= 0.35) but
    a LYING result field ("PASS", when the derived answer is FAIL) must
    still be rejected -- the field is cross-checked against the derived
    value, not trusted."""
    record = """
gate: lying_result_field
type: P
description: control genuinely fails but the result field lies about it
negative_control_name: known-negative case
negative_control_value: 0.10
gate_passes_when: >= 0.35
negative_control_result: PASS
"""
    result = run_checker(record)
    check(
        "test_negative_control_result_is_derived_not_trusted: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_negative_control_result_is_derived_not_trusted: names the mismatch",
        "not an input the checker trusts" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def test_negative_control_result_field_is_optional() -> None:
    """A valid Type P record with NO negative_control_result field at
    all must still be accepted -- the field is optional, not required,
    per the round-3 redesign."""
    record = """
gate: no_result_field_gate
type: P
description: valid record with no negative_control_result field
negative_control_name: known-negative case
negative_control_value: 0.10
gate_passes_when: >= 0.35
"""
    result = run_checker(record)
    check(
        "test_negative_control_result_field_is_optional: exit code is 0",
        result.returncode == 0,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )


def test_non_numeric_values_rejected() -> None:
    record = """
gate: bad_numbers_gate
type: P
description: values that are not numbers must not slip through
negative_control_name: nonsense control
negative_control_value: banana
gate_passes_when: >= not-a-number
"""
    result = run_checker(record)
    check(
        "test_non_numeric_values_rejected: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_non_numeric_values_rejected: flags the control value",
        "not a parseable, finite number" in result.stdout and "banana" in result.stdout,
        f"stdout:\n{result.stdout}",
    )
    check(
        "test_non_numeric_values_rejected: flags the malformed predicate",
        "must be formatted as one operator" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def test_nan_and_inf_values_rejected() -> None:
    """float('nan')/float('inf') parse without raising, but are not
    genuine recorded values -- and 'nan' trivially satisfies "fails the
    gate" against almost any operator (NaN compares False against
    everything but '!='), which would let a fabricated non-value pass
    as a real failing control. Found adversarially testing this checker
    against itself; must be rejected the same as non-numeric text."""
    record = """
gate: nan_gate
type: P
description: nan must not be accepted as a real recorded value
negative_control_name: fabricated
negative_control_value: nan
gate_passes_when: >= 0.35

gate: inf_threshold_gate
type: P
description: inf threshold must not be accepted either
negative_control_name: fabricated
negative_control_value: 0.10
gate_passes_when: >= inf
"""
    result = run_checker(record)
    check(
        "test_nan_and_inf_values_rejected: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_nan_and_inf_values_rejected: nan control value flagged",
        "not a parseable, finite number" in result.stdout,
        f"stdout:\n{result.stdout}",
    )
    check(
        "test_nan_and_inf_values_rejected: inf threshold flagged",
        "must be formatted as one operator" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def test_genuine_failing_control_accepted() -> None:
    """A record where the arithmetic genuinely supports FAIL: 0.10 does
    NOT satisfy >= 0.35. Must pass -- the checker isn't just rejecting
    everything."""
    record = """
gate: genuinely_failing_control
type: P
description: example threshold with a real failing control
negative_control_name: known-negative case X
negative_control_value: 0.10
gate_passes_when: >= 0.35
negative_control_result: FAIL
"""
    result = run_checker(record)
    check(
        "test_genuine_failing_control_accepted: exit code is 0",
        result.returncode == 0,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )


def test_type_u_still_accepted() -> None:
    record = """
gate: honest_type_u
type: U
description: honestly labeled convention gate, no negative control needed
"""
    result = run_checker(record)
    check(
        "test_type_u_still_accepted: exit code is 0",
        result.returncode == 0,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )


def test_duplicate_ids_case_and_homograph() -> None:
    # 'G1' vs 'g1' (ASCII case) and a Latin/Cyrillic homograph pair:
    # gate_c vs gаte_c (the 'a' in the second is U+0430 CYRILLIC
    # SMALL LETTER A, which visually matches Latin 'a').
    record = """
gate: G1
type: U
description: first record

gate: g1
type: U
description: same id, different case -- must collide

gate: gate_c
type: U
description: latin spelling

gate: gаte_c
type: U
description: cyrillic-a homograph of the same id -- must collide
"""
    result = run_checker(record)
    check(
        "test_duplicate_ids_case_and_homograph: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_duplicate_ids_case_and_homograph: reports 2 collisions",
        result.stdout.count("same id as gate") == 2,
        f"stdout:\n{result.stdout}",
    )


def test_uppercase_cyrillic_homoglyph_duplicate() -> None:
    """The chair's round-3 exact demonstration: round 2's homoglyph
    table was applied AFTER casefold, so 'К' (U+041A CYRILLIC CAPITAL
    LETTER KA) casefolds to 'к' (U+043A), which is absent from a
    lowercase-only table -- the classic uppercase IDN confusable set
    (К М Н Т В) silently passed through unmapped. One honest Type U
    record and one fabricated Type P record under a visually identical
    id must be caught as the same id."""
    record = (
        "gate: SOME_KEY_GATE\n"
        "type: U\n"
        "description: honest record, Latin K\n"
        "\n"
        "gate: SOME_КEY_GATE\n"
        "type: P\n"
        "description: fabricated record under a visually identical id (Cyrillic K)\n"
        "negative_control_name: x\n"
        "negative_control_value: 0.10\n"
        "gate_passes_when: >= 0.35\n"
    )
    result = run_checker(record)
    check(
        "test_uppercase_cyrillic_homoglyph_duplicate: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_uppercase_cyrillic_homoglyph_duplicate: reports the collision",
        "same id as gate" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def test_zero_width_space_field_rejected() -> None:
    # description is a single U+200B ZERO WIDTH SPACE -- must count as
    # missing, not present. (Category Cf.)
    record = "gate: zwsp_gate\ntype: U\ndescription: ​\n"
    result = run_checker(record)
    check(
        "test_zero_width_space_field_rejected: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_zero_width_space_field_rejected: names 'description' as missing",
        "missing required field 'description'" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def test_widened_invisible_chars_rejected() -> None:
    """U+3164 HANGUL FILLER (category Lo, NOT Cf) and U+00A0 NBSP
    (whitespace, but confirm it is actually caught rather than assumed)
    must both count as "no real value" -- round-2's Cf-only filter
    missed U+3164, contradicting its own code comment."""
    hangul_filler_record = "gate: hangul_filler_gate\ntype: U\ndescription: ㅤ\n"
    nbsp_record = "gate: nbsp_gate\ntype: U\ndescription:  \n"

    hangul_result = run_checker(hangul_filler_record)
    check(
        "test_widened_invisible_chars_rejected: U+3164 exit code is 1",
        hangul_result.returncode == 1,
        f"got exit {hangul_result.returncode}, stdout:\n{hangul_result.stdout}",
    )
    check(
        "test_widened_invisible_chars_rejected: U+3164 named as missing",
        "missing required field 'description'" in hangul_result.stdout,
        f"stdout:\n{hangul_result.stdout}",
    )

    nbsp_result = run_checker(nbsp_record)
    check(
        "test_widened_invisible_chars_rejected: U+00A0 exit code is 1",
        nbsp_result.returncode == 1,
        f"got exit {nbsp_result.returncode}, stdout:\n{nbsp_result.stdout}",
    )
    check(
        "test_widened_invisible_chars_rejected: U+00A0 named as missing",
        "missing required field 'description'" in nbsp_result.stdout,
        f"stdout:\n{nbsp_result.stdout}",
    )


def test_missing_declarations_file_is_trivial_pass() -> None:
    result = subprocess.run(
        [sys.executable, str(CHECKER), "/nonexistent/does_not_exist.txt"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    check(
        "test_missing_declarations_file_is_trivial_pass: exit code is 0",
        result.returncode == 0,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_missing_declarations_file_is_trivial_pass: says TRIVIAL PASS",
        "TRIVIAL PASS" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def main() -> int:
    print("check_gate_typing.py self-test")
    test_egfr_arithmetic_contradiction_is_rejected()
    test_operator_choice_attack_is_impossible()
    test_negative_control_result_is_derived_not_trusted()
    test_negative_control_result_field_is_optional()
    test_non_numeric_values_rejected()
    test_nan_and_inf_values_rejected()
    test_genuine_failing_control_accepted()
    test_type_u_still_accepted()
    test_duplicate_ids_case_and_homograph()
    test_uppercase_cyrillic_homoglyph_duplicate()
    test_zero_width_space_field_rejected()
    test_widened_invisible_chars_rejected()
    test_missing_declarations_file_is_trivial_pass()

    if FAILURES:
        print(f"\n{len(FAILURES)} assertion(s) FAILED: {FAILURES}")
        return 1
    print("\nall assertions PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
