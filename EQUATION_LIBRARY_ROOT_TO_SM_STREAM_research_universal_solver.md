<!-- IMPORTED REFERENCE, not native readout_universe content. This is the sibling research
     ecosystem's own root->Standard-Model equation stream (its ROOT-0 axioms, mother equation,
     Face 10, and SM domain closure chain) -- a DIFFERENT formal system than this repo's own
     DRL/Lens/AP0-AP20 stream. Kept here verbatim as a cross-reference so an AI working in this
     repo can see the sibling stream without switching repos; this file is not part of
     readout_universe's own C1-C7 claims register and carries no v2/ROADMAP status.
     SOT DESIGNATION (2026-07-25): READOUT_GENESIS_CORE.md's Appendix C, in the readout_genesis
     repo (the true root canon), is the primary Source of Truth for this equation stream's
     numbering/tiers/text. The research_universal_solver sibling copy is synced to match it. This
     file is kept in sync with both; if a mismatch is ever found, Appendix C wins. -->

# Equation Library — Root → Standard-Model Stream (imported, synced to READOUT_GENESIS_CORE.md Appendix C)

Tier legend: `Ax` axiom · `Ax→Th` near-forced, one posit · `Th` theorem · `Th_coqc` machine-checked
axiom-free (`Print Assumptions` ⇒ Closed) · `finite_diagnostic` measured/executed · `Dr` human
narrative/design · `fit_calibrated` fit to real data, not derived · `Open` not established.

**Semantic Reading Key (added 2026-07-25, after an external review correctly flagged that this
list, read alone, invites category errors it was never meant to license):**
- `A→B ≠ B→A` (EQ-003) is a directed admissible-TRANSITION relation on the retained graph, NOT
  material implication in propositional logic — it is the root of ordered-tape asymmetry, not a
  logical formula to be "solved" by setting `A=B`.
- "minimal" (EQ-034/EQ-037/EQ-038/EQ-045, etc.) always means the minimum value that still supports
  a NONTRIVIAL retained closure under the stated condition (e.g. `k>1` for EQ-037's `k=3`; the
  alternating-trilinear-witness-vanishes-below-3 argument for EQ-038's `dim V=3`) — never an
  unexplained jump from a bare divisibility/parity fact.
- This list is a COMPRESSED INDEX. The canonical prose in the sibling repos and the underlying
  `.v`/`.py` artifacts remain the full meaning; nothing here overrides them.
- `finite_diagnostic` entries (EQ-051, EQ-056, EQ-060-062, etc.) report a computed result inside a
  DECLARED fixture/regime, never a universal continuum theorem.
- `Th_coqc (abstract) / Open (concrete)` (EQ-021) marks a real, load-bearing split: the general
  algebraic structure is proven for ARBITRARY admissible data; which SPECIFIC object realizes it
  remains a separate, harder, still-open question — see the two-axis table below.

**Two-axis status (Root/Formal vs. Concrete/Architecture — the sibling repo's own required
separation, applied to the entries most at risk of the two axes being collapsed into one):**

| Equation | Root/Formal status | Concrete/Architecture status |
|---|---|---|
| EQ-021 | abstract `𝔾_n^(±)` G-adjoint split: `Th_coqc` | which concrete `𝔾_n` realizes it: `Open` (gated on T1) |
| EQ-032–034 | general non-injective-readout theorem: `Th_coqc` | which field plays "true state"/"record": domain-dependent, unresolved |
| EQ-036–041 | closure inside the declared minimal architecture: `Th_coqc`-adjacent | uniqueness of `SU(3)` over the UNRESTRICTED root: `Open` |
| EQ-045 | blind finite pipeline PASS on fixtures | unique algebra FORCED by the unrestricted root: `Open` |
| EQ-058 | fit formula (geometric mean) is exact arithmetic | the fit itself: `fit_calibrated`, not a derivation |
| EQ-062 | the numeric result is exact (independently rerun) | proposed field-role identification (Φ/Ψ = antimatter/matter): REFUTED |

**Correction to an external reviewer's 2026-07-25 recommendation (kept here for the record, not
silently reconciled):** a pasted review recommended treating SM-G0.1–G0.5 (automorphism-as-gauge)
as still-open "highest priority" work. The sibling repo's own `HANDOFF_NEXT_SESSION.md` and this
file's own Bottleneck survey below already document, from a DIRECT `coqc -q` recompile performed
2026-07-25, that SM-G0.1–G0.6 is closed structurally (axiom-free, 15 `Print Assumptions` calls all
"Closed under the global context"). Not reverted; flagged for transparency.

