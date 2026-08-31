# The Readout Contract for Human–AI Systems

Status: **v0.1 experimental; Phase-1 scope frozen**

This document translates the **Readout Condition** into a small executable
contract for Human–AI systems.  Phase 1 deliberately does **two things only**:

1. a distinction-level **Separation Eval** with bilingual clinical pilot data;
2. a stable **five-state runtime status vocabulary** in `omega/gates.py`.

Everything else discussed below is Phase 2.  It must not be reported as an
implemented capability.

The governing rule is:

> **No epistemic discrimination without provenance.**

For Human–AI design the normative interface is four verbs:

```text
Separate -> Attribute -> Revise -> Abstain
```

- **Separate** — the support must distinguish the asserted claim from a
  relevant rival.
- **Attribute** — the stated or contextually implicated basis must contain a
  jointly sufficient support bundle.
- **Revise** — if all surviving minimal support bundles are defeated, the
  downstream distinction must be withdrawn/re-checked.
- **Abstain** — if the records do not identify the contrast, do not guess.

The main paper should keep this layer normative.  Benchmark engineering lives
here and in the companion code, not in the philosophy paper.

---

## 1. Unit of audit

A sentence is often too coarse: one sentence can contain both licensed and
unlicensed distinctions.  RC-IR therefore represents one asserted contrast at
a time:

```text
DistinctionToken(
    claim=<asserted side>,
    rival=<relevant alternative>,
    provenance_nodes=[...],
    minimal_support_bundles=[...],
    basis_node_ids=[...],
    contributions=[...],
    required_access=[...]
)
```

`claim` and `rival` are semantic contrast roles.  `response_rule`, when known,
records how the output token was produced.  These are not the same object.

### Example

Source:

> No serious adverse effects were observed in the 32 participants studied.

Candidate distinction:

```text
claim = "the treatment is safe"
rival = "the study is too small to establish safety"
```

If the source is compatible with both, the categorical claim is
`NOT_IDENTIFIED`, even if the source is perfectly consistent with the words
"the treatment is safe".

Thus:

```text
consistency(source, claim) != separation(claim, rival | source)
```

---

## 2. Rival generation is part of the research problem

Separation Eval requires `(S, p, q)`.  The hard object is often `q`.

A useful rival is not necessarily logical negation.  It is a materially
relevant alternative that remains epistemically live under the source.

Phase 1 therefore **does not automate rival generation**.  The bilingual pilot
uses source-first human adjudication described in:

`benchmarks/rc_clinical_th_en/README.md`

The current 100-item builder produces only `DRAFT_SYNTHETIC` seed items.  They
must not be used for headline benchmark claims until independent human
annotation/adjudication has accepted the rivals and Thai/English equivalence.

---

## 3. Typed provenance

`ProvenanceNode.node_type` is functional rather than ontological.  The v0.1
vocabulary includes:

```text
retrieved
tool
user
episodic_memory
parametric
instruction
background_model
policy
decision_rule
calibration
measurement
testimony
other
```

The point is to prevent route laundering.  Retrieved evidence, parametric
memory, user testimony, calibration, and decision policy may jointly support a
claim but must remain separately auditable.

`implicated_basis` is **not automated in Phase 1**.  Contextually implicated
basis is optional/human-annotated.  Missing implicature annotation must not
block the benchmark.

---

## 4. Minimal jointly sufficient support bundles

RC-IR stores a family of minimal support bundles rather than one flat dependency
list:

```text
minimal_support_bundles = [
    {retrieved_doc, calibration},
    {independent_tool_result}
]
```

The family must be an antichain.  If `{A}` is sufficient, `{A,B}` is not stored
as another *minimal* bundle.

Node-specific undercutting defeat then routes as:

```text
defeat(A)
-> all bundles containing A die
-> if another minimal bundle survives, support survives
-> if none survives, re-check/withdraw
```

This v0.1 mechanism does not solve rebutting defeat or topology-changing policy
revision.  A policy change that rewires dependencies requires a newly compiled
RC-IR graph.

---

## 5. Signed support contributions

Support is not assumed monotone.  Additional information can weaken an earlier
support direction.

```text
SupportContribution(node_id="test",  value=+2.3026, scale="log_odds")
SupportContribution(node_id="prior", value=-4.5951, scale="log_odds")
```

