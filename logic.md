# Logic — Equation & Operator Ledger (Readout Universe v2.0-dev)

> Pure logic/equation reference sheet. No narrative — see [`philosophy.md`](philosophy.md)
> for the why/what-is/how-do-we-know. Every entry below carries its **source tier
> exactly as given in the source file** (never upgraded here) and a one-line
> pointer to that file. Tier legend:
>
> `Ax` axiom · `Th` theorem · `Th_coqc` machine-checked, axiom-free
> (`Print Assumptions` ⇒ Closed) · `finite_diagnostic` measured/executed,
> not proof · `Dr` declared bridge / human narrative · `Open` not
> established (carries a stance + falsifier at source) · `fit_calibrated`
> fit to data, not derived · `definition` declared object/gate ·
> `exact_algebra` identity proved within an explicitly declared model.

---

## 0. The root

| ID | Statement | Tier | Source |
|---|---|---|---|
| R-δ | **δ_R = (a ♯ b)** — one retained distinction, the primitive | `Ax`/`Dr` | `readout_genesis/README.md`; `v2/INFORMATION_DNA.md` |
| R-L | **L_R := D_W − W** — the graph Laplacian (D_W = weighted degree, W = weighted adjacency); named "the ONE genuinely derived link" from root to trunk | `Th_coqc` | `readout_genesis/README.md` |

### RD1–RD9 — the arithmetic genome

| ID | Statement | Tier | Source |
|---|---|---|---|
| RD1 | `0 : 𝔇` (the empty retention exists) | `Ax` | `v2/INFORMATION_DNA.md` |
| RD2 | `x:𝔇 ⇒ σx:𝔇` (every state can take one more step) | `Ax` | same |
| RD3 | `σx ≠ 0` (a step never erases back to nothing) | `Ax` | same |
| RD4 | `σx = σy ⇒ x = y` (retention = injectivity: distinct histories stay distinct) | `Ax` | same |
| RD5 | `[φ(0) ∧ ∀x(φ(x)→φ(σx))] ⇒ ∀x φ(x)` (induction) | `Ax` | same |
| RD6 | `x ⊕ 0 = x` (concat base) | `Ax` | same |
| RD7 | `x ⊕ σy = σ(x ⊕ y)` (concat step) | `Ax` | same |
| RD8 | `x ⊗ 0 = 0` (layer base) | `Ax` | same |
| RD9 | `x ⊗ σy = (x ⊗ y) ⊕ x` (layer step) | `Ax` | same |
| RD-der | retention order `x ⪯ y :⇔ ∃z (x⊕z=y)`; well-founded (no infinite descent); well-ordering `lt_wf`, `strong_induction`, second-order **categoricity** (every model isomorphic) | `Th_coqc` | `evidence/RD.v` (≈183 Theorem/Lemma decls), `evidence/URCF_RD_All.v` (≈678 decls) — both recompiled in-repo, Coq 8.20.1, exit 0 |

### RAR A1–A8 — logic of retention (formal ancestor, declared correspondence to book's own logic — `Dr`)

| ID | Axiom | Reading |
|---|---|---|
| A1 | distinguishability | a question is a set of candidate distinctions |
| A2 | transport | no inference without an admissible grammar (units/types match) |
| A3 | retention | only distinctions kept above a threshold count as structure |
| A4 | accessibility | derivability ≠ existence (direct/composite/inaccessible) |
| A5 | admissibility | the comparison metric is positive |
| A6 | identity-locking | the same entity tracked through every inference |
| A7 | obstruction | target of inference is consistency O=0, not annihilation |
| A8 | lens | validate through a lens that does not distort |

Source: `v2/INFORMATION_DNA.md` §Stratum 2 (`docs/root/math/Retained_Distinction_Logic.tex` §sec:rar).
Builds: truth = retention-under-transport; validity = zero-section consistency;
negation = access-reversal; contradiction = obstruction-not-explosion; gated
sequent calculus w/ soundness+normalization; modal difference — all `Dr`
relative to this book, formal source not re-verified here.

---

## 1. The trunk equation

**M ∂²Φ + D ∂Φ + K·L_R Φ + ∇V(Φ) = J − η**  (EQ-015)

Mixed tier, per-term ([`EQUATION_LIBRARY_ROOT_TO_SM_STREAM...`]):

