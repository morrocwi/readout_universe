# URR-C Native System — Entry Point

This file is the root-level entry point for the native
**Universal Retention–Cut–Readout System (URR-C)** calculation layer added on
top of the existing Readout Universe philosophy and logic corpus.

URR remains the native reader–record/DRL kernel. URR-C is the current canonical
master architecture, adding explicit accessible and hidden sectors, separate
write and return channels, append-only retention, and readout null spaces.

## Start here

1. [`v2/urr/README.md`](v2/urr/README.md) — package purpose, reading order and commands.
2. [`v2/urr/URR_CUT_EXTENSION.md`](v2/urr/URR_CUT_EXTENSION.md) — canonical URR-C master equation.
3. [`v2/urr/URR_C_MASTER.yaml`](v2/urr/URR_C_MASTER.yaml) — machine-readable master contract.
4. [`v2/urr/URR_C_DISCOVERIES.md`](v2/urr/URR_C_DISCOVERIES.md) — discoveries, tiers, safe wording and non-claims.
5. [`v2/urr/KNOWLEDGE_MAP.md`](v2/urr/KNOWLEDGE_MAP.md) — dependency and evidence map.
6. [`v2/urr/URR_NATIVE_TECHNICAL_SPEC.md`](v2/urr/URR_NATIVE_TECHNICAL_SPEC.md) — native DRL equations, pseudocode and original runner contract.
7. [`v2/urr/urr_system_spec.yaml`](v2/urr/urr_system_spec.yaml) — machine-readable DRL runner contract.
8. [`v2/urr/urr_reference_runner.py`](v2/urr/urr_reference_runner.py) — executable DRL reference runner.
9. [`v2/urr/CLAIM_LEDGER.yaml`](v2/urr/CLAIM_LEDGER.yaml) — novelty and evidence ledger.
10. [`v2/urr/EXECUTED_RUNS.md`](v2/urr/EXECUTED_RUNS.md) — canonical run records.

## Canonical master equation

\[
\boxed{
\begin{gathered}
\delta_R\Longrightarrow\mathscr H_T,
\qquad
X_n=(\Phi_n,\Psi_n)^\top,
\qquad
\mathsf H_\alpha=I-\mathsf O_\alpha,
\\
\mathbb G_T
=L_R\otimes I+I\otimes C_{\mathcal F}+C_{\rm int},
\\
\frac{\delta S_{\rm DRL}}{\delta X_n}
=\mathcal J_{C,\alpha,n}[X_n],
\\
\mathcal T_{n+1}
=\mathcal T_n\oplus
\Lambda_{T,\alpha,n}\mathsf H_\alpha X_n,
\\
r_{\alpha,n}=A_\alpha\mathsf O_\alpha X_n-\delta_{\alpha,n},
\qquad
P_{\alpha,n}=\Pi_\alpha(r_{\alpha,n}),
\\
I_R(P_{\alpha,n}\mid\Pi_\alpha)
=-\log_2p_{\Pi_\alpha}(P_{\alpha,n})\;\mathrm{rbit}.
\end{gathered}
}
\]

The balanced directed flux \(\mathcal J_C\) is defined in
`v2/urr/URR_CUT_EXTENSION.md`. The DRL side is derived only in its declared
scope; the unified derivation of the cut and tape from one action remains
`Open`.

## Benchmark and structural adapters

- [AP13 — nonlinear FPUT external benchmark](ap/AP13_URR_FPUT_EXTERNAL_BENCHMARK.md)
- [AP14 — DESI DR2 correlated BAO inverse benchmark](ap/AP14_URR_DESI_DR2_COSMOLOGY_BENCHMARK.md)
- [AP15 — Universal Retention–Cut smoke test](ap/AP15_READ_WRITE_CUT.md)

AP13 and AP14 are executable finite diagnostics. AP14's cosmology equations
are an external `Dr` readout adapter, not a derivation of cosmology from URR.
AP15 is a native structural smoke test of separate write, return, hidden and
tape channels; it does not derive black holes or a unified DRL–cut–tape action.

## Discoveries now recorded

The repository now records, with separate tiers, that in the AP15 finite
positive-flow realization:

- readable loss can coexist with exact total retention;
- `R=0` gives exact visible damping;
- `R>0` gives a return-memory kernel;
- return edges alter dynamical observability;
- append-only tape can remain retained outside direct readout;
- a horizon is represented as a channel-asymmetry readout, with a black-hole
  interpretation only as one optional special case.

## Core boundary

The native kernel contains retained distinction, finite relational grammar,
reader–record DRL dynamics, explicit readout, identifiability gates, claim
tiers, and the native information unit `rbit`.

Quantum postulates, relativity postulates, and other domain theories are not
part of the native kernel. External adapters do not inherit native evidence
tiers automatically. Runtime outputs remain `finite_diagnostic`.
