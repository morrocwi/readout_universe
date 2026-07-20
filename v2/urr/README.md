# URR-C Native System — AI Calculation Layer

This directory is the canonical calculation package for the
**Universal Retention–Cut–Return–Readout System (URR-C)**.

URR supplies the retained-distinction, finite-grammar, reader–record DRL,
readout, identifiability, and `rbit` kernel. URR-C 0.4 adds typed
accessible/hidden sectors, balanced write and return channels, separate tape
semantics, return-transformation kernels, finite-window observability, noise
models, and decoder-aware physical readability.

It is deliberately narrower than a theory-of-everything claim. Quantum theory,
relativity, and every other domain model remain external adapters.

## Reading order for an AI

1. [`URR_C_MASTER_0_4.md`](URR_C_MASTER_0_4.md) — canonical 0.4 equations and gates.
2. [`URR_C_MASTER_0_4.yaml`](URR_C_MASTER_0_4.yaml) — machine-readable 0.4 contract.
3. [`URR_C_PEER_REVIEW_0_4.md`](URR_C_PEER_REVIEW_0_4.md) — independent-style review and major-revision findings.
4. [`CLAIM_LEDGER.yaml`](CLAIM_LEDGER.yaml) — binding evidence and non-claim ledger.
5. [`EXECUTED_RUNS.md`](EXECUTED_RUNS.md) — canonical numerical outputs.
6. [`URR_NATIVE_TECHNICAL_SPEC.md`](URR_NATIVE_TECHNICAL_SPEC.md) — native DRL action and recurrences.
7. [`URR_C_DISCOVERIES.md`](URR_C_DISCOVERIES.md) — version 0.3 D0–D8 discovery development.
8. [`URR_CUT_EXTENSION.md`](URR_CUT_EXTENSION.md) — version 0.3 cut and AP15 background.
9. [`KNOWLEDGE_MAP.md`](KNOWLEDGE_MAP.md) — dependency and evidence map.
10. [`urr_system_spec.yaml`](urr_system_spec.yaml) and [`urr_reference_runner.py`](urr_reference_runner.py) — original DRL runner contract.
11. AP13–AP17 in [`../../ap/`](../../ap/) — external and structural benchmarks.

## Master structure

The doubled native space is

\[
\mathscr X_T=\mathscr H_T\oplus\mathscr H_T,
\qquad
X_n=(\Phi_n,\Psi_n)^T.
\]

Readout projectors are lifted by

\[
\bar O_\alpha=I_2\otimes O_\alpha,
\qquad
\bar H_\alpha=I-\bar O_\alpha.
\]

The cut is a declared force on the DRL equations:

\[
\boxed{\mathcal E_{\rm DRL}[X]_n=\mathcal J_{C,n}[X_n].}
\]

The reader equation remains explicitly telegraph-like:

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

For a finite observation window,

\[
\mathcal G_L=\begin{pmatrix}C\\CF\\\vdots\\CF^L\end{pmatrix}.
\]

Under a declared linear-Gaussian channel,

\[
\boxed{
I_{\rm read}(L)
=\frac12\log_2\det\left[
I+\Sigma_x^{1/2}\mathcal G_L^T\Sigma_N^{-1}
\mathcal G_L\Sigma_x^{1/2}
\right]\;\mathrm{rbit}.
}
\]

## Current discoveries

The binding ledger now records:

1. existence, retention, accessibility, and readability are distinct;
2. readable loss can coexist with exact total retention in AP15;
3. linear hidden elimination produces a memory kernel;
4. unreadable now does not imply unreadable forever;
5. a transformed return can remain reconstructable;
6. physical readability depends on time window, readout, noise, encoder, and decoder;
7. zero return in one finite protocol does not prove permanent destruction;
8. a gravitational black-hole classification requires an external causal and geometric horizon certificate.

## Install and run

```bash
python -m pip install -r v2/urr/requirements-benchmarks.txt
python v2/urr/smoke_test.py
python ap/ap13_urr_fput.py
python ap/ap14_urr_desi_dr2.py
python ap/ap15_read_write_cut.py \
  --output ap/results/AP15_READ_WRITE_CUT_RESULTS.json
python ap/ap17_return_transformation.py \
  --output ap/results/AP17_RETURN_TRANSFORMATION_RESULTS.json
```

## AP17 recorded result

```text
verdict: PASS
transformed-return rank: 2
distance from identity: 1.222171974564525
noiseless decoder error: 2.289691319182597e-16
Gaussian readable information: 7.825375266365017 rbit
partial-return rank/nullity: 1 / 1
zero-return readable information: 0 rbit
echo time: 0.885
hidden-elimination residual: 6.189493362285248e-15
finite-window rank: 1 -> 2 -> 3
```

## Binding boundary

- The linear mirror variable does not prove mechanistic reader-to-record handoff.
- The cut equations are presently forced equations, not one unified action.
- An injective growing tape and a fixed accumulator are different constructions.
- Linear-Gaussian readability is exact only under its declared distribution and noise assumptions.
- A finite window cannot prove that return is impossible forever.
- A native one-way cut does not derive a gravitational black hole.
- All runtime outputs remain `finite_diagnostic`.
