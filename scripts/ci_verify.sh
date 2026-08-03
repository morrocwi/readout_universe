#!/usr/bin/env bash
# CI gate for readout_universe -- one command re-checks the whole repo.
# Exits nonzero on any failure. Pattern copied from
# research_universal_solver/scripts/ci_verify.sh (this repo's sibling).
#
# CRITICAL: never pipe test/coqc output into tail/grep -- a real incident in
# this repo had `pytest | tail` swallow a non-zero exit code and a RED test
# reached a PR. If a log is needed, use `tee` under `set -o pipefail` (below)
# so the pipe's exit status is still the command's, not tee's.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "######## versions ########"
coqc --version | head -1
python3 --version

echo "######## 1/7  LTP battery (code/LTP1, code/LTP2_3_4) ########"
python3 code/LTP1_logic_as_residual_flow.py
python3 code/LTP2_3_4_battery.py

echo "######## 2/7  UPL_Sorites.v (the book's own formal floor) ########"
coqc code/UPL_Sorites.v
rm -f code/*.vo code/*.vok code/*.vos code/*.glob code/.*.aux 2>/dev/null || true

echo "######## 3/7  evidence/*.v chain (in-repo Coq evidence, re-verified) ########"
# No `make` target exists for this on this branch (see evidence/README.md,
# which documents the exact re-verification commands run here). Each file
# is Require-independent of the others -- no fixed compile order needed.
(
  cd evidence
  coqc RD.v
  coqc URCF_RD_All.v
  coqc DRL_Discrete.v
  coqc DRL_General_Legendre.v
  rm -f *.vo *.vok *.vos *.glob .*.aux 2>/dev/null || true
)

echo "######## 4/7  pytest suite (ap/) ########"
python3 -m pytest -q

echo "######## 5/7  gate-typing checker self-test (scripts/test_check_gate_typing.py) ########"
python3 scripts/test_check_gate_typing.py

echo "######## 6/7  gate-typing law (docs/GATE_TYPING_LAW.md) ########"
python3 scripts/check_gate_typing.py gates/GATE_DECLARATIONS.txt

echo "######## 7/7  omega + native_logic (tests/test_omega_all.py, test_claim_ir.py, test_native_logic.py, test_from_omega.py) ########"
python3 -m pytest -q tests/test_omega_all.py tests/test_claim_ir.py tests/test_native_logic.py tests/test_from_omega.py

echo "✅ ALL CI CHECKS PASSED — LTP battery, UPL_Sorites, evidence/*.v chain, pytest, gate-typing self-test, gate-typing law, omega/native_logic all green."