---

EQ-001  `Ax`         ∃ a,b : a ≠ b
EQ-002  `Ax→Th`      ∃ A : A discriminates E₁ ≠ E₂
EQ-003  `Th`         A→B ≠ B→A
EQ-004  `Th`         t(s) := min #steps(s₀ → s) ∈ ℕ
EQ-005  `Ax`         τ_c > 0
EQ-006  `Ax`         t = nΔθ,  n∈ℕ,  Δθ>0
EQ-007  `Ax/Th`      v = √(D/τ_c) < ∞
EQ-008  `Ax/Th`      L_R := D_W − W
EQ-009  `Ax`         1 RD := one retained-distinction record
EQ-010  `Ax`         x_domain --[Enc_Ω]--> x_RD
EQ-011  `Ax`         y_RD --[Dec_Ω]--> y_domain
EQ-012  `Ax`         Γ ⊢_{α,ρ,κ} φ
EQ-013  `Ax`         A ⇏ A⊗A
EQ-014  `Ax`         !_κA ⊢ A^⊗m,  m ≤ κ

---

EQ-015  `mixed`      M ∂²_t Φ + D ∂_t Φ + K·L_R Φ + ∇V(Φ) = J − η
                      [M∂²Φ: Dr · D∂Φ: finite_diagnostic · K·L_RΦ: Th_coqc (admissibility
                      skeleton) · η: finite_diagnostic/Open]
EQ-016  `Dr`         λ_c = D²/(4MK)
EQ-017  `finite_diagnostic` (PASS_WITH_LIMITS)
                      τ_R İ_R + L_R I_R = S_R + η_R

---

EQ-018  `Dr`         𝔖_n = (G_n, Λ_n, 𝒯_n, Θ_n)
EQ-019  `Dr`         X_n^A = (Φ_n^I, Ψ_n^I)^T
EQ-020  `Dr`         𝔾_n = L_{G_n}⊗I_ℱ + I_{G_n}⊗C_ℱ + C_int,n
EQ-021  `Th_coqc` (abstract) / `Open` (concrete instantiation)
                      𝔾_n^(+) = (𝔾_n + 𝔾_n^adjG)/2      [NOT naive transpose — retention-metric
                      𝔾_n^(-) = (𝔾_n − 𝔾_n^adjG)/2       G-adjoint, per source's own warning]
                      ⟨z, 𝔾_n^(-) z⟩_G = 0      [notation hardened 2026-07-25: same content,
                      stated in the retained inner product so a bare "z^T...z" is not misread as
                      a naive Euclidean transpose bilinear]
EQ-022  `Dr`/`finite_diagnostic` (executable)
                      Reader: M δ_t²Φ_n + D δ_t^cΦ_n + K𝔾[Θ_n]Φ_n + ∇V(Φ_n) − J_n = ℛ_Φ,n
                      Record: M δ_t²Ψ_n − D δ_t^cΨ_n + K𝔾[Θ_n]^TΨ_n + ∇²V(Φ_n)Ψ_n = ℛ_Ψ,n
EQ-023  `finite_diagnostic`
                      ∇V_i(Φ) = a_iΦ_i + b_iΦ_i³
                      (∇²V)_ii = a_i + 3b_iΦ_i²
EQ-024  `finite_diagnostic`
                      A_Φ = M/Δt² + D/2Δt
                      b_Φ,n = ℛ_Φ,n + J_n − K𝔾_nΦ_n − ∇V(Φ_n) + (2M/Δt²)Φ_n + (D/2Δt−M/Δt²)Φ_{n-1}
                      A_ΦΦ_{n+1} = b_Φ,n
EQ-025  `finite_diagnostic`
                      A_Ψ = M/Δt² − D/2Δt
                      b_Ψ,n = ℛ_Ψ,n − K𝔾_n^TΨ_n − ∇²V(Φ_n)Ψ_n + (2M/Δt²)Ψ_n − (M/Δt²+D/2Δt)Ψ_{n-1}
                      A_ΨΨ_{n+1} = b_Ψ,n

---

EQ-026  `Th_coqc` (2026-07-25 grounding)
                      R_O = Γ_{RAR,O}(D_O) = Ω_A∘A∘Π∘T_Σ(D_O)
EQ-027  `Th_coqc` (2026-07-25 grounding)
                      M_A[n] = K_A·θ(E[n]) + η_sel + η_map + η_self
EQ-028  `Th_coqc` (2026-07-25 grounding)
                      M_A[n] ≠ θ(E) ∀n
                      ε_tot = η_sel + η_map + η_self > 0 ∀n
EQ-029  `Dr`         I_Q = I_B + O_C + O_P + O_B

---

EQ-030  `Dr`         Z_n = (Φ_n, Ψ_n, Θ_n, U_n, Σ_n, 𝒯_n, Λ_n)
EQ-031  `Dr`         r = O(X)
                      O(hX) = O(X) ∀X ⟹ h internal rename
                      X ∼ X' ⟺ O(X) = O(X')
                      physical state = [X]
