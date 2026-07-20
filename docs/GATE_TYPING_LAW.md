# Gate Typing Law — a gate that cannot fail is not a readout

Status: process rule (governance), ratified by the chair 2026-07-20/21. This
is **not** a theorem and is not claimed as one. It does not prove anything
about physics, biology, or this repo's own equations; it is a discipline for
how *any* pass/fail threshold in *any* piece of work (in this repo or any
sibling repo) is allowed to be reported.

**What is human-enforced vs. machine-enforced -- do not conflate the two.**
The *law itself* (the typing rule below, the burden-of-proof rule, "Type U
must never appear in a headline verdict") binds every gate anywhere in this
project's line of work, and enforcing that is a human/reviewer obligation --
the same standing obligation that already makes `docs/AI_READING_GUIDE.md`'s
"no numbers without an executed run" and `docs/VERIFIED_RUNS.md`'s dated-log
requirement binding without a script that scans arbitrary prose for
violations. The *script*, `scripts/check_gate_typing.py`, enforces a single,
narrow, fully mechanical thing: that within one given declarations file,
every record that types itself `P` carries a negative control whose recorded
numbers actually, arithmetically, fail the gate's own stated threshold. It
cannot detect a Type U gate being cited as evidence in a PR description, a
paper, a different repo, or even a different file in this repo; it cannot
judge whether a chosen negative control is representative or whether a
threshold is well-chosen. Re-checkable by running the script; everything the
script does not check is still binding, just not machine-checked yet.

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

### The typing rule

Every gate used anywhere in this project's line of work (this repo or a
sibling repo) is typed, and the type is declared *before* the gate's PASS is
cited as evidence:

- **Type P (physical content).** The gate ships WITH a named negative
  control -- a case chosen (or known) to lack the property the gate is
  supposedly testing for -- and that negative control's actual, recorded
  value **demonstrably fails** the gate's own threshold. Only Type P gates
  may be cited as evidence, counted in an "N/N checks passed" summary, or
  appear in a headline verdict.
- **Type U (unit / convention).** Everything else: a threshold with no
  attached failing control, a check that would pass on any input in the
  plausible domain, a sanity check that a file exists or a number is
  numeric. Type U gates are not worthless -- they catch typos, missing
  files, and silent crashes -- but they carry **zero discriminating power**
  about the claim under test. They must be labelled `Type U` wherever they
  are reported and must **not** be counted in any "N/N checks passed"
  evidence claim and must **not** appear in a headline verdict.

