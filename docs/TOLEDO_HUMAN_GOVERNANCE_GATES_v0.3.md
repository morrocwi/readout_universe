# Toledo Human Governance Gates v0.3

**Repository role:** Readout Universe semantic / gate-level interpretation  
**Date:** 2026-09-11

This note mirrors the Toledo v0.3 human-governance extension into Readout Universe so that the knowledge-routing layer and the readout/gating layer share the same invariants.

The six added mechanisms are:

```text
TRUST_GATE
RIGHTS_AND_CONSENT
EXPERT_SET
ABSORPTIVE_CAPACITY
PERSISTENT_CASE_STEWARD
IMPACT_LEDGER
```

They are interpreted here as readout/gating constraints on whether a candidate state may be promoted, routed, or handed off.

---

# 1. Core relation

Toledo defines a Knowledge-like Thing:

```text
FIELD_PERSON
    +
AI_MEDIATED_EXCHANGE
    +
EXPERT_SET
    =
K*
```

with supporting evidence:

```text
research
own data
public/shared data
```

Formal shorthand:

```text
K* = Compose(F, A_exchange, E_set | R, D_own, D_public)
```

`K*` is a candidate knowledge object, not automatically verified truth.

Readout interpretation:

```text
A candidate readout is promotable only when
its material gate conditions are explicit,
traceable, and satisfied or explicitly unresolved.
```

---

# 2. Gate vector

For a case/state `x`, define the governance gate vector:

```text
G_h(x) = {
    g_trust,
    g_rights,
    g_expert,
    g_absorb,
    g_steward,
    g_impact
}
```

where:

```text
g_trust   = collaboration/trust sufficiency
g_rights  = consent/ownership/use-right sufficiency
g_expert  = expert-set coverage sufficiency
g_absorb  = recipient absorptive-capacity sufficiency
g_steward = continuity/accountability sufficiency
g_impact  = impact-measurement sufficiency
```

Promotion rule:

```text
PROMOTE(x)
only if every gate required for the intended transition
is PASS or explicitly represented as an accepted residual risk.
```

This avoids treating social/institutional constraints as invisible metadata.

---

# 3. TRUST_GATE

A correct semantic or technical match does not imply a workable relationship.

```text
TRUST_GATE = {
    shared_goal,
    role_clarity,
    language_fit,
    incentive_alignment,
    conflict_of_interest,
    expected_benefit,
    response_commitment,
    confidentiality_expectation,
    power_imbalance
}
```

Readout law:

```text
expert_match != collaboration
```

Operational gate:

```text
IF trust insufficient:
    block deep handoff
    route to relationship-building
```

---

# 4. RIGHTS_AND_CONSENT

No readout should erase provenance or silently detach knowledge from the rights of its contributors.

```text
RIGHTS_RECORD = {
    source_owner,
    contributor,
    consent_status,
    permitted_use,
    prohibited_use,
    confidentiality,
    commercial_use_permission,
    attribution_rule,
    community_rights,
    IP_expectation,
    benefit_sharing
}
```

Readout law:

```text
formalization != transfer_of_ownership
```

Hard gate:

```text
IF required rights unresolved:
    HOLD publication / commercialization / transfer
```

---

# 5. EXPERT_SET

Replace the single-expert assumption:

```text
E → E_set = {E1, E2, ..., En}
```

Coverage rule:

```text
E_set = minimum sufficient cover(problem_dimensions)
```

Readout law:

```text
A candidate interpretation must not be promoted as domain-complete
when material dimensions of the problem remain uncovered.
```

Do not maximize number of experts. Minimize uncovered material uncertainty.

---

# 6. ABSORPTIVE_CAPACITY

Knowledge availability and knowledge usability are distinct states.

```text
K_available != K_usable
```

Define:

```text
A_cap = {
    comprehension,
    technical_skill,
    management_skill,
    data_skill,
    time,
    team,
    finance,
    execution_capacity,
    maintenance_capacity
}
```

Routing law:

```text
IF A_cap LOW:
    do not route directly to the most sophisticated service
    route first to capacity-building or paired support
```

Thus routing is constrained by both problem fit and receiver capacity.

---

# 7. PERSISTENT_CASE_STEWARD

A distributed routing system requires persistent accountability.