EQ-032  `Th_coqc`    ∀X,R,O,x1,x2 : x1≠x2 → O(x1)=O(x2) →
                      ∀D : D(O(x1))=x1 → D(O(x2))=x2 → False
                      [no_decoder_recovers_state, InfoTrueRecordUnreadable_attempt.v]
EQ-033  `Th_coqc`    ∀X,R,O,h,x : h(x)≠x → O(h(x))=O(x) →
                      ∀D : D(O(h(x)))=h(x) → D(O(x))=x → False
                      [gauge_redundancy_forces_undecodability, InfoTrueRecordUnreadable_attempt.v]
EQ-034  `Th_coqc`    x1≠x2 → O(x1)=O(x2) →
                      (∃x:X, x=x1) ∧ (∃x:X, x=x2) ∧ ¬(∃D:R→X, D(O(x1))=x1 ∧ D(O(x2))=x2)
                      [true_state_exists_but_no_total_decoder, InfoTrueRecordUnreadable_attempt.v]
EQ-035  `Dr`         ⟨x,y⟩_G = x†Gy,  G>0
                      ‖x‖²_G = x†Gx ≥ 0

---

EQ-036  `Th_coqc`-adjacent (§21 closure)
                      Ω(…x_i,x_{i+1}…) = r·Ω(…x_{i+1},x_i…)
                      r² = 1 ⟹ r = ±1
                      r = −1
EQ-037  `Th_coqc`-adjacent (§21 closure)
                      Ω(x_1…x_k) = Ω(x_2…x_k,x_1)
                      (−1)^{k−1} = 1 ⟹ k odd
                      k = 3
EQ-038  `Th_coqc`-adjacent (§21 closure)
                      Ω(x,y,z) = 0 if dim V<3
                      dim V ≥ 3
                      dim V = 3,  V≅ℂ³
EQ-039  `Th_coqc`-adjacent (§21 closure)
                      U†GU = G,  G=I ⟹ U†U=I ⟹ U∈U(3)
EQ-040  `Th_coqc`-adjacent (§21 closure)
                      Ω(Ux,Uy,Uz) = det(U)·Ω(x,y,z)
                      det U = 1
                      SU(3) = {U∈U(3) : det U=1}
EQ-041  `Th_coqc`-adjacent (§21 closure)
                      9 − 1 = 8 = dim su(3)
EQ-042  `Dr`         𝒜 = { h : Oh=O, hF=Fh, h†Gh=G }
                      U'_{j←i} = h_j U_{j←i} h_i⁻¹
EQ-043  `Dr`         H_C = ∏_{e∈C} U_e
                      H_C' = h H_C h⁻¹
                      𝒦_C = H_C − I
EQ-044  `Dr`         𝓕_all = 𝓕_G+𝓕_EM+𝓕_W+𝓕_S+𝓕_res
                      χ4 = 1 − ‖𝓕_res‖²/‖𝓕_all‖²
EQ-045  `finite_diagnostic` (blind pipeline)
                      dim Z(𝔤) = 1
                      𝔤 ≅ u(1)⊕su(2)⊕su(3)
                      dim = 1+3+8 = 12
