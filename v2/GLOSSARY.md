# Readout Universe v2 — Glossary of Knowledge Formation, Imagination, and Epistemic Sovereignty

> Status note: this glossary separates existing Readout Universe terms from newly proposed extensions. It does not silently upgrade any claim tier. Existing canonical meanings in `logic.md`, `philosophy.md`, and `v2/TRANSLATION_PROTOCOL.md` win on conflict.

## Tier convention

- `definition` — stipulated term/object for this framework.
- `Dr` — declared interpretive bridge or methodological reading.
- `Open` — proposed but not established; requires a falsifier or future diagnostic.

---

## Problem

**Tier:** `definition` / bridge to existing residual formalism.

A **problem** is a residual that a bounded knower retains as requiring repair or explanation.

Existing residual form:

\[
r = A\varepsilon - \delta
\]

with residual energy

\[
V = \frac12 r^TWr.
\]

Proposed shorthand:

\[
\boxed{\text{Problem} = \text{Retained Residual}}
\]

A residual need not automatically count as a problem; a knower's selection/readout policy determines whether it is retained as action-relevant.

---

## Question

**Tier:** `definition` / `Dr`.

A **question** is the selection of a difference within a retained residual that the knower seeks to make distinguishable.

\[
Q_{\Pi_Q}: r \rightarrow d_Q
\]

where `\Pi_Q` is the question-selection policy and `d_Q` is the selected difference.

Proposed shorthand:

\[
\boxed{\text{Question} = \text{Selection of a difference to be made distinguishable}}
\]

---

## Hypothesis

**Tier:** `definition` / `Dr`.

A **hypothesis** is a retained candidate relation, or candidate grammar update, proposed by a bounded knower to account for a present residual and committed to a future readout that can discriminate it from alternatives.

\[
H_i: A_0 \rightarrow A_i = A_0 + \Delta A_i
\]

and

\[
H_i \Rightarrow \hat{\delta}_i.
\]

A useful hypothesis must in principle participate in a contrast that some record can discriminate:

\[
\exists \delta^*:\quad R(H_i,\delta^*) \neq R(H_j,\delta^*)
\]

for at least one relevant competing hypothesis `H_j`.

Proposed shorthand:

\[
\boxed{\text{Hypothesis} = \text{Retained Candidate Relation}}
\]

A hypothesis is not truth, not proof, and not merely a fluent explanation.

---

## Decisive Record

**Tier:** `definition` / `Dr`.

A **decisive record** is a record whose readout differs across at least two live candidate hypotheses and therefore reduces a live degeneracy in hypothesis space.

\[
R(H_i,\delta^*) \neq R(H_j,\delta^*)
\]

If available records cannot distinguish `H_i` from `H_j`, their difference lies in the relevant null space and the honest result is structural non-identifiability from those records.

---

## Imagination

**Tier:** `definition` / `Open` as an empirical model.

**Imagination** is the bounded capacity to transport, recombine, and transform distinguishable meanings across a reachable semantic field without prematurely collapsing their differences.

\[
\boxed{\mathcal I_A = \operatorname{Transport}(\mathcal S_A^{\mathrm{reachable}})}
\]

or in prose:

> Imagination is not infinity. It is mobility inside finitude.

Imagination is not identical to retrieval. Retrieval re-accesses an already retained configuration; imagination changes relations among meanings and may generate new candidate configurations or hypotheses.

Typical semantic operations include:

\[
\mathfrak T = \{\text{combine, substitute, invert, scale, splice, analogize, translate, recontextualize}\}.
\]

---

## Semantic Field

**Tier:** `definition`.

For a bounded knower `A`, the **semantic field** `\mathcal S_A` is the set or structured family of meanings that are actually reachable under that knower's current retained representations, context, tools, and transport operators.

It is not an infinite pre-given possibility space.

Human and AI semantic fields may differ in size, topology, constraints, and reachable transformations while remaining bounded.

---

## Semantic Breadth

**Tier:** `definition`.

**Semantic breadth** is the extent or diversity of meanings/families accessible within a knower's semantic field.

Breadth alone does not determine imagination:

\[
\mathcal I \not\propto |\mathcal S|
\]

by definition of this proposed framework, because mobility and distinction-retention also matter.

