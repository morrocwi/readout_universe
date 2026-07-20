# Gate Typing Law — a gate that cannot fail is not a readout

Status: process rule (governance), ratified by the chair 2026-07-20/21. This
is **not** a theorem and is not claimed as one. It does not prove anything
about physics, biology, or this repo's own equations; it is a discipline for
how *any* pass/fail threshold in *any* piece of work (in this repo or any
sibling repo) is allowed to be reported.

This document and its checker have been through four rounds of independent
adversarial review; each round found a real hole, not a cosmetic one, and
each fix (and the finding that forced it) is recorded in the git history of
this branch and in `scripts/test_check_gate_typing.py`'s docstring. Treat
that as a feature, not an embarrassment to hide: a law about gates that must
be able to fail should itself be able to fail review, and it did, four
times, and was fixed each time rather than argued with. Round 4 changed the
LAW ITSELF, not just the checker -- see "The typing rule" below for what
changed and why the one-sided version was incomplete.

**What is human-enforced vs. machine-enforced -- do not conflate the two.**
The *law itself* (the typing rule below, the burden-of-proof rule, "Type U
must never appear in a headline verdict") binds every gate anywhere in this
project's line of work, and enforcing that is a human/reviewer obligation --
the same standing obligation that already makes `docs/AI_READING_GUIDE.md`'s
"no numbers without an executed run" and `docs/VERIFIED_RUNS.md`'s dated-log
requirement binding without a script that scans arbitrary prose for
violations. The *script*, `scripts/check_gate_typing.py`, enforces a single,
narrow, fully mechanical thing: that within one given declarations file,
every record that types itself `P` declares its gate's own pass predicate
exactly once, and that predicate, applied to a recorded NEGATIVE control's
value, derives "does not pass", AND applied to a recorded POSITIVE control's
value, derives "passes". It cannot detect a Type U gate being cited as
evidence in a PR description, a paper, a different repo, or even a different
file in this repo; it cannot judge whether either control is representative
or whether a threshold is well-chosen; and -- named explicitly here, not
just in the Format section below -- it cannot verify that the declared
predicate is the gate's *real* pass condition as opposed to merely
self-consistent with itself. Re-checkable by running the script; everything
the script does not check is still binding, just not machine-checked yet.

## The law

Our own governing principle is **readout-not-truth**
(`main.tex` Part II; `v2/TRANSLATION_PROTOCOL.md`; `v2/POSITION.md` G7
"readout-vs-readout"): a check tells you what a specific instrument, under a
specific policy, reads out -- never what is true. A readout is only
informative if it is a readout *of something* -- if there exists some state
of the world the instrument would have reported differently. An instrument
that reads the same way regardless of the state of the world underneath it
is not reading the world at all; it is reporting its own construction.

Applied to a pass/fail gate, this has one direct consequence:

> **A gate that cannot fail is not a readout. It is a convention.**

If nothing you could plausibly feed the gate would make it fail, then a PASS
carries zero bits about whatever the gate was supposedly testing -- it only
confirms the gate exists and was run. Reporting that PASS as evidence for the
claim under test is exactly the equal-number / non-readout confusion this
book's lens is built to catch elsewhere (`v2/DOCTRINE_OF_QUANTITY.md`; G2 dual
Guard in `v2/POSITION.md`), applied to the meta-level of our own QA gates
instead of to a physics claim.

### The typing rule (current, two-sided form)

Every gate used anywhere in this project's line of work (this repo or a
sibling repo) is typed, and the type is declared *before* the gate's PASS is
cited as evidence:

- **Type P (physical content).** The gate ships WITH **both**:
  - a named NEGATIVE control -- a case chosen (or known) to lack the
    property the gate is supposedly testing for -- whose actual, recorded
    value the gate's own predicate **demonstrably does not pass**, and
  - a named POSITIVE control -- a case chosen (or known) to have that
    property -- whose actual, recorded value the gate's own predicate
    **demonstrably does pass**.

  Only Type P gates may be cited as evidence, counted in an "N/N checks
  passed" summary, or appear in a headline verdict.
