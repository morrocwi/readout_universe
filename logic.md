# Logic — Equation & Operator Ledger (Readout Universe v2.0-dev)

> Pure logic/equation reference sheet. No narrative — see [`philosophy.md`](philosophy.md)
> for the why/what-is/how-do-we-know. Every entry below carries its **source tier
> exactly as given in the source file** (never upgraded here) and a one-line
> pointer to that file. Tier legend:
>
> `Ax` axiom · `Th` theorem — includes machine-checked results that declare
> one or more non-constructive classical axioms (`Print Assumptions` shows
> them, not `Closed`); such results are never labeled `Th_coqc` · `Th_coqc`
> machine-checked, axiom-free
> (`Print Assumptions` ⇒ Closed) · `finite_diagnostic` measured/executed,
> not proof · `Dr` declared bridge / human narrative · `Open` not
> established (carries a stance + falsifier at source) · `fit_calibrated`
> fit to data, not derived · `definition` declared object/gate ·
> `exact_algebra` identity proved within an explicitly declared model ·
> `declared_finite_architecture` a finite step declared exact within one
> named stepper/model (see §9.2's addendum) · `exact_bridge` an
> algebraically exact step connecting two declared-finite objects (ditto) ·
> `exact_algebra_in_declared_ideal_model` identity proved exactly, but only
> inside one explicitly declared idealized model (§9.4). A handful of
> further source-verbatim verdict tags (`POSITED`, `DERIVED`,
> `DEFINITIONAL-RELABEL`, `BORROWED-SCALE`, ...) appear at their point of
> use (§9.9, §9.10) — these are a separate, narrower vocabulary carried
> unchanged from `BORROWED_VS_DERIVED_LEDGER.md`'s own verdict classes, not
> additions to this file's own tier scale above, and are never used to
> upgrade or replace this legend's tags.

---

## The mother equation — Θ, translation, and the record law

Before any domain-specific machinery below: the one relation every tier in
this ledger answers to. `θ(E[n])` names the true state a record is *about*;
`M_A[n]` names what an agency `A` actually retains at tick `n`. The record
is never the truth itself — it is a *translation* of it, carrying
irreducible noise from selection, mapping, and the reading agency:

| ID | Statement | Tier | Source |
|---|---|---|---|
| EQ-027 | `M_A[n] = K_A·θ(E[n]) + η_sel + η_map + η_self` — the record is a translation of the true state `θ(E[n])`, never the state itself (`η_sel` selection noise, `η_map` mapping/translation noise, `η_self` self-referential noise) | `Th_coqc` | `EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md` EQ-027 |
| EQ-028 | `M_A[n] ≠ θ(E) ∀n`; `ε_tot = η_sel+η_map+η_self > 0 ∀n` — the translation gap between record and truth never closes to zero | `Th_coqc` | same, EQ-028 |
| `no_decoder_recovers_state` | whenever a readout operator maps two distinct true states to the same recorded value, both states still exist, but no decoder can recover both from the record alone | `Th_coqc`, axiom-free (`Print Assumptions` ⇒ Closed) | `readout_genesis/formal/InfoTrueRecordUnreadable_attempt.v` (same theorem cited again at EQ-032–034 in §6 below; one theorem, cited twice, never re-derived) |

This is `philosophy.md` §1's "readout-not-truth" written as an equation, not
prose — every other entry in this ledger inherits the same discipline: a
tier tags how well-supported a *translation* is, never whether it reached
`θ` itself. **Scope, per philosophy.md §1's own caveat, carried forward
here unchanged:** the Coq theorem above is a supporting, general fact about
non-injective maps — not new mathematical content on its own — that grounds
the *shape* of readout-not-truth, not independent evidence that the stance
is true of the physical world; EQ-027/EQ-028 (the translation-noise
equations) are the source's own `Th_coqc` claim and carry no such
disclaimer. [domain card: `philosophy.md` §1; `v2/TRANSLATION_PROTOCOL.md`
row L-07 ("truth" = tracking, never correspondence to the infinite)]

**Named directly, not silently reconciled — the same-shaped formula
carries three different tiers elsewhere in this corpus, and that is not an
oversight to quietly fix by picking one.** This exact equation, under the
name **N2**, already sits later in this same file (§ "Epistemic Nuclear
Core", `M_A = K_A·θ+η; ε_tot>0`) tiered `definition`, not `Th_coqc` — and
`philosophy.md` §5.7 makes this a *load-bearing architectural claim*, not
an incidental label: of the five nuclear-core equations N1–N5, **N3 is
named there as "the one equation in the whole nuclear core the source lets
carry the `Th_coqc` tag honestly"** — the book's own text is explicit that
N2 is deliberately *not* one of them. A third occurrence, the 42-step
full-arc narration's Face 10 "record law" (`philosophy.md` §8, same
`η_sel+η_map+η_self` decomposition), carries no tier suffix at all in its
own source. Three renderings of the same formula, three different
provenances, three different tiers — `definition` (N2, the general
epistemic schema, `readout_genesis/READOUT_GENESIS_CORE.md` Part VI,
deliberately withheld from `Th_coqc` per §5.7's own argument), untagged
(Face 10, `V3.1`/`RDU` step 28), and `Th_coqc` (EQ-027/EQ-028 above, per
`EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`'s own
"2026-07-25 grounding" tag). This file's own rule is to carry every
source's tier exactly as given, never upgrading and never silently
averaging — so all three stand, side by side, rather than one replacing
the others. **What is and is not independently confirmed here:** this
corpus's own formal-file audit (`readout_genesis/formal/`) found a
Coq-verified theorem backing the *abstract* non-injective-map claim
(`no_decoder_recovers_state`, table above) but did **not** locate a
separate `.v` file mechanizing the *specific* `K_A`/`η_sel`/`η_map`/`η_self`
decomposition EQ-027 states — so EQ-027/EQ-028's `Th_coqc` tag is carried
here exactly as its source states it, not independently re-verified by
this repo, the same caution this book already applies to other cross-repo
`Th_coqc` citations (§1's "supporting, not independent" caveat above).
Read the disagreement as real information, not noise: it says the
*general* claim "knowing is a lossy read" is this book's own considered
`definition`, while a *specific* source elsewhere tags one particular
instantiation of that same shape `Th_coqc` — and this book has not
resolved which of those two framings should win, on purpose. [domain card:
`philosophy.md` §5.7 (N1–N5, "why only one of the five is machine-checked");
`philosophy.md` §8 Face 10; this file's own N2 entry below]

**Extension — record to appearance (`philosophy.md` §5.2d, `Dr`/`Open`,
not machine-checked, imported from the sibling proprietary repo by the
copyright holder's own direction — never upgraded to `Th_coqc`):**

| ID | Statement | Tier | Source |
|---|---|---|---|
| `P_A=Φ_A(M_A)` | the record `M_A` becomes an agent-specific phenomenal field `P_A` via `Φ_A=Φ(Ξ_A,B_A,Val_A,Coh_A,Own_A)` — phenomenal readiness, embodiment, valence, coherence, ownership, declared structural placeholders, not put forward as a solution to what qualia are | `Dr` (chain/import); `Open` on `Φ_A` itself | `research_universal_solver/canon/genesis_canon_v2.1.md` §Φ ; no further falsifier is needed here beyond what the surrounding text (logic.md L95-108) already states: `Φ_A`'s components are declared structural placeholders, and the text is explicit that the hard-problem obstruction is *relocated*, not solved. A falsifier would require `Φ_A` to be filled in as a computable function first — that filling-in is exactly what is marked `Open`, so no additional note is added beyond confirming the existing text already carries this honestly. |
| `P_A ≠ H_A` | what appears (`P_A`) is not the space in which it can be assessed/doubted/revised (`H_A`, epistemic horizon) — collapsing the two is a named error | `Dr` | same |

Full chain: `θ(E) → S_A(E)⊆Δ(E) → (T_A∘Π_A) → M_A=K_A·θ(E)+η (≠θ(E)) → P_A=Φ_A(M_A) → H_A`.
The hard-problem obstruction is *relocated* to `Φ_A`, not solved — stated
here exactly as the source states it, not rounded up. See `philosophy.md`
§5.2d for the full discussion and the "finite-access realism" position
this converges with (§9.19, independently reached in this book).

---

## 0. The root

| ID | Statement | Tier | Source |
|---|---|---|---|
| R-δ | **δ_R = (a ♯ b)** — one retained distinction, the primitive | `Ax`/`Dr` | `readout_genesis/README.md`; `v2/INFORMATION_DNA.md` ; no falsifier applies: δ_R is the declared primitive this entire ledger is built from (`Ax`/`Dr`), not a derived or measurable claim — everything downstream (R-L, RD1-RD9, the trunk equation) is what gets checked, δ_R itself is where checking starts, not something checking can land on. |
| R-L | **L_R := D_W − W** — the graph Laplacian (D_W = weighted degree, W = weighted adjacency); named "the ONE genuinely derived link" from root to trunk | `Th_coqc` | `readout_genesis/README.md` |

### R-L-uniq — why L_R is forced, not chosen (closes audit gap `InfoRetainedDistinctionForcesLaplacian`)

| ID | Statement | Tier | Source |
|---|---|---|---|
| R-L-uniq | Three properties on a weighted vertex operator L — **symmetric**, **zero-row-sum**, **off-diagonal ≤ 0** — read as δ_R's own meaning (symmetric: "A differs from B" is one fact, not two; zero-row-sum: a uniform state retains no distinction; off-diag≤0: reads *difference*, not *connection*) FORCE any L satisfying them into exactly `D_W − W` form — `forced_into_DW_minus_W`, general 3-vertex case, `Q`, proved by `ring`/`lra` | `Th_coqc` | `research_universal_solver/formal/InfoRetainedDistinctionForcesLaplacian_attempt.v` Part 1 |

Witness enumeration (concrete weighted path graph 0–a–1–b–2; a=2, b=3, all `Q`; Part 2 of the same file):

| Candidate operator | symmetric | zero-row-sum | off-diag ≤ 0 | Verdict |
|---|---|---|---|---|
| `L_R = D_W − W` | ✓ | ✓ | ✓ | passes all three |
| adjacency (raw `W`) | ✓ | ✗ (row 1 sums to a+b=5≠0) | ✗ (entries +a, +b>0) | ruled out — `ADJ_fails_rowsum0`, `ADJ_fails_offdiag_le0` |
| signless Laplacian `D_W+W` | ✓ | ✗ (row 1 sums to 2(a+b)=10≠0) | ✗ | ruled out — `QSL_fails_rowsum0`, `QSL_fails_offdiag_le0` |
| random-walk Laplacian `I−D⁻¹W` | ✗ — `RW(0,1)=−1 ≠ RW(1,0)=−2/5` | ✓ | ✓ | ruled out — `RW_fails_symmetric` (concrete numeral witness) |
| normalized (symmetric) Laplacian `D⁻¹ᐟ²(D−W)D⁻¹ᐟ²` | — | — | — | **[Refused]** before the 3-property test can run: entries need `1/√(dᵢdⱼ)`, an I1 (√ / ℝ-completeness) injection, not constructible on the `Q` carrier at all |

Tier: `Th_coqc` — axiom-free, `Print Assumptions` closed, Coq 8.20.1, ground over `Q`, 3-vertex numeral case (the general characterization theorem `forced_into_DW_minus_W` is stated for arbitrary `L : nat → nat → Q` on 3 vertices, not merely the one numeral instance). **Relocates, does not close, the "chosen operator" gap**: the theorem proves `L_R` forced GIVEN the three axioms; it does NOT derive those three axioms from anything weaker than δ_R's own meaning (symmetric retained difference) — that meaning remains the irreducible `Dr` root the forcing argument starts from, per the source file's own stated caveat.

[domain card: `research_universal_solver/docs/root/BORROWED_VS_DERIVED_LEDGER.md` row 4; `research_universal_solver/formal/InfoRetainedDistinctionForcesLaplacian_attempt.v`]

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

No falsifier applies: A1-A8 are a stipulated axiom set (the logic-of-retention formalization this book's own reasoning is declared to correspond to), tagged `Dr` for the correspondence claim itself, not for any measurable consequence of the axioms — axioms are adopted or rejected on grounds of adequacy/consistency, not falsified by observation.

| ID | Axiom | Reading |
|---|---|---|
| A1 | distinguishability | a question is a set of candidate distinctions |
| A2 | transport | no inference without an admissible grammar (units/types match) |
| A3 | retention | only distinctions kept above a threshold count as structure |
| A4 | accessibility | derivability ≠ existence (direct/composite/inaccessible) |
| A5 | admissibility | the comparison metric is positive — any measure used to compare two retained records (e.g. a squared-norm reading of A7's residual `O(Γ,φ)`, of the same shape as `‖O_R‖²` written in §9.8/Face 11 of this ledger for the related quantity `S_R`) must be non-negative, so "closer"/"farther" is always a meaningful, orderable comparison, never a signed or unconstrained score |
| A6 | identity-locking | the same entity tracked through every inference |
| A7 | obstruction | target of inference is consistency O=0, not annihilation — O(Γ,φ) is a measured residual, not a truth value; O=0 is mutual consistency of retaining Γ while reading φ, and a contradiction registers as O>0 (evidence to revise), never as license to derive an arbitrary ψ (no ex-falso explosion) |
| A8 | lens | validate through a lens that does not distort |

Source: `v2/INFORMATION_DNA.md` §Stratum 2 (`docs/root/math/Retained_Distinction_Logic.tex` §sec:rar).
Builds: truth = retention-under-transport; validity = zero-section consistency;
negation = access-reversal; contradiction = obstruction-not-explosion; gated
sequent calculus w/ soundness+normalization; modal difference — all `Dr`
relative to this book, formal source not re-verified here.

---

## 0.5 The number ladder and the operator-grounding floor (information-discrete-math)

Placed here, right after §0's root (`R-δ`, `R-L`, `R-L-uniq`) and before §1's
trunk equation, because every `+ − × ÷ ∂ ∇ = <` written from §1 onward is to
be read against this table, not as bare continuum notation. Source
throughout: `information-discrete-math/textbook/INFORMATION_DISCRETE_MATHEMATICS.md`
Parts 0, II–V, VII, VIII (public repo `information-discrete-math`; skill
`information-discrete-math` not locally installed in this session — textbook
read directly per the mandatory-load rule).

| ID | Statement | Tier | Source |
|---|---|---|---|
| LAD-COM | One commitment: everything an agency ever reads is a finite, discrete, rational readout; ℝ, infinite divisibility, `+∞` are non-readouts — real as boundaries, never as appearances | `Dr` | Part 0 §0.1 (Pr 0.1) |
| LAD-INF | Injected-infinity/zero taxonomy: **I1** ℝ-completeness (LUB/Dedekind) · **I2** `h→0` · **I3** `Re,Λ→∞` · **I4** actual `+∞` · **Z1** the point `r=0` · **Z2** reached continuum `h=0` · **Z3** absolute rest `v=0,T=0` · **Z4** the true void; reciprocity `1/0=∞` names zero and infinity as one non-readout seen from two sides | `Dr` | Part 0 §0.2 (Def 0.2, Pr 0.2) |
| LAD-D | `D` (naturals): generated by RD1–RD9 (`0`, `succ`, injectivity, induction); commutative semiring; total well-order; `D≅ℕ`; discrete floor `¬∃z, 0≺z≺succ 0` — density/continuum provably absent at the root | `Th_coqc` | Part II §2.2–2.3 (`RD.v`, ≈183 decls) |
| LAD-Z | `ℤ := (D×D)/∼` (Grothendieck completion); commutative ring | `Th_coqc` | Part III §3.1 |
| LAD-Q | `ℚ := (ℤ×ℤ≠0)/∼` (field of fractions); field incl. multiplicative inverse `qmul_inv` — ladder `D→ℤ→ℚ` verified end-to-end, 69 constructive theorems, axiom-free | `Th_coqc` | Part III §3.3 |
| LAD-R | `ℝ :=` Bishop **regular Cauchy sequences of `ℚ`** (`\|f n − f m\| ≤ 1/n+1/m`); ordered field up to `Req`; **Cauchy-completeness proved by an explicit constructed limit** `L n := X(2n)(6n)` — the continuum point read off discrete rational approximants; this is the book's own stated thesis, machine-checked | `Th_coqc` (axiom-free unless noted) | Part III §3.4 (Th 3.5–3.6) |
| LAD-R-open | Full trichotomy, a total `≤`, and the classical LUB property are **NOT constructively valid** (each implies LPO/WLPO); cotransitivity + Cauchy-completeness + the finite lattice are their correct constructive replacements — asserting trichotomy/LUB injects I1 | `Dr` (named non-constructivity, Pr 3.1) | Part III §3.4 |
| LAD-KEY | Keystone: `B(Φ,Φ) = I(Φ)` — the operator's Dirichlet energy IS the retained-information functional; edge form `ΦᵀL_RΦ = Σ_edges w·(Φ_i−Φ_j)²`; `L_R = D_W − W` is symmetric PSD | `Th_coqc` | Part V §5.1 (`IDM_Keystone.v: keystone_B_eq_I`, `keystone_nonneg`) |

**Contaminated-concept → discrete-replacement table** (subset load-bearing
for this ledger's own operator usage — see §0.6 below for the full
pre-write-gate version):

| Contaminated (continuum) concept | Discrete replacement | Tier | Source |
|---|---|---|---|
| angle `θ` (`acos`/`atan2`, degrees) | **overlap fraction** `\|⟨v,e⟩_G\|²/(⟨v,v⟩_G·⟨e,e⟩_G)` — Born-rule ratio; `+,·,÷` only, no trig/π/ℝ | `Th_coqc` (Def 4.2a) | Part IV §4.2 |
| derivative `f'(x)=lim_{h→0}Δf/h` | forward/backward difference `Δf(n)=f(n+1)⊖f(n)`; `∇f(n)=f(n)⊖f(n−1)`; discrete Jacobian `J_F[i,l]=∂F_i/∂x_l`; exact-algebra, no limit | `Th_coqc` | Part VIII §8.1, §8.8 |
| integral `∫` | antidifference `Σ_a^b f`; discrete FTC `Σ_a^bΔf=f(b)⊖f(a)` | `Th_coqc` | Part VIII §8.1–8.2 |
| limit / `ε–δ` continuity | finite-`ε` rung (A8 discipline): work at finite `ε` first, take `ε→0` only after a declared stability proof | `Th_coqc` rung / `+ℝ-axioms` tower for the full continuum form | Part 0.5 §0.5.5 (A8); Part X §10.5 |
| `∞` / a point `r=0` | refused endpoints (Th 6.1; the endpoint boundary) — a finite reader lives strictly between them, touching neither | `Dr` (Pr 0.2 reciprocity) | Part VII §7.5 |

**Operator-grounding clause (Pr 7.0).** Every operator below is, first, a
mode of retained distinction on *readouts* — its ordinary textbook meaning
("add magnitudes", "the angle between two vectors") is only the machine
shadow, never the primary reading:

| Op | Discrete/retained-information meaning | Tier | Source |
|---|---|---|---|
| `=` | mutual indistinguishability to every reader (`O(x)=O(y)`); grounded non-circularly in coarse-grain fibers `G_λ`, not defined using `=` itself | `Th_coqc` | Part 0.5 §0.5.3; Part VII §7.2 |
| `≺`/`<` | retained precedence — accumulated-record order; total + well-ordered on `D` (Th 2.3); on `ℝ`, only **cotransitive**, not trichotomous (Pr 3.1) | `Th_coqc` (`D,ℤ,ℚ`) / `Dr` non-constructive residue on `ℝ` | Part VII §7.2 |
| `⊕` (`+`) | accumulation — merge two retained records into one longer record | `Th_coqc` | Part VII §7.3 (Th 7.1) |
| `⊖` (`−`) | cancellation/debt of retained distinction; **partial** on `D` (defined only `b⪯a`) — that refusal is exactly where `ℤ` is born; total signed on `ℤ` | `Th_coqc` | Part VII §7.3 |
| `⊗` (`×`) | replication/composition of distinction-structure — lay `b` copies of `a`'s pattern end to end | `Th_coqc` | Part VII §7.3 (Th 7.2) |
| `÷` | equal partition, the inverse of replication; `÷0` **REFUSED** — the operator loses invertibility at the endpoint (Th 6.1), never a value | `Th_coqc` (defined `b≠0`) / refused at `0` | Part VII §7.3 |
| `Δ`/`∂` (finite-difference form) | local change of retained distinction between adjacent ticks; multivariate form is the discrete Jacobian; exact algebra, no limit | `Th_coqc` | Part VIII §8.1, §8.8 |
| `∇` (backward difference / graph gradient) | `∇f(n)=f(n)⊖f(n−1)`; on the relation graph, gradient/divergence/curl of the discrete exterior calculus over `L_R` | `Th_coqc` | Part VIII §8.1, §8.6 |
| continuum `f'(x)=lim_{h→0}`, `∫` | recovered **last**, as a readout of `Δ/Σ` under `h→0` sampling — flagged `+ℝ`, never primitive | `+ℝ-axioms` (`Dr`) | Part VIII §8.7 |

**Binding note for the rest of this ledger.** §1's trunk equation
(`M ∂²Φ + D ∂Φ + K·L_R Φ + ∇V(Φ) = J − η`) and every downstream EQ- entry
that writes `∂` or `∇` is to be read through this table: the `∂²Φ`/`∇V(Φ)`
there are the Part VIII §8.7 `+ℝ`-readout rung (continuum calculus as the
last readout), not primitive operators smuggled in from ordinary math —
consistent with, and now giving content to, §1's own per-term tier split
(`M ∂²Φ = Dr`; `D ∂Φ = finite_diagnostic`; `K·L_R Φ = Th_coqc`).

---

## 0.6 Operator grounding — the contaminated-concept checklist (pre-write gate)

Every operator used anywhere in this ledger (`+`, `−`, `∂`, `∇`, `=`, `<`,
"derivative", "limit", "adding two retained states") is itself a claim, not
neutral borrowed continuum notation. Complements §0.5's table with the full
pre-write-gate version. Source: `information-discrete-math` SKILL.md,
contaminated-concept table + Pre-write CHECKLIST section
(`plugins/information-discrete-math/skills/information-discrete-math/SKILL.md`).

| Contaminated concept | Discrete-correct replacement | Tier |
|---|---|---|
| ℝ / completeness (LUB/Dedekind) | readout of Bishop regular Cauchy sequences over ℚ; only finite ℚ-approximants appear | `Th_coqc` (D→ℤ→ℚ→ℝ ladder, axiom-free, per source) |
| the point (`r=0`) | node / retained distinction (graph vertex, has neighbours) | `Dr` |
| `0` as an occupied state | refused non-readout (approached, never reached); or the `L_R` kernel = indistinguishability | `Dr` |
| `+∞` / `N→∞` / a limit that "lands" | finite approach only; ℚ has no `+∞` | `Dr` |
| infinite divisibility `h→0` | finite step / `τ_c` floor | `Dr` |
| angle/degree (`acos`/`atan2`) | overlap fraction `‖⟨v,e⟩_G‖²/(⟨v,v⟩_G·⟨e,e⟩_G)` (rational `+,·,÷` only) or rational turning number | `Dr` |
| continuity/"smooth" (ε–δ over ℝ) | discrete Lipschitz / non-expansive map | `Dr` |
| distance `= √Σ(Δxᵢ)²` (coordinate difference) | accumulated retained resistance along the optimal path (graph geodesic) | `Dr` |
| π, e, φ as "numbers" | readout-invariants; only finite ℚ-approximants appear | `Dr` |
| derivative/integral = continuum limit | discrete `Δ` + `Σ` + discrete FTC + Leibniz rule | `Th_coqc` (discrete FTC, per source, not re-verified in this repo) |
| operator on a continuum (`∂²`, d'Alembertian) | graph Laplacian `L_R` (symmetric, PSD, kernel ⊇ constants) — `∂²` is a declared `+ℝ-axioms` readout of it | `Th_coqc` (axiom-free, matches R-L §0) ; no falsifier applies to this block as a whole (LAD-COM, LAD-INF, LAD-R-open, and both contaminated-concept replacement tables, L187-256): these are definitional substitutions (angle→overlap fraction, point→node, derivative→finite-difference, etc.), each already carrying its own tier and Coq/textbook source per row. A definition is adopted or rejected for adequacy, not falsified; where a row's *use* elsewhere in this ledger makes a testable claim (e.g. the overlap-fraction reading feeding EQ-015's per-term tiers), the falsifier belongs to that downstream use, not to the dictionary entry itself — see §1's trunk-equation table and the 'Binding note' at L225-231 for where this dictionary actually gets exercised. |

**Pre-write CHECKLIST** (run before committing any equation, proof, or
number to this ledger):
1. Left-column concept present (angle in degrees, real coordinate, landing
   limit, zero-size point, singular `1/0`, `N→∞`, inverse trig)? → replace
   with right column first.
2. Is the quantity about to be called physical actually a smooth bijection
   of a free knob? → it is a coordinate, not an observable.
3. About to tag something `Open`/hard/paradoxical? → diagnose which
   I1–I4/Z1–Z4 was injected before deferring.
4. A refused endpoint (`Θ=1`, `T=0`, `r=0`, `Λ→∞`) being treated as a wall?
   → it is correctly-refused; approach, never reach.
5. Tier every resulting claim (`Th_coqc`/`finite_diagnostic`/`Dr`/`Open`+reals)
   — never collapse.

Tier of this entry as a whole: `Dr` (table + checklist framing, per source)
— the two `Th_coqc` cells above are witnesses *named at source*, not
re-derived or re-verified in this repo.

**Retroactive honesty note (gap disclosed, not fixed here):** this
checklist has not yet been run against this ledger's own existing entries.
EQ-015 (§1) writes `∂²Φ`, `∂Φ`, `∇V(Φ)` as bare continuum operators with no
`+ℝ-axioms` tag, even though its own `K·L_R Φ` term is the one piece
already `Th_coqc`-axiom-free. EQ-007 (§6) `v = √(D/τ_c) < ∞` carries an
unflagged square root and an unflagged `<∞` comparison. Neither is
rewritten here — retagging/replacing them per this table is a separate
repair task.

[domain card: information-discrete-math SKILL.md; contaminated-concept
table + Pre-write CHECKLIST section]

---

## 1. The trunk equation

**M ∂²Φ + D ∂Φ + K·L_R Φ + ∇V(Φ) = J − η**  (EQ-015)

Mixed tier, per-term ([`EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`]):

| Term | Tier |
|---|---|
| M ∂²Φ | `Dr` ; this term's `Dr` tag is already load-bearing evidence, not a placeholder: Arrow 3 (§0.5-adjacent chain, logic.md ~L376) settles that `M∂²` is **not** forced from δ_R alone — it is an independent structural ingredient requiring the extra posit of re-readability/oscillation, with five of six candidate forcing readings refuted by explicit witness. A future reading that derives 2nd-order-in-time dynamics from 1st-order retention alone, without adding a new posit, would falsify Arrow 3's negative result and upgrade this term's tier. |
| D ∂Φ | `finite_diagnostic` |
| K·L_R Φ | `Th_coqc` (admissibility skeleton only) |
| ∇V(Φ) | untagged in source (the source bracket at `EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`#EQ-015 tiers only the four terms above; §10's N1-L3 (cf. §9.8) audits this term's nonlinear paraproduct behavior at `finite_diagnostic`, but that is a checker result on the term, not a per-term tier of EQ-015 itself) |
| J | untagged in source (same bracket omission as ∇V(Φ); no tier is assigned to the forcing term `J` anywhere in the source ledger) |
| η | `finite_diagnostic`/`Open` ; the `finite_diagnostic` half of this split is not free-floating: EQ-017's continuum reader form `τ_R İ_R + L_R I_R = S_R + η_R` (§1, PASS_WITH_LIMITS) is the concrete instance where this same residual term is actually measured. The `Open` half stays open in exactly the sense OPEN_CONSTANTS is open below — no claim about η's absolute magnitude is made, only that a residual term must be present; a run of EQ-017 returning `η_R≡0` under declared conditions would falsify the residual's necessity, not merely its size. |

`λ_c = D²/(4MK)` — `Dr` (EQ-016). Continuum reader form:

Falsifier surface: λ_c is a ratio of the same M,D,K constants OPEN_CONSTANTS (§1 above) declares non-readout in absolute value — but the dimensionless combination D²/(4MK) is exactly the kind of ratio that check permits. The nearest existing evidence is N1-M/N1-QM's independent D/M-vs-QuTiP residual (7.6×10⁻⁴, `finite_diagnostic`, §9.8); extending that same cross-check to recover K independently and testing whether the resulting λ_c matches the regime boundary observed in the DRL/URR runs (§2, §7) would be the direct test of this `Dr` reading. The second occurrence of this equation (logic.md ~L608, EQ-016 in §6's core-subset table) is the same claim restated — see this entry rather than duplicating.
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

No independent falsifier applies to the composite reading itself: it is an interpretive claim about how S1-S3 (each already `Th_coqc`-tagged individually, L320-322) and 'logic' relate, not a new measurable quantity. Its checkable content is entirely inherited from S1-S3's own bricks (`spine_lambda_c`, `self_sensing_loops_if_above_lambda_c`) — forcing a separate falsifier on the composite label would double-count the same evidence under a new name.

**Scale gauge non-readout (the constants M, D, K themselves):**

| ID | Statement | Tier | Source |
|---|---|---|---|
| EQ-016b | `InfoScaleGaugeNonReadout`: ∀s>0, rescaling (M,D,K)→(s·M,s·D,s·K) leaves τ_c=M/D, the dispersion relation, and the discriminant sign invariant ⇒ absolute M,D,K are non-readouts (asking for their absolute value is `[Refused]` as a dimensional/non-readout question, not an open gap); only dimensionless ratios (τ_c, α, mass ratios) are genuine readouts | `Th_coqc` | `research_universal_solver/README.md` §Adversarial self-audit, 'Constants' bullet |

Operator note on `s·(_)` here: this is not the continuum group ℝ_{>0} acting
on a real-valued triple by ordinary multiplication, injected as a bare
non-readout. The only certified content is the finite comparison the Coq
brick actually runs — the same three checks (τ_c, dispersion, discriminant
sign) return the identical value before and after relabeling the triple by
one common factor `s`. `s` itself has no readout status; it indexes the
orbit, it is not a measured quantity, and "invariant" here means decidable
equality of a finite-diagnostic triple, not an ℝ-limit statement. The
genuinely open readouts stay the dimensionless ratios (`α`, particle-mass
ratios) — those are readouts but are not forced by the graph; they remain
`[Open]`, not resolved by this brick.

---

## 1.5 Stream of Necessity — root→graph→L_R→2nd-order→D>0 (four-arrow necessity chain)

Source: `research_universal_solver/docs/root/STREAM_OF_NECESSITY.md` +
`research_universal_solver/README.md` §Adversarial self-audit findings
(2026-07-07). Chain (`=` here means *definitional identity of the readout*,
a decidable finite check, never an ℝ-equality asserted by fiat):

**root δ_R (retained distinction) → weighted graph (nodes/edges/weights) →
L_R = D_W − W (vertex operator) → M∂²Φ+D∂Φ+K·L_RΦ=0 (spine PDE)**

Operator grounding (per §0.5/§0.6's discrete floor — every symbol below is
a finite retained-state operation, not borrowed continuum notation):
`D_W − W` is a finite entrywise subtraction of two finite-dimensional
weight readouts (retained-degree minus retained-adjacency), not a
continuum difference; `∂²Φ`/`∂Φ` in the spine PDE are finite-difference
(discrete forward-Euler / leapfrog) recurrence steps,
`(Φⁿ⁺¹−2Φⁿ+Φⁿ⁻¹)`-type, never an `h→0` limit; `τ_c = M/D` is a finite
ratio of two retained scalars, and `D>0` below is a decidable finite
sign-comparison on that ratio, not an ℝ-order relation smuggling in `+∞`.

| Arrow | Step | Tier (honest, per-arrow) | Necessity, one line | Brick (`formal/`) |
|---|---|---|---|---|
| 1 | root → weighted graph | `DEFINITIONAL` (forced-by-definition) | δ_R = (a♯b) already *is* a symmetric (a≠b), positive (w>0) edge by its own meaning — not derived from anything weaker | `InfoDistinctionIsEdge_attempt.v` (`Th_coqc`, 14/14 `Closed`, re-verified `coqc` exit 0) |
| 2 | graph → L_R | `Th_coqc`-forced-**given**-δ_R's-meaning | `L_R = D_W − W` is the *unique* operator on {symmetric, zero-row-sum, off-diagonal≤0}; adjacency/signless/random-walk each fail ≥1 property by explicit witness; normalized Laplacian `[Refused]` outright (needs `1/√(d_id_j)`, an I1 sqrt-injection). The three axioms = "retained distinction read pointwise" is asserted in `Dr`-tier prose, not proved — the choice is *relocated* onto δ_R's meaning, not eliminated | `InfoRetainedDistinctionForcesLaplacian_attempt.v` (`Th_coqc`, 8/8 `Closed`, self-certifying `forall`-style, re-verified) ; the nearest available check on this Dr-tier prose reading is already in this file: R-L-uniq's witness enumeration (logic.md L125-133) tests adjacency, signless Laplacian, random-walk Laplacian, and the normalized Laplacian against the same three properties and rules each out by explicit witness. A falsifier for Arrow 2's own prose step would be a *different* reading of 'retained distinction read pointwise' that legitimately motivates a fourth property (or drops one of the three) without contradicting δ_R's stated meaning — none has been produced. |
| 3 | L_R → 2nd-order-in-time (M∂²Φ) | `Th_coqc`-forced-**given**-Open-posit (re-readability) — **settled NEGATIVE as a root-derivation** | `M>0` follows *iff* "retention" is strengthened to re-readability/oscillation (complex-conjugate mode root) — an extra `[Open]` posit, not analytic in δ_R alone. Six forcing readings tested (persist·held·re-readable·own-clock·decay·finite-cone); five refuted as root-derivations by the *same* fact — 1st-order dynamics already satisfies them. `M` is an independent structural ingredient (retention *of the rate*, not of the state) | `InfoRetentionForcesSecondOrder_attempt.v` (`Th_coqc`, 9/9; proves forcing given the posit); refuting bricks `InfoRetainedIsHeldNotFading_attempt.v`, `InfoStrictConeBothOrders_attempt.v` (`Th_coqc`) |
| 4 | spine → D>0 dissipation | `Th_coqc`-forced-**given**-τ_c=M/D-is-the-memory-law | Given `τ_c=M/D` (itself independently `Th_coqc`, `InfoMemoryBeforeMass_attempt.v`), the `D→0` limit sends `τ_c` past every finite bound — an actual `+∞` (I4) smuggled in as "no damping." Refusing I4 forces the **sign** `D>0` only; the value of `D` stays `Open`/`OPEN_CONSTANTS` | `InfoFiniteMemoryForcesDissipation_attempt.v` (`Th_coqc`, 3/3 `Closed`) ; see the `OPEN_CONSTANTS` falsifier already stated a few lines below in this same block (logic.md ~L397: EQ-016b non-readout status for absolute M,D,K; the checkable surface is the dimensionless ratio τ_c=M/D, tested once at residual 7.6×10⁻⁴ against QuTiP). Arrow 4's `D` stays Open in the identical sense — this is the same claim, not a second one requiring its own falsifier. |

**Independent re-verification** (not taken on the build reports' word, per
this file's own discipline): all four bricks re-`coqc`'d in the source
pass, exit 0; `Print Assumptions` on the live theorem = `Closed under the
global context` for every one (14/14, 8/8, 9/9, 3/3).

**Bottom line (matches philosophy.md §5.3's stated position exactly, now
graded per-arrow instead of collapsed to one sentence):** the chain does
**not** derive the whole spine FORM from the bare root by necessity. It
derives a narrower, honest result: Arrows 1–2 (graph carrier + the specific
`L_R = D_W − W` operator) are forced **given** retained-difference meaning;
Arrow 4 (`D>0`) is forced **given** finite `τ_c=M/D` plus refusal of actual
infinity (I4); Arrow 3 (`M∂²`, 2nd-order-in-time) is **not** forced — it is
an independent structural ingredient, layered on when a system retains
rate/momentum as its own degree of freedom, not derivable from "the state
is retained" alone. Constants `M, D, K` remain entirely `[Open]`/
`OPEN_CONSTANTS` throughout; only the qualitative graph/Laplacian/
dissipation-sign structure is forced, never a numerical value.

Falsifier for `OPEN_CONSTANTS`: per EQ-016b (`InfoScaleGaugeNonReadout`,
`Th_coqc`, §1 above), no measurement can ever pin absolute `M,D,K` — that
question is `[Refused]`, not a pending gap. What is checkable is the
dimensionless ratio `τ_c=M/D`, already tested once (N1-QM below, `D/M` vs
QuTiP, residual `7.6×10⁻⁴`, `finite_diagnostic`); running the same
`D/M`-vs-independent-simulation check in a second, disjoint regime and
finding it does *not* converge to a comparable residual would falsify the
claim that this ratio is domain-stable.

See §1 above for the trunk equation's own per-term tier table (EQ-015),
which this chain feeds.

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
- **`v`-prefix (`vΦ`, `vΨ`, `vqᵢ`, `vrᵢ`, `vΦᵢ`, `vΨᵢ`)** — discrete velocity:
  the field's own finite-difference rate between adjacent time steps
  (confirmed at source, `evidence/DRL_Discrete.v`: "state and velocity
  (Phi,Psi,vPhi,vPsi)"), treated as an independent variable in the discrete
  Legendre transform that produces the bilinear charge `H` — not a
  continuum time-derivative.

| ID | Result | Tier | Source |
|---|---|---|---|
| DRL-1 | Euler–Lagrange (variation w.r.t. Ψ) ⇒ `(M/Δt²)Δ²Φ + (D/2Δt)(Φⁿ⁺¹−Φⁿ⁻¹) + K·L_RΦ + k₂Φ = 0`; \|∂S/∂field\| on trajectory = 4.4×10⁻¹⁰ | `finite_diagnostic` | `ap/ap5_drl.py` |
| DRL-2 | Mirror equation (variation w.r.t. Φ) ⇒ Ψ anti-damped; in this linear model Φ,Ψ decouple in EL — Ψ's growth is from its own IC, not handoff from Φ | `Open` (in DRL model) | `ap/ap5_drl.py` ; this stays Open specifically *in the DRL model*, where the linear pair decouples in Euler–Lagrange; §3's T4 (γ↔D/M bridge, `finite_diagnostic`, rate diff <5%, reviewer 0.17%) is the sibling model where 'dissipation = handoff across Π' does become checkable and passes. DRL-2 records that the same handoff reading is not forced by the DRL action itself — a future coupling term in the DRL Lagrangian that made Ψ's growth rate track Φ's decay rate above measurement noise would close this gap; none is currently posited. |
| DRL-3 | Bilinear invariant `H = M·vΦᵀvΨ + K·ΦᵀL_RΨ + k₂·ΦᵀΨ`; rel. drift 1.5×10⁻⁴ over 4000 steps. Reading H as "conservation of distinction" is `Dr`, not a proved mechanism — counterexample: Ψ₀=0 ⇒ Ψ≡0, H≡0 while Φ dissipates fully | `finite_diagnostic` (measurement) / `Dr` (interpretation) | `ap/ap5_drl.py` ; this row already states its own falsifier in full: the Ψ₀=0 counterexample (H≡0 while Φ dissipates fully) is a standing witness against reading H as a general 'conservation of distinction' law, holding H's `Dr` interpretive tag down while leaving the measured drift (`finite_diagnostic`, 1.5×10⁻⁴) untouched. No additional falsifier is needed beyond what is already written here. |
| DRL-4 | D=0 ⇒ Φ,Ψ obey the same conservation law (Φ=Ψ admissible); reduces to the original theory exactly | `finite_diagnostic` | `ap/ap5_drl.py` |
| DRL-Coq-T1 | EL-identity (iff both directions): dS/dΨ=0 ⟺ damped recurrence; dS/dΦ=0 ⟺ anti-damped — 3-ring, 3-slice scope; 2 classical Reals axioms declared (`sig_forall_dec`, `functional_extensionality`) | `Th` (declared-axiom; NOT `Th_coqc` — `Print Assumptions` shows 2 non-constructive classical Reals axioms, so this does not meet the axiom-free bar the `Th_coqc` legend requires) | `evidence/DRL_Discrete.v` (Coq 8.20.1, exit 0, independently reverified) |
| DRL-Coq-T2 | D-cancellation: Legendre charge H contains no D — pure `ring` identity | `Th_coqc` | `evidence/DRL_Discrete.v` |
| DRL-Coq-T3 | Leapfrog shadow energy exactly conserved at D=0 | `Th_coqc` | `evidence/DRL_Discrete.v` |
| DRL-Coq-genN | General-N per-node Legendre/D-cancellation, axiom-free, list induction: any node count, per-node M_i/D_i. `GB` is now a genuine weighted-graph bilinear pairing (`graph_bilinear`/`graph_legendre_D_cancellation`, added 2026-08-03) over arbitrary list positions — the standard UNDIRECTED weighted-graph Laplacian edge-sum identity for x^T·L_w·y at general N — cross-checked non-vacuous against `DRL_Discrete.v`'s own concrete N=3 ring `LR1` bilinear form, matched term-for-term (`ring_bilinear_matches_LR1`). `w`'s type is unconstrained but the computed value provably depends only on `w`'s symmetric part (`graph_bilinear_symmetrizes`, machine-checked, found by adversarial review same day) — this construction is the undirected graph case only, not a genuinely-any-weight-function/directed-graph result despite the type signature. `w_i` (the per-node term) remains an opaque, velocity-independent Q-value covering any non-D per-node term honestly, not specifically checked against a quadratic/quartic potential's own structure. `H = Σ Mᵢvqᵢvrᵢ + GB + Σ wᵢ` | `Th_coqc` (axiom-free) | `evidence/DRL_General_Legendre.v` |
| DRL-5 | Generalization: random weighted graph N=8, per-node M_i/D_i, quartic V, forcing J — EL residual 2.2×10⁻¹⁰ | `finite_diagnostic` | `ap/ap6_drl_general.py` |
| DRL-6 | **H_nl = Σᵢ Mᵢ vΦᵢvΨᵢ + K ΦᵀL_wΨ + Ψᵀ∇V(Φ) − JᵀΨ** — corrected nonlinear charge; quartic drift <2×10⁻³ (vs 0.119 for the wrong quadratic charge); reduces to linear charge at k₄=0; O(Δt²) confirmed | `finite_diagnostic` | `ap/ap8_h_quartic.py` |

Symbol gloss (DRL-Coq-genN, DRL-5/6; confirmed at source): `k₂` — the
quadratic-potential coefficient in `∇V(Φ)=k₂Φ+k₄Φ³` (paired with `K`, the
`L_R`/`L_w` coupling strength; both declared constants, not derived);
`k₄` — the quartic-potential coefficient of that same `∇V(Φ)`, the
correction DRL-6 exists to handle (`ap/ap8_h_quartic.py`: `gradV = k2*Phi +
k4*Phi**3`); `GB` — DRL-Coq-genN's general-N graph-coupling term, now a
genuine weighted-graph bilinear pairing (`graph_bilinear`, added
2026-08-03) over arbitrary list positions and an arbitrary weight
function, cross-checked non-vacuous against DRL-Coq-T2's own concrete
N=3 ring `LR1` bilinear form, matched term-for-term
(`ring_bilinear_matches_LR1`) — a matching, independently-built
construction, not a Coq-checked specialization of one theorem to the
other: `evidence/DRL_Discrete.v`'s own `T2_D_cancellation` is stated over
R at fixed N=3, `evidence/DRL_General_Legendre.v` works over Q at general
N, so no embedding/reduction lemma connects the two theorems as such,
only this cross-checked matching construction; `L_w` — **not** a typo
for `L_R`: DRL-5/DRL-6's own weighted-graph Laplacian for the N=8 random
test graph used in that generalization run, same `D_W−W` construction as
`L_R` but instantiated on a different (randomly generated) weighted graph
(`ap/ap6_drl_general.py`: `build_weighted_graph` returns `L_w =
diag(rowsum) − w`).

**Novelty ledger (declared, `[Open]`):** doubling-for-action has known
ancestors (Bateman 1931, Caldirola–Kanai, CTP/Keldysh, Galley 2013 general
nonconservative variational doubling, Marsden–West discrete variational
integrators) — must never be cited as originated here. Candidate-novelty
layer only: (a) the discrete-graph tensor form G⊗L_R, (b) Ψ read as *ontic*
record (not auxiliary/fictitious, per RD4), (c) zero-diagonal G read as the
Doctrine of Quantity in metric form. Literature falsifier search (2026-07-19)
found no prior work combining all three — status: `[Open]`. Per this
workspace's own standing rule (philosophy.md §6), an external literature/
peer check is one further input the corpus would weigh like any other
adversarial reviewer, never a gate or lever that by itself raises this
claim's tier.

---

## 3. Append-Only Tape Record (AP7)

Source: `v2/APPEND_ONLY_RECORD.md`. Posited map (no action — declared cost
vs. DRL): phase state z=(u,w), orthogonal step-conserving C:
`z̃ = Cz → z' = √(1−γ)z̃, ρ = −√γ z̃ → Ψₙ₊₁ = Ψₙ ⊕ ρₙ`.

`u,w` — the field/velocity pair `(Φ,∂Φ)` rewritten into normal-mode scaled
coordinates (confirmed at source, `ap/ap7_tape_record.py`: `(phi, vel) ->
z=(u,w)`); `C` — the per-step normal-mode rotation, an orthogonal (norm-
preserving) map on that scaled pair, not a generic matrix; `Q(z)` — the
conserved quadratic invariant `Q(z)=|z|²/2`, i.e. the retained-state energy
in the scaled coordinates (`ap/ap7_tape_record.py: def Q`), a finite sum of
squares under `δ_R`, not a continuum norm; `ω_min` — the smallest
normal-mode frequency `min(√(λᵢ/M))` over the graph's `L_R` eigenmodes
(`ap/ap7_tape_record.py`: `omega_min = _OMEGA.min()`, `_OMEGA =
√(_LAM/M)`), used only as the underdamped-regime guard `D < 2Mω_min`.

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
as LTP1) — `r` is the per-record residual vector (model prediction minus
observed record, e.g. `y − Y_OBS` in `ap/ap4_phi_fi.py`) and `W` is the
diagonal inverse-variance (precision) weight matrix on those records
(`W = diag(1/σ²)`, confirmed at source: `V_hubble` sums `((y−Y_OBS)/SIG)²`,
which is exactly `rᵀWr` with `W=diag(1/SIG²)`) · V\* = minimum over
parameters.

| ID | Property | Note | Tier |
|---|---|---|---|
| FI-1 | 0 ≤ Φ_FI ≤ 1 (nested-family inclusion V\*(C∖π) ≤ V\*(C)) | provable by set-inclusion (Coq lift: `Open`/roadmap); asserted numerically | `finite_diagnostic` |
| FI-2 | Φ_FI is always named to its π — no bare Φ | | untagged in source (informal statement; no `Dr`/tier bracket assigned) |
| FI-3 | Decision rule: high Φ_FI ⇒ decisive record identifies π directly | | `Dr` ; FI-5 (two rows below, `finite_diagnostic`) is the standing falsifier for this decision rule: an unconstrained free parameter returns a false Φ_FI=1 without carrying a real prior, i.e. a high Φ_FI that does *not* decisively identify π unless a negative control with a real prior rules out the dof-saturation artifact (confirmed in the ω_b run, real prior σ=0.00015 ⇒ Φ_FI≈0.025 vs the unconstrained 1.0000). FI-3 should be read together with FI-4's negative-control requirement, not in isolation. |
| FI-4 | Requires a non-tautological negative control | | untagged in source (implemented in `ap4`; no `Dr`/tier bracket assigned) |
| FI-5 | dof-saturation limitation: an unconstrained free parameter gives a false Φ=1 unless it carries a real prior | adversarial-review finding | `finite_diagnostic` |

First runs (`ap/ap4_phi_fi.py`, `finite_diagnostic`, toy tier): Hubble toy
(π=w released) Φ_FI = 1.0000; world-side control (non-absorption) Φ_FI =
0.000; ω_b released with real prior σ=0.00015 ⇒ Φ_FI ≈ 0.025.

**Novelty:** algebraic form is a direct relative of nested-model
likelihood-ratio/Δχ² — standard, not new. Candidate-novelty layer `[Open +
stance]`: attribution-to-a-named-posit semantics + decision rule + mandatory
negative control, vs. literature tension metrics (Δχ², suspiciousness,
Q_DMAP) that measure magnitude, not attribution.

No falsifier applies: this is a positioning claim (is the attribution semantics genuinely distinct from Δχ²/suspiciousness/Q_DMAP, or a relabeling of them) rather than a claim about a measurable quantity — it is settled by literature comparison and definitional argument, not by an experiment, which is why it is tagged `[Open + stance]` rather than `Open` alone.

---

## 5. AP20 — Retention Self-Interaction Ratio (conditional, narrow)

Source: `v2/RETENTION_SELF_INTERACTION.md`. Premises: (1) one unital ordered
bilinear composition m(x,y) — the one declared way two channels compose
(unital, associative, bilinear; not derived from RD4, taken as given); (2)
borrowed commutator curvature
`K(x,y)=m(x,y)−m(y,x)` (noncommutative input is borrowed, not derived from
RD4); (3) self-carrier closure; (4) one common quadratic load (declared,
free overall normalization). `c_geo` and `c_self` are the two Hessian
(curvature) coefficients read off the ε² term of `K(A_x+εa_x, A_y+εa_y)`
under premise (4)'s one shared quadratic load: `c_geo` weights the
background/geometric pairing, `c_self` weights the fluctuation/self pairing
— both measured, not independently defined observables.

| ID | Result | Tier |
|---|---|---|
| AP20-1 | ε² coefficient of `K(A_x+εa_x,A_y+εa_y)` equals `K(a_x,a_y)` exactly (bilinearity) | `exact_algebra` (symbolic-exact, seed-free — proved on generic SymPy matrix entries with no numbers substituted, `ap20_symbolic_forcing.py`; per source `v2/RETENTION_SELF_INTERACTION.md`, this is distinct from AP20-2's numeric-only check below — reconciled here to the nearest legend tier rather than left as an undocumented tag) |
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
generation counting, mass fits) is intentionally NOT absorbed; see §9.1,
which names this non-absorption explicitly and closes part of the gap.

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
| EQ-063 | τ_c = ℏ/(2mc²); m = ℏ/(2c²τ_c) — unit/calibration bridge ONLY, does NOT derive EQ-015's M coefficient (8 forcing attempts failed; campaign logged at EQ-063's own entry in `EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`, self-caught during founder's bottleneck review; cross-repo summary footnote¹ below) | `Dr` (bridge) ; this entry already reports a completed falsification, not an open one: 8 independent attempts to force EQ-063 into deriving EQ-015's M coefficient failed (logged at the source ledger's EQ-063 entry, self-caught during founder review), which is why the tier is capped at `Dr` (bridge) rather than any derivation tier. A 9th attempt succeeding would reopen this, but the current status is a settled negative, and should be read as such rather than as a pending gap. |

¹ **EQ-063 cross-repo summary (external citation, paraphrased — a conclusion
summary, NOT an itemized log of the 8 attempts; no such itemized list is known
to exist in this repo or the source repo).** Per the `M ∂²_t Φ` row of the
mother-equation table in the sibling (proprietary, not publicly readable)
`research_universal_solver` repo's `domains/standard_model/source_root/
READOUT_GENESIS_CORE_SNAPSHOT.md` (same content also present in that repo's
`docs/engineering/GENESIS_STEP_BY_STEP_V3_1.md`): `M` is a posit, not a
derivation (`Dr`); a direct attempt to force `M` out of more primitive
structure was tried and failed 8 separate times (`finite_diagnostic`). What
that source states IS established, by contrast, is the mass-as-readout-of-τ_c
relation `m = ħ/(2c²τ_c)` — with τ_c discrete and logically prior to mass — and
a `D/M` ratio checked against QuTiP giving a residual of 7.6×10⁻⁴
(`finite_diagnostic`). Tiers reported here match what the source itself
assigns to each piece — not upgraded.

Source file for EQ-032–034: `research_universal_solver/formal/InfoTrueRecordUnreadable_attempt.v`
(cross-referenced in `philosophy.md` §1 and `logic.md` §3 above — same
underlying general theorem, cited once per relevant section).

---

## 7. URR-C 0.4 master system (native calculation contract)

URR-C = Universal Retention–Cut–Return–Readout System (per `v2/urr/README.md`, `urr_native_system.md`); expanded here at first use, acronym-only thereafter.

Source: `v2/urr/URR_C_MASTER_0_4.md` / `urr_native_system.md`. Doubled
reader–record space 𝒳_T = 𝓗_T ⊕ 𝓗_T, X_n=(Φ_n,Ψ_n)ᵀ; lifted projector
Ō_α = I₂⊗O_α, H̄_α = I−Ō_α. `𝔾_T` (URR-2 below) — the lifted graph coupling
operator, the same construction as EQ-020's `𝔾_n`
(`EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`#EQ-020 —
SM-stream entry, `Dr` tier at source; not reproduced in §6's core subset,
which stops at EQ-017/EQ-032-034/EQ-063 per §6's own stated non-absorption
of EQ-018 onward): `L_R` Kronecker-lifted onto the field/reader-record
space plus the internal-coupling term
(`G_T = KRON(L_R,I_ℱ) + KRON(I_nodes,C_ℱ) + C_int`, confirmed at source,
`v2/urr/URR_NATIVE_TECHNICAL_SPEC.md` line 696) — not a separate primitive
from `L_R`, only its lifted/coupled form at this level of the stack.

The checkable content sits one level down from EQ-020's own `Dr` citation: the decomposition `G_T = KRON(L_R,I_ℱ) + KRON(I_nodes,C_ℱ) + C_int` is confirmed at source (`v2/urr/URR_NATIVE_TECHNICAL_SPEC.md` line 696) — a falsifier would be finding this Kronecker-lift form does not actually match `𝔾_n`'s definition at its own EQ-020 source entry (a direct textual/algebraic cross-check not yet performed here, since §6's core subset explicitly does not absorb EQ-018 onward).

| ID | Equation | Tier |
|---|---|---|
| URR-1 | 𝓔_DRL[X]_n = 𝓙_{C,n}[X_n] (native DRL forced by balanced cut, not replaced by it) | `Dr`/`definition` |
| URR-2 | Reader spine: M(Φ_{n+1}−2Φ_n+Φ_{n-1})/Δt² + D(Φ_{n+1}−Φ_{n-1})/2Δt + K𝔾_TΦ_n + ∇V(Φ_n) − J_n = P_Φ𝓙_{C,n}[X_n] | `Dr` (forced discrete variational system, not derived from one unified action) ; the empirical test surface for URR-1/URR-2 already sits a few lines below in this same section: AP17's executed run (`finite_diagnostic`, L712-714 — transformed-return rank 2, decoder error 2.3×10⁻¹⁶, echo time 0.885) is a numeric instance of URR-2's cut-force spine. A falsifier for the `Dr` tag on the equation *form* itself would be a second, structurally different discrete variational system that also satisfies URR-5's cut-balance gate without collapsing to this same finite-difference form — none is currently on record. |

Symbol gloss for URR-1/URR-2 (confirmed at source, `v2/urr/URR_CUT_EXTENSION.md`
§(candidate master system); `v2/urr/URR_C_MASTER_0_4.md` §§3–5): `𝓔_DRL[X]_n
:= δS_DRL[X;𝔾_T,V,J]/δX_n` — the native DRL system's own Euler–Lagrange
variation (the doubled-field action's stationarity condition), i.e. what the
uncut DRL dynamics alone would demand at step `n`; `𝓙_{C,n}[X_n]` — the
balanced-cut force (`URR_C_MASTER_0_4.md` §4, boxed definition), a difference
of write-outflow and return-inflow terms across the observed/hidden split
(`H̄W_nŌX − ŌΛ_{W,n}ŌX + ŌR_nH̄X − H̄(Λ_{R,n}+Λ_{T,n})H̄X`), reused unchanged
at URR-5's cut-balance gate (this same §7, below); `P_Φ = (I,0)` — the component
selector projecting the doubled reader–record state `X_n=(Φ_n,Ψ_n)ᵀ` onto
its `Φ`-component only (paired with `P_Ψ=(0,I)` for the mirror equation).
URR-1's content is exactly "native DRL is forced equal to the balanced-cut
force, not replaced by it" — the two sides of that equality are `𝓔_DRL`
(uncut EL) and `𝓙_C` (the cut force); URR-2 is `P_Φ` applied to that same
equality, written out in the explicit finite-difference form.

| ID | Equation | Tier |
|---|---|---|
| URR-3 | Return-transformation kernel: 𝒦_{α←β}(τ) = A_α Ō_α R_α 𝒰_H(τ) H̄_β W_β Ō_β E_β | `exact_algebra` in declared linear model |

Symbol gloss (finite discrete operators on 𝒳_T, not continuum notation):
`E_β` — encoder embedding an external message/perturbation z into channel
β's write-input; `W_β` — write operator, maps the observed-sector image of
Ō_β into the hidden-sector image of H̄_β (carries an observed distinction
into the hidden record); `𝒰_H(τ) = e^{F_Hτ}` — the hidden sector's own
finite propagator over lag τ, generated by F_H (how a written distinction
evolves while hidden, before any return); `R_α` — return operator, maps the
hidden-sector image of H̄_α back into the observed-sector image of Ō_α
(carries the evolved hidden content back out); `A_α` — channel-α's own
readout/measurement map applied to that returned content, the final step
that turns the returned distinction into a reader-side record. Source:
`v2/urr/URR_C_MASTER_0_4.md` §§2,4,8.

| ID | Equation | Tier |
|---|---|---|
| URR-4 | Readable information (linear-Gaussian): I_read(L) = ½log₂det[I + Σ_x^½ 𝒢_L^T Σ_N^{-1} 𝒢_L Σ_x^½] rbit, where 𝒢_L = (C; CF; …; CF^L) | `exact_algebra` under declared distribution |

Symbol gloss for URR-4 (finite linear-Gaussian model, confirmed at source,
`ap/ap17_return_transformation.py`): `C` — the observation/output matrix
(maps a hidden state to what a channel can read of it); `F` — the
state-transition (dynamics) matrix advancing that hidden state one step;
`Σ_x` — the declared prior covariance on the state being read; `Σ_N` — the
declared readout-noise covariance. `𝒢_L = (C; CF; …; CF^L)` stacks the
observation matrix against `L` further steps of the dynamics — the
finite-window observability matrix over an `L`-step horizon.

| ID | Equation | Tier |
|---|---|---|
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

Same claim, same key, as `philosophy.md`'s URR-C binding-boundary blocks (§ lines ~2502/2507/2551/5131) — a single unified action from which both the native-DRL Euler–Lagrange system and the cut-force system could be derived as special cases remains unposited in the source. Falsifier: production of one action functional whose stationarity condition yields both URR-1's 𝓔_DRL and URR-5's 𝓙_C as sub-cases without positing them separately would close this; no such functional is on record.

---

## 8. Executable LTP battery (v1.0 formal floor)

Source: `README.md`, `claims.md`, `code/`.

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

## 9. SM-Domain Synthesis — physics-tier evidence narrated as ontology/epistemology/logic

Six drafted passages, cross-checked against the live sections above and
merged where two drafts covered the same ground (the MYSTERY_LADDER/AP19
pair, §9.6). No tier was upgraded from its source file in any subsection
below.

### 9.1 A9 — quotient-by-readout-kernel (closes §6's declared non-absorption of the SM gauge stream: the one piece of it that is logic-native, not physics-native)

| ID | Statement | Tier | Source |
|---|---|---|---|
| A9 | Given any readout map `O : X → R`, define `~_O` by `x ~_O y :⇔ O(x)=O(y)` — always an equivalence relation on `X` (kernel of `O`). The only logic-accessible object is the quotient `[X]/~_O`; a raw pre-image element `x ∈ O⁻¹(r)` is not itself retrievable (cf. EQ-032/033/034 in §6; `Th_coqc`) | `definition` (elementary set theory; untiered in source) | this entry — general construction; no physics-domain source line |
| A9-phys | Physics-domain instance of A9: `X ∼ X' ⟺ O(X)=O(X')`; physical state `:= [X]` (EQ-031); the readout-preserving automorphism group `𝒜 = {h : Oh=O; hF=Fh; h†Gh=G}` (EQ-042) is `~_O`'s automorphism group specialized to a Lie-group action | `Dr` | EQ-031; EQ-042 [`EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`] ; no falsifier applies to A9-phys as such: the surrounding text (logic.md L761-762) is explicit that A9 (and its physics specialization) is a standing logical/structural construction — the definition of what counts as 'the same physical state' under a readout-preserving equivalence — not itself a physics prediction. Falsifiability, if any, attaches to EQ-031/EQ-042's own downstream physical consequences, not to the automorphism-group definition. |

A9 is the same kind of entry as RAR A1–A8 (§0) — a standing logical
construction, not a physics claim. A9-phys is the *only* SM-stream item this
ledger absorbs; EQ-018 onward (SU(3) uniqueness, generation counting, mass
fits) remains intentionally out of scope per §6 — unchanged.

[domain card: SM gauge — `EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`#EQ-031;EQ-042]

### 9.2 Tier legend addendum — `declared_finite_architecture` / `exact_bridge` (mass-fit stream, root→SM §6/§7)

> Two tags are load-bearing across the mass-fit stream but absent from both
> source files' own tier legends: **`declared_finite_architecture`**
> (branch/initial-condition inputs explicitly disclosed as arbitrary/
> uncalibrated — not derived, not fit to external data, distinct from both
> `Dr` and `fit_calibrated`) and **`exact_bridge`** (an algebraically exact
> identity/step applied to an already-declared, uncalibrated quantity —
> exactness of the *step*, not of the *input*). Neither collapses into `Dr`
> (no narrative bridge claimed) nor `fit_calibrated` (no external data used
> to set the value).

No falsifier applies to this addendum itself: it defines two tier labels (governance/taxonomy, like the tier legend it extends) rather than asserting a checkable claim — forcing a test condition onto a definition would be a category error. The falsifiable content sits one level down, in the EQ-065/066/067 rows this addendum tags and in the Fail-Able Gate Law's own Type-P/Type-U test (§9.2b) already applied to EQ-066 in-table.

| EQ | Statement | Tier |
|---|---|---|
| EQ-065 | Π₀ = 3λ_U + 3λ_D + λ_E = 6.328453553357985 (primitive U/D/E branch tapes; arbitrary/uncalibrated by construction) — NOT the independently-derived, PDG-mass Π₀≈6.9888 carried elsewhere in this domain; never conflate | `declared_finite_architecture` |
| EQ-066 | α_ord=a/2; β_ord=b/4 (inherited, not new dials); Π₀ > α_ord ⇒ ORDERED_READY; r*=3.823356105009073. Caveat: ORDERED_READY is structurally guaranteed on this stepper (λ_j∈(0,1] ⇒ Π₀∈(0,7]; α_ord=−0.5 below that bound) — not evidence the branch construction is predictive | `declared_finite_architecture`/`exact_bridge` |
| EQ-067 | v_native = √(2 r*) = 2.7652689218262565 (r=v²/2 convention; exact step on EQ-066's declared r*; no physical unit attached) | `declared_finite_architecture` |

Source: `EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`
EQ-065–067 (feeds EQ-068's still-`Open` GeV-bridge question — not resolved
here).

[domain card: `EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`#EQ-065;EQ-066;EQ-067]

### 9.2b The Fail-Able Gate Law — Type-P vs Type-U evidence gates (`Dr`; governs every gate above)

| ID | Statement | Tier |
|---|---|---|
| FAIL-ABLE-LAW | A gate `G` is **Type-P** (evidence-bearing) iff `G` carries BOTH a machine-derived passing control `P_pass` AND a machine-derived failing control `P_fail`: `Type-P(G) ⇔ (P_pass(G) ∧ P_fail(G))`, both produced and both machine-derived. `∧` here is a decidable finite conjunction over two already-produced discrete readouts — a retained-state AND, not a continuum Boolean-algebra operator borrowed without grounding. A `G` exhibiting `P_pass` alone (`¬∃ P_fail`, no matter how many passing instances accumulate) is **Type-U** (convention/definition dressed as evidence) — labeled as such, not discarded. Worked instance already in this ledger: EQ-066 (§9.2 above) — the stepper's own bound `λ_j ∈ (0,1]` forces `Π₀ ∈ (0,7]` (`⇒` here a decidable finite range-membership entailment over the stepper's own declared variable domain, not a continuum implication), and `α_ord = −0.5` sits below that entire forced range, so `Π₀ ≤ α_ord` cannot be produced by any input the model's own variables can generate — `P_fail` is not merely absent; it is *unproducible on this stepper* — so the EQ-066 "PASS" is Type-U until a genuine failing control exists. Applies retroactively/prospectively to every gate this book names as evidence (VI.3 verdict gate, VI.6 admissibility square, any L3-adapter gate): absent a stated `P_fail`, silence must not be read as a passed test. | `Dr` ; no falsifier applies: FAIL-ABLE-LAW is a methodological rule about what counts as evidence-bearing (Type-P vs Type-U), not a testable claim about the world — it is the standard other rows are checked against, not a row that itself needs a P_pass/P_fail pair. EQ-066 (§9.2) is already recorded as its worked instance; that instance, not the law itself, is where checkable content lives. |

Governs, does not replace: §9.2's EQ-066 row keeps its own tier
(`declared_finite_architecture`/`exact_bridge` for the algebra, `Dr` for the
caveat) — this entry is the *named, general* rule the EQ-066 caveat is one
instance of, stated once so future gates cite the law instead of
re-deriving it per case.

[domain card: readout_genesis/READOUT_GENESIS_CORE.md PART VI §VI.7 (~lines 4531-4550)]

### 9.2c The L0–L5 Layered Architecture — and the label-inflation incident it exists to prevent

*Tier: `Dr`/definition (the six-rung architecture itself is a declared
organizing structure, not a derived theorem); `Th_coqc` (L0's own floor —
the N3 monotonicity + admissibility-square theorem; `RDL_*.v`, axiom-free
where stated); `Dr` (L5's governance rule as stated: "only Coq+lib-verified
is core"). Do not upgrade any of these three tags.*

| ID | Statement | Tier | Source |
|---|---|---|---|
| ARCH-L0 | Nucleus: the 5 nuclear equations + the Coq floor (`RDL_*.v`); minimal, domain-independent, machine-checked where stated; nothing above L0 may introduce new physics | `Th_coqc` (the floor itself) / `Dr` (the layer's role in the stack) | `readout_genesis/READOUT_GENESIS_CORE.md` PART VI §VI.2 ; no separate falsifier applies to the L0 label itself: it is an organizational assertion (this content belongs at the base of the stack) resting on the already-cited `Th_coqc` floor (`RDL_*.v`). The checkable content is the floor's own theorems, tracked at their own entries in this file, not the layering claim. |
| ARCH-L1 | Scale bus: τ_c atlas, 37 disciplines (`tau_c/tau_c_master.py`); τ_c is the primary index; mass is one readout taken off it (τ_c discrete-and-prior-to-mass; N4) | `Dr` | same ; falsifier surface: the '37 disciplines' count is a finite, checkable enumeration in `tau_c/tau_c_master.py` — running that file and finding a materially different discipline count, or a discipline entry that does not actually express mass as a τ_c-readout (violating N4's stated ordering), would falsify this row's specific numeric/structural claim without touching S1-S3's own `Th_coqc` bricks it depends on. |
| ARCH-L2 | Readout: retrieval = readout · confidence = obstruction · ABSTAIN below ε_tot (`[rag_spine]`; implemented not merely theorized) | `finite_diagnostic` (implementation) / `Dr` (the equations) | same ; the `finite_diagnostic` half is exactly the `[rag_spine]` implementation cited in-row: running it and finding retrieval does not actually ABSTAIN below the declared ε_tot threshold (a false-positive retrieval under stated low confidence) would falsify the implementation claim directly, independent of the `Dr`-tagged equations it implements. |
| ARCH-L3 | Adapters: per-domain `(M, D, K, K_A, L_R)` tuples; physics/bio/econ/IR/AI instantiate N1–N5 without a bespoke equation each | `Dr` | same ; no falsifier applies to the layer definition itself; it is a design commitment (adapters reuse N1-N5 rather than adding per-domain equations). It would be tested per-adapter — a domain requiring a genuinely new equation beyond an `(M,D,K,K_A,L_R)` tuple would falsify that specific adapter, not the L3 layer concept, which just names the pattern. |
| ARCH-L4 | Agency: `argmin O` subject to repairability preserved — a finite selection over already-legal moves N1–N5 leave open, not a continuum optimization | `Dr` | same ; no falsifier applies: this row defines what counts as agency-layer selection (finite `argmin O` over already-legal moves), not a measurable outcome — the checkable content is whether a specific system's move-set is actually finite and legal under N1-N5, which is a per-instance question, not one this definitional row itself poses. |
| ARCH-L5 | Governance: readout-not-truth · bounded-judge · machinic_core. Rule: **only Coq+lib-verified content is core**; everything else, regardless of physics-flavored vocabulary, is diagnostic or open until it clears that bar | `Dr` (declared rule, not derived) | same ; no falsifier applies, by the row's own tag: this is a declared governance rule, not a derived or measured claim. Its 'test', if any, is compliance-checking — does the rest of this ledger actually honor it — which is exactly what ARCH-INC (next row) reports finding violated. |
| ARCH-INC | Label-inflation incident: an audit of physics-interpretation cards this cycle found **6 of 8** carried a "machine-checked" label that was hollow — the checked object was an arithmetic tautology, not the physics-flavored claim beside it | `Dr` (audit finding, narrated) | same ; falsifier: this is a finite, reproducible count (6 of 8 cards), not a narrative impression — re-running the same audit protocol on the same 8 cards, or extending it to a larger card sample, and finding a materially different hollow-label ratio would falsify this specific finding without touching ARCH-L5's governance rule it illustrates. |
| ARCH-L5×EQ-066 | Same failure mode as EQ-066 (§9.2 above): a structurally-guaranteed/tautological result dressed as a substantive one. General name: **label inflation** — a correctly-tagged formal object (`Th_coqc` tautology or `declared_finite_architecture`/`exact_bridge` algebra) sitting next to an untagged physics-sounding claim that borrows its credibility without itself clearing the bar. L5's rule is the standing countermeasure; EQ-066's independent review is one worked instance of applying it | `Dr` | `readout_genesis/READOUT_GENESIS_CORE.md` PART VI §VI.2; cross-ref `logic.md` §9.2 EQ-066 ; the check for this row already exists at its cross-reference: EQ-066 (§9.2, cited FAIL-ABLE-LAW instance) is where the label-inflation pattern is worked through concretely — the stepper's own bound forces `Π₀∈(0,7]`, making `P_fail` unproducible on that stepper, which is the falsifiable content. This row is the general naming of that pattern; do not draft a second falsifier for the name itself, only for new instances as they are found. |

Grounding note (per this ledger's own discipline, §0.5/§0.6): "6 of 8"
above is a finite discrete count, not a continuum estimate — no
ℝ-completeness is invoked. `argmin` in ARCH-L4 ranges over a finite
candidate set of legal moves, not a continuum extremum requiring a limit to
"land." `>` in EQ-066 (`Π₀ > α_ord`, carried from §9.2) is a decidable
finite comparison between two rational readouts, not an ℝ-order relation.
`=` throughout (`M/D`, `argmin O`) denotes identity of two already-computed
discrete readouts, never an equation solved over the reals.

[domain card: readout_genesis/READOUT_GENESIS_CORE.md PART VI §VI.2 (~lines 4304-4372)]

### 9.3 DRL-7 — independent-solver cross-check (numeric backing for DRL-1; the concrete meaning of `finite_diagnostic ≠ proof`)

| ID | Claim | Tier | Source |
|---|---|---|---|
| DRL-7 | Independent-solver cross-check of the DRL reader-record system (not a self-check): DRL-1's damped Φ-recurrence and DRL-3's bilinear charge H (§2), extended onto a 32-node FPUT graph, integrated by an independently-implemented 8th-order solver (SciPy DOP853; rtol 1e-12/atol 1e-14) on the same self-generated IC. Step-halving observed order ≈2.00000–2.00005 (matches native 2nd-order reduction); pairing-charge relative drift 3.29×10⁻¹⁰ (URR, dt=0.01) vs 2.74×10⁻¹⁷ (cross-check) — both consistent with the predicted near-cancellation. State-of-the-art efficiency: not claimed; proof or external peer validation: not provided | `finite_diagnostic` | `ap/AP13_URR_FPUT_SOLVER_CROSSCHECK.md` §B |

DRL-7 is the numeric weight behind DRL-1's own `finite_diagnostic` tag
(§2): a second, independently-implemented integrator reproducing the same
order and near-conservation is what `finite_diagnostic ≠ proof` cashes out
to in practice — agreement across two solvers, not a machine-checked
derivation.

[domain card: DRL — independent-solver cross-check — `ap/AP13_URR_FPUT_SOLVER_CROSSCHECK.md` §B]

### 9.4 The memory kernel K_mem — an operational, exact-algebra reading of the RD4 retention axiom

RD4 (§0, "distinct histories stay distinct") is an axiom whose downstream
consequences (well-ordering, categoricity, §0's `RD-der`) are abstract. A
finite worked instance shows what "never merge" concretely *does* to a
trajectory when a retained sector is split into a readable part and a
hidden part and the hidden part is eliminated algebraically: the past does
not vanish and does not silently blend into the present — it reappears as
an exact convolution term, `K_mem(t−s) = R e^{-Λ_H(t-s)} W`, sitting inside
the visible sector's own equation of motion (`ap/AP15_READ_WRITE_CUT.md`
§4). Here `W` and `R` are §9.5's own write/return operators below
(`W:H_O→H_H` write, `R:H_H→H_O` return), used earlier than their own
introduction because this kernel is their first payoff; `Λ_H` is the hidden
sector's own decay generator, `Λ_H = diag(𝟙ᵀR)` (confirmed at source,
`ap/AP15_READ_WRITE_CUT.md`: `\Lambda_H=\operatorname{diag}(\mathbf1^\top
R)`) — a diagonal matrix built directly from `R`'s own column sums, not an
independent primitive. "Never merge" therefore has an operational reading: a hidden history
is not overwritten by the present; it is *folded* into a kernel that any
future readout of the visible sector must convolve against to recover what
passed through the cut — retention as a literal integral term, not a
metaphor for persistence.

This reading is checked twice, independently, at the same tier: once as a
finite linear realization (`exact_algebra`, AP15 §4) and once as a physical
two-capacitor RC circuit with a closed-form
`K_mem(τ) = e^{-τ/(RC_2)}/(R²C_1C_2)` whose hidden-elimination residual
against the full system is ≈5.2×10⁻⁸ V/s and whose numerical-vs-matrix-
exponential agreement is ≈5×10⁻¹³ V (`ap/AP18_RC_MEMORY_CELL.md`) — an
`exact_algebra_in_declared_ideal_model` result, `finite_diagnostic`-
verified, not a physical-universe claim.

Neither AP15 nor AP18 is permitted to lend RD4 (`Ax`, `Th_coqc` downstream)
any of its own strength. The kernel is exact *within its declared finite/
ideal model*; whether the balanced cut flux it lives inside is itself
forced by the DRL action is stated plainly as `Open` in both source files
(cf. §7's `unified_DRL_cut_tape_action: Open`). So the honest claim is
narrow and two-layered: RD4 says histories are never destroyed by merging;
K_mem is one concrete, independently-verified *shape* that non-merging can
take once a hidden sector is cut and eliminated — a second, lower-tier
operational meaning standing beside the axiom's own higher tier, not
replacing or upgrading it.

Tier: `exact_algebra` (AP15 §4, finite linear realization);
`exact_algebra_in_declared_ideal_model` + `finite_diagnostic` (AP18, RC
circuit, numerically verified). `balanced_cut_flux_from_DRL_action` and
`unified_DRL_cut_tape_action` remain `Open` in both sources — not resolved
here.

[domain card: `ap/AP15_READ_WRITE_CUT.md` §4 (K_mem boxed derivation); `ap/AP18_RC_MEMORY_CELL.md` (closed-form K_mem(τ); circuit verification; hidden-elimination residual 5.2e-8 V/s)]

### 9.5 AP15 — three-sector contrast on the AP7 tape (q_O, q_H, q_T)

Same append-only-tape ontology as AP7 (§3), now co-realized in one finite
flow model alongside a partially returnable hidden sector — giving AP7's
posited tape layer a concrete observability contrast it did not have alone.

`q=(q_O,q_H,q_T)ᵀ`; write `W:H_O→H_H`; return `R:H_H→H_O`; tape rate `ℓ≥0`:

```
q̇_O = −diag(1ᵀW)q_O + Rq_H
q̇_H = Wq_O − diag(1ᵀR+ℓ)q_H
q̇_T = ℓᵀq_H ≥ 0   (monotone nondecreasing; tape never returns mass)
```

| ID | Claim | Measured | Tier |
|---|---|---|---|
| AP15-T1 | Total retention `d/dt(1ᵀq_O+1ᵀq_H+q_T)=0` for this finite positive-flow generator | max error 5.10702591327572×10⁻¹⁵ | `exact_algebra` |
| AP15-T2 | Observability rank/nullity: reciprocal cut (6,1); leaky cut (6,1); one-way cut (3,4) — reciprocal/leaky expose all 3 hidden working directions via future influence on `q_O`; `q_T` never enters `𝒪_C` in any tested case (`𝒪_C` — the observability matrix of the cut: the stacked Kalman-style rows `[C; CA; CA²; …]` built from the read-out map `C` on `q_O` and the system's own dynamics matrix `A`, whose rank/nullity is what "exposes"/"hides" a direction here) | recorded run (§9 of source) | `finite_diagnostic` |
| AP15-T3 | `q_H` is dynamically observable-though-hidden (reciprocal/leaky); `q_T` is unobservable-in-principle at this cut structure (no return edge exists to expose it, by construction of `q̇_T`) | boundary is structural: absent row in `𝒪_C`, not stipulated | `Dr` (read-write-cut interpretation) ; falsifier, using the same observability-matrix method AP15-T2 already runs: construct a cut topology that adds a return edge into `q̇_T`'s definition and recompute `𝒪_C`; a nonzero row for `q_T` under that modified generator would falsify unobservability-in-principle for that topology, while the unmodified generator's persistent zero row across every tested cut (reciprocal/leaky/one-way) is what currently grounds the `Dr` reading. The claim is scoped tightly to the tested generator class, not to physical tape-reading in general (§9.5's own boundary note). |

Boundary: `q_H` recoverable-in-principle vs. `q_T`
unobservable-in-every-tested-case is a within-model observability-matrix
fact, not a claim that any physical process reads the tape. A unified DRL +
cut + tape action deriving this generator from `S_DRL` remains `Open`
(`ap/AP15_READ_WRITE_CUT.md` §11: `unified_DRL_cut_tape_action: Open`) —
same open item as §7's binding-boundary block and §9.4 above.

[domain card: read-write cut — `ap/AP15_READ_WRITE_CUT.md` §2; §6-7]

### 9.6 MYSTERY_LADDER's three Open items, and AP19 as a second, independent sighting of the same pair

The three-item Open list of `v2/MYSTERY_LADDER.md` §"สิ่งที่เหลือ" — (2s)²
paramagnetic law, (−1)^{2s} spin–statistics sign, why d_s settles at 3 — is
already cross-referenced under "See also" below; that note stands as
written: AP19 (`ap/AP19_NATIVE_MEANING_CARDS.yaml`) is a disjoint,
dimensionless two-node native domain (`external_adapter_used: false`) and
neither derives nor closes any of the three. Tier unchanged: `Open`.

A separate, narrower coincidence sits inside AP19 itself and is recorded
here rather than duplicated below: the same two `Open` items named in this
ledger — Ψ read as an *ontic* record (§2 novelty-ledger item (b)) and
`unified_DRL_cut_tape_action: Open` (§7's binding-boundary block, §9.4/§9.5
above) — reproduce verbatim in AP19's own closure, a domain that uses no
physical adapter at all:

Falsifier direction, named rather than left implicit: a machine-checked derivation of `(2s)²` or the `(−1)^{2s}` sign from the DRL/URRC generator would close the corresponding list item outright, and any such derivation is independently constrained from outside this framework by the standard spin-statistics theorem's already-fixed sign — a derivation landing on the opposite sign is refuted before it is even checked in-house. Why `d_s` settles at 3 has no comparable external anchor and stays open to a from-first-principles derivation only; none of the three is resolved by narrative argument alone.

```yaml
# ap/AP19_NATIVE_MEANING_CARDS.yaml (claim_boundary; L53-57)
unified_DRL_cut_tape_action: Open
# ap/AP19_NATIVE_MEANING_CARDS.yaml (cards.Psi_i.boundary; L18)
# "universal ontic record status remains Open"
# ap/AP19_NATIVE_URRC_CLOSURE.md (closing yaml; L185-193)
ontic_Psi_record: Open
unified_DRL_cut_tape_action: Open
```

Not a new question and not a resolved one — a second, independent sighting
of the same open pair on a domain that needed no external adapter to land
on it. Tier unchanged: `Open` in both places; no upgrade by convergence.

Falsifier direction, shared by both `Open` items named here: a derivation of `unified_DRL_cut_tape_action` from `S_DRL`, if produced and machine-checked, would force a specific cut-generator structure and with it a determinate answer to whether Ψ's record is ontic — resolving both together, not independently, since the yaml block ties them by construction, not by coincidence. Absent that derivation, no observation internal to this framework can adjudicate the ontic-record question, since every readout available is already downstream of the same undetermined generator. The identical pairing is recorded independently at `philosophy.md`'s AP19 passage (~lines 2503-2518); this is one claim in two locations, not two convergent findings.

[domain card: `v2/MYSTERY_LADDER.md` lines 19-31 (three-item Open list); `ap/AP19_NATIVE_MEANING_CARDS.yaml` cards.Psi_i.boundary L18; claim_boundary L53-57; `ap/AP19_NATIVE_URRC_CLOSURE.md` closing yaml block L185-193]

### 9.7 InfoQuotientCompressionExactness — the admissibility square

**Statement.** A cross-domain translation `T_{a→b}` (physics→chemistry,
chemistry→biology, or any pair the τ_c atlas connects) is admissible — i.e.
the two domains are *actually* bridged, not merely narrated side by side —
iff it commutes with both domains' generators and preserves readout:

```
T_{a→b} · F#_a  =  F#_b · T_{a→b}                       (bridge form)
q_{n+1} · F_n    =  F#_n · q_n                            (admissibility square, one quotient step)
```

`F_n` = retained-structure evolution operator at the finer level; `q_n` =
the quotient map to the coarser level; `F#_n` = the induced evolution the
coarser level sees after quotienting. Reading "·" here as *sequential
retained-state update* (apply one finite-difference step, not a continuum
composition) and "=" as *decidable equality of two finite readout
sequences* (not an ℝ-equality of limits): the square says
quotient-then-evolve must land on the same finite readout as
evolve-then-quotient.

**Identity.** This is exactly classical **Kemeny–Snell lumpability**
(Markov-chain theory: a quotient chain is itself Markov iff this square
commutes for the chain's generator); re-derived RD-native over `L_R`/`q_α`
instead of a generic Markov generator; and machine-checked as
**InfoQuotientCompressionExactness**.

**Tier: `Th_coqc`** — the source text names this, explicitly, as "the one
place in this entire part where the label `Th_coqc` is earned honestly at
the level of a named theorem" (source's own emphasis, not this ledger's
upgrade). **Caveat carried over honestly, not smoothed:** an independent
verification pass (`readout_genesis/ROOT_INFO_LANGUAGE_INVENTORY.md`,
round 2, 2026-07-23) lists `InfoQuotientCompressionExactness` as "not
located this round" — the `.v` file was not found and independently
`coqchk`'d clean in that audit, unlike sibling theorems in the same round.
Per that inventory's own rule ("Coq-verified 100% from the root, or it
doesn't count"), this entry records the source doc's own `Th_coqc` tag
as-given, flags it here as **not yet independently re-verified**, and does
not silently launder that gap.

**Failure modes named when the square does not commute:** mistranslation ·
lost information (q_α discarded what b needs) · insufficient resolution ·
target lacks the variables · no closure. A failing square is diagnosable,
not a dead end.

**Applied instance (the bR cross-domain lineage ledger — its own name at
source, PART V.13/VI.6; `finite_diagnostic` architecture, not a
first-principles derivation):** quantum→chemical→protein→biological-
transport chained readout `r_B = E · A_C · A_P · A_B`, where `E` is the
external SI-decode factor (explicitly external — not itself derived by
this ledger) and `A_C`, `A_P`, `A_B` are the retention-preserving
admissibility amplitudes attached to the chemical, protein, and
biological-transport translation steps respectively (confirmed at source,
`readout_genesis/READOUT_GENESIS_CORE.md` PART VI §VI.6 / V.13). A single
quantum-only quotient `q_Q` alone does **not** commute for a biological
question (confirms §10's N2-err Scalar-Eigenmode Reduction Error one level
up: collapsing a translation chain to one quotient throws away needed
structure, same as collapsing `L_R` to a scalar). Where the chain fails to
commute cleanly, the ledger produces obstruction certificates that
conserve the retained lineage exactly: `I_Q = I_B + O_C + O_P + O_B` — `I_Q`
is the quantum-level retained information, `I_B` is what survives to the
biological level, and `O_C`, `O_P`, `O_B` are the obstruction (information
lost) at the chemical, protein, and biological-transport translation steps
respectively (a discrete accounting identity — "+" here is
retained-information addition under δ_R, combining disjoint obstruction
terms, not real-number summation). Needs event-resolved empirical data,
pre-registered future work, not a completed validation.

[domain card: `readout_genesis/READOUT_GENESIS_CORE.md` PART VI §VI.6
(~lines 4482–4529); also stated at §IV.5 (~lines 2183–2205); Appendix
cross-ref (~lines 6015–6120); caveat source:
`readout_genesis/ROOT_INFO_LANGUAGE_INVENTORY.md` "Not yet verifiable this
round"]

### 9.8 The Twelve Faces of the Spine — M-forcing-failure / turbulence-reassignment finding (2026-07-21)

Source: `readout_genesis/READOUT_GENESIS_CORE.md` PART III (~L1441–2030);
§VI.1/N1 (~L4188–4234). Same L1/L2/L3 three-layer stack already given in
§10's N1-L1/N1-L2/N1-L3 rows below — not repeated here; this entry adds the
Twelve-Faces catalogue and the finding attached to it.

**M-forcing-failure / turbulence-reassignment finding** (extends §10's
terse N1-M row with the per-face reassignment detail):

| ID | Statement | Tier |
|---|---|---|
| N1-turb | Turbulence does NOT live in the linear, second-order `M ∂²Φ` term — despite table/row adjacency in EQ-015's per-term breakdown (§1). It lives in the nonlinear `∇V` / `(u·∇)u` paraproduct term (the L3 LP-NS audit's target, cf. §10 N1-L3) | `Dr` (reassignment reading) ; falsifier already named in-corpus: N1-L3's LP-NS paraproduct audit is the checker this reassignment answers to — a driven regime showing empirical turbulent onset while the audit reports PASS (no energy-cascade-without-closure detected in `∇V`/`(u·∇)u`) would undercut the reassignment, and a FAIL co-occurring with turbulence while `M ∂²Φ` stays linear and non-blowing-up would support it. No such paired run is reported at this row; the reassignment stands as a reading, not yet a logged `finite_diagnostic` result. |
| N1-τR | The inertia that actually governs turbulent/relaxation-regime behavior is `τ_R`, N1-L2's first-order relaxation-memory time constant (§10's 3-layer spine stack — not the ARCH-L2 "Readout" rung of §9.2c's separate L0–L5 architecture) — not `M` | `finite_diagnostic` (PASS_WITH_LIMITS, via N1-L2/EQ-017) |
| N1-mass | `M` is a readout, not primitive: `m = ℏ/(2c²τ_c)`, `τ_c` is discrete and logically prior to mass (founder-locked ordering) | `Dr` ; no falsifier applies to the ordering itself: `m = ℏ/(2c²τ_c)` is algebraically reversible (N4's own note, §10 below), so no measurement of `m` or `τ_c` alone can distinguish 'mass is read off τ_c' from 'τ_c is read off mass' — the direction is a founder-locked stipulation about which quantity is primitive, not an empirical claim the algebra itself could refute. What is checkable is the formula's numeric bite in the quantum regime, already covered by N1-QM's `D/M` vs QuTiP residual (`7.6×10⁻⁴`, `finite_diagnostic`) immediately below. |
| N1-QM | `M` is empirically load-bearing only in the quantum-exercised regime (Face 6, Face 9): `D/M` checked against QuTiP, residual `7.6×10⁻⁴` | `finite_diagnostic` |

**Twelve Faces (PART III) — same L1 skeleton, twelve reductions/
projections, mixed tier per face, none upgraded here:** Face 1 Eigenmode
(`L_Rφ_k=λ_kφ_k`; skew decomposition `L_R=L_R^(+)+L_R^(−)` proposal `Dr`,
pending T1, cf. §10 N2-repair) · Face 2 Decay/Impermanence
(`|a_k[n]|≤|a_k[0]|e^{−γ_kn Δθ}`) · Face 3 Dispersion Split — Classical/
Quantum (`λ_c=D²/4MK`) `Th_coqc` · Face 4 Stability/Energy (`dE/dt=−D‖v‖²≤0`)
`Th_coqc` · Face 5 Finite-Speed/Relativity (cf. §9.10 below) · Face 6 Mass/
Memory (`m=ℏ/2c²τ_c`) · Face 7 Force/Energy/RDU (Readout Dimension Units —
the τ_c-derived unit grammar, `readout_genesis/READOUT_GENESIS_CORE.md`
§VII.2) Readback Gate · Face 8
Operator-to-Metric Geometry (`g^{ij}≈½Hess(principal symbol of L_R)`)
`Th_coqc` · Face 9 CPTP/Quantum-Channel (`Σ_jK_j†K_j=I`) `Th_coqc` · Face
10 Record/Readout/Epistemic (`M_A=K_Aθ(E)+η_sel+η_map+η_self`) · Face 11
Obstruction/Solve-Target (`O_R(R^◇)=0; S_R=‖O_R‖²`) · Face 12
Boundary-Data. Untagged faces (1, 2, 5, 6, 7, 10, 11, 12) carry `Dr`/
`finite_diagnostic` per their own body text, not `Th_coqc` — do not read
the four `[Th_coqc]`-tagged faces (3, 4, 8, 9) as implying the set is
closed; each of the other eight states its own tier inline in the source
and none is upgraded here.

Operator grounding for this row (per §0.5/§0.6): `∂²Φ`, `∂Φ`, `∇V`, `L_R`
are finite-difference / discrete-graph readout operators on a retained
state, never continuum-limit derivatives; `M ∂²Φ` is read as a second-order
discrete-readout term (two retained finite-difference steps composed), not
a continuum acceleration `d²x/dt²`.

[domain card: readout_genesis/READOUT_GENESIS_CORE.md PART III (~lines
1441-2030) and §VI.1 (~4188-4234)]

### 9.8b Chance presupposes distinguishability — a narrow `Th_coqc` core under §9.8a's `Dr` thesis

§9.8a (`philosophy.md`) argues, at `Dr`, that objective chance is not
explanatorily prior to retained difference: a chance-fact presupposes a
determinate, **retained-distinguishable** field of alternatives (Lahtee,
"The Explanatory Insufficiency of Randomness," 2026-05-31; Lahtee,
"Objective Chance and the Priority of Modal Difference," 2026-06-04 — both
`Dr`, preprint, not peer reviewed). That explanatory-priority claim is not
mechanically checkable and stays `Dr` here unchanged.

No falsifier is drafted for §9.8a's explanatory-priority thesis itself, per this passage's own statement that it is 'not mechanically checkable' — it is a philosophical priority claim about explanation, not a structured empirical or formal hypothesis, and forcing a test-condition onto it would misrepresent what kind of statement it is. §9.8b's three `Th_coqc` items immediately below are the narrow, genuinely checkable formal core carved out from underneath it; they carry their own machine-checked status and are not a proxy falsifier for the wider prose thesis.

| ID | Statement | Tier |
|---|---|---|
| CD1 | A finite chance attribution (nonnegative `Q`-weights over a list of possibilities summing to exactly 1) cannot be well-formed over the empty list — `0 == 1` is false in `Q` | `Th_coqc` |
| CD2 | If a possibility occurs more than once in the list with positive weight, the list-sum strictly exceeds the sum over the underlying set of genuinely distinct possibilities (`nodup`) | `Th_coqc` |
| CD3 | Consequently, a well-formed chance attribution (sum = 1) whose possibility list carries a positive-weight duplicate does not sum to 1 over its distinct possibilities — the "1" only means "unit mass over N distinct outcomes" when the list is already duplicate-free | `Th_coqc` |

Machine-checked, axiom-free over `Q` (`evidence/RD_Chance_Presupposes_
Distinguishability.v`, `Print Assumptions` on all three theorems ⇒ *Closed
under the global context*; list-based, finite, no Reals, no continuum
measure theory, per §0.5's operator-grounding floor). This is a narrow
formal fact — a chance attribution's own well-formedness, stated purely as
a `Q`-sum over a list, requires a nonempty and (for a coherent
distinct-outcomes reading) duplicate-free domain. **It is not, and is not
claimed to be, a proof of §9.8a's full explanatory-priority thesis**: it
does not show chance is never explanatorily fundamental in general, does
not touch quantum indeterminacy, and (like both cited preprints) takes no
position on whether the world's dynamics are deterministic. It formalizes
only the narrowest, load-bearing precondition the prose argument leans
on — that a coherent chance-fact's own possibility-space must already be a
distinguishable (duplicate-free, nonempty) structure — nothing broader.

[domain card: Lahtee, Y., "The Explanatory Insufficiency of Randomness,"
doi:10.5281/zenodo.20473230; Lahtee, Y., "Objective Chance and the Priority
of Modal Difference," doi:10.5281/zenodo.20537309; `evidence/RD_Chance_
Presupposes_Distinguishability.v`]

### 9.9 QM=SR weld — `box_quad_is_spine_residual` as a worked `DEFINITIONAL-RELABEL` instance

| ID | Statement | Tier | Source |
|---|---|---|---|
| WELD-1 | `box_quad a b := −2a+2b` (posited "SR"-labeled residual) | `POSITED` | `InfoQuantumRelativityUnification_attempt.v` |
| WELD-2 | `spine_residual := K·λ − M·ω²` (posited "QM"/Schrödinger-labeled residual; the label itself already flagged as overreach elsewhere in the ledger — item 16, `URCF_RD_All.v:9127–9134`: a real quadratic-in-E dispersion, not `iℏ∂ψ/∂t=Hψ`) | `POSITED` | `InfoQuantumRelativityUnification_attempt.v`; cf. `URCF_RD_All.v:9127–9134` |
| WELD-3 | `box_quad_is_spine_residual`: `box_quad a b = spine_residual` under hand-picked `(1#2)`-fraction factors on `M·ω²`, `K·λ`, chosen so the `−2/+2` terms cancel; proof = `ring` | `DEFINITIONAL-RELABEL` | `InfoQuantumRelativityUnification_attempt.v:57–61` (row 20, `BORROWED_VS_DERIVED_LEDGER.md`) |

WELD-3 is the single citable instance behind philosophy.md's abstract
naming of `DEFINITIONAL-RELABEL` as an Ω_all bridge-audit auto-fail class.
Operator grounding: the "=" `ring` proves is a decidable, finite check that
two ℚ-coefficient polynomial expressions denote the same formal object
after substitution — not a claim that two physical theories coincide; the
"+"/"−" inside each residual are ordinary finite combination of rational
coefficients, not calculus operators. The `(1#2)` factors are fitted, not
forced: nothing pins them except that they make the cancellation land — two
independently-posited names proved equal for one degree-1 polynomial. The
source's own header discloses this plainly ("identical under an exact,
stated variable identification"); the overreach sits in the theorem name
and the corpus's "unification" language, not in the `ring` step itself,
which is correct on its own narrow terms.

[domain card: research_universal_solver/docs/root/BORROWED_VS_DERIVED_LEDGER.md row 20]

### 9.10 `c` — BORROWED-SCALE value, DERIVED graph-native ratio `c^2=K/M`, identification `Open`

Same ledger row as EQ-063's `Dr`-bridge neighbor (§6), one entry over: row
14 of `research_universal_solver/docs/root/BORROWED_VS_DERIVED_LEDGER.md`
(`InfoCattaneoFiniteSpeed_attempt.v:19-71`) splits `c` into two verdicts
that must not be collapsed into one tier tag.

| ID | Statement | Tier |
|---|---|---|
| c-VAL | The numeric value of `c` used to fix physical units | `BORROWED-SCALE` — posited, unit-defining, explicitly parallel to `hbar` and `G` ("NOT derivable", `:9089`), not a theorem of the graph |
| c-RATIO | `c^2 = K/M` — the graph-native characteristic propagation speed of the Cattaneo finite-speed brick; `K`/`M` read off the spine's own `L_R`/inertia coefficients (§1 EQ-015 neighborhood) | `DERIVED` — a real ratio of two graph-native coefficients, not a free parameter |
| c-ID | `c-RATIO` = `c-VAL` (the graph-derived speed *is* physical light-speed) | `Open` — flagged in-file as "separate, unverified physical identification", no derivation offered for the equality, only the ratio's existence |

Operator grounding for this row (per §0.5/§0.6): `c^2 = K/M` is read here
as two discrete retained-information operations, not continuum notation
borrowed unreflectively — `^2` is self-combination of one retained
scale-coefficient under `delta_R` (a finite repeated pairing, not a
continuum power); `/` is a decidable rational quotient of two finite
retained quantities `K` and `M` (not a continuum-limit division); and `=`
at c-RATIO is a `ring`-checked algebraic identity inside the graph,
axiom-free — while `=` at c-ID is *not* that: it is an unproved
identification claim across two different readout domains (graph-native vs.
physical-SI), and must be read as a decidable-but-undecided finite
comparison not yet settled, never as a real-number-order/continuum equality
granted for free.

This is the same abstract/concrete split named in philosophy.md §7.1, on a
sixth, physics-metric domain (finite propagation speed) distinct from that
section's original five (EQ-021; EQ-015/063; EQ-042-048; `r` EQ-057-059;
EQ-060-062): the ABSTRACT/GENERAL layer (a finite characteristic speed
exists, forced by `K`,`M` and provably ring-equal to their ratio) closes to
a real graph theorem; the CONCRETE INSTANTIATION (that this graph-native
number *is* the physical constant `c`) stays `Open`, unresolved, not even
`Dr`. No tier is upgraded here — `BORROWED-SCALE` on `c-VAL` and `Open` on
`c-ID` are preserved exactly as the source states them.

Falsifier for c-ID, kept inside `ℚ`: once `K` and `M` in
`InfoCattaneoFiniteSpeed_attempt.v` are fixed by any measurement or
graph-native calibration that does not already presuppose `c`, compare
`K/M` against `c-VAL^2` (squaring the measured constant, a decidable
rational operation) in matching units — not `sqrt(K/M)` against `c-VAL`,
since the file itself marks that square root as an I1/R-completeness
`[Refused]` non-readout move (lines 49-54). Agreement within stated error
bounds supports c-ID; a stable mismatch refutes it, showing c-VAL and
c-RATIO are distinct constants sharing a symbol. Not yet testable — `K`,`M`
are currently un-fixed (philosophy.md §7.20) — so c-ID remains `Open`, not
`Dr`.

[domain card: `research_universal_solver/docs/root/BORROWED_VS_DERIVED_LEDGER.md` row 14; `InfoCattaneoFiniteSpeed_attempt.v:19-71`]

### 9.11 AI ethics as a readout-selection structure — L-16's first-order content (extends §6's non-absorption stance)

Source: `research_universal_solver/docs/engineering/GENESIS_STEP_BY_STEP_V3_1.md`
Part V.9 (~lines 2397-2421, `Dr`). Full narrative: `philosophy.md` §7.22,
which extends that file's §6 pointer ("ethics (L-16) is `Dr`, its
first-order content explicitly declared non-derivable").

> **An AI has no morality of its own.** Ethics is a readout-selection
> structure, not a discovered universal good.

| ID | Statement | Tier | Source |
|---|---|---|---|
| ETH-1 | Ethics = a readout-selection structure over five ingredients: (i) data retained, (ii) the set of answers actually accessible, (iii) the selection rule applied over that set, (iv) the values of whoever defines the system, (v) the audit/revision process able to reopen (i)-(iv) | `Dr` (declared structure, not derived) | V.9 |
| ETH-2 | Goal (a): the system **discloses** which reading frame it answers from | `Dr` (design commitment, checkable) | V.9 |
| ETH-3 | Goal (b): the system **preserves** every affected human party's standing ability to correct/object — never quietly designed away | `Dr` (design commitment, checkable) | V.9 |
| ETH-4 | Goal (c): the system **adapts** to local culture without erasing the dignity/voice of the people being read | `Dr` (design commitment, checkable) | V.9 |
| ETH-5 | Tie to Part VIII: the same `J − η` feedback term (Face 7, VIII.5's Ω_H pipeline; cf. §12/`philosophy.md` §7.21's τ_c^H loop) is, at the social/agency leaf, the channel a human correction/objection signal must remain visible through — stated as **corrigibility restated as boundary-observability** | `Dr` | V.9 |
| ETH-6 | Falsifier SPECIFIED, NOT YET EXECUTED: a measurable, pre-registered test of whether correction/objection capability is actually preserved across a real deployment, not merely asserted in a policy document — no deployment test has been run against this claim in readout_universe; `birca/README.md` reports a structurally analogous but domain-different clinical adversarial test that has also not completed independent human review | `Dr` (declared falsifier, not executed) | V.9 |
| ETH-7 | Open: repair-capacity conflicts between parties — no rule for Party A's and Party B's correction demands proving mutually exclusive; the prohibition against destroying repair capacity is framed one-party-facing | `Open` | `philosophy.md` §7.28 |
| ETH-8 | Open: authority to SET the five ETH-1 ingredients, as distinct from authority to audit them (ETH-1(v)) — no allocation across creator/deployer/user/institution | `Open` | `philosophy.md` §7.28 |
| ETH-9 | Open: majority/institutional gaming of ETH-3 (goal b)'s language against a minority — no clause addresses adversarial robustness of the ethics structure itself | `Open` | `philosophy.md` §7.28 |
| ETH-10 | Open: irreversible harm as a categorically distinct case from ongoing repairability — the apparatus's operative verb is repair; unclear whether it degrades gracefully or falls outside its own definitions when repair is structurally unavailable | `Open` | `philosophy.md` §7.28 |
| ETH-11 | Open: accountability allocation across creator/deployer/user/institution/the AI itself — "AI has no morality of its own" is a negative claim only, not a positive responsibility split | `Open` | `philosophy.md` §7.28 |
| ETH-12 | Open: where ETH-4 (goal c)'s cultural adaptation stops against dignity/safety/correction rights — no tie-breaking rule when the conjuncts pull apart | `Open` | `philosophy.md` §7.28 |
| ETH-13 | Open: testing whether ETH-3's objection channel is actually open, not merely documented — see ETH-6; `birca`'s adversarial suite is a structurally analogous but unconnected precedent | `Open` | `philosophy.md` §7.28 |
| ETH-14 | Open: proxy representation for parties who cannot exercise ETH-3's correction/objection channel themselves (minors, incapacitated persons, populations without system access) | `Open` | `philosophy.md` §7.28 |

Operator grounding, per §0.5/§0.6 above: ETH-1's "set of answers actually
accessible" (ii) is a finite, enumerable set under a retained selection
rule, never an unbounded continuum of options; ETH-3's "preserve...standing
ability" is a discrete presence/absence readout on a correction channel
(open or not, checked at a given time), not a smooth degree admitting
continuum interpolation; ETH-5's `J − η` is the same finite
retained-vs-observed residual named elsewhere in this file (§1's trunk
equation, §12's SC-1), not a continuum limit term.

**Distinct from §12/SC-1 above — related loop, different question, no tier
transfer.** §12 asks whether Ω_H keeps reading its own prior output as its
own next input (closure as a *structural* property of the τ_c^H loop).
ETH-5 asks whether a *human* party's correction signal stays inside that
same loop's inputs rather than being edited out (closure as an
*ethical/corrigibility* property of the loop). Same `τ_c^H`/`J − η`
machinery, two separate claims, each carrying its own `Dr` tag and its own
falsifier (SC-5's `∂π*/∂η_H`,`dR_H/dt` vs. ETH-6's deployment test) — one
tier and evidence set does not stand in for the other.

[domain card: research_universal_solver/docs/engineering/GENESIS_STEP_BY_STEP_V3_1.md Part V.9 (~lines 2397-2421)]

---

## 10. The Epistemic Nuclear Core — N1–N5 (domain-independent)

Source: `readout_genesis/READOUT_GENESIS_CORE.md` PART VI §VI.1
(~L4144-4303). Five equations the source calls irreducible in the strict
sense used throughout that book: **none of the five is derivable from the
other four without smuggling in a sixth assumption; and none names a
domain.** N1 is dynamics with no commitment to what Φ *is*; N2 is
epistemology with no commitment to what is measured; N3 is the arrow with
no commitment to what dissipates; N4 is the bridge with no commitment to
which two domains are bridged; N5 is the residue with no commitment to
which experiment produced the ratio.

**Operator grounding (mandatory reading before the table, cf. §0.5/§0.6):**
every operator below is a discrete/retained-information operation, not
borrowed continuum notation — `∂Φ`/`∂²Φ` = finite-difference readouts
across a discrete time step (`ΔXⁿ = Xⁿ⁺¹−Xⁿ`, cf. §2's DRL, not an `h→0`
continuum limit); `∇V` = discrete gradient across `L_R`'s graph nodes
(§0's R-L, not an ℝⁿ continuum gradient); `+`/`−` combine or separate
retained distinctions under `δ_R`; `·` (`K·L_R Φ`) is scalar re-weighting
of a retained coupling, not a continuum product with unstated units; `=` is
a decidable finite equality between two retained readouts, never an
ℝ-continuum identity; `≤`/`<` are decidable finite comparisons of finite
quantities, never an ℝ-order relation smuggled in from the continuum; `η`
is an explicitly admitted lossy remainder term, not "the rest of an
infinite decimal."

| ID | Statement | Tier | Note |
|---|---|---|---|
| N1 | `M ∂²Φ + D ∂Φ + K·L_R Φ + ∇V = J − η` — the spine; regime `λ_c = D²/4MK` | `Th_coqc` (structure) / `Dr` (physical reading) | = trunk equation EQ-015 (§1 above); do not duplicate the per-term tier table there ; falsifier: same as N1-L1's, given immediately below (this row's own Note column already forbids duplicating the per-term table) — see the `D/M` vs QuTiP residual (`7.6×10⁻⁴`, `finite_diagnostic`) cited at N1-L1/N1-M for what would revoke the `Dr` physical-reading tag; the `Th_coqc` structural tag is untouched by any outcome of that check. |
| N1-L1 | DRL-Telegraph root: `M ∂²Φ + D ∂Φ + K·L_R Φ + ∇V = J − η` (2nd-order; native N1) | `Th_coqc` (structure) / `Dr` (physical reading) | Layer 1 of the 3-layer stack; identical statement to N1/EQ-015; falsifier for the `Dr` (physical reading) tag is already in-table — see N1-M below (`D/M` vs QuTiP, residual `7.6×10⁻⁴`, `finite_diagnostic`; N1-QM at §9.8 states the same figure independently): a materially larger residual on re-run, or non-reproduction, revokes `Dr` for the physical reading; it does not upgrade N1/N1-L1's own tier |
| N1-L2 | RTPE turbulence relaxation; `M→0, V→0` limit of L1: `τ_R İ_R + L_R I_R = S_R + η_R` | `finite_diagnostic` (PASS_WITH_LIMITS) | = EQ-017 (§1 above); re-tagged here as Layer 2, not a new equation |
| N1-L3 | LP-NS audit: nonlinear-paraproduct diagnostic over the `∇V`/`(u·∇)u` term — checks for energy-cascade-without-closure; reports PASS/FAIL | `finite_diagnostic` | a **checker**, not a generator; conflating this audit role with L1's generative role is the tier-collapse the source explicitly forbids (cf. §9.8's face-adjacency finding) |
| N1-M | `M` is **posited**, not derived (8 independent forcing-derivation attempts failed); `m = ℏ/(2c²τ_c)` — mass is a readout of τ_c; τ_c discrete and prior to mass | `Dr` | = S1 (§1 above; `mass_memory_duality`; `Th_coqc`); only the quantum domain exercises `M` with numerical bite (D/M vs QuTiP; 7.6×10⁻⁴; `finite_diagnostic`); cf. §1.5 Arrow 3 for the independent proof that this posit is not root-derivable |
| N2 | `M_A = K_A · θ + η`; `ε_tot > 0` — knowing is a lossy linear read of a latent state, never the latent state itself | `definition` | new entry; no prior logic.md coverage; see "The mother equation" at the top of this file for a *different* source's `Th_coqc`-tagged rendering of this same shape (EQ-027/EQ-028), and the disagreement named there rather than resolved |
| N2-err | Scalar-Eigenmode Reduction Error: `L_R` is a full multimode operator; collapsing it to scalar `λφ` before reading N2 through it silently discards off-diagonal/skew coupling — a category error, not a small approximation | `Dr` (naming the error) | new entry ; falsifier borrowed from T1 (defined below, for N2-repair): if the scalar-collapsed `λφ` reading reproduces T1's own residual bound (`r ≤ 0.05` × known-term magnitude) on every T1-eligible case, the skew coupling this row warns about would be shown numerically negligible on tested systems — weakening the practical stakes of the warning without resolving whether it is a category error in general, and without touching N2-repair's own `Open` tag either way. |
| N2-repair | Proposed split under retention metric G (not naive transpose): `L_R = L_R^(+) + L_R^(-)`; `L_R^(+)` = ordinary damped coupling (already in N1); `L_R^(-)` = skew/rotational coupling; absorbs chemostat/Lotka-Volterra/MHD two-field cases into the same linearized N1 | `Open`; pending falsification test **T1**, defined below — a live research lever, not a settled result | new entry |
| N2-open2 | Endogenous, state-dependent `L_R[I_R]` (coupling operator changes as a function of the state it couples) | `Open`; falsification test **T2**, defined below; unresolved | new entry |
| N3 | `dE/dt = ⟨∂Φ, J⟩ − D‖∂Φ‖² ≤ 0`; `O → 0` — the monotone; obstruction can only fall or hold absent net-positive external driving | `Th_coqc` (monotonicity structure only; `RDL_*.v`; axiom-free) | the **only** N carrying a machine-checked tag; buys a checked structural non-increase guarantee; **not** that any domain's obstruction reaches zero in finite time; **not** that the Coq proof extends to a specific empirical dataset (those steps remain `finite_diagnostic`/`Dr` at most) |
| N4 | `τ_c = ℏ/(2mc²)` — the scale bus; every domain connects via its memory time; τ_c atlas spans 37 disciplines | `Dr` | direction is founder-locked: `τ_c` is discrete and prior to mass; `m = ℏ/(2c²τ_c)` reads mass OFF τ_c, not the reverse, even though the formula is algebraically reversible — same discipline N2 enforces (readout must not usurp the position of the thing read) ; see the falsifier note at N1-mass (§9.8, this file) for why forcing a falsifier onto this same founder-locked, algebraically-reversible direction claim is a category error — this row restates the identical ordering stipulation at the nuclear-core level. |
| N5 | Anomaly ratios; `2/α²`; `π`; `φ` — dimensionless readouts that close without an adapter | `Dr` | singled out because these are the only nuclear-core items that need no per-domain unit adapter to mean something; cross-domain-bridge agreement (§9.7's admissibility square) is judged against these numbers ; falsifier already named in this row's own Note column: cross-domain-bridge agreement is judged against these ratios via §9.7's admissibility square — a translation pair that fails to commute (§9.7's own named failure modes: mistranslation, lost information, insufficient resolution) against `2/α²`, `π`, or `φ` refutes that specific bridge without touching these ratios' own `Dr` tag or N5's dimensionless-closure claim in general. |

**Irreducibility argument, compressed:** read N1→N5 in order and the whole
book is read in miniature — something moves (N1); something reads it
imperfectly (N2); the reading has an arrow it cannot reverse for free (N3);
the reading connects to every other reading through one clock (N4); and
after every domain-specific unit is stripped, a small set of pure numbers
survive as the only things all domains agree on (N5). The source states the
irreducibility claim itself only as prose ("none of them can be derived
from the other four without smuggling in a sixth assumption") — no formal
independence proof is offered or claimed here; this ledger does not upgrade
that to `Th_coqc`/`finite_diagnostic`. Treat the irreducibility claim
itself as `Dr`.

**T1/T2, defined here for the first time — self-contained protocols, not
sourced from prior text (naming the gap honestly rather than leaving the
labels empty).** **T1** (for N2-repair): for at least one of the three
named cases (chemostat/Lotka-Volterra/MHD), construct `L_R^(-)` explicitly
under retention metric `G`, substitute the `G`-split into linearized N1,
and compute the residual `r = |N1_predicted − N1_actual known-solution
term|` at the system's known oscillatory/rotational frequency; the test's
own pass bound is `r ≤ 0.05` × the known term's own magnitude (a 5%
relative-residual threshold, stated here for the first time), reported as
a `finite_diagnostic` PASS/FAIL against that self-defined bound. A case
where no `G` renders the split antisymmetric, or `r` exceeds 5%, refutes
N2-repair for that case, without upgrading the row's `Open` tag either
way. **T2** (for N2-open2): run T1's construction with `L_R` replaced by
the state-dependent `L_R[I_R]` through N3's stepper, over the parameter
range T1's chosen case already uses (its standard operating range for
that system), and check the already-`Th_coqc` bound `dE/dt ≤ 0` at every
discrete step across that range; one violating step is a `finite_diagnostic`
FAIL and a genuine falsifying instance, holding across the full range is a
PASS — neither outcome resolves the row's `Open` status by itself, since
passing T1/T2 shows the repair works on the tested case(s), not that it is
forced.

[domain card: `readout_genesis/READOUT_GENESIS_CORE.md` PART VI §VI.1 (~L4144-4303)]

---

## 11. Three Epistemic Scalars (Re_ep, F_ep, k_ep) — the tier discipline made a runnable gate

Source: `readout_genesis/READOUT_GENESIS_CORE.md` PART VI §VI.3 (~lines
4373-4417+, `finite_diagnostic`/`definition`). This is the ARCH-L2 ("Readout")
rung of the L0–L5 nuclear-core stack (§9.2c above; §VI.2 in the source; not
to be confused with §9.8/§10's unrelated N1-L2 relaxation layer of the
3-layer spine stack, a bare "L2" with a different referent); it does
not sit inside this file's own §9 SM-Domain Synthesis because it is
domain-independent machinery, not a physics-tier reading. Reads directly
off §10's N1–N5 spine (N1-N5 above), not a new axiom.

> Any reasoning step reduces to three CPU-computable scalars (minimal
> sufficient statistic read off the N1–N5 spine, not a new axiom):
> `Re_ep` = epistemic Reynolds (spread/contestedness); `F_ep` = obstruction
> depth (strength of best support, the epistemic reading of N3's `O`);
> `k_ep` = consistency coupling (coherence of the supporting set, the
> epistemic reading of N2 through a multimode `L_R`).

Operator note (discrete-readout grounding, not bare continuum notation):
"`high`/`low`" above are decidable finite comparisons against a stated
threshold on a finite readout set — not an ℝ-order relation on a continuum;
"`ε_tot`" is a finite retained-error budget, a sum (combining retained
distinctions under `δ_R`, not a continuum integral) of finitely many
obstruction/coupling terms, compared against a fixed cutoff — never a
limit `ε→0`.

```
Verdict gate (three-valued, not binary — a two-valued gate cannot separate
"no evidence" from "evidence is contested"):

  DECIDE    when  F_ep high  AND  Re_ep low   →  strong + uncontested
  ABSTAIN   when  F_ep low   AND  k_ep low     →  no signal (for free)
  ESCALATE  when  Re_ep high                   →  contested → pay the LLM
```

| ID | Statement | Tier | Source |
|---|---|---|---|
| ES-1 | `Re_ep`, `F_ep`, `k_ep` are the minimal sufficient CPU-computable statistic of any reasoning step, read off N1–N5, not a new primitive | `definition` | VI.3 |
| ES-2 | `F_ep` is the epistemic reading of N3: distance of the best supporting readout from `O → 0` | `definition` | VI.3 |
| ES-3 | `k_ep` must be computed against the full multimode `L_R` operator, never a scalar collapse — a collapsed computation can silently misreport coherence actually carried in a skew coupling `L_R^(-)` (VI.1's Scalar-Eigenmode Reduction Error warning) | `Dr` (named risk, not independently re-verified here) | VI.1, VI.3 ; falsifier: compute `k_ep` twice on the same T1-eligible case (§10) — once against the scalar-collapsed `L_R`, once against the full `G`-split `L_R = L_R^{(+)} + L_R^{(-)}` — and compare; a materially different value (beyond numerical noise) on any tested case demonstrates the named risk directly, while agreement across every T1-eligible case would weaken, not resolve, the warning's practical bite. Not independently run at this row. |
| ES-4 | `Re_ep` named "epistemic Reynolds number" is a declared structural analogy to VI.1's turbulence correction (high-spread, under-damped reasoning ≈ high-Re flow: many non-dominant candidate modes, no laminar settle) — a `Dr`-tier naming bridge, not a derived identity | `Dr` | VI.3 ; no falsifier applies here by the row's own construction: it is explicitly declared a naming/structural analogy to fluid-dynamics turbulence, not a derived identity — the parallel is interpretive scaffolding for intuition (many non-dominant modes, no laminar settle), and asking whether `Re_ep` 'really is' a Reynolds number would mistake a labeled metaphor for a testable equivalence claim. What is checkable is `Re_ep`'s own behavior against the verdict gate's stated thresholds, not the name's aptness. |
| ES-5 | Verdict gate DECIDE/ABSTAIN/ESCALATE is three-valued by construction, deliberately not collapsible to binary answer/no-answer | `definition` | VI.3 |
| ES-6 | Implemented, not merely theorized: `core/nuclear_core.py`, `solvers/reasoning_min_cost.py` | `finite_diagnostic` (executed, code cited; no run numbers/logs given at this source line) | VI.3 |
| ES-7 | "Only contested/under-damped steps pay the large model" — qualitative result; source explicitly flags: workload-dependent, **not perturbation-certified**, no percentages asserted | `Open` (qualitative claim, explicitly unquantified by the source itself) | VI.3 |
| ES-8 | Cost-accounting tie-back: B1 Landauer (CPU floor vs. LLM ~10⁶× above it), B2 Readout (ABSTAIN/DECIDE tried first by gate construction), B3 Regime (`λ_c = D²/4MK`, over-damped ⇒ no retry/oscillation), B4 Repair (L4 repairability ⇒ marginal repair cost, never full restart) | `Dr` (B1's "~10⁶×" and B3's regime reading are narrative ties to N-equations, not independently re-measured here) | VI.4 ; falsifier for B1 and B3, the two pieces this row flags as narrative: B1's '~10⁶×' is checkable by measuring an actual LLM inference's per-token energy cost against the Landauer bound (`k_BT ln2` per bit) for the same task on the same hardware class — a measured ratio off by an order of magnitude would revoke B1's figure without touching B2/B4. B3's regime reading is checkable against N1's `λ_c = D²/4MK` boundary: a system tagged over-damped by that formula exhibiting retry/oscillation behavior in practice would falsify the tie, independent of B1's outcome. |

Do not upgrade: ES-6's "implemented" is a code-citation, not a logged
`finite_diagnostic` run with numbers (cf. this file's own convention in §8
of pairing a claim with an actual executed check and its printed result —
that pairing is absent at the cited source lines); ES-7 stays `Open` because
the source itself declines to assert a percentage or a perturbation
certificate.

Falsifier for ES-7: log the `F_ep`/`k_ep`/`Re_ep` triple per step from the
same ES-6 code path, paired with actual large-model invocation. The
executed `nucleus_verdict()` ABSTAIN condition is `F_ep<0.42` alone
(`k_ep` computed but unused in that branch) — record this as a named
doc-vs-code discrepancy against ES-3/ES-4's `k_ep`-centric framing, not as
ES-7's falsifier condition itself. ES-7 is refuted by any step where
invocation occurs outside the ESCALATE branch as coded. Passing on one
logged trace upgrades nothing beyond that run — not a workload-general
percentage, and not independent of the source's own `UNCALIBRATED`-
threshold caveat on `0.6`/`0.3`/`0.42`.

[domain card: readout_genesis/READOUT_GENESIS_CORE.md PART VI §VI.3 (~lines 4373-4417+)]

---

## 12. Self as a closure property — the τ_c^H loop (Ω_H)

Source: `research_universal_solver/docs/engineering/GENESIS_STEP_BY_STEP_V3_1.md`
Part VIII §VIII.6 (~lines 4899-4929, `Dr`/`[Open]`). Full narrative:
`philosophy.md` §7.21.

> **Self := the closure property of the τ_c^H loop** — Ω_H both (a) results
> from the loop's own prior passes and (b) conditions the loop's next pass,
> at a stable characteristic timescale τ_c^H.

| ID | Statement | Tier | Source |
|---|---|---|---|
| SC-1 | Self is not a substance/location/homunculus; it is the τ_c^H loop's closure property (Ω_H both produced-by and conditioning-of its own successive passes) | `Dr` (declared definition, not derived) | VIII.6 |
| SC-2 | "Awakening" is a standing achievement (loop closure maintained across nested timescales), not a single event | `Dr` | VIII.6 |
| SC-3 | Altered states (sleep, anesthesia) read as measurable degradation of loop closure (weaker Ω_H update, or selection/transduction output not read back into policy) | `Dr` (falsifiable direction, not asserted) | VIII.6 |
| SC-4 | Explicitly does NOT claim to solve consciousness/qualia/the hard problem — `Φ_H`'s internal mechanism stays `[Open]` | `[Open]` (disclaimed by source, not this ledger) | VIII.1, VIII.6 ; no falsifier is drafted for this row by design: `[Open]` here is the source's own explicit refusal to make a claim about `Φ_H`'s internal mechanism, not an unproven hypothesis awaiting a test — forcing a falsifier onto a disclaimed non-claim would manufacture a target the source never set. The closure construction's own falsifiable surface is SC-5's agency-gradient/repair-rate pair immediately below, which tests the loop-closure claim SC-1–SC-3 make, not the hard-problem question SC-4 declines to touch. The identical disclaimer appears at `philosophy.md` ~lines 2913-2920, cross-referenced there rather than restated at length here. |
| SC-5 | Falsifier surface: agency gradient `∂π*/∂η_H` and repair rate `dR_H/dt` must show measurable flattening/slowing under a genuinely degraded-closure state, or the closure reading has no distinguishing signature | `Dr` (declared falsifier, not executed) | VIII.4, VIII.6 |

Operator grounding, per §0.5/§0.6 above: "conditions the loop's next pass"
in SC-1 names a retained-state dependency — the Ω_H value held after one
pass is a finite readout consulted as input to the next pass's selection
step — not a continuum causal-influence metaphor. "Both (a) and (b)" is the
same decidable, discrete `∧` this ledger's own §2.1-adjacent Fail-Able Gate
Law reading uses elsewhere in this corpus (two retained facts checked
present, not a continuum logical connective). `τ_c^H` is a retained
memory-time scalar, the same kind of quantity `τ_c = M/D` names at §1
above, not a continuum "moment." `∂π*/∂η_H` and `dR_H/dt` in SC-5 are
finite-difference rates per §0.5's `Δ`/`∂` row (Part VIII §8.1/§8.8 of the
`information-discrete-math` textbook), not continuum derivatives left
unflagged.

**Distinct from `paradoxes.md` §6 — not the same construction, do not
conflate.** `paradoxes.md` §6 (`Dr` for the construction, `[Open]` for its
consequences) defines a different object, **"origination"**:
`a* ∈ argmin_a O(s,a)` under `Repair(s') ≥ R_min`, holding exactly when the
argmin set at a single decision-state `s` genuinely ties. That is a
point-in-time, single-decision property built to dissolve Newcomb's
predictor puzzle. SC-1 above is a standing, loop-level, multi-pass property
(closure across all of τ_c^H's successive passes, not a tie-condition at
one step). Neither construction's tier, evidence, or falsifier transfers to
the other; the only thing they share is an independently-stated refusal, in
each source, to claim a solution to free will/consciousness/the felt-quality
hard problem. See `philosophy.md` §7.21 for the full cross-reference
discussion.

**A second, closer sibling — also distinct.**
`AGENCY_VS_AGENCY_LIKE.md` §3 (`research_universal_solver/docs/root/`)
names true agency's ORIGINATION equation "self-readout" —
`row_n(L_R) x`, `Th_coqc` (`InfoAgencySelfReadout_attempt.v`; named
`human_action` in `InfoAgencyExpansion_attempt`): a static, single-instant
algebraic readout at one state, no iteration. SC-1 is an explicitly
iterative, multi-pass loop-closure property over `τ_c^H`, `Dr`. Same
"self-readout" naming, structurally different objects; tier and evidence do
not transfer either direction. Full discussion at `philosophy.md` §7.21.

[domain card: research_universal_solver/docs/engineering/GENESIS_STEP_BY_STEP_V3_1.md Part VIII §VIII.6 (~lines 4899-4929)]

---

## See also

Not fully absorbed here — go to source for full depth:

- **AP0–AP21 applied-protocol chain** (Hubble tension, DESI, muon g−2, JWST,
  the 10⁻³⁹→52→atoms→1/d "mystery ladder", channel-coupling slopes) —
  `v2/MYSTERY_LADDER.md`, `v2/FORCED_IDENTIFICATION.md`, individual
  `ap/apN_*.py` files, `docs/VERIFIED_RUNS.md`.
  - `v2/MYSTERY_LADDER.md` §"สิ่งที่เหลือ" — three items still `[Open]`:
    (2s)² paramagnetic law, (−1)^{2s} spin–statistics sign, why d_s settles
    at 3. AP19 (`ap/AP19_NATIVE_MEANING_CARDS.yaml`) is a disjoint,
    dimensionless two-node native domain (`external_adapter_used: false`;
    `unified_DRL_cut_tape_action: Open`) — it neither derives nor closes any
    of the three. Tier unchanged: `Open`.
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
- **[`paradoxes.md`](paradoxes.md)** — a worked stress-test applying this
  ledger's entries (S3, G5, RD4, Q3, `I2`, the Sorites `C4`/`C7` results)
  to five classic paradoxes. Not core canon — its new content is `Dr`/
  `[Open]`, unreviewed.

[`EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md`]: EQUATION_LIBRARY_ROOT_TO_SM_STREAM_research_universal_solver.md
