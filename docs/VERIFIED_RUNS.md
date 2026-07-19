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

## 2026-07-19 — AP3 blind trial #3 (DESI DR2 evolving dark energy)

| Check | Command | Result |
|-------|---------|--------|
| AP3 (5 tests: grammar sanity/CPL→ΛCDM exact, pivot z∈[0.3,0.6], DESY5-combo near-null 0.50% over 10 BAO observables with (h,ωm) free, BAO+CMB-only point residual 1.33% (NOT fully null — asserted honestly), Ωm-alone insufficient >1%) | `python3 -m pytest ap/ap3_desi_mirage.py -q` | 5 passed |

## 2026-07-19 — AP4: สมการใหม่ Φ_FI (Forced-Identification Fraction)

| Check | Command | Result |
|-------|---------|--------|
| AP4 (4 tests: Hubble closure-borne Φ=1.0000 [V 18.2→0.0000 ปลด w], world-side control Φ=0.000, nested-inclusion bounds, Φ-carries-its-posit) | `python3 -m pytest ap/ap4_phi_fi.py -q` | 4 passed |

## 2026-07-19 — AP5: DRL (Discrete Retention Lagrangian)

| Check | Command | Result |
|-------|---------|--------|
| AP5 (4 tests: EL residual <1e-8 บน trajectory จริง [วัด 4.4e-10] — D-term derive จาก action สำเร็จ; reader ตาย/record โต; ประจุ distinction H drift <1e-3 [วัด 1.5e-4]; reduction D=0 อนุรักษ์) | `python3 -m pytest ap/ap5_drl.py -q` | 4 passed |

## 2026-07-19 — ultracode wf_ddeca0cf-fbb: DRL three gates (6 sonnet agents, ทุกด่านมี verifier)

| Check | Command | Result |
|-------|---------|--------|
| Coq DRL_Discrete.v (T1 EL-iff ×3, T2 D-cancellation, T3 D=0 invariant) | `coqc evidence/DRL_Discrete.v` | exit 0; axioms: sig_forall_dec + funext (declared); verifier recompiled clean-slate + non-vacuousness hand-derivation |
| AP6 general DRL (EL residual 2.2e-10 nonlinear+forced+heterogeneous N=8; H quadratic 2.2e-4; **finding: quartic breaks quadratic-H, drift 0.119**; exact reduction to ap5) | `python3 -m pytest ap/ap6_drl_general.py -q` | 4 passed; verifier re-ran + heterogeneity/tautology probes CONFIRMED |
| Literature falsifier | WebSearch/WebFetch adversarial | novelty SURVIVES ×3 (narrowed); verifier full-text-checked Galley/GraphCON/2309.03286, caught 1 fabricated quote (fixed: paraphrase) |

Full suite after integration: `python3 -m pytest -q` → **43 passed**.

## 2026-07-19 — external-critique check (DRL handoff claim)

| Check | Command | Result |
|-------|---------|--------|
| Decoupling counterexample: Ψ₀=0 run | inline script (ap5 machinery) | **Ψ≡0 ตลอด, H≡0, ขณะ E_Φ 1.99→1.6e-6** — ยืนยันข้อวิจารณ์: H เป็น bilinear invariant ไม่ใช่บัญชีการสูญเสีย; "handoff" downgrade เป็น [Open] |

## 2026-07-19 — AP7: append-only tape record (re-execution ในบ้าน)

| Check | Command | Result |
|-------|---------|--------|
| AP7 (4 tests: additive conservation <1e-12 + decay=(1−γ)ⁿ; RD4 reconstruct <1e-9; Π-window d_readout<1e-6 vs d_tape≈1e-2; bridge γ↔D/M rate mismatch <5%) | `python3 -m pytest ap/ap7_tape_record.py -q` | 4 passed |

## 2026-07-19 — AP8: H_quartic found (ปิดคำถามเปิดจาก ultracode)

| Check | Command | Result |
|-------|---------|--------|
| AP8 (4 tests: quartic drift <2e-3 ด้วย H_nl ที่ถูก [เทียบ >1e-2 ของประจุผิด], forced case <5e-3, ยุบกลับประจุเดิม identical เมื่อ k4=0, O(dt²) via dt-halving) | `python3 -m pytest ap/ap8_h_quartic.py -q` | 4 passed |
