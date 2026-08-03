# Paradoxes — a worked stress-test (Readout Universe v2.0-dev)

> **What this file is.** A worked example, not core canon: five classic
> philosophical paradoxes (Liar, Sorites, Ship of Theseus, Newcomb, Zeno)
> run directly through the machinery in [`philosophy.md`](philosophy.md) and
> [`logic.md`](logic.md), plus one exploratory attempt to formally define
> "origination" (the undefined term S3 uses to distinguish true agency from
> a self-sensing loop) and apply it to Newcomb's Paradox. Everything new in
> this file was originally freshly-produced reasoning, most of it tiered
> `Dr` or `[Open]` because it had not yet been reviewed. **That has since
> changed for the six items in the "Upgrade attempts log (2026-08-03)"
> section below**: an independent maker-checker pass has now run against
> all six, re-verifying each one directly (recompiling Coq files from
> clean, re-running numeric scripts, re-reading and re-grepping cited
> sources) rather than rubber-stamping the maker's self-report. That
> pass's scope was narrow — Coq compilation/axiom-freedom, numeric
> reproduction, and citation accuracy — it is not yet a pass through
> this corpus's full adversarial-review pipeline, and it left most tier
> verdicts unchanged (see the log for exactly what moved and what
> didn't). Where a paradox test lands on `Th_coqc` outside that log,
> that machine-checked result already existed in the cited source file;
> this document did not add new proof, only pointed the existing
> machinery at a new question.
>
> Tier legend (same as `philosophy.md`/`logic.md`, never collapse):
> `Th_coqc` (machine-checked, axiom-free) ≠ `finite_diagnostic` (executed
> numeric run — evidence, not proof) ≠ `Dr` (declared-bridge / human
> narrative reading) ≠ `Open` (not established, but never bare — always
> carries a stance and a falsifier) ≠ `fit_calibrated` (fit to data, not
> derived) ≠ `definition` (declared object/gate, stipulated, not derived or
> measured).

---

## Scoreboard

| Paradox | Tier reached | What happened |
|---|---|---|
| Sorites | `Th_coqc` (scope: monotone only) | **Resolved**, in the narrow sense the source Coq floor actually covers |
| Zeno | `Th_coqc` (floor) + `DERIVED` (finite speed) | **Dissolved** — the ontology has no dense continuum to exploit |
| Ship of Theseus | `Dr` (emergent fit; RD4 leg now has a direct `Th_coqc` citation, Q3/eigenmode still uncited) | Reframed with real machinery (RD4 + Q3), not proved |
| Liar | `Dr` — the corpus states this itself | Located, not closed; the framework says so plainly |
| Newcomb (base case) | `[Open]` | No dedicated machinery; assembled from unrelated gates |
| Newcomb (with "origination" defined) | `Dr`, partly `[Open]` | New traction, but a fresh unproved construction, not a fix |

The pattern is not random: the framework is strongest exactly where a
paradox trades on a continuum/infinity assumption (Sorites, Zeno) — that is
what its discrete-math floor was built to refuse — and weakest on
self-reference (Liar) and decision theory under a presumed-omniscient
predictor (Newcomb), which `philosophy.md` §6 already discloses it does not
claim to have solved.

---

## 1. Sorites Paradox (heap / bald man)

*Tier: `Th_coqc`, scope explicitly narrow (monotone case only) — see
`philosophy.md` §6's own caveat: "The Coq floor is narrow... do not extend
its scope by inference."*

The vague-boundary question ("how many grains make a heap?") translates,
via the Lens Law dictionary in `philosophy.md` §3, to: where does the
readout policy `Π` sit relative to the `τ_c*` knife-edge? This is not a
metaphor — it is the literal three-file-binding case `philosophy.md` §5.5
names as the *only* node in the whole corpus meeting its own strict
binding criterion (chapter ↔ Coq file ↔ executable diagnostic, all three at
once):

- `logic.md` §8, `C4`: `finite_diagnostic` — `LTP2_3_4_battery.py` executed,
  3/3 PASS, "smooth world, exactly one readout jump, jump tracks `Π`."
- `logic.md` §8, `C7`: `Th_coqc` — `coqc code/UPL_Sorites.v` compiles,
  `Print Assumptions` reports Closed, axiom-free, verified independently
  three times.

**Verdict:** genuinely resolved, but only inside the declared monotone
scope — a smooth, one-directional world. The general Sorites (non-monotone,
adversarial orderings of the heap) is not covered and the corpus is
explicit that extending the claim beyond monotone would itself be the kind
of overclaim its own discipline forbids.

[domain card: logic.md §8 (C4, C7); philosophy.md §5.5]

**Upgrade attempt (2026-08-03):** an independent maker/checker round found a
genuine one-reversal extension (`UPL_Sorites_OneReversal.v`,
`flip_bound_three`) — hypotheses relaxed to `g_mono_left`/`g_mono_right`
with the single straddling pair left unconstrained, strictly weaker than
the committed file's global `g_mono`. Independently recompiled twice from
clean (`coqc -q`, `Print Assumptions flip_bound_three` →
`Closed under the global context`, no `Admitted`/`admit`/`Axiom`):
`Th_coqc`, axiom-free — same tier this row already carries. What is new is
narrower: this specific extension is now committed at
[`code/UPL_Sorites_OneReversal.v`](code/UPL_Sorites_OneReversal.v)
(re-verified compiling in-place at that path), but is **not yet
cross-referenced from `philosophy.md`/`logic.md` and has not been run
through this corpus's own full adversarial-review process** — the
Scoreboard tier is unchanged because it already read `Th_coqc`; the
"monotone only" scope note stands until this extension is formally folded
into the main Sorites result rather than sitting beside it.

---

## 2. Zeno's Paradox (Achilles and the tortoise / the dichotomy)

*Tier: `Th_coqc` for the discrete floor itself; `DERIVED` (not full
`Th_coqc`) for the finite propagation speed that answers the motion
question*

Zeno's argument needs a *dense* continuum — between any two points there is
always a third — to generate infinite subdivision. `philosophy.md` §5.2a
states, of exactly this move: *"Density... is provably absent at the
root; it can only ever be a later readout, never a primitive fact about
number."* The injected-infinity taxonomy tags Zeno's own move directly:
`I2`, infinite divisibility `h→0` (§2.5/§5.2a) — one of four ways a
continuum operator silently smuggles an infinity this floor refuses to
grant for free.

Two further pieces of machinery apply directly, not by analogy:

- **Finite-difference, not limit** (`philosophy.md` §5.2a): `Δf(n) =
  f(n+1) ⊖ f(n)` is rational algebra on a discrete stepper, with no
  limiting process run. Achilles's motion is a finite number of discrete
  steps by construction, not a continuum traversal of infinitely many
  subintervals.
- **Cattaneo finite-speed brick, `c² = K/M`** (`logic.md` §9.10, `DERIVED`
  — graph-native, not `Th_coqc`): a genuinely finite characteristic
  propagation speed derived from `L_R`/inertia structure, not posited. This
  is the closest thing the corpus has to a direct answer to "how does
  finite motion cross an apparently-infinite subdivision" — because in this
  ontology there is no infinite subdivision to cross.
- **Honest limit on the above:** `philosophy.md` §5.6a's Stream of
  Necessity lists "finite-causal-cone" as one of six readings tried and
  *failed* as a way to force-derive `M` directly from retention alone — the
  finite speed is real but not free; it needs an additional posit
  (re-readability), not bare retention.

**Verdict:** dissolved rather than resolved — the paradox does not arise in
this ontology, because the dense-continuum premise Zeno needs is the exact
thing `I2` was built to name and refuse. This is the second-strongest
result in this file, after Sorites, and for the same underlying reason:
both paradoxes are continuum/infinity exploits, and continuum/infinity
refusal is this corpus's founding move.

[domain card: philosophy.md §2.5, §5.2a, §5.6a; logic.md §9.10]

**Upgrade attempt (2026-08-03): no progress** — the two named untried
readings from `philosophy.md` §5.6a's Stream of Necessity ("recoverable
via a different channel while fading," "bounded away from zero infinitely
often without exact return") remain unformalized; no new `.v` file targets
either. The checker also found the maker's grep-hit citation list for
"own-clock"/"impermanence" mentions undercounted real matches elsewhere in
the corpus — a genuine overclaim in the evidence, though it does not change
the underlying conclusion (still zero Coq formalizations of either
reading). Tier stays `Th_coqc` (floor) + `DERIVED`, unchanged.

---

## 3. Ship of Theseus

*Tier: `Dr` — a real, working fit assembled from existing machinery, but
never built for this purpose and never directly cited anywhere in the
corpus*

No file in this corpus mentions Ship of Theseus. Three pieces of existing
machinery apply cleanly without forcing:

- **RD4, the retention axiom** (`philosophy.md` §5.1): *"distinct histories
  never merge."* Two ships built from materially-identical parts but
  reached by different histories (continuous plank-by-plank repair vs.
  reassembly from stored original parts) are, by RD4, different retained
  states regardless of material identity at the end.
- **Q3, "identity by role, not by number"** (`philosophy.md` §1): the
  equal-number fallacy forbids substituting two things that compute to the
  same *quantity* but hold different *roles* in the readout graph. Two
  ships with identical atom-counts still occupy different roles (one is
  "the ship that never left dock," the other is "the ship reassembled in a
  warehouse") — Q3 says this is enough to keep them distinct, independent
  of material sameness.
- **"A thing is a persisting eigenmode"** (`philosophy.md` §5.2): identity
  is not the raw material (the planks) but the pattern that survives on
  `L_R`'s spectrum — reframing "which ship is the real one" as "which
  eigenmode actually persisted," a question RD4 + Q3 already answer.

**Verdict:** a genuine, load-bearing reframe — the paradox dissolves into
"you were asking whether two different retained-histories are the same
quantity, and the framework already forbids that move" — but this is
`Dr`-tier synthesis assembled for this exercise, not a result the corpus
itself derived or reviewed. No falsifier has been proposed for it yet.

[domain card: philosophy.md §1 (Q3), §5.1 (RD4), §5.2 (eigenmode)]

**Upgrade attempt (2026-08-03):** an independent maker/checker round
formalized the retention-sense half of this reframe.
`formal/Scratch_ShipOfTheseus_RD4.v` derives
`distinct_histories_never_merge : forall x y : D, x <> y -> succ x <> succ
y` as a one-line contrapositive of `RD.v`'s pre-existing `RD4_succ_inj`;
independently recompiled fresh (deleted `.vo`/`.vok`/`.vos`/`.glob`, reran),
`Print Assumptions` → `Closed under the global context`: `Th_coqc`,
axiom-free. This resolves — with a real, verified citation trail
(`formal/RD.v:42`, cross-referenced verbatim in `logic.md:51` and
`v2/INFORMATION_DNA.md:20`) — a concern that "RD4, the retention axiom"
cited above might point at an unrelated or undefined axiom; it does not.
**This does not lift the row's overall tier**: Q3 and the eigenmode framing
remain untouched, prose-only, and the combined argument stays `Dr` exactly
as before. What changed is narrower and factual: the Scoreboard's former
"no direct citation" note is no longer accurate for the RD4 leg alone (see
Scoreboard, updated above).

---

## 4. Liar Paradox ("this sentence is false")

*Tier: `Dr` — and the corpus's own translation dictionary already says so*

`philosophy.md` §3's Lens-Law dictionary carries the row **"Sorites/Liar/
Ω_∞ → L-10"** directly: Liar goes through the Grammar gate (Ω_∞), which
checks for a self-injected infinity in the question itself before any
answer is attempted. "This sentence is false" supplies no evidence `ε`, no
readout policy `Π`, no discrete step at which to evaluate a residual `r =
Aε − δ` — it is a loop with no `δ_R` anchoring it to anything retained
outside itself.

The corpus states its own verdict plainly (`philosophy.md` §6): the Liar is
**"relocated to a residual loop without a world anchor, not closed."** That
is not a resolution — it is a diagnosis of exactly why no resolution is
being offered: there is nothing here for the obstruction machinery `O(Γ,φ)`
to compare against, because there is no retained state on either side of
the comparison.

**Verdict:** a useful reframe (it tells you *where* the loop is, and why it
has no anchor) but explicitly not a closure, and the corpus does not
pretend otherwise.

[domain card: philosophy.md §3 (L-10), §6]

**Upgrade attempt (2026-08-03):** an independent maker/checker round
produced a new, genuinely axiom-free lemma in the corpus's own
Evidence/Policy vocabulary — `no_policy_can_anchor_its_own_negation`
(`research_universal_solver/formal/InfoLiarNoAnchoredResolution_attempt.v`),
formalizing that no policy can be anchored to its own negation.
Independently recompiled: both `Print Assumptions` calls report
`Closed under the global context` — `Th_coqc`. This is a genuine new
building block toward the still-unchecked `LTP5 liar loop` item in
`v2/ROADMAP_V2.md`, but it is a negative/impossibility result only —
**no actual self-reference/quining term for the Liar sentence itself was
built or found**, so this row's verdict stays `Dr` exactly as the corpus
states it above. The file is now committed at
`research_universal_solver/formal/InfoLiarNoAnchoredResolution_attempt.v`
(re-verified compiling in-place); not yet cross-referenced from
`v2/ROADMAP_V2.md`'s own LTP5 item.

---

## 5. Newcomb's Paradox — base case

*Tier: `[Open]` — no dedicated machinery exists; what follows is assembled
from gates built for other purposes*

Nothing in this corpus addresses Newcomb's Paradox directly. Three existing
gates, none built for this, can be pointed at it:

- **S3** (`logic.md` §1, `Th_coqc`): distinguishes a "self-sensing loop"
  from "true agency," which "adds origination" — but **origination is never
  defined anywhere in either file.** It is a named but empty slot.
- **G5, the identifiability gate** (`philosophy.md` §4): a null-space
  question's honest answer is "structurally unanswerable from these
  records," not a guess. Applied to "the predictor is always right," this
  flags the premise itself as a candidate injected infinity (I1/I4-style
  idealization) rather than a fact to accept.
- **The Fail-Able Gate Law** (`philosophy.md` §2.1): evidence only counts
  if it has both a passing and a failing control. A predictor track record
  with no recorded failures is Type-U by definition — a convention dressed
  as evidence, not proof that perfect prediction is possible.

**Verdict:** honestly `[Open]`. The above is a plausible argument built
from parts, not a framework result — and the term that looks like the
actual key ("origination") has no formal content anywhere in the corpus.

[domain card: logic.md §1 (S3); philosophy.md §4 (G5), §2.1 (Fail-Able Gate Law)]

**Upgrade attempt (2026-08-03):** an independent maker/checker round
formalized a **Predictor-Premise-Rejection Law** (`Dr`) combining G2 (Ω_∞
dual guard / unbounded-∀ injected infinity), G5 (identifiability /
null-space), and the Fail-Able Gate Law into one mechanically-applicable
three-conjunct rule for rejecting an "always-right predictor" premise as
`Type-U` (stipulated convention) rather than `Type-P` (evidence-bearing).
Independently re-verified against the source text and the existing
`Th_coqc` bricks it leans on
(`InfoAgencySelfReadout_attempt.v`). This is `Dr` — a stated combination of
existing gates, not machine-checked, not an executed diagnostic — and it
does **not** upgrade the underlying Newcomb verdict past `[Open]`: the
checker confirmed the maker's own honest admission that conjunct (ii)
(identifiability) is currently undecidable from this corpus's own stated
limits (the §6.3(c) regime-undecidability gap below), so only conjuncts
(i)/(iii) actually resolve — and those turn out to be the same fact
(the unbounded "always") counted twice, not two independent lines of
evidence. `[Open]` remains the correct, honest ceiling for this row.

---

## 6. Newcomb's Paradox, retried — a candidate definition of "origination"

*Tier: `Dr` for the construction; `[Open]` for its consequences; explicitly
NOT `Th_coqc` anywhere in this section — nothing here has a Coq file or an
executed diagnostic behind it*

### 6.1 What already exists, one repo over

`research_universal_solver/formal/InfoAgencySelfReadout_attempt.v` proves
(`Th_coqc`, axiom-free) that `agency(n,edges,x,i) := row_n(L)x_i` — a purely
deterministic readout of an existing state. That file states its own limit
directly: *"agency is not an uncaused mover... Held OFF this tier: any
claim that this is human free will (Dr)."* It is **not** what S3 means by
origination; it is the self-sensing-loop half of S3's own distinction.

A draft formula for the other half already exists, undischarged, in
`research_universal_solver/docs/root/AGENCY_VS_AGENCY_LIKE.md`:

> `a* = argmin_a O(s,a)` subject to `Repair(s') ≥ R_min` — "the argmin/
> Repair layer and the felt-quality hard problem are **relocated, not
> asserted here [Open]**."

So a candidate shape for origination already existed, deliberately left
unproved, one repo away from where S3 uses the word. This document did not
invent the starting point; it found where the corpus itself had already
parked it.

### 6.2 A candidate sharpening (new in this document, `Dr`)

> **Origination(a\*, s)** holds iff `a* ∈ argmin_a O(s,a)` under
> `Repair(s') ≥ R_min`, **and the argmin set at `s` has more than one
> element** — a genuine tie in obstruction-minimization under the same
> constraint.

Reasoning: if the argmin is unique, `a*` is a pure function of `s` — this
*is* `agency(s)`, already `Th_coqc`, nothing new. If the argmin genuinely
ties, `s` alone does not contain enough information to determine which
action gets chosen — the fact of which one *was* chosen is a new `δ_R`
created at the decision, not one read out of a prior retained state.

This is structurally reminiscent of (not identical to, and not proved
equivalent to) `InfoTrueRecordUnreadable_attempt.v`'s non-injective-readout
theorem — a decoder trying to recover "which action will be chosen" from
`s` alone, at a tie point, is attempting to invert a relation that is by
construction one-to-many there.

**Declared falsifier:** if `O(s,·)` under the stated constraint can be
shown strictly convex almost everywhere (ties only at measure-zero edge
cases), this construction is empty — origination reduces to ordinary
deterministic argmin, always predictable in principle, and the whole
section collapses to nothing.

### 6.3 Applied to Newcomb

- **(a) Is a perfect predictor of a truly originating agent coherent?** No,
  under this construction — claiming to compute `a*` from `s` alone at a
  genuine tie point claims a decoder proved not to exist there. This is
  the same shape of move `G2`'s injected-infinity guard already flags for
  `I1`/`I4` — not a new gate, an application of an existing one.
- **(b) What can a predictor do to a non-originating agent (no tie,
  self-sensing loop only)?** Everything — `agency = row(L)x` is an ordinary
  readout; a predictor with access to the same retained state predicts it
  directly, no paradox, because "prediction" here is just another readout.
- **(c) Is one-box vs. two-box decidable once the regime is known?**
  Partially. Self-sensing regime → one-boxing is sound (the predictor is
  reading an already-determined state). Origination regime → the premise
  "predictor is highly accurate" contradicts (a) above, so the puzzle's own
  setup is not self-consistent in this regime. **But** the framework has no
  way to determine *which* regime an agent is in without first running the
  optimization to completion — an unresolved epistemic gap, honestly a new
  `[Open]` item, not a byproduct that disappears.

### 6.4 Self-critique, applied the way this corpus's own review culture demands

- **Partial `DEFINITIONAL-RELABEL` risk** (the auto-fail class
  `philosophy.md` §3 itself names): the tie-breaking argument *borrows the
  shape* of the non-injective-readout theorem without proving the bridge —
  it has never been shown that the argmin-to-action map at a tie is
  formally the same kind of object `InfoTrueRecordUnreadable` is about. A
  hostile reviewer in this corpus's own style would flag this immediately:
  borrowed rhetoric, not a borrowed proof.
- **A cheaper move already exists and does most of the same work**: `G5`
  alone — "perfect predictor" as a candidate injected infinity — answers
  Newcomb's central move without any new machinery. What this section adds
  is *texture* (a structural account of exactly where certainty breaks,
  instead of a flat refusal), which has value only if the tie-breaking
  bridge is eventually proved; until then it is decoration on top of a
  gate that already worked.
- **Scope check against `philosophy.md` §6**: this construction must not be
  read as a claim about human free will, consciousness, or that Gödel/Liar/
  self-reference is solved — none of that is asserted or implied here, and
  `AGENCY_VS_AGENCY_LIKE.md`'s own hedge ("felt-quality hard problem...
  relocated, not asserted") is carried forward unchanged.

**Verdict:** real new traction over the base case (§5) — a precise place to
say the paradox breaks, instead of no machinery at all — but this is a
fresh, unreviewed `Dr`-tier hypothesis with a declared falsifier, not a
result. It should not be cited as more than that until a formal bridge
(Coq or an executed diagnostic) backs the tie-breaking claim in §6.2.

[domain card: research_universal_solver/formal/InfoAgencySelfReadout_attempt.v;
research_universal_solver/docs/root/AGENCY_VS_AGENCY_LIKE.md;
philosophy.md §4 (G5), §5.1 (non-injective readout), §6]

**Upgrade attempt (2026-08-03):** an independent maker/checker round built
an honest toy model of `O(s,a)` from this repo's own `ap6_drl_general.py`
obstruction machinery and computationally tested the §6.2 falsifier.
Result (`finite_diagnostic`: 0/7 genuine ties across both a convex regime
and a non-convex double-well regime, on generically-forced states): the
falsifier's predicted outcome holds — the origination construction is
empty for every generically-forced state tested — though by a different
mechanism than the falsifier itself named (symmetry-breaking by any
nonzero forcing, not strict convexity a.e.). An exact tie
(`|O1-O2|=2.22e-16`) does appear, but only in the idealized symmetric
special case `s=0, J=0` exactly, and is already destroyed by forcing as
small as `eps=1e-8`. This is one executed numeric run on a chosen toy `O`,
not a proof about §6.2's actual undefined `O`/`Repair` — it does not change
this row's tier, which stays `Dr` for the construction and `[Open]` for its
consequences, exactly as before.

---

## See also

- [`philosophy.md`](philosophy.md) and [`logic.md`](logic.md) — the core
  distillation this file stress-tests; nothing here has been folded back
  into either.
- `research_universal_solver/formal/InfoAgencySelfReadout_attempt.v` and
  `research_universal_solver/docs/root/AGENCY_VS_AGENCY_LIKE.md` — the
  un-discharged origination draft §6 builds on.
- This file's own status: every `Dr`/`[Open]` item above is a candidate for
  future adversarial review, not a settled addition to the corpus's
  Th_coqc floor. Treat accordingly.

---

## Upgrade attempts log (2026-08-03)

A maker-checker upgrade round ran independently against all six items above.
Every checker verdict below was produced by a re-verification pass separate
from the maker (recompiling Coq files from clean, re-running numeric scripts,
re-reading and re-grepping cited sources directly) — not a rubber stamp of
the maker's self-report. Recorded here in full, including the four items
where nothing moved, per this corpus's own culture of keeping negative
results on the record rather than silent.

1. **Sorites (non-monotone extension).** Outcome: **upgraded** (new result,
   now committed at `code/UPL_Sorites_OneReversal.v`). Checker: **CONFIRMED**,
   `Th_coqc` — independently recompiled `UPL_Sorites_OneReversal.v` twice
   from clean, axiom-free, confirmed the relaxed hypotheses are strictly
   weaker than the committed file's global monotonicity. Correctly scoped:
   sits beside the existing monotone-only result, does not replace it, and
   is not yet cross-referenced from `philosophy.md`/`logic.md`.

2. **Zeno (untried 7th forcing reading for `M`).** Outcome: **no_progress**.
   Checker: **PARTIALLY_CONFIRMED**, tier unchanged — the two named
   unformalized readings are still unformalized (verified by direct file
   read and corpus-wide grep); flagged one genuine flaw in the maker's own
   evidence (an undercount of real citation hits for "own-clock"/
   "impermanence" elsewhere in the corpus) that does not change the
   underlying conclusion.

3. **Ship of Theseus (Coq formalization of RD4 half).** Outcome:
   **upgraded** (narrow, real). Checker: **CONFIRMED**, `Th_coqc` — recompiled
   `Scratch_ShipOfTheseus_RD4.v` fresh, axiom-free; verified the RD4 citation
   trail (`RD.v:42`, `logic.md:51`, `v2/INFORMATION_DNA.md:20`) resolves a
   previously live concern about an unrelated/undefined axiom. Correctly
   scoped: does not touch Q3 or the eigenmode framing, so the row's overall
   `Dr` tier stands.

4. **Newcomb base case (G2+G5+Fail-Able Gate Law combination).** Outcome:
   **upgraded** (new named law, `Dr`). Checker: **CONFIRMED**, `Dr` — verified
   every cited source quote and the two `Th_coqc` bricks it leans on; caught
   one minor wording inconsistency (a biconditional stated in prose but the
   formal rule is one-directional) that does not affect the tier claim. The
   underlying Newcomb verdict stays `[Open]`, exactly as the maker claimed —
   the checker independently confirmed the identifiability conjunct is
   genuinely undecidable from this corpus's own stated limits.

5. **Liar Paradox (impossibility lemma).** Outcome: **upgraded** (new
   negative result). Checker: **CONFIRMED**, `Th_coqc` — recompiled
   `InfoLiarNoAnchoredResolution_attempt.v`, both theorems axiom-free;
   verified by direct proof-term reading that both lemmas are correct and
   match the claimed Evidence/Policy vocabulary. Correctly scoped: no
   self-reference/quining term for the Liar sentence was built, so the row's
   `Dr` verdict stands unchanged.

6. **Newcomb origination falsifier (§6.2 computational test).** Outcome:
   **unchanged** (falsifier holds; refuted the maker's own initial
   hypothesis that ties might be common). Checker: **CONFIRMED**,
   `finite_diagnostic` — independently reproduced the maker's numeric
   results near bit-for-bit (0/7 ties in both regimes tested; the one exact
   tie at the idealized `s=0, J=0` point; the same forcing-sweep magnitudes)
   and independently re-ran an equivalent forcing-sweep script from scratch.
   One evidence-only run on a chosen toy `O`; does not touch §6.2's actual
   undefined `O`/`Repair`, so this row's `Dr`/`[Open]` verdict stands
   unchanged.