```text
CASE_STEWARD = {
    case_id,
    responsible_person_or_unit,
    case_history,
    current_state,
    failed_routes,
    active_commitments,
    unresolved_conflicts,
    next_followup
}
```

Readout law:

```text
persistent_context != persistent_accountability
```

AI can preserve context, but a live case must retain a human/institutional accountability pointer.

---

# 8. IMPACT_LEDGER

Readout Universe should distinguish activity from effect.

```text
OUTPUT != OUTCOME != IMPACT
```

Ledger:

```text
IMPACT_LEDGER = {
    baseline,
    intervention,
    output,
    outcome,
    intermediate_impact,
    long_term_impact,
    negative_effect,
    attribution_confidence,
    counterfactual_method_if_available,
    followup_date
}
```

Promotion law:

```text
Do not promote OUTPUT claims into IMPACT claims
without an explicit evidence bridge.
```

When causal attribution is claimed:

```text
require defensible comparison / baseline / counterfactual logic
```

---

# 9. AI mediation as a typed transformation

AI-mediated translation must itself have provenance.

```text
AI_TRANSLATION_RECORD = {
    original_statement,
    translated_statement,
    assumptions_added,
    ambiguity,
    unresolved_terms,
    confidence,
    evidence_links,
    omitted_context,
    alternative_interpretations
}
```

Field-to-expert:

```text
F_original
    → AI_translate
    → F_confirmed
    → E_set
```

Expert-to-field:

```text
E_original
    → AI_translate_back
    → E_confirmed
    → F
```

Typing constraint:

```text
AI_translation(original)
must not be typed as
identity(original)
without human confirmation.
```

---

# 10. State-transition semantics

Extend the case state:

```text
S_t = {
    K,  # knowledge clarity
    T,  # trust
    R,  # rights
    E,  # expert-set adequacy
    A,  # absorptive capacity
    P,  # prototype/product maturity
    V,  # technical validation
    M,  # market / real-adoption evidence
    B,  # business-model maturity
    O,  # operations
    F,  # finance
    C,  # compliance
    I,  # IP
    N,  # network
    G,  # growth
    X   # global readiness
}
```

Each action creates a new state version:

```text
S_t
  → Action_t
  → Evidence_t
  → S_(t+1)
```

No previous state is erased.

This preserves DAG-style acyclicity per version while allowing iterative real-world learning across versions.

---

# 11. Failure as evidence

```text
FAILURE_RECORD = {
    attempt,
    expected_result,
    actual_result,
    reason_for_failure,
    cost,
    lesson,
    next_decision
}
```

Readout law:

```text
failed route = information
```

A later agent must be able to distinguish:

```text
not_yet_tried
from
tried_and_failed
```

---

# 12. Gate-aware promotion

Conceptual pseudocode:

```text
FUNCTION READOUT_PROMOTION(candidate, target_transition):

    required_gates = gates_for(target_transition)

    FOR gate in required_gates:
        evaluate(gate)

    IF any hard gate == FAIL:
        RETURN HOLD

    IF any soft gate == UNRESOLVED:
        attach residual_risk

    preserve:
        provenance
        prior_state
        failure_history
        rights_record
        impact_record

    RETURN PROMOTABLE_WITH_TRACE
```

---

# 13. Toledo handoff relation

The semantic sequence is:

```text
Problem
    ↓
Rights + Trust
    ↓
Field Person ↔ AI ↔ Expert Set
    ↓
K*
    ↓
Absorptive Capacity
    ↓
Dynamic Tool Routing
    ↓
Solution / Prototype / Validation
    ↓
Real Adoption Environment
    ↓
Innovation-in-Real-Adoption
    ↓
Toledo Handoff
    ↓
NIA 4G / other scale systems
```

Persistent state objects:

```text
CASE_STEWARD
EVIDENCE_LEDGER
IMPACT_LEDGER
RIGHTS_RECORD
FAILURE_RECORD
```

---

# 14. Cross-repository contract

Operational implementation lives in:

```text
morrocwi/toledo
  docs/TOLEDO_HUMAN_GOVERNANCE_EXTENSIONS_v0.3.md
```

Repository responsibilities:

```text
readout_universe:
    gate semantics
    typed transitions
    traceability constraints
    promotion invariants

toledo:
    case workflow
    human governance
    service routing
    continuity
    impact tracking
```

The two documents should evolve together when any of the six mechanisms changes semantics.
