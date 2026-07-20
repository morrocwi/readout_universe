#!/usr/bin/env python3
"""test_check_gate_typing.py -- self-test for scripts/check_gate_typing.py.

Not part of the ap/ pytest suite on purpose (pytest.ini scopes testpaths
to ap/ deliberately -- see the comment there). This is a standalone
stdlib-only script, invoked directly by scripts/ci_verify.sh, that drives
the checker as a subprocess against small fixture files and asserts exit
codes and, where it matters, that the right problem is actually named in
the output (not just "it failed for some reason").

Every case here traces to a real finding from an independent-review
round on this checker. Four rounds so far -- each is named below with the
function that regression-tests it, and NOTHING here is a vacuous
assertion: every check() pairs an exit code with a specific message
substring, not just "did it fail".

  Round 1 (accepted a self-declared "FAIL" literal next to unrelated
  numbers):
  - test_egfr_arithmetic_contradiction_is_rejected
  - test_non_numeric_values_rejected

  Round 2 fix of round 1 (self-testing this checker found more holes
  before round 2 was even reported):
  - test_nan_and_inf_values_rejected

  Round 3 (round 2's fix still let the record pick WHICHEVER operator
  made its own arithmetic read FAIL, since the operator was still
  declared on the control, not the gate; also found the homoglyph table
  and blank-field stripping both had real coverage gaps):
  - test_operator_choice_attack_is_impossible
  - test_uppercase_cyrillic_homoglyph_duplicate
  - test_widened_invisible_chars_rejected (U+3164, U+00A0)

  Round 4 (round 3's one-sided check -- negative control only -- let an
  UNSATISFIABLE predicate vacuously certify every record, since nothing
  ever satisfies it and "does not pass" is trivially true; also found
  the blank-character list still missed U+2800, and the homoglyph table
  still missed three more Cyrillic letters):
  - test_unsatisfiable_predicate_without_positive_control_rejected: the
    chair's own exact reproduction (0.95 against a >= 999999 gate).
  - test_valid_two_sided_record_accepted: a record that genuinely
    discriminates in both directions must still be accepted.
  - test_positive_control_that_fails_gate_rejected: a positive control
    that does NOT satisfy the gate's predicate is rejected the same way
    a bad negative control is.
  - test_braille_pattern_blank_field_rejected (U+2800).
  - test_additional_cyrillic_homoglyphs_duplicate (Ѕ U+0405, Ј U+0408,
    Ӏ U+04C0).

  Carried forward from earlier rounds (still valid under the current
  format):
  - test_duplicate_ids_case_and_homograph: ASCII case + lowercase
    Cyrillic homograph.
  - test_zero_width_space_field_rejected: U+200B specifically (Cf).
  - test_type_u_still_accepted: the checker isn't just rejecting
    everything.
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
ASSERTION_COUNT = 0


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
    global ASSERTION_COUNT
    ASSERTION_COUNT += 1
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
positive_control_name: same-ligand pair (as originally reported)
positive_control_value: 0.47
gate_passes_when: >= 0.35
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
    """Round 3's worked counter-example: a gate documented as
    ">= 0.80 passes", with a negative control of 0.95 (which obviously
    PASSES the real gate) -- round 2 of this checker let the record
    declare its OWN operator to make the arithmetic read FAIL regardless
    of what the gate actually does. Under this format there is no field
    where a self-serving operator could even be written."""
    record = """
gate: score_gate_attack
type: P
description: score must be >= 0.80 to pass this gate (high score = pass)
negative_control_name: attempted round-2-style attack
negative_control_value: 0.95
positive_control_name: genuine pass
positive_control_value: 0.90
gate_passes_when: >= 0.80
"""
    result = run_checker(record)
    check(
        "test_operator_choice_attack_is_impossible: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_operator_choice_attack_is_impossible: names the negative-control contradiction",
        "the recorded negative control" in result.stdout
        and "SATISFIES the gate's own declared predicate" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def test_unsatisfiable_predicate_without_positive_control_rejected() -> None:
    """The chair's exact round-4 reproduction: a gate genuinely
    documented as ">= 0.80 passes" with the predicate instead declared
    as an unreachable ">= 999999". Round 3 of this checker required only
    a negative control, and 0.95 correctly derives "does not satisfy
    >= 999999" -- so the one-sided check vacuously passed (exit 0). The
    two-sided requirement rejects this record outright: there is no
    positive_control_name/positive_control_value field at all, which is
    itself now a missing-required-field error (an unsatisfiable
    predicate cannot admit ANY genuine positive control, so this record
    could never be completed honestly)."""
    record = """
gate: score_gate_unsatisfiable_predicate_attack
type: P
description: score must be >= 0.80 to pass, this control genuinely fails
negative_control_name: attempted attack
negative_control_value: 0.95
gate_passes_when: >= 999999
"""
    result = run_checker(record)
    check(
        "test_unsatisfiable_predicate_without_positive_control_rejected: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_unsatisfiable_predicate_without_positive_control_rejected: names missing positive_control_value",
        "declared Type P but missing 'positive_control_value'" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def test_positive_control_that_fails_gate_rejected() -> None:
    """A positive control that does NOT satisfy the gate's own predicate
    must be rejected the same way a bad negative control is -- 0.10 does
    not satisfy >= 0.80."""
    record = """
