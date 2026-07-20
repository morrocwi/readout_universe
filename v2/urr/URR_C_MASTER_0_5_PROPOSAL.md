# URR-C 0.5 — proposal: the retention → admissible-law → DRL → telegraph hierarchy

> **Status: PROPOSAL. Not canonical. Does not replace `URR_C_MASTER_0_4.md`.**
> Author: founder, 2026-07-21. Assessed and annotated by the orchestrator the same day.
> Nothing here is promoted until the corrections in §3 are applied and an independent
> cross-vendor review passes.

## 1. Verdict — yes, this is an upgrade

It is an upgrade for three specific reasons, not as a general impression.

**1.1 It introduces `Adm_δR`, the set of admissible dynamical laws.** Version 0.4 jumped
straight from the retention root `δ_R` to one particular action. That jump quietly implied
the action was forced. Naming the intermediate object — *the set of laws retention permits* —
is the single most valuable structural change in the proposal, because it creates the place
where the framework's real boundary lives. Everything the root fails to force is a statement
about the size of `Adm_δR`, and until now there was no slot to write those statements into.

**1.2 It puts the telegraph equation in the right ontological position.** The telegraph pair
is now a *consequence inside a realization*, not a root. The reader operator `𝔗⁺` and the
anti-damped record operator `𝔗⁻` are exactly `T1_el_psi_node1/node2` and `T1_el_phi_node1`
(`Th_coqc`, axiom-free over ℚ, 3-ring scope), so this placement is backed, not asserted.

**1.3 It states its own limit correctly.** The proposal says plainly that
`S_DRL ⇏ {J_C, T, K, Π}` and calls the result a *philosophy-first unified master
architecture*, explicitly NOT a *fully unified single-action theory*. That matches
`URR_C_MASTER_0_4.yaml`'s own `open_problems.unified_action` and the peer-review note. A
version that knew less about where it stops would be a downgrade even if it covered more.

## 2. What is restatement rather than new

For the record, so nobody counts these twice: §II's `Λ_α ∘ Σ_α = I` is
`F3_lifted_recompose`; §VI's tape injectivity `E_T(r)=E_T(r′) ⟹ r=r′` with monotone growth
is `F6_append_cell_injective`; §VIII's return composition is `F7`; §IV's `ρᵀ J_C = 0` is
`F5_balanced_cut_conserves_declared_total`. All already machine-checked. Their appearance
here is correct placement, not new ground.

## 3. Corrections required before this can be promoted

### 3.1 BLOCKING — §V presents `M` as if it were part of the structure

Section V writes the reader equation with the `M(Φ_{n+1} − 2Φ_n + Φ_{n−1})/Δt²` term
present, with no marking. Two results established 2026-07-21 make that presentation
misleading:

- `InfoRetentionLagrangian_attempt.v`'s Euler–Lagrange theorems are stated
  `forall M D K K2 dt …` with side conditions **only** `~(h == 0)` and `~(dt == 0)`. There
  is no `M ≠ 0` anywhere. The action never constrained `M`.
- `InfoActionDoesNotForceM_attempt.v` (`Th_coqc`, 9× `Closed under the global context`)
  exhibits an explicit witness at `M = 0` on the same 3-ring making the action's own imported
  gradient vanish, and shows it is not reachable from any `M ≠ 0` system by the scale gauge.

So `M ≠ 0` is a **declared choice, not a consequence** — and it is a choice about what the
word *retained* means: `M = 0` is a world that forgets, `M > 0` is a world in which a
distinction can return on its own. `InfoRetentionForcesSecondOrder_attempt.v` derives `M > 0`
only after positing that retention means re-readable, and fences that posit itself.

**Required:** §V must mark `M` as a card entry, and §I's `Adm_δR` must record its first
concrete theorem: **first-order (`M = 0`) systems are members of `Adm_δR`.** That is exactly
the kind of statement the new set was introduced to hold, and leaving it out wastes the
proposal's own best idea.

### 3.2 BLOCKING — §III/§V present `K` as a parameter beside `M` and `D`

`forced_into_DW_minus_W` forces `L_R` into the `D_W − W` form from
`{sym3, rowsum0, offdiag_le0}` — all three homogeneous of degree 1, so `t·L` satisfies them
too for `t > 0`. The root therefore forces the **form** of `L_R`, never its **scale**, and
`K` is precisely that leftover scale. `InfoKLRSplitGauge_attempt.v` (`Th_coqc`, 18×
`Closed`) proves the consequences of the split freedom `(K, L_R) → (K/t, t·L_R)`:

| quantity | invariant under `(M,D,K)→s(M,D,K)` | invariant under `(K,L_R)→(K/t,t·L_R)` |
|---|---|---|
| `K` | no | no |
| `λ` | yes | no |
| `K·λ` | no | **yes, literally** |
| `τ_c = M/D` | yes | yes |
| `c² = K/M` | yes | **no** |
| `disc = D²−4MKλ` | sign only | **yes, literally** |

**Required:** the invariant object is `K·𝔾_T`, not `K`. Any numeric threshold written in
`M·K` is convention-dependent; the convention-free form is `D² < 4·M·(K·λ)`. And `c² = K/M`
must carry a note that it is not well defined until `L_R`'s normalization is fixed.

### 3.3 `Adm_δR`'s membership conditions are prose, not a test

§I lists four conditions in words. A set whose membership cannot be decided is a name, not a
definition, and this house does not promote names. Either give a decidable test, or tag the
four conditions `Dr` and say so.

### 3.4 No tier tags anywhere

Every line of a canonical document in this family carries `Th_coqc` / `finite_diagnostic` /
`Dr` / `Open`. The proposal has none. The continuum reduction at the end especially needs
one: passing to `∂_t²` injects I2 (infinite divisibility) by the house's own infinity
diagnosis, so the continuum telegraph is a **report**, correctly demoted in the proposal's
prose, but it must be tagged rather than merely described.

## 4. The corrected placement, in one line

    δ_R  ⟹  Adm_δR  ∋  {M = 0 systems, M > 0 systems}   ← the root does not choose
              ⊃  F_DRL  ⟹  (𝔗⁺[Φ], 𝔗⁻[Ψ])              ← Th_coqc, 3-ring scope
              →  J_C → T → K → Y → P                      ← not derived from S_DRL [Open]

The card carries exactly two entries at this level: **`M`**, because it fixes what *retained*
means, and **`K`**, because it fixes the unit of distinction. `L_R` and the sign of `D` are
not on the card — the root forces them.

## 5. Recommendation

Adopt the hierarchy and `Adm_δR`. Do not adopt §V as written until 3.1 and 3.2 are applied,
because as written it presents two card entries as if they were structure — which is the one
error this whole architecture exists to prevent.