| Term | Tier |
|---|---|
| M ∂²Φ | `Dr` |
| D ∂Φ | `finite_diagnostic` |
| K·L_R Φ | `Th_coqc` (admissibility skeleton only) |
| η | `finite_diagnostic`/`Open` |

`λ_c = D²/(4MK)` — `Dr` (EQ-016). Continuum reader form:
`τ_R İ_R + L_R I_R = S_R + η_R` — `finite_diagnostic` (PASS_WITH_LIMITS) (EQ-017).

**Explicit statement:** the trunk's *form* is posited from narrower
assumptions, not forced by the root (`v2/EVERYTHING_BRIDGE.md` §0, Bridge B0
tagged `Dr`). Falsifier of B0: a logical phenomenon of the LTP battery whose
analogue provably cannot be posed on L_R, or vice versa.

**τ_c scale bus:** `τ_c = M/D` (memory time; mass is a readout of τ_c);
`τ_c* = T_osc/(4π)` (every thing's own horizon — the spine "knife-edge");
`τ_c > τ_c*` ⇔ alive/agency-like regime. Per-clause tiers (Universal Step,
`v2/EVERYTHING_BRIDGE.md` §1):

| Clause | Statement | Tier |
|---|---|---|
| S1 | τ_c = M/D; mass is a readout of it | `Th_coqc` (`mass_memory_duality`) |
| S2 | τ_c* = T_osc/(4π); black-hole horizon = spine knife-edge | `Th_coqc` (`spine_lambda_c`, `horizon_is_spine_knife_edge`) |
| S3 | alive/agency-like iff τ_c > τ_c*; true agency adds origination | `Th_coqc` (`self_sensing_loops_if_above_lambda_c`, `InfoAgencySelfReadout`) |

**We do NOT claim** that S1–S3 make mass/horizon/agency claims of this book —
they remain claims of their home repo (`research_universal_solver`), imported
here only by the declared (`Dr`) bridge (`v2/EVERYTHING_BRIDGE.md` §"We do NOT
claim (v2 additions)").

Composite reading "logic = the S3-regime specialization of the one step":
`Dr`.

---

## 2. The Discrete Retention Lagrangian (DRL)

Source: `v2/DISCRETE_RETENTION_LAGRANGIAN.md`. Doubled field X = (Φ,Ψ)ᵀ on
graph nodes × discrete time step n (discrete throughout — no continuum sum).

**𝕃ⁿ[X] = (M/2Δt)·ΔXᵀ(G⊗I)ΔX + (D/2)·Xᵀ(Ω⊗I)ΔX − (Δt/2)·Xᵀ(G⊗(K·L_R + k₂I))X**

where ΔXⁿ = Xⁿ⁺¹ − Xⁿ, and:

- **G = [[0,1],[1,0]]** — retention metric (zero diagonal ⇒ no field has its
  own norm; magnitude exists only paired reader×record).
- **Ω = [[0,1],[−1,0]]** — retention symplectic (carries the D-damping term
  through structure, not by hand).

| ID | Result | Tier | Source |
|---|---|---|---|
| DRL-1 | Euler–Lagrange (variation w.r.t. Ψ) ⇒ `(M/Δt²)Δ²Φ + (D/2Δt)(Φⁿ⁺¹−Φⁿ⁻¹) + K·L_RΦ + k₂Φ = 0`; \|∂S/∂field\| on trajectory = 4.4×10⁻¹⁰ | `finite_diagnostic` | `ap/ap5_drl.py` |
| DRL-2 | Mirror equation (variation w.r.t. Φ) ⇒ Ψ anti-damped; in this linear model Φ,Ψ decouple in EL — Ψ's growth is from its own IC, not handoff from Φ | `Open` (in DRL model) | `ap/ap5_drl.py` |
| DRL-3 | Bilinear invariant `H = M·vΦᵀvΨ + K·ΦᵀL_RΨ + k₂·ΦᵀΨ`; rel. drift 1.5×10⁻⁴ over 4000 steps. Reading H as "conservation of distinction" is `Dr`, not a proved mechanism — counterexample: Ψ₀=0 ⇒ Ψ≡0, H≡0 while Φ dissipates fully | `finite_diagnostic` (measurement) / `Dr` (interpretation) | `ap/ap5_drl.py` |
| DRL-4 | D=0 ⇒ Φ,Ψ obey the same conservation law (Φ=Ψ admissible); reduces to the original theory exactly | `finite_diagnostic` | `ap/ap5_drl.py` |
| DRL-Coq-T1 | EL-identity (iff both directions): dS/dΨ=0 ⟺ damped recurrence; dS/dΦ=0 ⟺ anti-damped — 3-ring, 3-slice scope; 2 classical Reals axioms declared (`sig_forall_dec`, `functional_extensionality`) | `Th_coqc` (declared-axiom form) | `evidence/DRL_Discrete.v` (Coq 8.20.1, exit 0, independently reverified) |
| DRL-Coq-T2 | D-cancellation: Legendre charge H contains no D — pure `ring` identity | `Th_coqc` | `evidence/DRL_Discrete.v` |
| DRL-Coq-T3 | Leapfrog shadow energy exactly conserved at D=0 | `Th_coqc` | `evidence/DRL_Discrete.v` |
| DRL-Coq-genN | General-N Legendre/D-cancellation, axiom-free, list induction: any node count, per-node M_i/D_i, any graph, any potential (abstract w_i — covers k₂qr, quartic Ψᵀ∇V, forcing −JᵀΨ). `H = Σ Mᵢvqᵢvrᵢ + GB + Σ wᵢ` | `Th_coqc` (axiom-free) | `evidence/DRL_General_Legendre.v` |
| DRL-5 | Generalization: random weighted graph N=8, per-node M_i/D_i, quartic V, forcing J — EL residual 2.2×10⁻¹⁰ | `finite_diagnostic` | `ap/ap6_drl_general.py` |
| DRL-6 | **H_nl = Σᵢ Mᵢ vΦᵢvΨᵢ + K ΦᵀL_wΨ + Ψᵀ∇V(Φ) − JᵀΨ** — corrected nonlinear charge; quartic drift <2×10⁻³ (vs 0.119 for the wrong quadratic charge); reduces to linear charge at k₄=0; O(Δt²) confirmed | `finite_diagnostic` | `ap/ap8_h_quartic.py` |

**Novelty ledger (declared, `[Open]`):** doubling-for-action has known
ancestors (Bateman 1931, Caldirola–Kanai, CTP/Keldysh, Galley 2013 general
nonconservative variational doubling, Marsden–West discrete variational
integrators) — must never be cited as originated here. Candidate-novelty
layer only: (a) the discrete-graph tensor form G⊗L_R, (b) Ψ read as *ontic*
record (not auxiliary/fictitious, per RD4), (c) zero-diagonal G read as the
Doctrine of Quantity in metric form. Literature falsifier search (2026-07-19)
found no prior work combining all three — status: `[Open → Dr-leaning]`,
pending external peer review.

---

## 3. Append-Only Tape Record (AP7)

Source: `v2/APPEND_ONLY_RECORD.md`. Posited map (no action — declared cost
vs. DRL): phase state z=(u,w), orthogonal step-conserving C:
`z̃ = Cz → z' = √(1−γ)z̃, ρ = −√γ z̃ → Ψₙ₊₁ = Ψₙ ⊕ ρₙ`.

| ID | Claim | Measured | Tier |
|---|---|---|---|
| T1 | Additive exact conservation: `Q(zₙ)+ΣQ(ρⱼ)=Q(z₀)` | rel. error <10⁻¹²; decay = (1−γ)ⁿ, error <10⁻⁹ (true by construction) | `finite_diagnostic` |
| T2 | RD4-in-dynamics: reconstruct z₀ from (z_N, tape) | error <10⁻⁹; blank-cell recovery <10⁻¹⁰ | `finite_diagnostic` |
| T3 | Π-window vs tape retention: readouts indistinguishable under ε_Π=10⁻⁶ while tape retains distinction ~fully | d_readout <10⁻⁶, d_tape ≈10⁻² | `finite_diagnostic` |
| T4 | γ↔D/M bridge: γ = 1−e^(−(D/M)Δt) matches DRL spine decay envelope (underdamped, uniform regime) | rate diff <5% (reviewer: 0.17%); breaks 85–98% when D > 2Mω_min | `finite_diagnostic` |

Layering (this file's own verdict): DRL = variational layer of damped
readout (has action, Coq-backed); Tape = ontology layer of record (posited,
reversible, additive); T4 = the bridge. "Dissipation = handoff across Π" is
now `finite_diagnostic [in tape model]`; still `Open` in DRL itself (linear
pair decoupled). Kinship: collision models/repeated interactions
(Ciccarello et al. 2022), isometric/Stinespring dilation (Sz.-Nagy 1953),
Landauer 1961/Bennett 1982.

**Cross-repo grounding (2026-07-25):** the pigeonhole point underlying T2/T3
now has an independent, general, `Th_coqc` axiom-free proof in
`research_universal_solver/formal/InfoTrueRecordUnreadable_attempt.v`
(`no_decoder_recovers_state`) — a general non-injective-map theorem, not
DRL/tape-specific, not evidence for or against the tape's own posited B_γ.
Recorded as cross-reference only, not imported.

---

## 4. Φ_FI — Forced-Identification Fraction

Source: `v2/EQUATION_FI.md`.

> **Φ_FI(q; A₁, A₂, C, π) = 1 − V\*(C∖π) / V\*(C)**

q = a same-named quantity two chains A₁,A₂ read · C = closure forcing q₁=q₂
· π = one posit of C released · V = residual energy ½rᵀWr (same functional
as LTP1) · V\* = minimum over parameters.

| ID | Property | Tier |
|---|---|---|
| FI-1 | 0 ≤ Φ_FI ≤ 1 (nested-family inclusion V\*(C∖π) ≤ V\*(C)) | provable by set-inclusion (Coq lift: `Open`/roadmap); asserted numerically | `finite_diagnostic` |
| FI-2 | Φ_FI is always named to its π — no bare Φ | untagged in source (informal statement; no `Dr`/tier bracket assigned) | |
| FI-3 | Decision rule: high Φ_FI ⇒ decisive record identifies π directly | `Dr` | |
| FI-4 | Requires a non-tautological negative control | untagged in source (implemented in `ap4`; no `Dr`/tier bracket assigned) | |
| FI-5 | dof-saturation limitation: an unconstrained free parameter gives a false Φ=1 unless it carries a real prior | `finite_diagnostic` (adversarial-review finding) | |

First runs (`ap/ap4_phi_fi.py`, `finite_diagnostic`, toy tier): Hubble toy
(π=w released) Φ_FI = 1.0000; world-side control (non-absorption) Φ_FI =
0.000; ω_b released with real prior σ=0.00015 ⇒ Φ_FI ≈ 0.025.

**Novelty:** algebraic form is a direct relative of nested-model
likelihood-ratio/Δχ² — standard, not new. Candidate-novelty layer `[Open +
stance]`: attribution-to-a-named-posit semantics + decision rule + mandatory
negative control, vs. literature tension metrics (Δχ², suspiciousness,
Q_DMAP) that measure magnitude, not attribution.

---

## 5. AP20 — Retention Self-Interaction Ratio (conditional, narrow)

Source: `v2/RETENTION_SELF_INTERACTION.md`. Premises: (1) one unital ordered
bilinear composition m(x,y); (2) borrowed commutator curvature
`K(x,y)=m(x,y)−m(y,x)` (noncommutative input is borrowed, not derived from
RD4); (3) self-carrier closure; (4) one common quadratic load (declared,
free overall normalization).

| ID | Result | Tier |
|---|---|---|
| AP20-1 | ε² coefficient of `K(A_x+εa_x,A_y+εa_y)` equals `K(a_x,a_y)` exactly (bilinearity) | symbolic-exact, seed-free (`ap20_symbolic_forcing.py`) |
| AP20-2 | c_self/c_geo = 1; (c_geo+c_self)/c_geo = 2; (c_total/c_geo)² = 4 | `finite_diagnostic`, TOL=1e-11, 100 seeds × 3 load scales — ratio forced to exactly 1 by DECLARED premise (4), not derived |

**Withdrawn (review round 2):** calling `(c_total/c_geo)²=4` a "response
ratio" is withdrawn — no response observable was ever defined; squaring an
asserted number is not a response law. If defined later, belongs here as
`Open`/future work only. Still open: why RD forces a noncommutative channel
algebra; why curvature = commutator; why self-carrier closure; why premise
(4) rather than an independent choice; any SM/RD4-alone derivation.

---

## 6. Physics/logic bridge equations — root→SM stream (core subset)

Full stream: EQ-001 through EQ-071 in
[`EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`]
(imported reference; SoT numbering = `readout_genesis/READOUT_GENESIS_CORE.md`
Appendix C). Only the root→trunk-adjacent entries are reproduced here —
the Standard-Model gauge/representation stream (EQ-018 onward into SU(3),
generation counting, mass fits) is intentionally NOT absorbed; see §7.

| EQ | Statement | Tier |
|---|---|---|
| EQ-001 | ∃ a,b : a ≠ b | `Ax` |
| EQ-002 | ∃ A : A discriminates E₁ ≠ E₂ | `Ax→Th` |
| EQ-003 | A→B ≠ B→A (a directed admissible-transition relation on the retained graph — NOT propositional implication) | `Th` |
| EQ-004 | t(s) := min #steps(s₀ → s) ∈ ℕ | `Th` |
| EQ-005 | τ_c > 0 | `Ax` |
| EQ-006 | t = nΔθ, n∈ℕ, Δθ>0 | `Ax` |
| EQ-007 | v = √(D/τ_c) < ∞ | `Ax/Th` |
| EQ-008 | L_R := D_W − W | `Ax/Th` |
| EQ-009 | 1 RD := one retained-distinction record | `Ax` |
| EQ-010/011 | x_domain --[Enc_Ω]--> x_RD ; y_RD --[Dec_Ω]--> y_domain | `Ax` |
| EQ-015 | trunk equation (see §1) | mixed |
| EQ-016 | λ_c = D²/(4MK) | `Dr` |
| EQ-017 | τ_R İ_R + L_R I_R = S_R + η_R | `finite_diagnostic` (PASS_WITH_LIMITS) |
| EQ-032 | ∀X,R,O,x1,x2: x1≠x2 → O(x1)=O(x2) → ∀D: D(O(x1))=x1 → D(O(x2))=x2 → False (`no_decoder_recovers_state`) | `Th_coqc` |
| EQ-033 | gauge-redundancy analogue: h(x)≠x → O(h(x))=O(x) → no total decoder (`gauge_redundancy_forces_undecodability`) | `Th_coqc` |
| EQ-034 | both true states exist, no total decoder recovers both (`true_state_exists_but_no_total_decoder`) | `Th_coqc` |
| EQ-063 | τ_c = ℏ/(2mc²); m = ħ/(2c²τ_c) — unit/calibration bridge ONLY, does NOT derive EQ-015's M coefficient (8 forcing attempts failed) | `Dr` (bridge) |

Source file for EQ-032–034: `research_universal_solver/formal/InfoTrueRecordUnreadable_attempt.v`
(cross-referenced in `philosophy.md` §1 and `logic.md` §3 above — same
underlying general theorem, cited once per relevant section).

---

## 7. URR-C 0.4 master system (native calculation contract)

Source: `v2/urr/URR_C_MASTER_0_4.md` / `URR_NATIVE_SYSTEM.md`. Doubled
reader–record space 𝒳_T = 𝓗_T ⊕ 𝓗_T, X_n=(Φ_n,Ψ_n)ᵀ; lifted projector
Ō_α = I₂⊗O_α, H̄_α = I−Ō_α.

| ID | Equation | Tier |
|---|---|---|
| URR-1 | 𝓔_DRL[X]_n = 𝓙_{C,n}[X_n] (native DRL forced by balanced cut, not replaced by it) | `Dr`/`definition` |
| URR-2 | Reader spine: M(Φ_{n+1}−2Φ_n+Φ_{n-1})/Δt² + D(Φ_{n+1}−Φ_{n-1})/2Δt + K𝔾_TΦ_n + ∇V(Φ_n) − J_n = P_Φ𝓙_{C,n}[X_n] | `Dr` (forced discrete variational system, not derived from one unified action) |
| URR-3 | Return-transformation kernel: 𝒦_{α←β}(τ) = A_α Ō_α R_α 𝒰_H(τ) H̄_β W_β Ō_β E_β | `exact_algebra` in declared linear model |
| URR-4 | Readable information (linear-Gaussian): I_read(L) = ½log₂det[I + Σ_x^½ 𝒢_L^T Σ_N^{-1} 𝒢_L Σ_x^½] rbit, where 𝒢_L = (C; CF; …; CF^L) | `exact_algebra` under declared distribution |
| URR-5 | Cut-balance gate: ρᵀ𝓙_{C,n}[X]=0 for declared retention covector ρ (AP15: ρ=𝟙) | `definition`/gate |
| F0 | retained-difference injective | `Th_coqc` (`evidence/URR_C_Foundational_Chain.v`) |
| F3 | lifted readout split (`F3_lifted_recompose`) | `Th_coqc` |
| F4 | master projection (`F4_master_implies_component_equations`) | `Th_coqc` |
| F5 | balanced cut conserves declared total (`F5_balanced_cut_conserves_declared_total`) | `Th_coqc` |

AP17 executed run (`finite_diagnostic`): transformed-return rank 2, distance
from identity 1.222, noiseless decoder error 2.3×10⁻¹⁶, Gaussian readable
information 7.825 rbit, echo time 0.885.

Binding boundary (verbatim, `v2/urr/`):
```yaml
native_DRL: derived_narrow
forced_DRL_cut_equations: Dr
linear_hidden_elimination: exact_algebra_in_declared_scope
linear_return_kernel: exact_algebra_in_declared_scope
linear_Gaussian_readability: exact_under_declared_distribution
AP17_runtime: finite_diagnostic
unified_DRL_cut_tape_action: Open
all_retained_states_eventually_return: not_claimed
physical_black_hole_from_native_cut_alone: not_claimed
```

---

## 8. Executable LTP battery (v1.0 formal floor)

Source: `README.md`, `CLAIMS.md`, `code/`.

| Claim | Statement | Check | Tier |
|---|---|---|---|
| C1 | Inference-as-descent converges monotonically under constant evidence | `python3 code/LTP1_logic_as_residual_flow.py` | `finite_diagnostic` (V → 8.2e-26; 0 violations) |
| C2 | A settled conclusion revises under an evidence flip | same | `finite_diagnostic` (+1.000 → −1.000) |
| C3 | Residual floor never reaches zero under noise | same | `finite_diagnostic` (mean V = 0.00795 > 0) |
| C4 | Sorites: smooth world, exactly one readout jump, jump tracks Π | `python3 code/LTP2_3_4_battery.py` | `finite_diagnostic` (LTP2 3/3 PASS) |
| C5 | Bounded inference diverges iff discarded difference is load-bearing | same | `finite_diagnostic` (LTP3 2/2 PASS) |
| C6 | Distinct worlds, identical records; Fisher singular | same | `finite_diagnostic` (LTP4 3/3 PASS) |
| C7 | Sorites core machine-checked, axiom-free (monotone scope only) | `coqc code/UPL_Sorites.v` | `Th_coqc` (exit 0, 3× "Closed under the global context") |

---

## See also

Not fully absorbed here — go to source for full depth:

- **AP0–AP20 applied-protocol chain** (Hubble tension, DESI, muon g−2, JWST,
  the 10⁻³⁹→52→atoms→1/d "mystery ladder", channel-coupling slopes) —
  `v2/MYSTERY_LADDER.md`, `v2/FORCED_IDENTIFICATION.md`, individual
  `ap/apN_*.py` files, `docs/VERIFIED_RUNS.md`.
- **The URR-C sector apparatus in full** (typed hidden/accessible channel
  algebra, tape-type taxonomy, nonlinear return kernels, stability gates) —
  `v2/urr/` (`URR_C_MASTER_0_4.md`, `.yaml`, `URR_C_COQ_FORMAL_CHAIN.md`,
  `CLAIM_LEDGER.yaml`).
- **The full Standard-Model equation stream** (SU(3) closure, generation
  counting, gauge/representation assignment, mass fits, EQ-018–EQ-071) —
  [`EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`],
  cross-referenced against `readout_genesis/READOUT_GENESIS_CORE.md`
  Appendix C (Source of Truth for this numbering).
- **v1.0 book's own logic-of-the-finite-knower chapters** (defeasibility
  L-06, truth-as-tracking L-07, classical logic as idealized projection
  L-09, Sorites/Liar/Ω_∞ L-10, incompleteness-as-identifiability L-11) —
  `main.tex` Part II.

[`EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`]: EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md
