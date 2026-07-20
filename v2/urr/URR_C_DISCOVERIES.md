# URR-C Discoveries Ledger

**Version:** 0.3.0-cut  
**Date:** 2026-07-20  
**Binding rule:** every statement below must be quoted at its own tier.

This file records what the Read–Write Cut work adds to the native URR system.
It separates exact algebra, executed diagnostics, architectural interpretation,
and open claims.  It is not a press-release list and does not promote AP15 into
an unrestricted theorem.

## D0 — Four notions must be separated

\[
\boxed{
\text{existence}
\neq
\text{retention}
\neq
\text{accessibility}
\neq
\text{readability}
}
\]

A state may remain retained while lying outside a particular readout's
accessible sector.

```yaml
tier: doctrine_and_definition
status: native_architectural_distinction
```

## D1 — Readable loss can be retained cross-cut flux

In the AP15 positive finite-flow realization,

\[
\dot q_O=-\Lambda_Oq_O+Rq_H,
\qquad
\dot q_H=Wq_O-(\Lambda_R+\Lambda_T)q_H,
\qquad
\dot q_T=\Lambda_Tq_H.
\]

The combined generator has zero column sums, hence

\[
\boxed{
\frac{d}{dt}
\left(\mathbf1^Tq_O+\mathbf1^Tq_H+\mathbf1^Tq_T\right)=0.
}
\]

Therefore a decrease in the readable sector can coexist with exact total
retention.

```yaml
exact_scope: AP15_positive_linear_flow
runtime_tier: finite_diagnostic
architectural_reading: Dr
general_universe_claim: not_made
```

**Safe wording:** observed loss can be realized as retained flux across a
readout cut.

**Forbidden wording:** all apparent loss in nature has been proved to be hidden
retention.

## D2 — A one-way cut produces exact visible damping in the finite model

When the write channel is nonzero and the return channel vanishes,

\[
W\neq0,
\qquad
R=0,
\]

then

\[
\boxed{\dot q_O=-\Lambda_Oq_O.}
\]

The hidden sector accumulates what leaves the directly readable sector.  AP15
measured, at its declared final time,

\[
q_O:1\rightarrow0.0107627442,
\qquad
q_H:0\rightarrow0.9892372558,
\]

with total-retention error below \(5.2\times10^{-15}\).

```yaml
algebra_tier: exact_in_declared_finite_model
runtime_tier: finite_diagnostic
black_hole_derivation: false
```

## D3 — A return channel generates a memory kernel

For the no-tape linear hidden equation

\[
\dot q_H=Wq_O-\Lambda_Hq_H,
\]

elimination of \(q_H\) gives

\[
\boxed{
\dot q_O(t)
=-\Lambda_Oq_O(t)
+Re^{-\Lambda_Ht}q_H(0)
+\int_0^t
K_{\rm mem}(t-s)q_O(s)\,ds
}
\]

with

\[
\boxed{K_{\rm mem}(u)=Re^{-\Lambda_Hu}W.}
\]

Thus the same cut grammar contains two limiting behaviours:

\[
R=0\Rightarrow\text{damping without return},
\qquad
R>0\Rightarrow\text{return memory}.
\]

```yaml
tier: exact_algebra
scope: finite_linear_hidden_sector_elimination
nonlinear_generalization: Open
```

## D4 — Return controls dynamical observability

With direct readout

\[
y=Cq,
\qquad C=(I_O,0_H,0_T),
\]

the observability matrix is

\[
\mathcal O_C=
\begin{pmatrix}
C\\CA\\\vdots\\CA^{d-1}
\end{pmatrix}.
\]

For the AP15 matrices:

| Case | Rank | Nullity |
|---|---:|---:|
| reciprocal cut | 6 | 1 |
| one-way cut | 3 | 4 |
| leaky cut | 6 | 1 |

The remaining null direction in the reciprocal case is the append-only tape,
which has no return edge.

\[
\boxed{
\text{directly unreadable}
\neq
\text{destroyed}
}
\]

```yaml
matrix_results: exact_for_recorded_AP15_matrices
runtime_tier: finite_diagnostic
general_observability_statement: conditional_on_A_and_C
```

## D5 — Append-only retention can outlive the hidden working state

If \(\Lambda_T\ge0\),

\[
\dot q_T=\Lambda_Tq_H\ge0
\]

for nonnegative retained quantities.  AP15's one-way-with-tape case ended with

\[
q_O=0.0107627442,
\quad
q_H=0.6978201446,
\quad
q_T=0.2914171112.
\]

The hidden working sector need not be monotone because it may itself write to
the tape, while the tape remains append-only.

```yaml
construction_tier: exact_for_positive_flow
runtime_tier: finite_diagnostic
unified_DRL_tape_action: Open
```

## D6 — A horizon is a channel-asymmetry readout, not a new substance

Define

\[
\boxed{
\chi_\alpha
=
\frac{\|W_\alpha\|}
{\|W_\alpha\|+\|R_\alpha\|+\varepsilon}.
}
\]

AP15 returned

| Channel | \(\chi\) |
|---|---:|
| reciprocal | \(0.5\) |
| leaky | \(0.9523809524\) |
| one-way | approximately \(1\) |
| source-like reverse | \(0\) |

The value depends on the chosen sector decomposition, norm, and readout policy.
It is therefore a readout of asymmetry, not an observer-independent essence.

```yaml
tier: definition
interpretation: Dr
```

## D7 — Black-hole language becomes one special case

The cut grammar does not begin with a black hole.  A black-hole-like one-way
readout is represented only as the limiting channel class

\[
W\neq0,
\qquad
R=0.
\]

The same grammar can also represent forgetting, write-only memory, failed
acknowledgement, secrecy, absorbing sectors, sensors, and broken return
channels without claiming that those systems are physically identical.

```yaml
tier: Dr
black_hole_physics_derived: false
external_relativity_adapter_required: true
```

## D8 — The master open problem is now sharper

The new central question is no longer merely whether a hidden sector can be
written down.  It is:

> Can the reader–record DRL, directed read–write cut, and injective append-only
> tape be derived from one native finite action, or can such a unification be
> ruled out?

```yaml
tier: Open
stance: positive
success_condition: derive one typed action and its reductions
failure_condition: prove incompatibility under declared assumptions
```

## Canonical evidence

- `v2/urr/URR_CUT_EXTENSION.md`
- `v2/urr/URR_C_MASTER.yaml`
- `ap/AP15_READ_WRITE_CUT.md`
- `ap/ap15_read_write_cut.py`
- `ap/results/AP15_READ_WRITE_CUT_RESULTS.json`

## One-sentence public summary

> URR-C shows, exactly in a finite positive-flow model and diagnostically in
> AP15, that a readout can lose access while the combined visible, hidden, and
> append-only retained quantity remains conserved; return channels turn that
> hidden sector into memory, while absent return leaves it in the readout null
> space.
