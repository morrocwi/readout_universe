# URR-C Native System — AI Calculation Layer

This directory is the canonical native calculation package for the
**Universal Retention–Cut–Readout System (URR-C)**.

URR supplies the retained-distinction, finite-grammar, reader–record DRL,
readout, identifiability and `rbit` kernel. URR-C is the current master
architecture: it adds observer-relative accessible/hidden sectors, separate
write and return channels, append-only retention and dynamical readout null
spaces.

It is deliberately narrower than a theory-of-everything claim. Quantum theory,
relativity, and all other domain models are optional external adapters and do
not modify the kernel.

## Reading order for an AI

1. [`URR_CUT_EXTENSION.md`](URR_CUT_EXTENSION.md) — canonical URR-C master equation and exact finite reductions.
2. [`URR_C_MASTER.yaml`](URR_C_MASTER.yaml) — machine-readable master equation contract.
3. [`URR_C_DISCOVERIES.md`](URR_C_DISCOVERIES.md) — discoveries, evidence tiers, safe wording and falsifiers.
4. [`KNOWLEDGE_MAP.md`](KNOWLEDGE_MAP.md) — scope, dependency graph and claim boundaries.
5. [`URR_NATIVE_TECHNICAL_SPEC.md`](URR_NATIVE_TECHNICAL_SPEC.md) — native DRL equations and normative pseudocode.
6. [`urr_system_spec.yaml`](urr_system_spec.yaml) — machine-readable DRL runner contract.
7. [`urr_reference_runner.py`](urr_reference_runner.py) — executable DRL reference implementation.
8. [`example_ring.yaml`](example_ring.yaml) — smallest complete DRL runnable example.
9. [`CLAIM_LEDGER.yaml`](CLAIM_LEDGER.yaml) — novelty, evidence and non-claims.
10. [`EXECUTED_RUNS.md`](EXECUTED_RUNS.md) — recorded commands and numerical outputs.
11. AP13–AP15 in [`../../ap/`](../../ap/) — external and structural benchmark adapters.

## Canonical master equation

Let

\[
\mathsf H_\alpha=I-\mathsf O_\alpha
\]

separate retained hidden directions from the sector directly accessible to
readout \(\alpha\). The current native master architecture is

\[
\boxed{
\begin{gathered}
\delta_R\Longrightarrow\mathscr H_T,
\qquad
X_n=(\Phi_n,\Psi_n)^\top,
\qquad
\mathbb G_T
=L_R\otimes I+I\otimes C_{\mathcal F}+C_{\rm int},
\\[1mm]
\mathcal E_{\rm DRL}[X]_n
:=\frac{\delta S_{\rm DRL}}{\delta X_n}
=\mathcal J_{C,\alpha,n}[X_n],
\\[1mm]
\mathcal T_{n+1}
=\mathcal T_n\oplus
\Lambda_{T,\alpha,n}\mathsf H_\alpha X_n,
\\[1mm]
r_{\alpha,n}=A_\alpha\mathsf O_\alpha X_n-\delta_{\alpha,n},
\qquad
P_{\alpha,n}=\Pi_\alpha(r_{\alpha,n}),
\\[1mm]
I_R(P_{\alpha,n}\mid\Pi_\alpha)
=-\log_2p_{\Pi_\alpha}(P_{\alpha,n})\;\mathrm{rbit}.
\end{gathered}
}
\]

The balanced flux operator is

\[
\begin{aligned}
\mathcal J_{C,\alpha}[X]
={}&
\mathsf H_\alpha W_\alpha\mathsf O_\alpha X
-
\mathsf O_\alpha\Lambda_{W,\alpha}\mathsf O_\alpha X
\\
&+
\mathsf O_\alpha R_\alpha\mathsf H_\alpha X
-
\mathsf H_\alpha(\Lambda_{R,\alpha}+\Lambda_{T,\alpha})
\mathsf H_\alpha X.
\end{aligned}
\]

This is a `Dr` architecture. The cut/tape terms are not yet derived from the
DRL action.

## Exact finite-flow reduction

AP15 realizes the cut with nonnegative readable, hidden and tape quantities:

\[
\dot q_O=-\operatorname{diag}(\mathbf1^TW)q_O+Rq_H,
\]

\[
\dot q_H=Wq_O-\operatorname{diag}(\mathbf1^TR+\ell)q_H,
\]

\[
\dot q_T=\ell^Tq_H.
\]

Within this model,

\[
\frac{d}{dt}(\mathbf1^Tq_O+\mathbf1^Tq_H+q_T)=0
\]

exactly. Eliminating the hidden sector gives

\[
K_{\rm mem}(u)=Re^{-\Lambda_Hu}W.
\]

Thus `R=0` produces exact visible damping in the finite model, while `R>0`
produces delayed return memory.

## Recorded discoveries

See [`URR_C_DISCOVERIES.md`](URR_C_DISCOVERIES.md) for the binding ledger. The
current concise list is:

1. existence, retention, accessibility and readability are distinct;
2. readable loss can coexist with exact total retention;
3. one-way write gives visible damping in the finite flow model;
4. return gives a memory kernel;
5. return edges alter observability and nullity;
6. append-only tape can retain content outside direct readout;
7. horizon-ness is a channel-asymmetry readout;
8. black-hole language is one optional special case;
9. the sharpened open problem is a unified DRL–cut–tape action.

## Install and run

Core DRL smoke test:

```bash
python -m pip install numpy pyyaml
python v2/urr/smoke_test.py
```

Benchmark dependencies and reruns:

```bash
python -m pip install -r v2/urr/requirements-benchmarks.txt
python ap/ap13_urr_fput.py
python ap/ap14_urr_desi_dr2.py
python ap/ap15_read_write_cut.py \
  --output ap/results/AP15_READ_WRITE_CUT_RESULTS.json
```

Recorded full external runs:

```bash
python ap/ap13_urr_fput.py --full
python ap/ap14_urr_desi_dr2.py --full
```

## Binding boundary

- DRL reader recurrence and `D`-cancellation have support only in their declared scopes.
- The linear mirror variable does not prove mechanistic handoff from reader to record.
- The append-only tape remains a separate construction.
- No unified DRL–cut–tape action is claimed.
- AP13 is an external numerical benchmark.
- AP14 uses cosmology as a `Dr` adapter; cosmology is not derived from URR-C.
- AP15 is a finite structural smoke test; it does not derive black holes or prove universal linearity.
- All runtime outputs remain `finite_diagnostic`.
