# URS–RDT v0.8-FH — attribution ledger and assessment

Founder's instruction, 2026-07-21: *"ถ้าใช้สมการเก่าให้เครดิตเค้าด้วย"*. This file is that
instruction carried out, piece by piece, before any part of v0.8-FH is treated as ours.

## 1. The architectural judgement is right

Refusing a generic "approximate quotient" because it would break RD4 and the exact-quotient
gate, and instead introducing a **separate, explicitly-labelled** finite-horizon layer, is the
correct move. It keeps `=_R ⊊ ≡_exact ⊊ ≈_{α,δ,H}` as three distinct relations rather than
quietly widening the exact one. The measured evidence supports the need: the exact gate finds
nothing to compress in chaotic N-body (bridge ledger B28), and forcing a coarse quotient without
a gate produces 64% force error (B29).

## 2. Attribution ledger — what each piece already is

| v0.8-FH piece | Prior art it is | Credit |
|---|---|---|
| `≈_{α,δ,H}`: histories equivalent iff readouts stay within `δ` over horizon `H` | **approximate bisimulation / bisimulation metrics** — behavioural equivalence with a precision parameter, with an established theory of error propagation and composition | Desharnais, Gupta, Jagadeesan & Panangaden (bisimulation metrics, 2004); Girard & Pappas (approximate bisimulation for control systems, 2007–2011) |
| `𝔏 = sup_h ‖DΠ·DO·DF^{[h]}·𝔡‖` — weight the local defect by the readout's sensitivity to it, refine where the product is large | **dual-weighted-residual (DWR) goal-oriented a posteriori error estimation**; the local residual weighted by the adjoint solution is *the* refinement indicator | Becker & Rannacher (DWR, 1996–2001); adjoint/tangent-linear sensitivity, standard in optimal control and data assimilation |
| §31 thresholds Share / Monitor / Refine / Rollback against `β₁δ, β₂δ, δ` | **adaptive mesh refinement driven by an error indicator with tolerance bands** | standard AFEM practice, same lineage as above |
| §29 expiring licence `τ_share`, refresh-or-refine | **certified reduced-basis methods** and **online-adaptive model order reduction**: a rigorous a posteriori bound that triggers basis enrichment when exceeded | Rozza, Huynh & Patera (certified RB, 2008); Peherstorfer & Willcox (online adaptive ROM, 2015) |
| §32 exact checkpoints + rollback | **checkpointing for adjoint/reverse computation**; periodic full-order correction in ROM | Griewank & Walther (revolve, 2000) |
| §28 `ε_local^max ≈ δ·e^{-λH}` | standard **Lyapunov-weighted error budgeting**; the shadowing literature is the rigorous version | Anosov; Bowen (shadowing); standard in molecular dynamics and NWP as error-doubling-time budgeting |

Stated plainly: **v0.8-FH is, structurally, certified reduced-order modelling with
goal-oriented adaptivity**, transplanted onto the retention ontology. None of that diminishes
it — but by this project's own law the kinship is declared before the word *new* is used, and
the previous three URS documents did not have a kinship section at all.

## 3. What survives as ours after crediting

**The residual tape (§30) is the genuinely distinctive piece.** Every method above computes an
error indicator and then *discards* what it dropped — the estimate bounds the damage but the
dropped content is gone. Here the discarded residual `r_{C,n}` is **retained on the tape with
its certificate**, so the compression is auditable and reversible: you can reopen a cell, replay,
and reconstruct. That is not a performance feature, it follows directly from RD4, and it is the
one place where the ontology forces a design that standard ROM does not have.

Also ours, more weakly: making the *licence* a first-class object with an expiry rather than a
tolerance checked incidentally, and requiring the readout contract `(O_α, Π_α, δ_α, H, η_α)` to
be declared up front rather than chosen post hoc.

## 4. The critique that matters — the certificate rests on an object known to fail here

`𝔏` is built from `DΠ·DO·DF^{[h]}` — a **linearisation**, propagated through the flow. In a
chaotic system the tangent/adjoint operator grows like `e^{λh}`, so:

- the sensitivity that the whole gate depends on **diverges exponentially in `H`**, and
- the first-order expansion justifying it is valid only for `h` short compared with the Lyapunov
  time — i.e. it degrades precisely in the regime §28 was written for.

This is a well-known failure mode, not a subtlety: adjoint sensitivity analysis of chaotic
systems produces gradients that blow up and become meaningless past a few Lyapunov times. The
established repair is **Least Squares Shadowing** (Q. Wang, 2013–2014), which computes a
shadowing trajectory instead of a diverging adjoint.

So §27–§28 as written are self-limiting: `ε_local^max ≈ δ·e^{-λH}` correctly says the budget
shrinks exponentially, but `𝔏` — the thing used to *decide* whether to share — is computed with
the same diverging operator. **The certificate and the thing it certifies degrade together.**
This must be stated in the section, and LSS named as the candidate repair, or the first
implementation will discover it the expensive way.

## 5. Tier and next step

Status is correctly self-labelled `[Open] architecture proposal`. It should stay there until:

1. `𝔏`'s own validity horizon is bounded and stated (the §4 problem);
2. an implementation exists and is measured against **Barnes–Hut and FMM**, not against the
   direct `O(N²)` solver — all four URS benchmarks so far compared against a baseline
   practitioners do not use, and this one must not repeat that;
3. the certificate is shown not to be violated beyond `η_α` on a chaotic run with a declared
   horizon, i.e. the promised failure rate is measured rather than assumed.

The falsifiable form is already available and should be pre-registered before the run:
*there exists a `(δ, H)` pair for which `D_FH < D_exact` by a useful factor while the measured
readout error stays under `δ` for the declared horizon.* If no such pair exists, the
finite-horizon layer is dead for chaotic N-body and we will know it cheaply.