---

## Semantic Mobility

**Tier:** `definition` / `Open` for measurement.

**Semantic mobility** is the capacity for meanings to participate in transformations or transport across the semantic field.

A high-cardinality semantic field with few usable transport relations may support less hypothesis generation than a smaller but more connected field.

---

## Cross-Domain Transport

**Tier:** `definition` / `Dr`.

**Cross-domain transport** is semantic transport that preserves enough relevant structure to move a distinction or relation from one domain-family into another without merely renaming it.

\[
D_i \leftrightarrow D_j
\]

must preserve a load-bearing relation, not only lexical similarity.

This extends the repo's existing Lens Law discipline: translation must alter the working representation, not decorate an unchanged foreign argument with native vocabulary.

---

## Live Semantic Family

**Tier:** `definition` / `Open`.

A **live semantic family** is a family of meanings whose internal distinctions remain available to readout and whose members still support non-trivial transport under a declared operator/policy.

Informally:

\[
\boxed{\text{Live Semantic Family} = \text{Distinction Retained} + \text{Recoverable Transport}}
\]

"Live" here is not a biological claim.

---

## Distinction-Retention Parameter `\lambda`

**Tier:** `Open`.

`\lambda` is proposed as a local/domain-scoped parameter describing whether a semantic transport preserves a distinction direction under a declared operator and readout policy.

For distinction direction `d`:

\[
\lambda_T(d) \neq 0
\]

means the distinction remains readout-active in that direction, whereas

\[
\lambda_T(d) = 0
\]

means that distinction direction is collapsed by the current transport/readout composition.

Critically:

\[
\lambda=0
\]

does **not** imply that the source meanings are ontologically identical. It implies only that their difference is unreadable under the declared operator/policy.

A future formalization must specify the operator class, representation, spectrum/singular structure if linearized, and the exact readout on which `\lambda` is defined.

---

## Recoverable / Reversible Transport

**Tier:** `definition` / `Open`.

**Recoverable transport** preserves enough distinction for the prior semantic state to remain discriminable within the declared family.

**Reversible transport** is stronger: it requires an inverse (globally or locally, depending on scope).

Therefore

\[
\lambda_i \neq 0
\]

for one direction does not by itself imply global reversibility.

For linear/local models, reversibility requires an appropriate full-rank condition on the relevant subspace.

---

## Semantic Collapse

**Tier:** `definition` / `Dr`.

A **semantic collapse** occurs when a transport or rigid readout maps previously distinguishable meanings in a family to an indistinguishable record.

For family `\mathcal F`:

\[
T_{\mathrm{rigid}}(s_i)=c \qquad \forall s_i\in\mathcal F
\]

implies

\[
T_{\mathrm{rigid}}(s_i)-T_{\mathrm{rigid}}(s_j)=0.
\]

In a fully collapsed linearized family, all active distinction directions satisfy

\[
\lambda_1=\lambda_2=\cdots=\lambda_k=0.
\]

This is a collapse of readout distinction, not proof that the meanings were identical in the ground state.

---

## Rigid Word / Premature Semantic Closure

**Tier:** `Dr`.

A **rigid word** is not simply a stable label. The problematic case is a label or category used as if one readout exhausted the live semantic family it compresses.

The failure mode is:

\[
\boxed{\text{Premature Semantic Closure} = \text{collapse of live distinctions before inquiry is complete}}
\]

Language can either open transport edges or close them. The target of critique is premature collapse, not language itself.

---

## Semantic Graph

**Tier:** `definition` / `Open` for diagnostics.

A knower's semantic field can be represented provisionally as a graph

\[
G_A=(V_A,E_A)
\]

where

- `V_A` = reachable meanings or semantic configurations,
- `E_A` = available transport relations/operators.

Imagination is therefore not reducible to node count. Connectivity, cross-domain paths, transport constraints, and distinction retention matter.

---

## Hypothesis Space

**Tier:** `definition` / `Dr`.

For question `Q`, a knower's **hypothesis space** is the set of candidate relations reachable from that knower's semantic field under allowed semantic transports and then selected as relevant to `Q`.

\[
\mathcal H_A(Q)
=
\Gamma_Q\left(\operatorname{Reach}_{\mathfrak T_A}(\mathcal S_A)\right)
\]

