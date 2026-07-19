# Roadmap v2.0 — earning the title "The Philosophy and Logic of Everything"

> The title is earned node by node through the book's own **three-file binding**
> criterion: human-readable chapter ↔ machine-checked script ↔ executable
> diagnostic, all passing simultaneously. v1.0 has ONE fully bound node (sorites).
> "Of everything" remains a candidacy label with an open boundary until the gates
> below close. No gate may be declared closed without an executed run logged in
> `docs/VERIFIED_RUNS.md`.

## Gate 0 — the lens is law (DONE in scaffold, enforcement ongoing)

- [x] `TRANSLATION_PROTOCOL.md` (Ω_all): every problem translated INTO the
      information-philosophy language before solving; binding rule §4.
- [ ] Enforcement check: every merged v2 analysis shows its Step-1 translation.

## Gate 1 — close the book's own planned protocols (from v1.0 Appendix)

- [ ] **LTP5** liar loop (lifts the liar half of L-10 from `Dr`).
- [ ] **LTP6** AGM postulate check (belief-revision bridge).
- [ ] **LTP7** classical-limit regime map (quantitative L-09).

## Gate 2 — widen the Coq floor

- [ ] Defeasibility (L-06) from `finite_diagnostic` → `Th_coqc`.
- [ ] Sorites beyond monotone g (declared scope limit of `UPL_Sorites.v`).
- [ ] Gödel formal bridge through the null space of a self-referential grammar
      (declared `Open` in v1.0; stance recorded, not claimed).

## Gate 3 — domain nodes to three-file binding (see `DOMAIN_LEDGER.md`)

Order by artifact readiness:
- [ ] D3 universal step: import statement + a book-side LTP that reads τ_c/τ_c\*
      regime split on a toy graph (source theorems are already `Th_coqc`).
- [ ] D6 health: one bound node from the 61-PASS health stream.
- [ ] D7 bounded-AI: LTP3 ↔ 0.5B ceiling — needs the ≥300-sample confirm
      (pilot N=40 is not binding).
- [ ] D2 physics spine: blocked on the corpus's own open falsifiers
      (no surviving readout-vs-readout prediction yet — inherited honestly).

## Gate 4 — applied protocols (AP*)

- [x] **AP1** Hubble-tension identifiability (`ap/ap1_hubble_identifiability.py`,
      4 pytest PASS 2026-07-19) — toy tier: h_CMB shown to lie in the null space
      of the θ★ record once one closure posit is freed; tension relocated to
      closure posits. Upgrade path: full likelihood + error propagation.
- [x] **AP2** Einstein Probe FXTs (`ap/ap2_fxt_amati.py`, 3 pytest PASS
      2026-07-19) — toy tier: below-Amati unreachable by viewing angle
      *within the single-power-law deboost family (E_iso∝δ^p, p∈[2,3],
      toy-assumed)* — family-scoped support for the paper's refutation, NOT a
      bound on structured jets with angle-dependent E_p (GRB 170817A
      literature); Π-selection + null-space demands recorded
      in `v2/POSITION.md` §2. Caveat: abstract-only reading — retract the
      "ยังไม่ปิด" half if the full paper already does selection modeling/Γ-bounds.
- [x] **AP3** DESI DR2 evolving dark energy (`ap/ap3_desi_mirage.py`, 5 pytest
      PASS 2026-07-19) — toy tier, TWO best-fit points tested: BAO+CMB+DESY5
      point near-null within BAO (0.50%, ≤ per-bin floor 0.7–2.5%) → SN-driven
      part reads as cross-chain clash (AP1 structure); BAO+CMB-only point
      leaves 1.33% residual (> best floor) → PARTIAL cross-chain reading only;
      some genuine BAO-side pull remains. Falsifier: BAO-alone full likelihood
      preferring CPL >~2σ.
