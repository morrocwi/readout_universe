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

## The chain

    δ_R → Adm_δR → F_DRL → S_DRL → (𝔗⁺,𝔗⁻) → J_C → T → K → Y → I_read → P

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

## What the ledger shows at a glance

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
