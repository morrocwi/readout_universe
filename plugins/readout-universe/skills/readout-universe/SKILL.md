---
name: readout-universe
description: Load before stating ANY claim as settled fact, in ANY domain — not just math/physics. Trigger points include, but are not limited to: before writing the words "proven," "verified," "safe," "confirmed," "settled," or "this works" about a result you have not personally checked; before citing a benchmark, metric, measurement, or test result as though it were the state of the world rather than one finite executed readout; before writing a claim label of "Open," "unresolved," or "hard/paradoxical" without also stating a stance and a falsifier; before repeating a source's own self-description of its rigor (e.g. "machine-checked," "peer-reviewed," "industry-standard") without re-checking it; before letting a narrative interpretation ("this means X is true") sit next to a measured or derived result without marking which one it is; and before finalizing any document, PR, report, or answer that mixes claims of different evidentiary strength without labeling them differently. Gives the six-tier evidence-tagging discipline (Th_coqc / finite_diagnostic / Dr / Open / fit_calibrated / definition) so a claim's stated strength never exceeds what was actually checked, measured, or declared.
---

# Readout Universe — tag every claim with the tier its evidence actually earns

## The one commitment

*Tier of this stance itself: `Dr` — a declared epistemological posture this
skill asks you to adopt, not a proof that it is the correct one.*

There is no truth-behind-the-claim waiting to be read off directly. What you
ever have, when you assert something, is a finite readout — a result
produced by some process (a proof checker, a test run, a benchmark, a human
judgment, a source you are relaying) at some resolution, under some method.
The discipline this skill teaches is: **name which kind of readout you have,
honestly, every time — and never let the label creep stronger than the
evidence that produced it.** A narrative reading does not get to wear a
machine-checked result's badge; a single measured run does not get to wear
"proof"; an unresolved question does not get to sit bare, unmarked, as if it
were simply true or simply false.

This is the operational core of the `readout_universe` repository
(`morrocwi/readout_universe`, MIT-licensed), applied here to claims in *any*
domain — code review, a benchmark result, a user-facing answer, a security
finding, a research note — not only the physics/math content the repository
itself is about.

## The tier legend — six tags, never collapsed into each other

Quoted from the source discipline (`philosophy.md`'s opening front-matter
blockquote, before its numbered sections). `logic.md`'s own tier-legend
blockquote near the top of that file is canonical and wins on any
disagreement — but note it is a *superset* of the six tags below: it also
defines `Ax`, `Th`, and `exact_algebra` (named explicitly in philosophy.md's
own "this is a subset" framing), plus `declared_finite_architecture` and
`exact_bridge` (defined in logic.md itself, not called out by name in
philosophy.md's shorter framing). The six tags here are the ones this skill
actually teaches:

| Tier | Meaning | What it is NOT |
|---|---|---|
| `Th_coqc` | machine-checked, axiom-free (Coq, `Print Assumptions` ⇒ Closed) | not "true"; a formal system closing under stated axioms/scope |
| `finite_diagnostic` | measured / executed numeric run (pytest, assert) | not proof; a single executed instance |
| `Dr` | declared-bridge / human narrative reading | not established fact; an interpretation with a named bridge |
| `Open` | not established | never bare — always paired with a stance and a falsifier |
| `fit_calibrated` | fit to data, not derived | not `Th_coqc`; a calibration, not a first-principles derivation |
| `definition` | declared object/gate — a stipulated/definitional statement, not derived or measured | not `Dr`; a naming/setup move, not a narrative-bridge reading |

Outside this repository's own Coq-proof context, `Th_coqc` will rarely apply
literally — treat it as the general slot for "independently, mechanically
verified, closed, no hidden assumption," and reserve it for cases that
actually meet that bar (a passing formal proof, a fully reproducible
deterministic check with no unstated axiom). For most everyday claims —
code, ops, product, research outside formal proof — the tier doing the real
work day to day is the distinction between `finite_diagnostic` (I ran this
and observed X), `Dr` (I am interpreting/bridging what was observed into a
larger narrative), and `Open` (I don't have evidence either way, here is my
stance and what would change my mind). `fit_calibrated` and `definition` are
narrower, specific slots — reach for them only when they actually fit,
described in their own row above; do not stretch them to stand in for `Dr`
or `Open`.

Two disciplinary rules the source repository states explicitly and that this
skill inherits unchanged:

- **A claim of the strongest tier must actually resolve against a live
  check, not be asserted from memory or reputation.** In the repository's
  own words: a "machine-checked" claim must resolve against the live Coq
  theorem corpus; a miss auto-downgrades `Th_coqc → Dr` (`philosophy.md`
  §2, gate G9). The general form of this rule: if you cannot point at the
  check that produced a strong-tier claim right now, downgrade it until you
  can.
- **`Open` is never bare.** A claim tagged `Open` must carry a stated stance
  (what you currently believe, tentatively) and a falsifier (what
  observation would change that belief) — an unmarked shrug is not an
  honest `Open` tag.

## Pre-write checklist — run before stating any claim

1. **What produced this claim?** A proof/formal check → candidate
   `Th_coqc`. An executed run/measurement/test/benchmark you watched happen
   → candidate `finite_diagnostic`. Your own interpretation or a bridge
   between two things → `Dr`. A stipulated definition or setup move →
   `definition`. A calibration/fit against data → `fit_calibrated`.
   Nothing yet → `Open`, with a stance and a falsifier.
2. **Is the tier this claim is about to be written at actually resolved
   against a live check right now** — or are you relaying what a source
   said, what you remember, or what "should" be true? If the latter, either
   check it now or downgrade the tier and say plainly that you're relaying,
   not verifying.
3. **Are two different-tier claims sitting in the same sentence
   unmarked?** — e.g. a measured number next to an interpretation of what
   it means. Split them and tag each separately; do not let the stronger
   tier's confidence bleed onto the weaker one.
4. **If tagging something `Open`/"unresolved"/"hard"** — have you stated
   both a stance and a falsifier? A bare `Open` is disallowed by this
   discipline.
5. **Would restating this claim to someone else, verbatim, overclaim what
   you actually have?** If yes, weaken the tier or the wording until it
   would not.

## Where the depth lives

This file is a compact operational summary, not the full corpus. For depth,
worked examples, and the philosophical grounding this discipline is built
on:

- `philosophy.md` (repository root) — the narrative why/what-is/how-do-we-know,
  including the tier discipline's rationale (§2), the Fail-Able Gate Law
  (§2.1 — a gate only counts as evidence-bearing if it has shown both a
  passing *and* a correctly-rejected failing control), the operator-grounding
  checklist for contaminated continuum concepts (§2.5), and case studies of
  the discipline catching real overclaims mid-flight (§2, "Case study").
- `logic.md` (repository root) — the canonical tier legend, in an unlabeled
  blockquote near the top of the file (a superset of the six tags above),
  and the full equation/operator ledger showing the discipline applied
  entry-by-entry to concrete claims, each tagged at the source's own stated
  tier, never upgraded.
- Repository: `https://github.com/morrocwi/readout_universe` (MIT license,
  branch `main`). Author: Yaoharee Lahtee (ORCID 0009-0005-3861-0626).
  Publisher: Open Civil Science Initiative. Status at time of writing: v1.0
  book frozen (`main.tex`), v2.0-dev in active development — a repository
  status note, not a tiered claim.

Do not duplicate `philosophy.md` or `logic.md` content here beyond what is
needed to apply the discipline in the moment; when in doubt about an exact
definition, go read the source file rather than paraphrase from memory of
this skill.