- **Type U (unit / convention).** Everything else: a threshold with no
  attached controls, a check that would pass (or fail) on any input in the
  plausible domain, a sanity check that a file exists or a number is
  numeric. Type U gates are not worthless -- they catch typos, missing
  files, and silent crashes -- but they carry **zero discriminating power**
  about the claim under test. They must be labelled `Type U` wherever they
  are reported and must **not** be counted in any "N/N checks passed"
  evidence claim and must **not** appear in a headline verdict.

**Why two-sided, not one-sided (this is a correction to the law itself, not
just to the script -- record it honestly, because that is the point of this
document).** The law as first ruled required only a negative control. That
catches a gate that PASSES EVERYTHING -- the EGFR disease documented in Case
1 below: a 0.35 Jaccard threshold that passed all 10 of 10 available pairs,
including every different-ligand pair, so the "negative" control the
benchmark cited didn't fail either. It does **not** catch the mirror
disease: a gate that FAILS EVERYTHING. A gate with an unsatisfiable or
wildly implausible threshold derives "does not pass" for essentially any
input, including a case that plainly *should* pass by the gate's own stated
purpose -- and a one-sided check, looking only for a failing control, cannot
tell that apart from a genuinely discriminating gate. Demonstrated
concretely, by the chair's own adversarial round against the one-sided
version of this checker:

```
description: score must be >= 0.80 to pass, this control genuinely fails
negative_control_value: 0.95
gate_passes_when: >= 999999
```

`0.95` plainly satisfies the gate's REAL condition (`score >= 0.80`), but
because the declared predicate is effectively unreachable (`>= 999999`), the
one-sided checker derived "does not pass" and certified the record: exit 0,
PASS. Pick any implausible threshold and every record self-certifies -- a
gate that rejects everything is exactly as worthless as evidence as a gate
that accepts everything, and the one-sided law rewarded it. A gate is
evidence only if it can be shown to **discriminate in both directions**;
"has one control that fails" is necessary but was never sufficient, and it
took an adversarial round finding the exact counter-example to see that the
first ruling of this law was half-formed.

The two-sided form closes this **structurally**, not by judging
plausibility (a script cannot know whether `999999` is a reasonable
threshold, and must not pretend to): an unsatisfiable predicate admits **no**
valid positive control (nothing can be recorded that genuinely satisfies
it), so the record cannot be completed at all -- see
`gates/GATE_DECLARATIONS.txt` Counter-Example #2 for exactly how this record
is now rejected, and its own honestly-recorded note on the plausibility gap
that remains even after this fix.