EQ-046  `Dr`         x ↦ e^{iα}x
EQ-047  `Dr`         x ↦ ρ_R(g)x
                      C_2(R)
                      𝓘 : R_1⊗…⊗R_n → 1
EQ-048  `Dr`         3⊗3̄ → 1+…
                      3⊗3⊗3 → 1+…  via ε_{abc}x^a y^b z^c
EQ-049  `Th_coqc`-adjacent (§21 closure)
                      P/Q ≅ Z₃
                      τ(p,q) = p+2q (mod 3)
                      τ(3)=1,  τ(3̄)=2,  τ(8)=0
                      τ(R⊗8) = τ(R)
                      1+2=0,  1+1+1=0
EQ-050  `Dr`         ℋ_physical ⊆ ℋ_{τ=0}
EQ-051  `finite_diagnostic` (exact pass, Z₃/2D case only)
                      z_e ∈ Z₃
                      u_p = ∏ z_e^ε
                      S = κΣ|u_p−1|²
                      |ω−1|² = 3
                      r = e^{−3κ}
                      q(κ) = (1−r)/(1+2r)
                      ⟨W(C)⟩ = q^{A(C)}
                      σ = −log q > 0
EQ-052  `Dr`/`finite_diagnostic`
                      N_A ≲ μ^A
                      Σ N_A ρ^A ≲ Σ(μρ)^A
                      μρ < 1  ⟺  I_retain=−log ρ > S_surface=log μ
EQ-053  `Th_coqc`-adjacent (§21 closure)
                      S_p(U) = κ‖U−I‖²_F
                      ‖U−I‖² = 6−2Re Tr U
                      K_κ(U) = exp[κ(χ_3+χ_3̄)] = Σ_R c_R(κ)χ_R
                      c_R(κ) = ∫_{SU(3)} K_κ χ_R^*
                      dK/dκ = (χ_3+χ_3̄)K
                      c_R'(κ) = Σ_S(N_{3S}^R+N_{3̄S}^R)c_S
                      c_R(0) = δ_{R0}
                      u = c_3/3c_0
                      v = c_8/8c_0
EQ-054  `Th_coqc`    c_0'(κ) = 2c_3(κ)
                      [source: InfoAllOrderCharacter.v / all_order_character_v1_0.py — a
                      DIFFERENT file than EQ-053's §11; not the same equation block in the
                      original text, footnoted separately per review]
EQ-055  internal exact (§12)
                      P_e = ∫_𝒢 ρ_e(h)dμ(h)
                      P² = P
                      P†_G = P
                      ‖P_eT‖_G ≤ ‖T‖_G

---

EQ-056  `finite_diagnostic`
                      reader roots:  M s² + D s + K = 0  ⟹  Re(s) = −D/(2M)
                      record roots:  M s² − D s + K = 0  ⟹  Re(s) = +D/(2M)
EQ-057  `Dr`/`finite_diagnostic` (dissolves I1-injection)
                      ρ(n) := r^n,  r ∈ ℚ,  r > 1
EQ-058  `fit_calibrated` (3 DISTINCT numbers, same formula, different inputs — NOT an equality)
                      r_U = √(587.963 · 135.827) ≈ 282.597083
                      r_D = √(20.00 · 44.75)     ≈  29.917803
                      r_E = √(206.85 · 16.81)    ≈  58.970290
EQ-059  `Th_coqc` (identity itself) — proposed use as item-1's r: `Open`/REJECTED, not adopted
                      φ = (1+√5)/2,  x²−x−1 = 0
EQ-060  `finite_diagnostic`
                      Δ² = D²−4MK
                      λ_c<1 : Re(s) = ∓D/2M   (K-independent)
                      λ_c>1 : Re(s) = [D±√(D²−4MK)]/2M   (K-dependent)
EQ-061  `finite_diagnostic`
                      step_reader: A_Φ = M/dt² + D/2dt
                      step_record: A_Ψ = M/dt² − D/2dt
EQ-062  `finite_diagnostic` (NEGATIVE finding — refutes its own opening hypothesis)
                      |Φ| envelope:  1.215839 → 0.183275
                      |Ψ| envelope:  1.105998 → 322.802505
                      Φ·Ψ (n=10) = −1.188008  →  Φ·Ψ (n=1999) = −59.738547   (ratio ≈50.28×)

