# Verified runs — executed check log

Rule: a claim from `CLAIMS.md` may be cited as `finite_diagnostic`/`Th_coqc` only
if a dated executed run appears here (machine-dependent timings are never claimed).

## 2026-07-19 — Lenovo Legion 5 15ARH05 (Ubuntu, Python 3 miniforge, Coq 8.20.1)

| Check | Command | Result |
|-------|---------|--------|
| C1–C3 | `python3 code/LTP1_logic_as_residual_flow.py` | `SUITE: PASS 3/3` — C1 V→8.20e-26, 0 violations; C2 +1.000→−1.000; C3 mean V=0.00795>0 |
| C4–C6 | `python3 code/LTP2_3_4_battery.py` | `SUITE: PASS 8/8` — LTP2 3/3 (flip n=1039@Π=0.5, n=2414@Π=0.8); LTP3 2/2; LTP4 3/3 (rank 3/4, det=0) |
| C7 | `coqc code/UPL_Sorites.v` | exit 0; 3× `Closed under the global context` |

All expected values match `CLAIMS.md` exactly. Note: README floor is Coq 8.18;
this run used 8.20.1 — compiles clean, axiom-free check intact.

## 2026-07-19 — evidence/ clone re-verification (same machine, Coq 8.20.1)

| Check | Command | Result |
|-------|---------|--------|
| RD object stratum | `cd evidence && coqc RD.v` | exit 0; discrete core `Closed under the global context`; some sections report `classic` (see evidence/README.md) |
| URCF consolidated | `coqc URCF_RD_All.v` | exit 0; bulk axiom-free; ℝ-touching theorems borrow `classic` / `functional_extensionality_dep` / `ClassicalDedekindReals.*` — recorded un-softened |

## 2026-07-19 — AP protocols (blind trials on same-day arXiv, toy tier)

| Check | Command | Result |
|-------|---------|--------|
| AP1 Hubble identifiability (4 tests: grammar sanity 0.5%, closure-on pins h, closure-off null direction <1e-3, r_s escape percent-level) | `python3 -m pytest ap/ap1_hubble_identifiability.py -q` | 4 passed |
| AP2 FXT Amati reachability (3 tests: extended-jet on-locus exact, compact above-locus monotone, below-locus unreachable ∀p∈[2,3]) | `python3 -m pytest ap/ap2_fxt_amati.py -q` | 3 passed |

Both TOY TIER (declared in file headers). Full suite: `python3 -m pytest -q` → 7 passed, 0.37s.

## 2026-07-19 — lens Phase 1 world-class gates (live solver link)

| Check | Command | Result |
|-------|---------|--------|
| Gates suite incl. G2 dual Guard (Z+I), G9 theorem hook (real hit `sqrt2_is_not_a_readout` + fake-name auto-downgrade), G10 LimitCertificate on 1/n decay, G11 unregistered-pair refusal | `python3 -m pytest -q` | **19 passed** |

## 2026-07-19 — lens Phase 2+3 (triage, timescale atlas, compute muscle, drift detector)

| Check | Command | Result |
|-------|---------|--------|
| Full suite incl. G12 murg triage, G13 tau_c atlas (electron-zone neighbour + floor flag), compute.solve_closure('acceleration')=5.0, vendor md5 drift detector | `python3 -m pytest -q` | **25 passed** |
| evidence/ Coq recompile (opt-in) | `RUN_COQ=1 python3 -m pytest ap/ap0_lens_gates.py::test_evidence_recompiles_opt_in -q` | 1 passed (55.8s) |
