# Verified runs — executed check log

Rule: a claim from `claims.md` may be cited as `finite_diagnostic`/`Th_coqc` only
if a dated executed run appears here (machine-dependent timings are never claimed).

## 2026-07-19 — development workstation (Ubuntu, Python 3 miniforge, Coq 8.20.1)

| Check | Command | Result |
|-------|---------|--------|
| C1–C3 | `python3 code/LTP1_logic_as_residual_flow.py` | `SUITE: PASS 3/3` — C1 V→8.20e-26, 0 violations; C2 +1.000→−1.000; C3 mean V=0.00795>0 |
| C4–C6 | `python3 code/LTP2_3_4_battery.py` | `SUITE: PASS 8/8` — LTP2 3/3 (flip n=1039@Π=0.5, n=2414@Π=0.8); LTP3 2/2; LTP4 3/3 (rank 3/4, det=0) |
| C7 | `coqc code/UPL_Sorites.v` | exit 0; 3× `Closed under the global context` |

All expected values match `claims.md` exactly. Note: README floor is Coq 8.18;
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

## 2026-07-19 — DRL three gates (multi-agent run, ทุกด่านมี verifier)

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

## 2026-07-19 — AP9: falsifier ของ stance "coupling = 1/k_eff"

| Check | Command | Result |
|-------|---------|--------|
| AP9 (4 tests: 1/α ที่ Planck = 33.3/49.4/52.4; shared-k spread 42% = ตายที่ precision รอดแค่ order-of-magnitude; adjoint-dim map ตาย 76%; numerology exhibit 12% ติดป้าย "ไม่ใช่หลักฐาน") | `python3 -m pytest ap/ap9_coupling_channels.py -q` | 4 passed |

## 2026-07-19 — Coq general-N Legendre (Task #2 ปิด)

| Check | Command | Result |
|-------|---------|--------|
| `DRL_General_Legendre.v` (general-N/heterogeneous/abstract-graph+potential D-cancellation + kinetic corollary) | `coqc evidence/DRL_General_Legendre.v` | exit 0; **2× Closed under the global context (axiom-free)** |
| Solver PR #185 merged after adversarial audit APPROVE (51ea29b): ℚ-port 6/6 axiom-free + THEOREM_INDEX + ledger amendment proposal (ledger row untouched, gated on ratification) | — | merged, verified on solver main |

## 2026-07-19 (ดึก) — AP9 sharpening: Λ-anchor

| Check | Command | Result |
|-------|---------|--------|
| Λ-anchor: 1/α₃(M_P) = (b₃/2π)·ln(M_P/Λ) ทั้งก้อน; depth ฝั่ง coupling 47.05 vs ฝั่งมวลอิสระ ln(m_Pl/m_p)=44.04 — ต่างกัน 3.01 = ln(m_p/Λ) **pin ในบ้านทั้งสองฝั่ง** | `python3 -m pytest ap/ap9_coupling_channels.py -q` | 5 passed |

Full suite: `python3 -m pytest -q` → **56 passed**.

## 2026-07-19 (ดึก) — AP10: b₁₂₃ แยกร่าง (ไม่ใช่ derive)

| Check | Command | Result |
|-------|---------|--------|
| AP10 (3 tests exact-Fraction: counting×atoms คืน (7, 19/6, 41/10) เป๊ะ; abelian ไร้ selfload; atoms load-bearing ทุกตัวด้วย sensitivity pin) | `python3 -m pytest ap/ap10_b_decomposition.py -q` | 3 passed |

Full suite: `python3 -m pytest -q` → **59 passed**.

## 2026-07-19 (ดึกมาก) — AP11: อะตอมสามเม็ดยุบเป็นสูตรเดียว

| Check | Command | Result |
|-------|---------|--------|
| AP11 (4 tests: (−1)^{2s}[(2s)²−1/3] คืนอะตอมทั้งสาม exact; reconstruct slopes AP10; ⟨cos²⟩=1/d pinned d=3(0.3342)+d=4(0.2500) [seeded MC ของเทสจริง]; paramagnetic axis = (2s)² ทุก s∈{0..2}) | `python3 -m pytest ap/ap11_spin_atoms.py -q` | 4 passed |

Full suite: `python3 -m pytest -q` → **63 passed**.

## 2026-07-19 (ปิดคืน) — AP12: กราฟคายอะตอม 1/d เอง

| Check | Command | Result |
|-------|---------|--------|
| AP12 (3 tests: direction-partition 1.000/0.486/0.342 บน tori d=1,2,3 [target 1, ½, ⅓]; spectral-dim 1.1/2.3/3.3 เรียงถูก; size-control ยืนยันอ่านมิติไม่ใช่ขนาด) | `python3 -m pytest ap/ap12_dimension_readout.py -q` | 3 passed |

Full suite: `python3 -m pytest -q` → **66 passed**.

## 2026-07-20 — development workstation (ANSE.ASIA workstation, Coq 8.20.1) — URR-C foundational chain compiles

Tier CORRECTION, not a new proof: no new theorem or physics was added in this run.
The prior manifest status (`formal_draft_pending_coqc`, `machine_checked_now: false`)
was drafted on a machine with no coqc available and understated the chain's real
status; this run supplies the missing executed evidence.

| Check | Command | Result |
|-------|---------|--------|
| `evidence/RD.v` → `evidence/DRL_Discrete.v` → `evidence/DRL_General_Legendre.v` → `evidence/URR_C_Foundational_Chain.v` | `make verify-urr-coq` (git rev `daa2f36274bd2afb466de46c5e6f11220beeba9a`) | exit 0; 132× `Closed under the global context` across the run (123/124 `Print Assumptions` calls in RD.v — the sole exception `Con_PA_classical` reports the expected `classic` axiom — plus 2/2 in `DRL_General_Legendre.v` plus all 7/7 in `URR_C_Foundational_Chain.v`: `F0_RD4_retained_difference_injective`, `F3_lifted_recompose`, `F4_master_implies_component_equations`, `F5_balanced_cut_conserves_declared_total`, `F6_append_cell_injective`, `F7_declared_left_decoder_recovers_message`, `foundational_master_chain_core`) |
| `evidence/URR_C_Foundational_Chain.v` Admitted/Axiom/admit./Parameter scan | `grep -nE "Admitted\|^ *Axiom\|admit\.\|Parameter " evidence/URR_C_Foundational_Chain.v` | no matches (grep exit 1 = clean; file is fully axiom-free) |
| Full suite | `python3 -m pytest -q` | **66 passed** (unchanged from the row above — no test count regression) |

Re-verified after rebasing this work onto the AP18 commits (upstream `95260e6`, pushed to the
same branch concurrently): `make verify-urr-coq` exit 0 and `python3 -m pytest -q` 66 passed
again. The `daa2f36…` rev above is the provenance of the original run, not the current head —
this branch is being rebased as it moves, so re-run the two commands rather than trusting a rev.

See `v2/urr/URR_C_COQ_FORMAL_CHAIN.yaml` and `v2/urr/URR_C_COQ_FORMAL_CHAIN.md` for the
per-theorem tier update this run authorizes (only theorems named in a `Print Assumptions`
"Closed under the global context" line move to `Th_coqc`; `Dr`/`Open` rows are untouched).