**Burden of proof.** A gate with no attached, demonstrably-discriminating
pair of controls is Type U *by default*. The burden is on whoever wants to
cite the gate as evidence to produce both controls -- never on the reader to
notice their absence. This mirrors the existing rule in
`docs/AI_READING_GUIDE.md` ("no numbers enter a document without an executed
run beside them"): here, no gate enters a headline claim without both a
failing control and a passing control beside it.

This is one further, narrower instance of a pattern this repo already
enforces elsewhere: `v2/POSITION.md` G2 refuses to let a non-readout
(injected zero or infinity) stand in for a readout; `v2/POSITION.md` G9
auto-downgrades a "machine-checked" claim that doesn't actually resolve in
the Coq library. The gate-typing law is the same refusal, aimed at our own
QA thresholds instead of at a physics or logic claim.

## Why this had to be written down: two real failures, same day

Both cases below are our own work, not a hypothetical. They are recorded
here unsparingly, by name, because the chair's ruling was explicit that
softening or anonymizing them would defeat the point: the failure mode is
"we built a gate, it passed, we reported the pass" -- and it happened twice
in one day, in two unrelated domains, which is what forced this to become a
law rather than a one-off fix.

### Case 1 — EGFR C797S benchmark: same-ligand Jaccard gate had zero discriminating power

The benchmark declared a "normal form" gate: for a pair of co-crystal
structures with the *same* bound ligand, the Jaccard similarity of their
contact-residue sets must be `>= 0.35`. The gate was reported PASS at
**0.47** for the tested same-ligand pair, and the pass was cited as evidence
that the structural-comparison method works.

When the chair computed the Jaccard similarity for **all 10 pairwise
combinations** across the available structures -- not just the one
same-ligand pair the gate was built around -- every single pair passed
`>= 0.35`, **including every different-ligand pair**. Worse: one
different-ligand pair, **osimertinib vs. brigatinib, scored 0.70** -- higher
than the 0.47 same-ligand pair the gate was supposedly testing. A gate meant
to detect "same ligand -> similar contacts" could not distinguish same-ligand
from different-ligand pairs at all; every input in the tested domain passed
regardless of the property under test.

The same benchmark carried a second gate in the same family: a "rescue" gate
requiring `>= 5` contact residues for a structure to count. The observed
range across all structures in hand was a **minimum of 10 and a maximum of
19** contact residues. Any ligand with a solved co-crystal structure at all
necessarily clears 5 by a wide margin -- the gate passes because a crystal
structure exists, not because the drug binds the way the claim requires.

Under this law, both gates are **Type U**: no negative control was attached,
and when the chair supplied the closest available thing to one (the full
10-pair matrix, including different-ligand pairs), it did not fail -- it
*passed harder than the case it was meant to validate*. Neither gate should
have been cited as evidence for the benchmark's conclusion. This is not a
claim that the underlying biology is wrong; it is a claim that these two
gates, as built, carried no information about it either way.

### Case 2 — PSII near-vs-far OEC structural-change gate: negative control landed at the same magnitude, opposite sign

A Photosystem II (PSII) analysis reported a structural-change effect size of
**Cohen's d = 0.60** for near-vs-far oxygen-evolving-complex (OEC)
comparisons, and reported that value as evidence of a real structural
difference associated with proximity to the OEC.

A zero-biology negative control -- a comparison constructed to carry no
biological signal by design -- was then run through the identical pipeline
and returned **Cohen's d = -0.40**: nearly the same magnitude as the
reported effect, with the opposite sign. A pipeline that produces an effect
of comparable size out of a control known to contain no real signal is not
demonstrating discriminating power at d = 0.60; it is demonstrating that its
output magnitude is dominated by something other than the effect it claims
to measure (pipeline noise floor, normalization artifact, or similar), and
that a same-magnitude, opposite-sign reading is well within that floor.

Under this law: the d = 0.60 headline gate is **Type U** as reported, because
its own negative control did not fail cleanly -- it produced a comparably
large statistic. If this analysis is revisited, the honest report is either
(a) a control-normalized effect size with the noise floor explicitly
subtracted out and re-tested against a *fresh* negative control, or (b) an
explicit Type U label on the current number with no headline claim attached.

## Format: gate declarations

`gates/GATE_DECLARATIONS.txt` holds this repo's live gate declarations
(currently none -- see that file's header for why, and for the worked
format example built from Case 1 above). It is a plain-text, `#`-comment,
blank-line-separated record format with no YAML/JSON dependency, so the
checker below runs on the same bare interpreter (`numpy`/`scipy`/`sympy`/
`pytest` only) that CI already verifies in `.github/workflows/verify.yml`.

Each record is a block of `key: value` lines:

```
gate: <short stable id, snake_case, used to detect duplicates>
type: P                  # or U -- no other value accepted
description: <one line: what the gate checks and its real pass condition>
negative_control_name: <required for Type P only>
negative_control_value: <required for Type P only -- the actual measured value, a real finite number>
positive_control_name: <required for Type P only>
positive_control_value: <required for Type P only -- the actual measured value, a real finite number>
gate_passes_when: >= 0.35  # required for Type P only -- the GATE's OWN pass predicate,
                            # declared ONCE, as "<operator> <threshold>";
                            # operator one of >= > <= < == !=
```

Type U records need only `gate`, `type`, `description`. There is no result
field of any kind on a Type P record -- neither control carries a
caller-supplied verdict. Both verdicts are **derived** by the checker from
`gate_passes_when` applied to each control's value.

**Both controls declare only their value; the gate declares its own
predicate, once.** This is a deliberate design change, and it has been
tightened twice by two different rounds of adversarial review:

- *Round 3* removed a self-declared `gate_operator` on the control (an
  earlier format let the record pick *whichever* operator made its own
  arithmetic read `FAIL`, independent of what the gate's real pass
  condition actually is -- demonstrated with a `>= 0.80` gate and a control
  of `0.95`, which plainly passes the real gate, declaring `gate_operator:
  <=` and passing anyway). Under the current format that specific attack is
  **not expressible**: there is exactly one operator per gate, attached to
  the gate, not the control.
- *Round 4* found that removing the operator-choice freedom was not enough
  on its own: a **one-sided** check (negative control only) is vacuously
  satisfied by an unsatisfiable predicate, because "does not pass" is
  trivially true for almost any value when the threshold is unreachable
  (the exact `0.95` / `>= 999999` counter-example is quoted under "The
  typing rule" above). The fix is the two-control requirement itself: an
  unsatisfiable predicate can no longer self-certify, because it admits no
  value that could honestly be recorded as `positive_control_value`.

See the worked counter-examples in `gates/GATE_DECLARATIONS.txt`: the
literal `0.70` vs `>= 0.35` EGFR record from Case 1 (round-1 finding), the
`0.95` vs `>= 0.80` operator-choice attack (round-3 finding), and the `0.95`
vs `>= 999999` unsatisfiable-predicate attack (round-4 finding, the reason
the law itself now requires two controls) -- all three rejected by the
current checker, all regression-tested in `scripts/test_check_gate_typing.py`.

**Residual, unfixable risks (named explicitly, not folded into "what it does
not do" below -- this is the chair's own required framing, extended for the
round-4 finding).** The two-sided requirement does not make the checker
omniscient. Two separate things remain genuinely unfixable by tooling:

1. The checker verifies that a record is *internally self-consistent* --
   that its own `gate_passes_when`, applied to its own
   `negative_control_value`, derives "does not pass", and applied to its own
   `positive_control_value`, derives "passes". It **cannot** verify that
   `gate_passes_when` itself is the gate's *real* pass condition as stated
   in the gate's own `description` prose. Someone can still write a
   `description` that says one thing and a `gate_passes_when` that says
   another, self-consistently, and the checker will accept it. **A reviewer
   must confirm the declared `gate_passes_when` predicate is the gate's
   actual pass condition.**
2. The checker cannot judge whether either recorded control value is a
   REPRESENTATIVE, plausible measurement rather than a contrived extreme
   chosen only to make the arithmetic pass. `gates/GATE_DECLARATIONS.txt`
   Counter-Example #2 shows this concretely: even after the two-sided fix,
   a `positive_control_value: 1000000` would satisfy an unreachable `>=
   999999` predicate and pass the checker, even though "a score of
   1000000" is not a plausible measurement for anything real. **A reviewer
   must confirm both recorded control values are genuine, plausible cases**
   -- the checker only confirms the arithmetic, never the plausibility.

Neither of these is a gap this tool closes or claims to; both are named
human-review obligations.

## Machine checker

`scripts/check_gate_typing.py` reads a declarations file (default
`gates/GATE_DECLARATIONS.txt`, or a path given as `argv[1]`) and:

- exits **0** and says so explicitly if the file is absent or has zero live
  (non-comment) records -- the honest trivial-pass case, distinct from "all
  gates verified";
- exits **1**, listing every problem found (not just the first), if any
  record declared `type: P` is missing `negative_control_name`,
  `negative_control_value`, `positive_control_name`, `positive_control_value`,
  or `gate_passes_when`; if `gate_passes_when` is not formatted as one
  operator (`>= > <= < == !=`) followed by a finite number; if
  `negative_control_value`, `positive_control_value`, or the threshold
  inside `gate_passes_when` does not parse as a finite number (`"banana"`,
  `"not-a-number"` are rejected as non-numeric; `"nan"` and
  `"inf"`/`"-inf"`/`"infinity"` are separately rejected even though Python's
  `float()` parses them without raising -- a NaN or infinite "recorded
  value" is not a real measurement, and NaN in particular trivially
  satisfies "fails the gate" against almost any operator, which would let a
  fabricated non-value pass as genuine -- found while adversarially testing
  this checker against itself); if **evaluating `gate_passes_when` at
  `negative_control_value` is `True`** -- i.e. the recorded negative control
  arithmetically SATISFIES the gate's own declared predicate; if
  **evaluating `gate_passes_when` at `positive_control_value` is `False`**
  -- i.e. the recorded positive control does NOT satisfy the predicate
  (this is the round-4 fix: an unsatisfiable predicate like `>= 999999`
  fails here because no genuine value can be recorded as a positive
  control for it); if `gate`/`type`/`description` is missing (including a
  field whose only content renders blank: ordinary whitespace, Unicode
  format/control/combining-mark characters (categories Cf, Cc, Mn, Me --
  e.g. U+200B ZERO WIDTH SPACE), or a short list of individually-named
  blank-rendering characters found by review -- the Hangul filler family
  (U+115F, U+1160, U+3164, U+FFA0) and U+2800 BRAILLE PATTERN BLANK (round
  4; "⠀⠀⠀" survived as a "named" control until this was added), all
  stripped before the presence check); if `type` is not exactly `P` or `U`;
  or if a `gate` id repeats after Unicode NFKC-normalization, a homoglyph
  substitution pass applied BEFORE casefold, then casefold
  (`_HOMOGLYPH_TO_ASCII` in the script, listing both upper- and lower-case
  Cyrillic/Greek Latin-lookalike forms explicitly -- applying the table
  only after casefold was a round-2 bug: `casefold('К' U+041A) == 'к'
  U+043A`, a different character absent from a lowercase-only table, so
  the classic uppercase confusable set К М Н Т В silently passed through
  unmapped; verified directly before fixing it, and regression-tested with
  the exact `SOME_KEY_GATE` / `SOME_КEY_GATE` pair; round 4 added three
  more Cyrillic confusables the table still missed: Ѕ U+0405, Ј U+0408, Ӏ
  U+04C0 -- **this table is a running list of gaps found so far, not a
  closed problem**; the finite-table disclaimer covers this, but do not
  read the table's growth as convergence), so `G1`/`g1` and the homoglyph
  pairs the table lists, in either case, both count as the same id;
- exits **0** and prints a `Type P: N / Type U: M` summary, with a reminder
  that Type U gates must not be counted as evidence, if every declared
  Type P record's own predicate, applied to its own negative control,
  derives "does not pass", AND applied to its own positive control,
  derives "passes".

What it does **not** do, by design: it does not evaluate whether either
control is representative, whether the threshold itself is well-chosen, or
whether a control genuinely has/lacks the property under test for reasons
the numbers alone cannot show (e.g. a mislabeled structure). That judgment
is human (or reviewer-AI) work, the same way `docs/VERIFIED_RUNS.md` records
a dated executed run without re-deriving the physics inside it. Nor does it
detect a Type U gate being cited as evidence somewhere the checker never
looks -- a PR description, a paper, a different file.

**Named separately, because these are the sharpest remaining gaps and
folding them into the paragraph above would read as hiding them:**

1. The checker cannot verify that `gate_passes_when` matches the gate's
   *real* pass condition as described in the gate's own `description`
   prose. It only verifies that the record is internally self-consistent.
   A reviewer must independently confirm the declared `gate_passes_when` is
   actually what the gate does; the checker has no way to read intent out
   of prose and does not attempt to.
2. The checker cannot judge whether either control's recorded value is a
   *plausible, genuine* measurement rather than an extreme value chosen
   only to satisfy the arithmetic (see `gates/GATE_DECLARATIONS.txt`
   Counter-Example #2's own worked note on this). A reviewer must confirm
   both control values are real, representative cases.

The checker enforces exactly two things, both mechanical: the paperwork (a
Type P record has every required field, non-empty, and declares its
predicate in exactly one place) and the two-sided arithmetic (the gate's own
predicate, applied to its own negative control, derives "does not pass";
applied to its own positive control, derives "passes"). Everything else the
law requires -- including both residual risks named above -- remains a
human obligation stated in this document, not a property the exit code
certifies.

## CI wiring

`scripts/ci_verify.sh` runs, as its last two steps:

- `scripts/test_check_gate_typing.py` (`5/6`) -- the checker's own
  self-test, driving `scripts/check_gate_typing.py` as a subprocess against
  small fixture records and asserting the exit code (and, where it matters,
  that the right problem is named). **31 assertions**, one per named
  finding across four independent-review rounds, printed and counted at
  runtime (the script prints its own total; do not restate a count here
  without re-running it -- an earlier draft of this document claimed 26,
  then 27, before the actual count was checked against the file). Covers:
  the EGFR-style arithmetic contradiction, the round-3 operator-choice
  attack, the round-4 unsatisfiable-predicate attack (rejected for a
  missing positive control), a positive control that fails its own gate
  (rejected symmetrically), a genuinely two-sided valid record and a bare
  Type U record (both accepted -- the checker isn't just rejecting
  everything), non-numeric and non-finite (`nan`/`inf`) values, duplicate
  ids under ASCII-case, lowercase-homograph, uppercase-Cyrillic-IDN
  (`SOME_KEY_GATE` / `SOME_КEY_GATE`), and round-4's additional Cyrillic
  homoglyphs (Ѕ/Ј/Ӏ) normalization, the widened invisible-character set
  (U+200B, U+3164, U+00A0, and round-4's U+2800 BRAILLE PATTERN BLANK),
  and a missing declarations file. This runs on every CI invocation, not
  just once at authoring time, so a future edit to the checker that
  reintroduces one of these holes fails CI immediately.
- `scripts/check_gate_typing.py gates/GATE_DECLARATIONS.txt` (`6/6`) -- the
  real check against this repo's own declarations file. On the current repo
  state this passes trivially (0 live gates declared) and says so in the CI
  log rather than passing silently -- see `docs/VERIFIED_RUNS.md` for the
  dated executed output.

## What this law does not do

It does not retroactively fix the EGFR or PSII benchmarks -- those live in
other repos/threads and are recorded here only as the motivating cases; any
correction to them is separate follow-up work, not part of this change. It
does not certify any *existing* gate in this repo as Type P or Type U --
none were declared before this law existed, and declaring them retroactively
without doing the actual two-sided control work would repeat the exact
mistake this law exists to stop. It is a process rule that makes the
"gate had no discriminating control in one direction or the other" failure
mode loud and mechanical to check going forward; it is not a proof that any
particular gate, past or future, is or is not measuring what it claims to
measure.

It also does not claim to be finished. This document has been revised four
times because adversarial review kept finding real holes -- a self-declared
result, a self-declared operator, an unsatisfiable predicate, specific
Unicode edge cases -- not because the underlying principle (readout-not-truth
applied to our own gates) changed. Expect a fifth round to find something
this one still misses; that expectation is not a weakness of the law, it is
what the law itself predicts about any gate, including its own.