gate: bad_positive_control_gate
type: P
description: positive control that does not actually pass the gate
negative_control_name: genuine fail
negative_control_value: 0.10
positive_control_name: fabricated positive
positive_control_value: 0.10
gate_passes_when: >= 0.80
"""
    result = run_checker(record)
    check(
        "test_positive_control_that_fails_gate_rejected: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_positive_control_that_fails_gate_rejected: names the positive-control contradiction",
        "the recorded positive control" in result.stdout
        and "does NOT satisfy the gate's own declared predicate" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def test_valid_two_sided_record_accepted() -> None:
    """A record that genuinely discriminates in both directions -- 0.10
    fails >= 0.35, 0.47 passes it -- must be accepted; the checker isn't
    just rejecting everything."""
    record = """
gate: genuinely_discriminating_gate
type: P
description: example threshold with real controls on both sides
negative_control_name: known-negative case X
negative_control_value: 0.10
positive_control_name: known-positive case Y
positive_control_value: 0.47
gate_passes_when: >= 0.35
"""
    result = run_checker(record)
    check(
        "test_valid_two_sided_record_accepted: exit code is 0",
        result.returncode == 0,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )


def test_type_u_still_accepted() -> None:
    record = """
gate: honest_type_u
type: U
description: honestly labeled convention gate, no controls needed
"""
    result = run_checker(record)
    check(
        "test_type_u_still_accepted: exit code is 0",
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
positive_control_name: nonsense control 2
positive_control_value: 0.90
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
positive_control_name: fabricated 2
positive_control_value: 0.90
gate_passes_when: >= 0.35
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
    """Round 3's exact demonstration: round 2's homoglyph table was
    applied AFTER casefold, so 'К' (U+041A CYRILLIC CAPITAL LETTER KA)
    casefolds to 'к' (U+043A), absent from a lowercase-only table -- the
    classic uppercase IDN confusable set (К М Н Т В) silently passed
    through unmapped."""
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
        "positive_control_name: y\n"
        "positive_control_value: 0.90\n"
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


def test_additional_cyrillic_homoglyphs_duplicate() -> None:
    """Round 4 finding: the homoglyph table still missed Ѕ (U+0405
    CYRILLIC CAPITAL LETTER DZE), Ј (U+0408 CYRILLIC CAPITAL LETTER JE),
    and Ӏ (U+04C0 CYRILLIC LETTER PALOCHKA) -- all visually indistinguishable
    from Latin S, J, I respectively. Disclosed in docs/GATE_TYPING_LAW.md
    as a finite, still-incomplete table; these three are now covered."""
    record = (
        "gate: SDZE_GATE\n"
        "type: U\n"
        "description: latin S spelling\n"
        "\n"
        "gate: ЅDZE_GATE\n"  # Ѕ is U+0405 CYRILLIC CAPITAL LETTER DZE
        "type: U\n"
        "description: cyrillic Dze homograph of the same id\n"
    )
    result = run_checker(record)
    check(
        "test_additional_cyrillic_homoglyphs_duplicate: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_additional_cyrillic_homoglyphs_duplicate: reports the collision",
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
    nbsp_record = "gate: nbsp_gate\ntype: U\ndescription:  \n"

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


def test_braille_pattern_blank_field_rejected() -> None:
    """Round 4 finding: U+2800 BRAILLE PATTERN BLANK (category So) is
    visually blank but was not covered by the Cf/Cc/Mn/Me categories or
    the Hangul-filler list -- "⠀⠀⠀" (three blank Braille cells) survived
    as a "named" negative_control_name."""
    record = "gate: braille_gate\ntype: U\ndescription: ⠀⠀⠀\n"
    result = run_checker(record)
    check(
        "test_braille_pattern_blank_field_rejected: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_braille_pattern_blank_field_rejected: named as missing",
        "missing required field 'description'" in result.stdout,
        f"stdout:\n{result.stdout}",
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
    test_unsatisfiable_predicate_without_positive_control_rejected()
    test_positive_control_that_fails_gate_rejected()
    test_valid_two_sided_record_accepted()
    test_type_u_still_accepted()
    test_non_numeric_values_rejected()
    test_nan_and_inf_values_rejected()
    test_duplicate_ids_case_and_homograph()
    test_uppercase_cyrillic_homoglyph_duplicate()
    test_additional_cyrillic_homoglyphs_duplicate()
    test_zero_width_space_field_rejected()
    test_widened_invisible_chars_rejected()
    test_braille_pattern_blank_field_rejected()
    test_missing_declarations_file_is_trivial_pass()

    print(f"\n{ASSERTION_COUNT} assertion(s) run")
    if FAILURES:
        print(f"{len(FAILURES)} assertion(s) FAILED: {FAILURES}")
        return 1
    print("all assertions PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