**Burden of proof.** A gate with no attached failing control is Type U *by
default*. The burden is on whoever wants to cite the gate as evidence to
produce the falsifying control -- never on the reader to notice its absence.
This mirrors the existing rule in `docs/AI_READING_GUIDE.md` ("no numbers
enter a document without an executed run beside them"): here, no gate enters
a headline claim without a failing control beside it.

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
type: P            # or U -- no other value accepted
description: <one line: what the gate checks and its threshold>
negative_control_name: <required for Type P only>
negative_control_value: <required for Type P only -- the actual recorded value, a real number>
gate_operator: >=  # required for Type P only -- one of >= > <= < == != ; the
                   # comparison that DEFINES A PASS of the gate itself
negative_control_threshold: <required for Type P only -- the gate's own threshold, a real number>
negative_control_result: FAIL   # required for Type P only -- literally "FAIL", nothing else accepted
```

Type U records need only `gate`, `type`, `description`.

`gate_operator` + `negative_control_threshold` together state the gate's own
pass condition precisely enough to compute with (e.g. a gate documented as
"Jaccard >= 0.35 passes" declares `gate_operator: >=` and
`negative_control_threshold: 0.35`). The checker does not take
`negative_control_result: FAIL` on faith: it evaluates
`gate_operator(negative_control_value, negative_control_threshold)` and
rejects the record if that evaluates `True` -- i.e. if the "negative"
control would actually pass the gate. See the worked counter-example in
`gates/GATE_DECLARATIONS.txt`, which is the literal `0.70 >= 0.35`
EGFR record from Case 1 below, marked `FAIL` and rejected by the checker
for exactly that contradiction (an earlier version of this checker did not
catch this; `scripts/test_check_gate_typing.py` now regression-tests it).

## Machine checker

`scripts/check_gate_typing.py` reads a declarations file (default
`gates/GATE_DECLARATIONS.txt`, or a path given as `argv[1]`) and:

- exits **0** and says so explicitly if the file is absent or has zero live
  (non-comment) records -- the honest trivial-pass case, distinct from "all
  gates verified";
- exits **1**, listing every problem found (not just the first), if any
  record declared `type: P` is missing `negative_control_name`,
  `negative_control_value`, `gate_operator`, `negative_control_threshold`, or
  `negative_control_result`; if `negative_control_result` is anything other
  than the literal string `FAIL`; if `gate_operator` is not one of
  `>= > <= < == !=`; if `negative_control_value` or
  `negative_control_threshold` does not parse as a finite number
  (`"banana"`, `"not-a-number"` are rejected as non-numeric; `"nan"` and
  `"inf"`/`"-inf"`/`"infinity"` are separately rejected even though
  Python's `float()` parses them without raising -- a NaN or infinite
  "recorded value" is not a real measurement, and NaN in particular
  trivially satisfies "fails the gate" against almost any operator,
  which would let a fabricated non-value pass as genuine -- found while
  adversarially testing this checker against itself); if
  **evaluating `gate_operator(negative_control_value,
  negative_control_threshold)` is `True`** -- i.e. the recorded control
  arithmetically passes the gate despite being labelled `FAIL`; if
  `gate`/`type`/`description` is missing (including a field whose only
  content is a Unicode format character such as U+200B ZERO WIDTH SPACE,
  which is stripped before the presence check); if `type` is not exactly
  `P` or `U`; or if a `gate` id repeats after Unicode NFKC-normalization +
  casefold + a small documented table of common Cyrillic/Greek
  Latin-lookalike substitutions (`_HOMOGLYPH_TO_ASCII` in the script --
  NFKC + casefold alone do NOT catch cross-script homographs, since e.g.
  Cyrillic 'а' has no NFKC decomposition to Latin 'a'; this is a finite
  hand-picked table, not exhaustive UTS #39 confusable detection), so
  `G1`/`g1` and the common homograph pairs it lists both count as the
  same id;
- exits **0** and prints a `Type P: N / Type U: M` summary, with a reminder
  that Type U gates must not be counted as evidence, if every declared
  Type P record is fully evidenced and arithmetically consistent.

What it does **not** do, by design: it does not evaluate whether the chosen
negative control is representative, whether the threshold itself is
well-chosen, or whether the control genuinely lacks the property under test
for reasons the numbers alone cannot show (e.g. a mislabeled structure).
That judgment is human (or reviewer-AI) work, the same way
`docs/VERIFIED_RUNS.md` records a dated executed run without re-deriving the
physics inside it. Nor does it detect a Type U gate being cited as evidence
somewhere the checker never looks -- a PR description, a paper, a different
file. The checker enforces exactly two things, both mechanical: the
paperwork (a Type P record has every required field, non-empty) and the
arithmetic (the field values it *does* have are numeric and self-consistent
with the FAIL label). Everything else the law requires remains a human
obligation stated in this document, not a property the exit code certifies.

## CI wiring

`scripts/ci_verify.sh` runs, as its last two steps:

- `scripts/test_check_gate_typing.py` (`5/6`) -- the checker's own
  self-test, driving `scripts/check_gate_typing.py` as a subprocess against
  small fixture records and asserting the exit code (and, where it matters,
  that the right problem is named) for: the EGFR-style arithmetic
  contradiction (must be rejected), non-numeric values (must be rejected), a
  genuinely failing control (must be accepted), duplicate ids under
  case/homograph normalization (must be caught), a zero-width-space-only
  field (must count as missing), and a missing declarations file (must be
  the trivial pass). This runs on every CI invocation, not just once at
  authoring time, so a future edit to the checker that reintroduces one of
  these holes fails CI immediately.
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
without doing the actual negative-control work would repeat the exact
mistake this law exists to stop. It is a process rule that makes the
"gate had no failing control" failure mode loud and mechanical to check
going forward; it is not a proof that any particular gate, past or future,
is or is not measuring what it claims to measure.
