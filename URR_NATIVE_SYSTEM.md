# URR-C Native System — Entry Point

This file is the root-level entry point for the native
**Universal Retention–Cut–Return–Readout System (URR-C)** calculation layer.

URR remains the native reader–record/DRL kernel. URR-C 0.4 adds typed
accessible/hidden sectors, balanced write and return channels, separate tape
semantics, return-transformation kernels, finite-window readability, noise and
decoder gates.

## Start here

1. [`v2/urr/URR_C_MASTER_0_4.md`](v2/urr/URR_C_MASTER_0_4.md) — canonical human-readable master equation.
2. [`v2/urr/URR_C_MASTER_0_4.yaml`](v2/urr/URR_C_MASTER_0_4.yaml) — machine-readable 0.4 contract.
3. [`v2/urr/URR_C_PEER_REVIEW_0_4.md`](v2/urr/URR_C_PEER_REVIEW_0_4.md) — independent-style major-revision review.
4. [`v2/urr/URR_C_DISCOVERIES.md`](v2/urr/URR_C_DISCOVERIES.md) — earlier D0–D8 discovery ledger.
5. [`v2/urr/URR_CUT_EXTENSION.md`](v2/urr/URR_CUT_EXTENSION.md) — version 0.3 cut-development background.
6. [`v2/urr/URR_NATIVE_TECHNICAL_SPEC.md`](v2/urr/URR_NATIVE_TECHNICAL_SPEC.md) — native DRL action and recurrence.
7. [`v2/urr/CLAIM_LEDGER.yaml`](v2/urr/CLAIM_LEDGER.yaml) — evidence, novelty and non-claim ledger.
8. [`v2/urr/EXECUTED_RUNS.md`](v2/urr/EXECUTED_RUNS.md) — canonical run records.
9. [`v2/urr/KNOWLEDGE_MAP.md`](v2/urr/KNOWLEDGE_MAP.md) — dependency and evidence map.

## Upgraded master system

Let

\[
\mathscr X_T=\mathscr H_T\oplus\mathscr H_T,
\qquad
X_n=(\Phi_n,\Psi_n)^T,
\]

and lift a readout projector to the doubled space:

\[
\bar O_\alpha=I_2\otimes O_\alpha,
\qquad
\bar H_\alpha=I-\bar O_\alpha.
\]

The native DRL equations are forced by a balanced cut term rather than
replaced by it:

\[
\boxed{
\mathcal E_{\rm DRL}[X]_n=\mathcal J_{C,n}[X_n].
}
\]

The explicit reader component remains telegraph-like:

\[
\boxed{
\begin{aligned}
&M\frac{\Phi_{n+1}-2\Phi_n+\Phi_{n-1}}{\Delta t^2}
+D\frac{\Phi_{n+1}-\Phi_{n-1}}{2\Delta t}\\
&\quad+K\mathbb G_T\Phi_n+\nabla V(\Phi_n)-J_n
=P_\Phi\mathcal J_{C,n}[X_n].
\end{aligned}
}
\]

The return–transformation kernel is

\[
\boxed{
\mathcal K_{\alpha\leftarrow\beta}(\tau)
=A_\alpha\bar O_\alpha R_\alpha\mathcal U_H(\tau)
\bar H_\beta W_\beta\bar O_\beta E_\beta.
}
\]

For a sampled observation window,

\[
Y_L=\mathcal G_Lx_0+N_L,
\qquad
\mathcal G_L=\begin{pmatrix}C\\CF\\\vdots\\CF^L\end{pmatrix}.
\]

Under a declared linear-Gaussian policy,

\[
\boxed{
I_{\rm read}(L)
=\frac12\log_2\det\left[
I+\Sigma_x^{1/2}\mathcal G_L^T\Sigma_N^{-1}
\mathcal G_L\Sigma_x^{1/2}
\right]\;\mathrm{rbit}.
}
\]

## Benchmarks and structural adapters

- [AP13 — nonlinear FPUT external benchmark](ap/AP13_URR_FPUT_EXTERNAL_BENCHMARK.md)
- [AP14 — DESI DR2 correlated BAO inverse benchmark](ap/AP14_URR_DESI_DR2_COSMOLOGY_BENCHMARK.md)
- [AP15 — Universal Retention–Cut smoke test](ap/AP15_READ_WRITE_CUT.md)
- [AP17 — Return Transformation and Physical Readability](ap/AP17_RETURN_TRANSFORMATION_READABILITY.md)

AP17 records:

```text
verdict                              PASS
transformed-return rank              2
distance from identity               1.222171974564525
noiseless decoder error              2.289691319182597e-16
Gaussian readable information        7.825375266365017 rbit
partial-return rank                  1
no-return readable information       0 rbit
echo time                            0.885
hidden-elimination residual          6.189493362285248e-15
finite-window rank                   1 -> 3
```

The result demonstrates that a returned form can differ strongly from the
identity while remaining reconstructable under a declared decoder.

## Binding boundary

```yaml
native_DRL: derived_narrow
forced_DRL_cut_equations: Dr
linear_hidden_elimination: exact_algebra_in_declared_scope
linear_return_kernel: exact_algebra_in_declared_scope
linear_Gaussian_readability: exact_under_declared_distribution
AP17_runtime: finite_diagnostic
unified_DRL_cut_tape_action: Open
all_retained_states_eventually_return: not_claimed
physical_black_hole_from_native_cut_alone: not_claimed
```

Quantum theory, relativity, and other domain theories remain external adapters
and do not inherit native evidence tiers automatically.
