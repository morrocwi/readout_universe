# The Readout Contract for Human–AI Systems

Status: executable design specification (v0.1, experimental)

This document translates the **Readout Condition** into a runtime contract for
Human–AI systems.  It does not claim that the current repository solves
hallucination, chain-of-thought faithfulness, contamination, or memory revision
in general.  It defines a narrow interface that makes those failure families
auditable at the level of **distinctions**, not merely whole answers.

The governing rule is:

> **No epistemic discrimination without provenance.**

A Human–AI system should therefore be able to do four things for each
claim-level distinction:

1. **Separate** — show that its support distinguishes the asserted claim from a
   relevant rival.
2. **Attribute** — identify a jointly sufficient support bundle and distinguish
   retrieved/tool/user/memory/parametric/instruction/model/policy contributions.
3. **Revise** — withdraw or re-check downstream distinctions when all surviving
   minimal support bundles are defeated.
4. **Abstain structurally** — when the supplied records do not identify the
   contrast, return the unresolved rival and the additional access that would
   resolve it rather than guessing.

This contract is intentionally compatible with the existing Omega/Claim-IR
architecture.  `omega.claim_ir.Claim` remains the claim-level layer.
`omega.rc_ir.DistinctionToken` is a new layer above it.

---

## 1. Unit of audit

A full sentence is often too coarse.  One sentence can contain multiple
licensed and unlicensed distinctions at once.

RC-IR therefore uses:

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

The distinction between `claim` and `rival` is essential.  A source that is
compatible with both does not license choosing one over the other.

### Example

Source:

> No serious adverse effects were observed in the 32 participants studied.

Candidate distinction:

```text
claim = "the treatment is safe"
rival = "the study is too small to establish safety"
```

If the source remains compatible with both alternatives, the correct RC verdict
is `NOT_IDENTIFIED`, not `LICENSED`.

This is stronger than consistency checking:

```text
consistent(source, claim) = true
consistent(source, rival) = true
=> separation = false
```

---

## 2. Typed provenance

`ProvenanceNode.node_type` is functional rather than ontological.  The current
v0.1 vocabulary is:

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

A single physical artifact may play different roles in different pipelines.
The purpose of the type is to make route changes visible, not to declare a
universal ontology of information.

### Why route typing matters

For a RAG answer, retrieved text and parametric memory are not interchangeable.
For an agent, a current user statement and an old episodic memory are not
interchangeable.  For a diagnosis, a test result and a population prior are not
interchangeable.  RC requires those routes to remain separately auditable even
when they jointly support one final claim.

---

## 3. Minimal jointly sufficient support bundles

A distinction may have several independent sufficient routes.  RC-IR stores the
family of **minimal** support bundles rather than one flat dependency list.

```text
minimal_support_bundles = [
    {retrieved_doc, calibration},
    {independent_tool_result}
]
```

The stored family must be an antichain: a strict superset of an already stored
bundle is not minimal and is rejected by the schema.

This representation supports node-specific undercutting defeat:

```text
defeat(retrieved_doc)
=> first bundle dies
=> independent_tool_result bundle survives
=> distinction remains supported
```

If all minimal bundles die, the distinction must become stale, withdrawn, or
re-checked.

This v0.1 mechanism does **not** solve rebutting defeat or topology-changing
policy revision.  If the rule of decision itself changes, a new RC-IR graph must
be produced and audited.

---

## 4. Signed support contributions

Support layers are not assumed to improve monotonically.  A prior, background
model, or later observation may weaken an earlier evidential contribution.

RC-IR therefore stores signed contributions on an explicitly named scale:

```text
SupportContribution(node_id="test",  value=+2.3026, scale="log_odds")
SupportContribution(node_id="prior", value=-4.5951, scale="log_odds")
```

Total:

```text
-2.2925 log_odds
```

The runtime must never add unlike scales.  If more than one scale is present,
the caller must select one explicitly.

---

## 5. Separation Eval

`omega.separation_eval` implements the first executable Human–AI evaluation
surface.

The caller supplies bundle-level readouts:

```json
{
  "node_ids": ["source"],
  "claim_compatible": true,
  "rival_compatible": true,
  "evaluator": "human annotation"
}
```

The evaluator returns one of:

```text
LICENSED
NOT_IDENTIFIED
UNSUPPORTED
PROVENANCE_INCOMPLETE
```

### Decision rule

For a recorded minimal support bundle `B`:

