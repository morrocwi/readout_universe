# Independent-Style Peer Review — URR-C 0.4

## Recommendation

**Major revision. Suitable as a computational research framework; not yet
supportable as a new fundamental physical theory.**

The framework is strongest when presented as a typed calculation and
falsification contract joining doubled variational dynamics, explicit readout,
hidden-state elimination, return channels, tape semantics, and claim-tier
control.

## Major strengths

1. The native DRL equations remain explicit and reproducible.
2. Readout is separated from ontology through operators, null spaces, noise,
   and policy.
3. AP15 supplies a valid finite counterexample to identifying readable loss
   with destruction.
4. The upgraded return kernel distinguishes returned form from recoverable
   information.
5. Evidence tiers and non-claims are unusually explicit.
6. AP17 is reproducible and contains numerical falsification gates.

## Corrections required and applied

### A. DRL was hidden in the previous master box

The previous master displayed only

\[
\delta S_{\rm DRL}/\delta X=\mathcal J_C.
\]

This obscured the telegraph-like reader equation and the anti-damped mirror.
Version 0.4 displays both component equations explicitly.

### B. The cut was not fully typed on reader–record space

The projectors now lift to

\[
\bar O=I_2\otimes O,
\qquad
\bar H=I-\bar O,
\]

and component selectors \(P_\Phi,P_\Psi\) state which equation receives each
force component.

### C. The current equation is forced, not one unified action

The defensible present interpretation is a discrete
Lagrange-d'Alembert-type forced variational system. Calling it one native
action would exceed the evidence.

### D. Memory and return were conflated

The reduced visible memory kernel

\[
K_{\rm mem}(\tau)=Re^{F_H\tau}W
\]

is a feedback kernel in the visible equation. The return–transformation kernel
also includes encoding and readout:

\[
\mathcal K_{\alpha\leftarrow\beta}
=A_\alpha R_\alpha U_HW_\beta E_\beta.
\]

They are related but answer different questions.

### E. Distance from identity is not an information measure

A rotation, change of basis, or unit conversion can make
\(\|\mathcal K-I\|\) large while preserving all reconstructable information.
Version 0.4 uses rank, noise-whitened singular values, decoder covariance, and
linear-Gaussian mutual information.

### F. Tape semantics were ambiguous

An injective growing tape and a fixed-dimensional positive accumulator are now
separate constructions.

### G. Conservation was too generic

The AP15 \(\mathbf1^Tq\) balance does not automatically extend to a signed
doubled DRL state. A declared retention covector \(\rho\) and the certificate

\[
\rho^T\mathcal J_C=0
\]

are now required whenever conservation is claimed.

### H. A one-way cut is not a black-hole certificate

A gravitational black-hole adapter must additionally supply a metric, causal
structure, and horizon certificate. The native cut is broader.

## Relation to established work

The individual mathematical components overlap established fields:

- Bateman-type doubled damped/anti-damped systems;
- forced Lagrangian and discrete Lagrange-d'Alembert equations;
- Mori–Zwanzig/generalized Langevin memory kernels;
- Kalman observability and finite-window state reconstruction;
- linear Gaussian channels and log-determinant mutual information;
- Maxwell–Cattaneo/telegraph-type damped wave equations.

Therefore novelty must remain restricted to the particular conjunction,
ontology, executable contract, and claim discipline until a full literature
comparison is completed.

Selected comparison sources:

- Widder, Zimmer, and Schilling, *On the generalized Langevin equation and the
  Mori projection operator technique*, arXiv:2503.20457;
- Sharma, Patil, and Woolsey, *Energy-preserving Variational Integrators for
  Forced Lagrangian Systems*, arXiv:1801.04996;
- Nasiri and Safari, *A symmetric treatment of damped harmonic oscillator in
  extended phase space*, arXiv:quant-ph/0505147;
- Barna and Kersner, *Heat conduction: a telegraph-type model with
  self-similar behavior of solutions*, arXiv:1002.0999;
- Kalman observability rank and Gramian theory as standard linear-systems
  comparison machinery;
- general-relativistic event-horizon definitions as a separate domain adapter.

## Technical risks

1. The mirror variable \(\Psi\) resembles known doubled systems; its ontic
   record interpretation is not derived by the linear DRL.
2. Positive retention cannot be assumed for arbitrary signed state vectors.
3. Nonnormal hidden dynamics can amplify transiently despite stable
   eigenvalues.
4. Nonlinear hidden elimination need not yield a stationary convolution
   kernel.
5. A finite observation window cannot prove permanent absence of return.
6. The linear-Gaussian information equation is not universal outside its
   declared distribution and noise model.
7. The architecture may re-express known state-space models without new
   predictive content unless domain-specific falsifiers are supplied.

## Required next evidence

1. Formally verify the forced component equations and lifted projector typing.
2. Prove the AP17 linear identities in a declared finite formal scope.
3. Add calibrated RC, thermal, and coupled-oscillator data with sensor noise.
4. Compare inferred kernels against independent system-identification
   baselines.
5. Test nonlinear return and echo with out-of-sample predictions.
6. Keep black-hole work as a GR adapter until Einstein-equation and causal
   certificates are supplied.
7. Obtain external human review before novelty promotion.

## Verdict by category

| Category | Verdict |
|---|---|
| Internal mathematical organization | coherent after 0.4 corrections |
| Reproducibility | good for finite scripts |
| Empirical physical validation | early |
| Fundamental-physics claim | unsupported at present |
| Computational framework value | promising |
| Individual mathematical novelty | not established |
| Conjunction novelty | `Open` |
| Recommendation | major revision, continue testing |
