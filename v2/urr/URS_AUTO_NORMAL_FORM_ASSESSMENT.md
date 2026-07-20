# Automatic normal-form discovery — independent assessment and extraction

Assessed by the orchestrator, 2026-07-21, by re-running the supplied benchmark and adding one
robustness test the original did not have.

## 1. Verdict: this one is real, and it is the first of the three that is

Two earlier URS benchmarks (classical `111`-avoidance, quantum permutation-symmetric circuit)
both had the same defect: **the abstraction was supplied by the author** — "normal form = last
two bits", "normal form = Hamming weight" — and that supplied step is what did all the work.
Both recovered a textbook method (transfer matrix; Dicke basis) against a baseline nobody uses.

This benchmark closes that hole. The symmetry is **hidden by random relabelling and not
supplied**, and the solver recovers it. Reproduced independently:

| N | cells found | hidden partition recovered | exact gate | 2^N | quotient | amplitude error |
|---|---|---|---|---|---|---|
| 12 | 4×4×4 | yes | dev = 0.0 | 4,096 | 125 | 7.0e-16 |
| 15 | 5×5×5 | yes | dev = 0.0 | 32,768 | 216 | 7.2e-16 |
| 18 | 6×6×6 | yes | dev = 0.0 | 262,144 | 343 | 2.0e-15 |
| 21 | 7×7×7 | yes | dev = 0.0 | 2,097,152 | 512 | 8.0e-15 |

Both negative controls pass, and both could have failed:
- **defect qubit** — one qubit perturbed: the solver splits it out (1×4×5×5, four cells) rather
  than forcing it back into its old block.
- **generic random couplings** — the solver refuses compression entirely, returning ten
  singleton cells and a quotient of 1024 = 2^10.

The pipeline *discover → audit → quotient → evolve → verify* runs, with the exactness audit
gating compression rather than following it. That is the correct order and it is not cosmetic.

## 2. Correction: the reported timings are contaminated

The supplied JSON and CSV **disagree about the same run**: at N=18 the JSON reports
`discovery_ms = 32.58`, `one_shot = 3.62×`, while the CSV reports `0.47` and `99.86×`. Two
different runs are being presented as one dataset, and the speedup figure is drawn from the
contaminated one — which is why the graph shows a spurious dip at N=18.

Independent reproduction gives monotonic behaviour with no dip:

| N | discovery (ms) | one-shot speedup |
|---|---|---|
| 12 | 0.39 | 0.75× |
| 15 | 0.48 | 4.9× |
| 18 | 0.64 | 149× |
| 21 | 0.85 | 2,088× |

The corrected story is **better** than the reported one: discovery cost is essentially flat
while the full simulation grows exponentially, so one-shot speedup rises monotonically and
crosses 1× between N=12 and N=15. Use these numbers; discard the dip.

## 3. Kinship — must be declared before the word "new" is used

`refine_partition` computes a stable colouring by iterating
`(local parameter, current colour, sorted weighted-neighbour signature)`. That is
**1-dimensional Weisfeiler–Leman colour refinement** (Weisfeiler & Lehman 1968), the standard
algorithm for computing the coarsest **equitable partition** of a weighted graph. The
subsequent quotient is **exact lumpability** (Kemeny & Snell, for Markov chains) applied to a
quantum carrier, and the per-cell basis is the symmetric (Dicke) subspace, standard in
collective-spin physics.

None of this diminishes the result, but by this project's own rule kinship is declared before
novelty is claimed. What is genuinely ours is the **composition**: refinement as an
*admissibility* test, an exactness audit as a *gate on compression*, cells splitting the moment
a real distinction appears, and refusal to compress recorded as a first-class outcome rather
than a failure.

## 4. The finding that matters most: the method is brittle, and precisely so

The random-coupling control that "passes" is simultaneously the statement of the limitation:
it refuses compression because generic couplings have no *exact* block symmetry. Real systems
have *approximate* symmetry. So I tested the obvious question the benchmark did not ask —
what happens under small parameter noise? (N=15, same model, noise added to θ and to the
couplings.)

| noise | cells found | quotient dim | compression |
|---|---|---|---|
| 0 | 3 | 216 | 151.7× |
| 1e-14 | 3 | 216 | 151.7× |
| **1e-10** | **15** | **32,768** | **none** |
| 1e-8 | 15 | 32,768 | none |
| 1e-6 | 15 | 32,768 | none |
| 1e-3 | 15 | 32,768 | none |

**The cliff sits between 1e-14 and 1e-10** — at the refinement's own rounding tolerance
(`decimals=12`), far below any physically meaningful precision. Perturb the couplings by one
part in 10^10 and the entire speedup vanishes.

So the honest scope is: **the method works on exactly-symmetric models, and exact symmetry is
measure-zero in parameter space.** This is not a fatal objection — it is a precisely located
one, which is more useful.

## 5. What this earns, and what it does not

Earned: the framework can **discover** a structural normal form from the rules alone, audit its
exactness before using it, refuse when there is nothing to find, and split when a distinction
appears. That is a working pipeline, not a philosophical claim, and it is the first URS result
of which that is true.

Not earned: any claim about generic systems, about approximate symmetry, or about complexity
classes. The 4096× dimension reduction at N=21 is real for exactly-block-symmetric models and
exactly zero for anything perturbed off that set.

## 6. The next experiment, which is now well-posed

Replace exact refinement with **tolerance-aware refinement**: merge cells whose parameters
agree within ε, and derive a bound on the observable error introduced by that merge. The
question becomes quantitative — *how much accuracy is bought per unit of compression* — and it
is falsifiable: if no ε gives a useful trade (compression collapses before the error budget is
met), approximate URS is dead and we will know it. That experiment is worth more than another
exactly-symmetric demonstration.