- [x] **AP4** Φ_FI first run (`ap/ap4_phi_fi.py`, 4 pytest PASS 2026-07-19) —
      the new equation (v2/EQUATION_FI.md) separates closure-borne (Hubble,
      Φ=1.0000) from world-side (control, Φ=0.000) exactly. Next: Coq lift of
      the nested-inclusion bound; Φ_FI on DESI two points + g−2; literature
      novelty falsifier before ANY external claim.
- [x] **AP5** DRL first run (`ap/ap5_drl.py`, 4 pytest PASS 2026-07-19) — the
      Discrete Retention Lagrangian (v2/DISCRETE_RETENTION_LAGRANGIAN.md):
      RD4-forced doubling derives the damped spine from an action (EL residual
      4.4e-10) with conserved distinction charge (drift 1.5e-4) — closes the
      corpus's declared "D-term BORROWED" gap in-repo; Coq lift + general-graph
      + literature falsifier pending.
- [x] **AP6** DRL generalization (`ap/ap6_drl_general.py`, ultracode, 4 pytest
      PASS) — nonlinear+forced+heterogeneous EL derived (2.2e-10); OPEN finding:
      quadratic-H breaks under quartic V (drift 0.119) — hunt H_quartic.
- [x] **AP7** append-only tape record (`ap/ap7_tape_record.py`, 4 pytest PASS)
      — external critique re-executed under our discipline: additive exact
      conservation, RD4-in-dynamics reversibility, Π-window vs tape retention,
      and the γ↔D/M bridge matching DRL's spine envelope <5%. Kinship declared
      (collision models / Sz.-Nagy / Landauer-Bennett). Open: composite
      action+injective-tape (v2/APPEND_ONLY_RECORD.md).
- [x] **AP8** H_quartic found (`ap/ap8_h_quartic.py`, 4 pytest PASS) — AP6's
      0.119 drift was a wrong-charge artifact; the Legendre charge of the
      nonlinear Lagrangian (k2ΦΨ → Ψᵀ∇V(Φ), plus −JᵀΨ) conserves <2e-3 with
      O(dt²) scaling; reduces identically to the linear charge at k4=0.
- [x] **AP9** channel-count falsifier (`ap/ap9_coupling_channels.py`, 4 pytest
      PASS) — naive "coupling = 1/k_eff" maps KILLED at precision (adjoint-dim
      76% off; shared-k spread 42%); surviving content = b0-as-channel-count
      (standard) + order-of-magnitude shared budget; restated target (2026-07-19 late,
      external-AI exchange): derive the SLOPES (b1,b2,b3) from the
      Degree-Circulation grammar — 52 then emerges free as accumulated
      impedance (Λ-anchor test pinned: whole value = slope×depth, no
      boundary residue; same depth 47 as the proton hierarchy);
      anti-numerology exhibit pinned.
- [x] **AP10** b₁₂₃ decomposed (`ap/ap10_b_decomposition.py`, 3 pytest PASS,
      exact rationals) — (41/10, 19/6, 7) = SM representation COUNTING × three
      universal kinematic atoms (11/3 gauge-selfload / 2/3 Weyl / 1/3 scalar);
      abelian = zero circulation-like selfload (why U(1) grows UV-ward).
      Falsifier moved one level deeper: derive the THREE ATOMS from the
      Degree−Circulation grammar (spin/orientation of graph channels) —
      then b₁₂₃ and 52 all emerge free. [Open + stance; ledger: this file
      derives NOTHING new — Gross-Wilczek-Politzer kinship declared.]
- [ ] **AP11+** further blind trials on problems with unknown frontier answers —
      the standing test of the "no philosophy does this cheaper" stance
      (`v2/POSITION.md` §5).

## Standing rules (inherited, binding)

- Executed-run-before-claim; runs logged in `docs/VERIFIED_RUNS.md`.
- Borrowed-vs-derived verdict quoted for every imported physics element.
- Readout-vs-readout only; the Ω_∞ / zero-infinity guard runs before deferring
  to any external benchmark's verdict.
- Prose adds no domain: artifact or absence, stated plainly.