---

EQ-063  `Dr` (bridge/definitional, founder-locked; related check `finite_diagnostic`, D/M vs
        QuTiP residual 7.6×10⁻⁴) — self-caught omission during the founder's bottleneck review:
        EQ-015's M has no equation anywhere in this library connecting it to τ_c, despite the
        mother-equation table's own note that "mass is a readout of τ_c." Numbered at the end to
        avoid renumbering EQ-030 onward; conceptually belongs beside EQ-005/EQ-015.
                      τ_c = ℏ/(2mc²)   [N4 SCALE BUS]
                      m = ħ/(2c²τ_c)   [readout direction — mass is what τ_c looks like]
                      NOTE: this is a unit/calibration bridge, NOT a derivation of EQ-015's `M`
                      coefficient's role or value in the mother equation — that remains posited
                      (8 forcing attempts failed, EQ-015's own tier note). Do not read EQ-063 as
                      closing EQ-015's gap.

EQ-064  `fit_calibrated` (M_joint) / `finite_diagnostic` (accuracy check) — 2026-07-25 RTM
        operational-closure arc. EQ-015's posited `M` is CALIBRATED (not derived) from a declared
        Reader/Record transition tape via method-of-moments EIV correction + independent-
        replicate IV, with a fail-closed Reader/Record 5% agreement gate.
                      M_hat = (a1ᵀy2 + a2ᵀy1) / (2 a1ᵀa2)     [replicate-IV, preferred]
                      M_joint = 1.0004294772248     (0.042948% error vs the disclosed fixture's
                      known M_true=1; 500-seed sweep mean error 0.335552% at σ=1e-5)
                      Merged to main, both repos. Does NOT close EQ-015's `M` the way EQ-063 does
                      not — calibration on a declared synthetic tape, not a root-native derivation.

EQ-065  `declared_finite_architecture` — primitive U/D/E branch tapes for v1.13's Π₀ (EQ-053's
        neighbor). Branch initial conditions EXPLICITLY DISCLOSED AS ARBITRARY/uncalibrated
        (checked directly against every candidate PR in both repos — none derive them).
                      Π₀ = 3λ_U + 3λ_D + λ_E = 6.328453553357985
                      (0.0037% error vs the fixture's known-M reconstruction)
                      REQUIRED CAVEAT: architecturally declared, NOT the same (independently-
                      derived, real-PDG-mass) Π₀≈6.9888 already carried elsewhere in this domain
                      (`item1_fit_calibrated_v1.py`) — must never be conflated (Cross-Role Readout
                      Contamination, this library's own EQ-021 warning pattern repeated here).

EQ-066  `declared_finite_architecture`/`exact_bridge` — order-vacuum threshold closure. α_ord=a/2,
        β_ord=b/4 INHERITED from EQ-023's own mother potential (not new dials).
                      Π₀ > α_ord  ⇒  ORDERED_READY,  r* = 3.823356105009073
                      REQUIRED CAVEAT (independent scientific-methodology review, 2026-07-25):
                      ORDERED_READY on THIS stepper is STRUCTURALLY GUARANTEED regardless of the
                      branch-tape data — λ_j∈(0,1] forces Π₀∈(0,7], and α_ord=−0.5 sits below that
                      unconditional lower bound. Do not cite ORDERED_READY as evidence the branch
                      construction is predictive.

EQ-067  `declared_finite_architecture` — native vacuum amplitude, r=v²/2 convention applied to
        EQ-066's r*.
                      v_native = √(2 r*) = 2.7652689218262565     (no physical unit attached)

EQ-068  `finite_diagnostic` (THREE NEGATIVE FINDINGS, all disclosed, none hidden) — 2026-07-25
        attempts to bridge EQ-067's v_native to real GeV-scale physics, DRAFT/UNMERGED in both
        repos pending resolution of the open discrete-vs-continuum question named below:
        (a) fit Λ_RD→GeV = 246/v_native = 88.96060634765863 (`fit_calibrated`, Attempt-17-style),
            independently predict Higgs mass from EQ-066's radial-curvature proxy (never used in
            the Λ fit): 218.005 GeV predicted vs real PDG 125.20 GeV — 74.13% error, FAILS a 5%
            band.
        (b) SAME test with ZERO fitted parameters via the ratio m_higgs_native/v_native vs real
            m_H/v — identical 74.13% error (Λ cancels algebraically; confirms (a) is real).
        (c) zero-external-input internal consistency: m_from_τc_native := 1/(2·(M_joint/D)) (M/D
            used only as a declared `Dr`-tier ANALOGY to τ_c, not claimed identical to EQ-063's
            τ_c object) vs EQ-067's curvature-mass route — ratio 0.0612, NOT CONSISTENT, 94%
            deviation.
        OPEN QUESTION, explicitly not resolved: whether comparing EQ-064–067's native-unit outputs
        against real GeV values is a valid readout-vs-readout comparison, or a category error
        against a non-readout (dimensional constants ℏ,c,G — see `ZERO_INFINITY_DUAL_DIAGNOSIS.md`'s
        STANDING GUARD) — conflicts with this domain's own routine use of PDG masses as
        `fit_calibrated` inputs elsewhere (e.g. EQ-058); found, not settled, 2026-07-25. A real,
        pre-existing, `Th_coqc` discrete-to-apparent-continuum bridge
        (`PERSISTENT_WALK_TELEGRAPH_DERIVATION.md`, τ_c-parametrized, "partially discharged") was
        located and is structural only — supplies no numeric GeV conversion. An `ultracode`
        multi-agent survey for further candidate bridge mechanisms was launched the same day;
        check `research_universal_solver/domains/standard_model/item1_exploration/
        ITEM1_EXPLORATION_LOG.md` for the outcome before citing this as final.

---

## Bottleneck survey (2026-07-25, CORRECTED same day)

Reading the whole stream in numeric order surfaces one recurring pattern, not a set of unrelated
gaps: the ABSTRACT/GENERAL layer (ROOT-0, Face 10, gauge redundancy, SU(3) closure) is increasingly
`Th_coqc`-backed; the CONCRETE-INSTANTIATION layer — which specific object out of the admissible
space is the real one — is `Dr`/`Open`/`fit_calibrated` every single time it appears:

- EQ-021: `𝔾_n^(±)` split is `Th_coqc` only in the ABSTRACT case; the concrete instance is `Open`.
- EQ-015/EQ-063: `M`'s VALUE/role is posited, not derived (8 failed forcing attempts); the τ_c
  bridge (EQ-063) is a unit calibration, not a derivation of EQ-015's coefficient.
- EQ-042–048: gauge/representation assignment is almost entirely `Dr`.
- EQ-057–059: item 1's `r` — every root-native candidate closed/rejected; terminal state is
  `fit_calibrated`.
- EQ-060–062: matter/antimatter — every concrete field-role instantiation tested (Attempts 1-2) was
  refuted; only the fully general, field-agnostic theorem (EQ-032–034, Attempt 3) survives.

**Correction (sibling repo's own analysis, imported here unmodified):** the first-draft version
named SM-G0.1–G0.5 as the gating node, citing a stale line in the sibling repo's own
`domains/standard_model/README.md`. SM-G0.1–G0.6 (automorphism-as-gauge) was independently
re-verified `coqc -q`-closed, axiom-free, since 2026-07-24. **Honest revised conclusion:** the
closure is STRUCTURAL only (any group) — non-triviality for the actual root dynamics stays `Open`,
which is why EQ-042–048 stay `Dr`. The sibling domain's own currently-tracked highest-leverage P0
item is **generation multiplicity — completely untouched** (Kobayashi-Maskawa CP violation
requires ≥3 generations). Item 1 (Δ_j/κ_j/`r`, EQ-057–059) was already exhaustively tried and
closed only via `fit_calibrated`.

---

Independently peer-reviewed 2026-07-25 against live source (coqc compiles, script reruns, direct
file reads) — 5 corrections applied vs. the first-draft compiled list, see the header note above
for the canonical source. This copy is a reference import; readout_universe's own DRL equations
(v2/DISCRETE_RETENTION_LAGRANGIAN.md) are a separate, independently-derived formal system, already
cross-referenced there (2026-07-25) against EQ-032..EQ-034 above for the shared pigeonhole point.
