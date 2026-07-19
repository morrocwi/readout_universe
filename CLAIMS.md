# CLAIMS — one falsifiable statement per row (v1.0, 2026-07-19)
| # | Claim | Check | Expected |
|---|-------|-------|----------|
| C1 | Inference-as-descent converges monotonically under constant evidence | `python3 code/LTP1_logic_as_residual_flow.py` | C1 PASS; V -> 8.2e-26; 0 violations |
| C2 | A settled conclusion revises under an evidence flip | same | C2 PASS; +1.000 -> -1.000 |
| C3 | Residual floor never reaches zero under noise | same | C3 PASS; mean V = 0.00795 > 0 |
| C4 | Sorites: smooth world, exactly one readout jump, jump tracks Pi | `python3 code/LTP2_3_4_battery.py` | LTP2 3/3 PASS |
| C5 | Bounded inference diverges iff discarded difference is load-bearing | same | LTP3 2/2 PASS |
| C6 | Distinct worlds with identical records; Fisher singular | same | LTP4 3/3 PASS |
| C7 | Sorites core machine-checked axiom-free (monotone scope) | `coqc code/UPL_Sorites.v` | exit 0; 3x Closed |

## We do NOT claim
finite_diagnostic = proof; Coq scope beyond monotone g; B1 uniqueness; Goedel/liar/ethics solved;
supersession of any tradition in Part IV; machine-independent timings.