Hence two knowers facing the same problem and records may still generate different hypothesis spaces when

\[
\mathcal S_A\neq\mathcal S_B
\]

or

\[
\mathfrak T_A\neq\mathfrak T_B.
\]

---

## Bounded Imaginer

**Tier:** `Dr`.

A **bounded imaginer** is an agent whose imaginative transformations occur within a finite/conditioned reachable semantic field rather than an actually infinite space of unconstrained meanings.

Humans and AI are both treated here as bounded imaginers, although their bounds, representations, and transport mechanisms can differ substantially.

---

## Epistemic Sovereignty

**Tier:** `definition` / `Dr`.

**Epistemic sovereignty** is the retained control of a knower over the operations that determine the direction, admissibility, and revision of their knowledge-producing process.

Represent it as a vector rather than a single score:

\[
\mathbf S_A^{epi}
=
(c_P,c_Q,c_H,c_D,c_R)
\]

where

- `c_P` — control over problem framing,
- `c_Q` — control over question formation,
- `c_H` — control over hypothesis retention/selection,
- `c_D` — control over decisive-record criteria,
- `c_R` — control over revision.

A user may preserve some components while delegating others to AI or another agent.

Typing a prompt does not by itself establish epistemic sovereignty.

---

## Revision Control

**Tier:** `definition` / `Dr`.

**Revision control** is the capacity and authority to modify or discard a retained grammar/hypothesis when new records produce a load-bearing residual against it.

A knowledge process that preserves problem and hypothesis ownership but refuses revision under decisive counter-records has lost an essential part of epistemic self-correction.

---

## Knowledge-Formation Loop

**Tier:** `Dr` synthesis of existing and proposed terms.

Proposed expanded loop:

\[
\boxed{
\text{World}
\rightarrow
\text{Readout}
\rightarrow
\text{Problem}
\rightarrow
\text{Question}
\rightarrow
\text{Imagination}
\rightarrow
\text{Hypotheses}
\rightarrow
\text{Decisive Record}
\rightarrow
\text{Revision}
}
\]

or in compact native form:

\[
\theta(E)
\rightarrow
M_A
\rightarrow
r
\rightarrow
P
\rightarrow
Q
\rightarrow
\mathcal I
\rightarrow
\mathcal H
\rightarrow
\delta^*
\rightarrow
R
\rightarrow
A'.
\]

The loop is open-ended: `A'` generates new readouts and may expose new residuals.

---

## Education for Imagination

**Tier:** `Dr` / `Open` as empirical educational claim.

A proposed educational objective is not only to increase semantic inventory but also to increase mobility and preserve distinctions long enough for cross-domain hypothesis formation.

Conceptually:

\[
\boxed{
\text{Education for Imagination}
=
\text{Expand Meanings}
+
\text{Increase Mobility}
+
\text{Preserve Distinctions}
}
\]

Whether this formulation predicts measurable creativity or hypothesis diversity remains `Open` and should be tested rather than assumed.

---

## Minimal Research Program

**Tier:** `Open`.

Future diagnostics should distinguish mere verbal variation from genuinely different hypothesis families.

Possible measures include:

\[
N_H = \text{number of non-equivalent hypotheses}
\]

and

\[
D_H = \text{number of hypothesis families separated by different decisive records}.
\]

A basic falsifiable direction is to test whether interventions that increase semantic breadth and/or cross-domain transport increase `D_H`. If they do not, the proposed link between semantic mobility and imagination is weakened.

---

## Summary formulas

\[
\boxed{\text{Problem}=\text{Retained Residual}}
\]

\[
\boxed{\text{Question}=\text{Selected Difference}}
\]

\[
\boxed{\text{Hypothesis}=\text{Retained Candidate Relation}}
\]

\[
\boxed{\text{Imagination}=\text{Bounded Semantic Transport}}
\]

\[
\boxed{\text{Semantic Collapse}=\text{Loss of Readout Distinction under a declared operator/policy}}
\]

\[
\boxed{\text{Epistemic Sovereignty}=\text{Control over framing, questioning, hypothesis selection, decisive records, and revision}}
\]

And the central thesis:

> **Imagination is not infinity. It is mobility inside finitude.**