Total:

```text
-2.2925 log_odds
```

Unlike scales must never be added silently.

---

## 6. Separation Eval

`omega.separation_eval` evaluates bundle-level compatibility readouts supplied
by a human annotator or another declared instrument:

```json
{
  "node_ids": ["source"],
  "claim_compatible": true,
  "rival_compatible": true,
  "evaluator": "human annotation"
}
```

Gold audit outcomes:

```text
claim yes, rival no   -> LICENSED
claim yes, rival yes  -> NOT_IDENTIFIED
claim no              -> UNSUPPORTED
missing bundle readout -> PROVENANCE_INCOMPLETE
```

A readout over a strict superset does **not** silently certify a smaller minimal
bundle.  The extra node may be the thing doing the separating.

---

## 7. USR and MSR are a mandatory pair

### Unauthorized Separation Rate (USR)

```text
USR = unauthorized categorical assertions / categorical assertions
```

### Missed Separation Rate (MSR)

```text
MSR = licensed separations withheld / gold licensed separations
```

**USR must never be reported alone.**  An always-abstain system trivially avoids
unauthorized assertions but fails useful separation.

For systems that emit a continuous separation score, report the operating curve
across declared `kappa` values:

```python
evaluate_operating_curve(cases, kappas=[...])
```

RC does not posit one universal kappa.

---

## 8. Five-state runtime vocabulary

`omega.gates.RCGateStatus` defines exactly:

```text
LICENSED
AUGMENTED
PROVENANCE_INCOMPLETE
NOT_IDENTIFIED
ABSTAIN
```

These are Human–AI runtime/disposition states.  They do **not** replace:

- `RUN / NOT_IMPLEMENTED` implementation status;
- Claim-IR tiers;
- bridge classes;
- proof-kernel verdicts.

A legacy stub remains `NOT_IMPLEMENTED` and receives no fake RC verdict.

`ABSTAIN` is an action state.  The underlying audit result must still record
whether abstention arose from non-identification, unsupported content,
provenance incompleteness, or an external safety/governance rule.

---

## 9. Structured abstention

When the source does not separate the alternatives, preferred output is not
just "low confidence".  The audit record should preserve:

```text
status: ABSTAIN
claim: <requested conclusion>
unresolved_rival: <still-compatible alternative>
reason: <why current support does not separate them>
required_access: <information that a qualified workflow would need>
```

In clinical contexts, `required_access` is an **epistemic requirement**, not a
patient-facing medical order.  RC must route any actual test/treatment action
through the appropriate clinician/governance layer.

---

## 10. Phase-2 items — explicitly deferred

The following are **not** Phase-1 deliverables:

- automatic rival generation;
- automatic implicature detection;
- causal-influence / faithfulness perturbation runner;
- contamination probe generator;
- provenance-aware long-term agent memory;
- Readout Card UI;
- automatic clinical next-step recommendation.

Before an agent-memory claim is promoted, the design must collide explicitly
with knowledge-editing / ripple-effect literature as well as TMS/ATMS/argument
maintenance.  "Defeat upstream -> stale downstream" is not presented as an
engineering novelty merely because RC gives it a provenance interpretation.

If a Readout Card is later implemented, it **must compile deterministically from
RC-IR/audit records**.  It must not be a free-form explanation generated by the
same model whose provenance is under audit.  Otherwise the receipt becomes a
new unverified claim surface.

---

## 11. Phase-1 deliverables

Implemented on branch `rc-ir-separation-eval`:

- `omega/rc_ir.py`
  - `DistinctionToken`
  - typed provenance nodes
  - signed contributions
  - minimal support bundles
  - node-specific support survival
- `omega/separation_eval.py`
  - distinction separation
  - USR + MSR
  - kappa operating curve
- `omega/gates.py`
  - five RC runtime statuses
  - legacy stubs remain visibly `NOT_IMPLEMENTED`
- `benchmarks/rc_clinical_th_en/`
  - rival/adjudication protocol
  - reproducible 100-item Thai/English synthetic seed builder
  - seed items remain non-headline evidence until human adjudication
- regression tests under `tests/`

The next evidence step is not another AI review.  It is independent human
annotation/review of the rivals and the first model comparison on USR/MSR.
