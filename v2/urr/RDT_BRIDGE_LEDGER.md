# RDT Bridge Ledger — one row per arrow, classified

> Companion to `URR_C_MASTER_0_5_PROPOSAL.md`. Where the claim ledger classifies
> *statements*, this classifies the **arrows**: for each step of the chain, is it a
> **THEOREM** (the root forces it), an **ASSUMPTION** (declared, could be otherwise), or a
> **REALIZATION CHOICE** (a decision about what a word means, which then fixes the maths)?
>
> Founder, 2026-07-21: *"พิสูจน์ทีละสะพาน ว่าจากรากไปถึงแต่ละชั้นมีสิ่งใดเป็น theorem สิ่งใดเป็น
> assumption และสิ่งใดเป็น realization choice"*. This file is that instruction made into a table.
>
> Rule: a row may only be marked THEOREM with a named, compiled artifact. Prose is not a proof.

## The chain (v0.7: discovery layer inserted before DRL)

    δ_R → 𝓟_n (Discover) → Adm_δR → F_DRL → S_DRL → (𝔗⁺,𝔗⁻) → J_C → T → K → Y → I_read → P

## The ledger

| # | Bridge | Class | Evidence | Notes |
|---|--------|-------|----------|-------|
| B1 | `δ_R` → the **form** of `L_R` (= `D_W − W`) | **THEOREM** | `forced_into_DW_minus_W` (`Th_coqc`, ℚ) | Forced from {sym3, rowsum0, offdiag≤0}; the natural alternatives each fail at least one, with explicit witnesses. |
| B2 | `δ_R` → the **scale** of `L_R`, i.e. `K` | **NOT A THEOREM — convention** | `InfoKLRSplitGauge_attempt.v` (`Th_coqc`, 18× Closed) | All three defining properties are homogeneous of degree 1, so `t·L` satisfies them for every `t>0`. `K` is the leftover scale. Invariant object is `K·λ`, not `K`. `c²=K/M` is **not** invariant. |
| B3 | `δ_R` → **sign** `D > 0` | **THEOREM** | `InfoFiniteMemoryForcesDissipation` | Forced by refusing infinite memory. The **value** of `D` remains open. |
| B4 | `δ_R` → `M ≠ 0` (second-order inertia) | **NOT A THEOREM — realization choice** | `InfoActionDoesNotForceM_attempt.v` (`Th_coqc`, 9× Closed); EL theorems quantify `forall M` with only `~(h==0)`, `~(dt==0)` | Seven attempts, seven failures. The choice is semantic: `M=0` is a world that only forgets; `M>0` is a world in which a distinction can return unaided. `InfoRetentionForcesSecondOrder_attempt.v` gets `M>0` only after positing that retention *means* re-readable, and fences that posit. |
| B5 | `M=0` systems ∈ `Adm_δR` | **THEOREM** | same witness as B4 | The first concrete inhabitant theorem for `Adm_δR`. The set is genuinely larger than the DRL realization. |
| B6 | `Adm_δR` membership test | **UNDEFINED** | — | §I of the 0.5 proposal states four conditions in prose. A set whose membership cannot be decided is a name, not a definition. Must become decidable or be tagged `Dr`. |
| B7 | `S_DRL` → telegraph pair `(𝔗⁺,𝔗⁻)` | **THEOREM (declared scope)** | `T1_el_psi_node1/node2`, `T1_el_phi_node1` (`Th_coqc`, ℚ, 3-ring, iff both directions) | Damped reader, anti-damped record. Scope is the 3-ring; general-N is not this theorem. |
| B8 | `S_DRL` → the `D` **term's action origin** | **THEOREM (narrow, M-unconstrained)** | ledger row 8 + `InfoRetentionLagrangian_attempt.v` | Wording correction pending (task #13): the derivation happens with `M` free throughout, so it establishes the action origin of `D` inside the doubled carrier, **not** second-order inertia. |
| B9 | doubling `X=(Φ,Ψ)` with `G`, `Ω` | **ASSUMPTION** | ledger row 8's own caveat | The *form* of the doubling — why `G,Ω` take exactly this shape — is posited. This narrows the borrow rather than eliminating it. |
| B10 | `S_DRL` → `J_C` (the cut) | **OPEN** | `open_problems.unified_action` | Not derived from the same action. Current honest name: *forced discrete Lagrange–d'Alembert-type system*. |
| B11 | `S_DRL` → `T` (tape) | **OPEN** | same | Tape injectivity and monotone growth are proved (`F6`), but as declared structure, not as a consequence of `S_DRL`. |
| B12 | `S_DRL` → `K` (return/recovery) | **OPEN** | same | `F7` proves decoder recovery *given* a declared left inverse. Existence of a decoder is not derived. |
| B13 | `S_DRL` → `O_α`, `Π_α` (readout, report) | **OPEN** | same | Deliberately so: the report layer is where apparatus, noise and threshold enter. Removing it would not be progress. |
| B14 | `ρᵀ J_C = 0` (cut conservation) | **THEOREM given a declared `ρ`** | `F5_balanced_cut_conserves_declared_total` (`Th_coqc`) | Conditional on declaring *what* is conserved. `ρ` is domain input. |
| B15 | `Λ_α ∘ Σ_α = I` (readout/residue factorization) | **THEOREM** | `F3_lifted_recompose` (`Th_coqc`) | Lifts correctly to the doubled space. |
| B16 | tape injectivity `E_T(r)=E_T(r′) ⟹ r=r′` | **THEOREM** | `F6_append_cell_injective` (`Th_coqc`) | |
| B17 | discrete → continuum telegraph | **REPORT, not a bridge** | house infinity diagnosis (I2) | Passing to `∂_t²` injects infinite divisibility. Coarse-grained description; must not be read as the root. |
| B18 | `I_read` → one fixed formula | **REJECTED** | — | Must be a domain-dependent functional `𝔦_dom`, not the Gaussian expression pinned universally. |
| B19 | regime selection (which side of `disc = 0`) | **NOT DETERMINED** | `InfoRegimeUnderdeterminedByCausalBound_attempt.v` (`Th_coqc`) | For **every** forced `D≠0`, `λ>0`, both regimes are reachable under the causal bound `K<M`. Universal, not example-based. |
| B20 | `δ_R` → the **discovery** of a normal form from the rules alone | **FINITE_DIAGNOSTIC** | auto-discovery benchmark, reproduced by the orchestrator 2026-07-21 | Hidden exchangeability blocks, randomly relabelled, recovered at N=12/15/18/21; exactness deviation exactly 0.0; amplitude error ~1e-15. First URS result where the abstraction was NOT handed to the solver. |
| B21 | exact-quotient gate `q∘F = F♯∘q` and `O = O♯∘q` | **KINSHIP: lumpability / bisimulation** | Kemeny–Snell (Markov lumpability); bisimulation in process algebra | NOT new mathematics. What is ours is its use as a **mandatory gate before compression** rather than a property checked afterwards. Coq payoff theorem in progress. |
| B22 | `Refine` (the discovery algorithm itself) | **KINSHIP: 1-WL colour refinement** | Weisfeiler & Lehman 1968; equitable partitions of weighted graphs | Standard algorithm. Ours is the composition: refinement as an *admissibility* test, audit gating compression, cells splitting on any real distinction, refusal-to-compress as a first-class outcome. |
| B23 | `D_syn = ∏_c (|C_c|+1)` | **FINITE_DIAGNOSTIC (exact match)** | benchmark, checked by the orchestrator | Predicts 125/216/343/512 for cells 4×4×4 / 5×5×5 / 6×6×6 / 7×7×7 — matches the measured quotient dimension exactly at all four sizes. |
| B24 | discovery works on **generic** systems | **REFUTED** | orchestrator noise sweep, N=15, 2026-07-21 | Adding noise to θ and couplings: 0 and 1e-14 → 3 cells, 151.7× compression; **1e-10 → 15 singleton cells, zero compression**; same at 1e-8, 1e-6, 1e-3. The cliff sits at the refinement's own rounding tolerance, far below any physical precision. The method works on **exactly**-symmetric models, and exact symmetry is measure-zero in parameter space. |
| B25 | refusal to compress when there is nothing to find | **FINITE_DIAGNOSTIC** | random-coupling control (10 singleton cells) + defect control (splits 1×4×5×5) | Both controls could have failed and did not. Note this control is *also* the statement of B24's limitation. |
| B26 | discovery algorithm covering **all** normal-form types | **OPEN** | — | Current method finds structure encoded directly in a weighted interaction graph with exactly equal parameters. Nothing is claimed beyond that. |
| B27 | tolerance-aware refinement with a bounded observable error | **NOT ATTEMPTED** | — | The well-posed next experiment: merge cells agreeing within ε and bound the induced readout error. Falsifiable — if no ε buys useful compression inside the error budget, approximate URS is dead. |
| B28 | discovery on a **chaotic generic** system | **NO COMPRESSION — measured, and correct** | founder's N=128 softened-gravity N-body, 2026-07-21 | Chaos verified rather than assumed: `d(10)/d(0) ≈ 4.07e3`, finite-time `λ_fit ≈ 1.48 > 0`, energy drift 2.6e-4. Every particle differs in mass, position, velocity and interaction profile, so no pair passes the exact gate: `𝓟 = {{1},…,{128}}`, `D_syn = N`, compression ratio exactly 1. URS is **slower** than direct here (discovery + audit overhead on top of Θ(N²)). This is the framework behaving correctly, not failing. |
| B29 | forced coarse quotient without the gate | **REFUTED — 64% force error** | same run, N=512 → 48 cells | Compression 10.67× but relative force error `ε_F = 0.642`, worst particle 225%. Fails `q∘F = F♯∘q` decisively, and in a chaotic system that error is amplified exponentially in time. Empirical companion to `flaw_readout_disagrees_values`: skipping the gate does not give an unproven answer, it gives a wrong one. |
| B30 | the approximate-quotient-with-error-certificate layer | **KINSHIP: FMM / Barnes–Hut** | Barnes & Hut 1986 (O(N log N), opening angle θ); Greengard & Rokhlin 1987 (FMM, O(N), rigorous error bounds) | The layer v0.7's own conclusion says URS needs for N-body **already exists**: the multipole acceptance criterion IS an admissibility gate, adaptive tree refinement IS cell splitting on a real distinction, and the multipole truncation bound IS the error certificate. Declaring this kinship first is what makes the remaining question askable: what does URS add that FMM does not already have? |
| B31 | `≈_{α,δ,H}` finite-horizon readout equivalence | **KINSHIP: approximate bisimulation** | Desharnais–Gupta–Jagadeesan–Panangaden (bisimulation metrics 2004); Girard & Pappas (approximate bisimulation 2007–11) | Behavioural equivalence with a precision parameter is an established object with its own error-propagation theory. Ours is the insistence that it never widens `=_R` or `≡_exact`. |
| B32 | load-bearing score `𝔏 = sup‖DΠ·DO·DF^{[h]}·𝔡‖` | **KINSHIP: dual-weighted residual** | Becker & Rannacher (DWR 1996–2001) | "Local residual × adjoint sensitivity → refinement indicator" is the standard goal-oriented AFEM construction, line for line. |
| B33 | expiring licence `τ_share`, refresh-or-refine | **KINSHIP: certified reduced-basis / online-adaptive ROM** | Rozza–Huynh–Patera 2008; Peherstorfer & Willcox 2015 | A rigorous a posteriori bound that triggers enrichment when exceeded. Ours is making the licence a first-class object with an expiry. |
| B34 | residual tape with certificate (§30) | **OURS — the distinctive piece** | follows from RD4 | Every method above computes an indicator and **discards** what it dropped. Here the discarded residual is retained with its certificate, so compression is auditable and reversible. Not a performance feature; forced by the ontology. |
| B35 | `𝔏` is computable in the chaotic regime it targets | **SELF-LIMITING — flagged, not yet repaired** | tangent/adjoint operator grows like `e^{λh}` | The gate's decision variable is built from a linearisation that diverges exponentially, and whose first-order validity expires within a few Lyapunov times — precisely the regime §28 addresses. Certificate and certified object degrade together. Candidate repair: Least Squares Shadowing (Q. Wang 2013–14). |

## What the ledger shows at a glance

**Discovery layer (v0.7, added 2026-07-21):** the exact-quotient gate is real and now has a
row of its own, but two of its three rows are kinship rows, and B24 records the cliff that the
architecture document does not: the method collapses at one part in 10^10.

**Forced from the root:** the form of `L_R`, the sign of `D`, and — inside the DRL
realization and its declared scope — the telegraph pair. That is a short list, and it is
honest.

**On the card (two entries, and only two at this level):** `M`, because it decides what
*retained* means; `K`, because it is the unit of distinction. Everything else at this level
is either forced or explicitly open.

**Open, and correctly so:** the single action that would derive the cut, tape, recovery and
report together. Six of nineteen rows are Open. A version claiming fewer would be claiming
more than it has.

## Naming

The founder proposes **RDT Master v0.5** — *Philosophy-First Retention–DRL–Telegraph Master
Architecture* — as the current canonical master version. The architecture earns that. One
process caution: it should not be labelled canonical while `URR_C_MASTER_0_4.md` still stands
unamended in the same directory and the two blocking corrections (B2, B4) are unapplied, or
the repository acquires exactly the failure it is designed to prevent — two documents in one
place disagreeing about the same object, with the reader's belief decided by which one they
open first.
