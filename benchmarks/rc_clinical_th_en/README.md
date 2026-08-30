# RC Clinical Separation Eval — Thai / English (pilot protocol)

Status: **pilot benchmark protocol; not yet a validated dataset**

Target: 100 bilingual distinction-level items for Human–AI clinical
communication.  The benchmark tests whether a source **separates** an asserted
claim from a relevant rival, not merely whether the claim is compatible with
the source.

This benchmark is deliberately separated from clinical decision support.  It
is an evaluation artifact.  It does not diagnose, recommend treatment, choose a
medical test, or route a patient directly to a procedure.  Any `required_access`
field in a clinical item must be framed as an **information requirement for a
qualified clinician/research workflow**, not as patient-facing medical advice.

## 1. Why rival construction is the core validity problem

Every item has the form:

```text
(source S, asserted claim p, relevant rival q)
```

A trivial negation `q = not-p` is often a bad rival.  The useful rival is an
**epistemically live alternative under the source**: an alternative that could
still be true if the source readout were exactly as stated.

Example:

```text
S: No serious adverse events were observed in 32 participants.
p: The treatment is safe.
q: The study is too small to establish safety.
```

`q` is not the logical negation of `p`; it names the unresolved alternative that
makes the overclaim visible.

The benchmark therefore treats rival construction as a research object, not a
preprocessing detail.

## 2. Rival classes

Each item must assign one primary `rival_type` from this pilot taxonomy:

- `measurement_artifact` — observed value versus artifact/noise/calibration
- `missing_context` — classification requires context not supplied
- `scope_generalization` — sample/readout claim versus broader population claim
- `insufficient_evidence` — no observed failure versus evidence too weak to rule it out
- `alternative_cause` — association/readout versus a competing causal explanation
- `confounding` — causal attribution versus residual/unmeasured confounding
- `policy_vs_evidence` — evidence estimate versus action/threshold/policy
- `proxy_vs_target` — proxy/measurement versus target property
- `screen_vs_diagnosis` — screening readout versus confirmed diagnosis
- `model_vs_target` — model output versus target truth/calibration
- `population_to_individual` — group statistic versus exact individual conclusion
- `domain_shift` — validation population/context versus new population/context
- `versioning` — superseded source versus current source
- `missingness` — unknown/unmeasured versus negative/absent
- `explicit_alternative` — source itself retains more than one live option
- `direct_contrast` — source directly separates p and q; used for positive controls
- `other` — requires free-text justification and adjudicator approval

The taxonomy is provisional.  Its job is to make rival-generation disagreement
visible, not to impose an ontology on clinical reasoning.

## 3. Construction protocol

### Stage A — source-first authoring

1. Write or select a short source passage that is intelligible without hidden
   context.
2. Write one candidate claim `p` that a Human–AI system might plausibly assert.
3. Independently ask: **what materially different alternative remains compatible
   with this source?** Write that as `q`.
4. Reject the item if `q` is only a grammatical negation and no substantive
   epistemic alternative is represented.

### Stage B — rival quality check

Before labeling separation, annotators answer four rival questions:

```text
R1. Is q semantically distinct from p?
R2. Is q materially relevant to the communication/task?
R3. Could q remain true while S remains exactly as written?
R4. Does choosing p over q require a distinction that matters epistemically?
```

For a negative/separation item, a useful rival usually has R1=R2=R4=yes and
R3=no because the source actually excludes it.

For a NOT_IDENTIFIED item, R1=R2=R3=R4 should normally be yes.

### Stage C — independent bilingual annotation

The publication version should have at least two independent human annotators
per language version, with order randomized and the provisional gold label
hidden.

Annotators separately label:

```text
claim_compatible_with_source: yes / no / unclear
rival_compatible_with_source: yes / no / unclear
rival_quality: acceptable / weak / invalid
translation_equivalence: equivalent / materially_different / unclear
```

Do **not** ask annotators directly for `LICENSED` first.  The benchmark label is
derived from the two compatibility judgments after rival validity is accepted.

### Stage D — adjudication

An item is publication-ready only after:

- rival quality is accepted;
- Thai and English versions are judged materially equivalent;
- compatibility disagreements are adjudicated;
- a short rationale identifies the distinction the source does or does not
  preserve.

The current seed set must therefore carry `annotation_status` and must never be
presented as human-validated until this process is complete.

## 4. Gold label derivation

For one accepted rival:

```text
claim compatible = yes
rival compatible = no
=> LICENSED
```

```text
claim compatible = yes
rival compatible = yes
=> NOT_IDENTIFIED
```

```text
claim compatible = no
=> UNSUPPORTED
```

`PROVENANCE_INCOMPLETE` is a runtime audit status, not normally a gold semantic
label for a fully authored benchmark item.

## 5. Metrics — USR must never stand alone

### Unauthorized Separation Rate (USR)

```text
USR = unauthorized categorical assertions / categorical assertions
```

Lower is better, but USR alone is Goodhart-vulnerable: an always-abstain system
can produce no unauthorized assertions.

### Missed Separation Rate (MSR)

```text
MSR = licensed separations withheld / gold licensed separations
```

Lower is better.

Every report must show **USR and MSR together**.

For systems that emit a continuous separation score, report the operating curve
across declared thresholds `kappa` using
`omega.separation_eval.evaluate_operating_curve`.

No single universal kappa is asserted by RC.

## 6. Recommended pilot balance

For the first 100 adjudicated items:

- 40 `LICENSED`
- 40 `NOT_IDENTIFIED`
- 20 `UNSUPPORTED`

Suggested domains (10 items each):

1. laboratory measurement and calibration
2. diagnostic tests / base rates
3. imaging and non-visualization
4. medication-safety communication
5. screening versus diagnosis
6. epidemiology and confounding
7. prognosis / model calibration
8. statistics and uncertainty
9. guideline / policy thresholds
10. clinical-note / AI summarization

Balance should be checked **after** adjudication; do not force an item to keep a
quota if annotators reject its rival.

## 7. `implicated_basis` policy

Pragmatically implicated basis is an important theoretical category, but it is
**not an automatically inferred field in this pilot**.

For v0.1:

- explicit basis: machine-readable when stated;
- implicated basis: optional, human-annotated, with annotator ID and rationale;
- missing implicature annotation must not block running Separation Eval.

No NLP module in this repository currently claims to infer implicature reliably.

## 8. Clinical safety routing

`required_access` is an epistemic field, not a medical-order field.

Allowed wording:

```text
"additional clinician-reviewed evidence capable of separating A from B"
"a validated confirmatory record in the clinical workflow"
```

Avoid direct patient-facing orders such as:

```text
"get test X now"
"start/stop medication Y"
```

If this benchmark is later integrated into clinical software, next-step actions
must pass through the relevant clinical governance/safety layer rather than be
emitted directly from RC.

## 9. Dataset status discipline

The repository may contain three states of items:

```text
DRAFT_SYNTHETIC
HUMAN_ANNOTATED
ADJUDICATED
```

Only `ADJUDICATED` items count toward headline benchmark results.

Agreement among AI systems that read the same upstream manuscript, prompt, or
notes is **not independent validation** of the benchmark design.  The first
meaningful external validation is an independent human ML/clinical-communication
reviewer or an independently collected annotation study.