```text
claim compatible = true
rival compatible = false
=> LICENSED
```

```text
claim compatible = true
rival compatible = true
=> NOT_IDENTIFIED
```

```text
claim compatible = false for every evaluated minimal bundle
=> UNSUPPORTED
```

```text
no readout for a recorded minimal bundle
=> PROVENANCE_INCOMPLETE
```

A readout over a strict superset does **not** silently certify a smaller minimal
bundle.  That would hide which added node supplied the separation.  The caller
must run the ablation/readout explicitly.

---

## 6. Unauthorized Separation Rate

For a benchmark in which the system actually makes categorical assertions:

```text
USR = unauthorized asserted distinctions / asserted distinctions
```

An asserted distinction is unauthorized when:

- the separation verdict is not `LICENSED`; or
- the distinction is supportable but the represented/implicated basis omits a
  sufficient support bundle.

This metric is intentionally harsher than factual accuracy.  A lucky true
answer can still be an unauthorized separation if the stated source did not
license the distinction it asserted.

---

## 7. Structured abstention

When a distinction is not identified, the preferred output is not a generic
"low confidence" message.  The system should return an epistemic receipt:

```text
status: ABSTAIN
claim: <requested conclusion>
unresolved_rival: <still-compatible alternative>
reason: available support does not separate the alternatives
required_access:
  - <new record/test/tool that would discriminate>
```

This follows the existing Translation Protocol discipline: a null-space or
non-identifiable question is answered as structurally unanswerable from the
current records rather than guessed.

---

## 8. Human-facing Readout Card

RC-IR is machine-facing.  Human users should normally receive a compact
`Readout Card` rather than the full provenance graph:

```text
Answer: X
Based on: source A + tool B
Added assumptions: model C
Still compatible with: rival D
Would change if: node E is defeated
Next useful access: test F
```

This is not chain-of-thought.  It is a claim-level epistemic receipt.

---

## 9. Mapping to AI failure families

### Hallucination

RC reading: an asserted distinction has no licensed support bundle or no
recoverable provenance route.

Design response: block or abstain at distinction level rather than treating the
whole answer as one pass/fail object.

### Unfaithful explanation / silent lift

RC reading: represented basis differs materially from the support route that
actually changes the response.

Design response: perturb omitted nodes.  If the distinction changes while the
represented basis remains unchanged, record an undeclared-influence witness.
RC does not require private chain-of-thought to run this test.

### Contamination / memorization

RC reading: output varies across cases that are equivalent under the declared
source route because an undeclared retained route distinguishes them.

Design response: construct source-equivalent probes and test whether downstream
responses separate them.  Detection power is relative to the declared source:
a fully discriminating source leaves fewer equivalence pairs to probe.

### Agent memory

RC reading: stored proposition without stored minimal support family cannot be
revised correctly when upstream support is defeated.

Design response: memory objects should store at least
`(claim, support_bundles, provenance_version, status)` and route defeat through
those bundles.

---

## 10. What is implemented now

Implemented on branch `rc-ir-separation-eval`:

- `omega/rc_ir.py`
  - typed `ProvenanceNode`
  - signed `SupportContribution`
  - antichain-validated `SupportBundle`
  - `DistinctionToken`
  - represented/implicated basis
  - minimal-support defeat routing
- `omega/separation_eval.py`
  - bundle-level separation evaluator
  - `LICENSED / NOT_IDENTIFIED / UNSUPPORTED / PROVENANCE_INCOMPLETE`
  - Unauthorized Separation Rate
  - structured-abstention recall
  - JSON CLI
- regression tests under `tests/`

Not yet implemented:

- automatic extraction of relevant rivals from free text;
- automatic NLI/entailment scoring;
- causal influence perturbation runner;
- contamination probe generator;
- provenance-aware long-term agent memory store;
- automatic Readout Card renderer;
- topology-changing defeat/revision.

The absence of these components is not reported as a PASS.  They remain explicit
next-stage work.

---

## 11. Minimal adoption path

A Human–AI team can use v0.1 without adopting the larger Readout Universe:

1. decompose one output into claim-level distinctions;
2. name one relevant rival per distinction;
3. type the sources that materially support it;
4. record minimal jointly sufficient support bundles;
5. obtain claim/rival compatibility readouts for those bundles;
6. run `omega.separation_eval`;
7. abstain when the source does not separate the alternatives;
8. store the support family if the claim enters agent memory.

That is the smallest executable contract implied by the Readout Condition.
