#!/usr/bin/env python3
"""test_check_gate_typing.py -- self-test for scripts/check_gate_typing.py.

Not part of the ap/ pytest suite on purpose (pytest.ini scopes testpaths
to ap/ deliberately -- see the comment there). This is a standalone
stdlib-only script, invoked directly by scripts/ci_verify.sh, that drives
the checker as a subprocess against small fixture files and asserts exit
codes and, where it matters, that the right problem is actually named in
the output (not just "it failed for some reason").

Every case here traces to a real finding from the reviewer round on this
checker:
  - test_egfr_arithmetic_contradiction_is_rejected: the exact 0.70/0.35
    "FAIL" record from docs/GATE_TYPING_LAW.md, which round 1 of this
    checker WRONGLY accepted. Regression test for Finding 1.
  - test_non_numeric_values_rejected: "banana" / "not-a-number", which
    round 1 also wrongly accepted. Finding 1.
  - test_genuine_failing_control_accepted: a record where the arithmetic
    really does support FAIL -- must still pass, or the checker is just
    rejecting everything.
  - test_duplicate_ids_case_and_homograph: "G1" vs "g1", and a Latin vs
    Cyrillic homograph pair, must both be caught as the same id.
    Finding 2.
  - test_zero_width_space_field_rejected: a field containing only
    U+200B must count as missing, not present. Finding 3.

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
    NOT fail a >= 0.35 gate, no matter what the result field claims.
    Round-1 of this checker accepted this record (exit 0); it must not."""
    record = """
gate: egfr_c797s_contact_jaccard_same_ligand
type: P
description: same-ligand co-crystal pairs show contact-residue Jaccard >= 0.35
negative_control_name: different-ligand pair, osimertinib vs brigatinib
negative_control_value: 0.70
gate_operator: >=
negative_control_threshold: 0.35
negative_control_result: FAIL
"""
    result = run_checker(record)
    check(
        "test_egfr_arithmetic_contradiction_is_rejected: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_egfr_arithmetic_contradiction_is_rejected: names the arithmetic contradiction",
        "arithmetic contradicts the FAIL label" in result.stdout,
        f"stdout:\n{result.stdout}",
    )


def test_non_numeric_values_rejected() -> None:
    record = """
gate: bad_numbers_gate
type: P
description: values that are not numbers must not slip through
negative_control_name: nonsense control
negative_control_value: banana
gate_operator: >=
negative_control_threshold: not-a-number
negative_control_result: FAIL
"""
    result = run_checker(record)
    check(
        "test_non_numeric_values_rejected: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_non_numeric_values_rejected: flags the value",
        "not a parseable, finite number" in result.stdout and "banana" in result.stdout,
        f"stdout:\n{result.stdout}",
    )
    check(
        "test_non_numeric_values_rejected: flags the threshold",
        "not-a-number" in result.stdout,
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
gate_operator: >=
negative_control_threshold: 0.35
negative_control_result: FAIL

gate: inf_threshold_gate
type: P
description: inf threshold must not be accepted either
negative_control_name: fabricated
negative_control_value: 0.10
gate_operator: >=
negative_control_threshold: inf
negative_control_result: FAIL
"""
    result = run_checker(record)
    check(
        "test_nan_and_inf_values_rejected: exit code is 1",
        result.returncode == 1,
        f"got exit {result.returncode}, stdout:\n{result.stdout}",
    )
    check(
        "test_nan_and_inf_values_rejected: both records flagged",
        result.stdout.count("not a parseable, finite number") == 2,
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
gate_operator: >=
negative_control_threshold: 0.35
negative_control_result: FAIL
"""
    result = run_checker(record)
    check(
        "test_genuine_failing_control_accepted: exit code is 0",
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


def test_zero_width_space_field_rejected() -> None:
    # description is a single U+200B ZERO WIDTH SPACE -- must count as
    # missing, not present.
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
    test_non_numeric_values_rejected()
    test_nan_and_inf_values_rejected()
    test_genuine_failing_control_accepted()
    test_duplicate_ids_case_and_homograph()
    test_zero_width_space_field_rejected()
    test_missing_declarations_file_is_trivial_pass()

    if FAILURES:
        print(f"\n{len(FAILURES)} assertion(s) FAILED: {FAILURES}")
        return 1
    print("\nall assertions PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
