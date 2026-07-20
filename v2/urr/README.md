# URR Native System — AI Calculation Layer

This directory is the canonical native calculation package for the
**Universal Retention–Readout System (URR)**.

It is deliberately narrower than a theory-of-everything claim. The kernel
contains retained distinction, a finite relation operator, reader–record DRL
dynamics, explicit readout, identifiability checks, claim tiers, and the native
information unit `rbit`. Quantum theory, relativity, and all other domain
models are optional external adapters and do not modify the kernel.

## Reading order for an AI

1. [`KNOWLEDGE_MAP.md`](KNOWLEDGE_MAP.md) — scope, dependency graph and claim boundaries.
2. [`URR_NATIVE_TECHNICAL_SPEC.md`](URR_NATIVE_TECHNICAL_SPEC.md) — equations and normative pseudocode.
3. [`URR_CUT_EXTENSION.md`](URR_CUT_EXTENSION.md) — general read–write cut, memory kernel and observability extension.
4. [`urr_system_spec.yaml`](urr_system_spec.yaml) — machine-readable native contract.
5. [`urr_reference_runner.py`](urr_reference_runner.py) — executable reference implementation.
6. [`example_ring.yaml`](example_ring.yaml) — smallest complete runnable example.
7. [`CLAIM_LEDGER.yaml`](CLAIM_LEDGER.yaml) — novelty, evidence and non-claims.
8. [`EXECUTED_RUNS.md`](EXECUTED_RUNS.md) — recorded commands and numerical outputs.
9. AP13–AP15 in [`../../ap/`](../../ap/) — external and structural benchmark adapters.

## Native equation

\[
\delta_R\to\mathscr H_T\to\mathbb G_T\to
X_n=(\Phi_n,\Psi_n)^\top\to S_{\rm DRL}\to
(A_\alpha,\Pi_\alpha)\to P_\alpha.
\]

The state equation is generated from the discrete action in the technical
specification. A reported value is always a readout and never silently
promoted to truth.

## URR-C extension

The read–write cut adds observer-relative accessible and hidden sectors:

\[
\mathsf H_\alpha=I-\mathsf O_\alpha,
\qquad
\mathcal C_\alpha
=
\mathsf H_\alpha W_\alpha\mathsf O_\alpha
+
\mathsf O_\alpha R_\alpha\mathsf H_\alpha.
\]

The candidate extended equation is

\[
\frac{\delta S_{\rm DRL}}{\delta X}=\mathcal C_\alpha X.
\]

This is a `Dr` architecture. The cut term is not yet derived from the DRL
action. AP15 tests a finite retained-flow realization in which one-way write,
leaky return, memory, append-only tape and readout null spaces are all explicit.

## Install and run

Core smoke test:

```bash
python -m pip install numpy pyyaml
python v2/urr/smoke_test.py
```

Benchmark dependencies and quick reruns:

```bash
python -m pip install -r v2/urr/requirements-benchmarks.txt
python ap/ap13_urr_fput.py
python ap/ap14_urr_desi_dr2.py
python ap/ap15_read_write_cut.py \
  --output ap/results/AP15_READ_WRITE_CUT_RESULTS.json
```

Recorded full runs:

```bash
python ap/ap13_urr_fput.py --full
python ap/ap14_urr_desi_dr2.py --full
```

## Binding boundary

- DRL reader recurrence and the `D`-cancellation structure have formal or
  executed support only in their declared scopes.
- The linear mirror variable does not prove mechanistic handoff from reader to
  record.
- The append-only tape is a separate construction; no unified DRL+tape action
  is claimed.
- URR-C supplies a general cut grammar, but no unified DRL+cut action is
  claimed.
- AP13 is an external numerical benchmark.
- AP14 uses cosmology as a `Dr` readout adapter; cosmology is not derived from
  URR.
- AP15 is a finite structural smoke test; it does not derive black holes or
  prove that every real system is a linear retained-flow system.
- All runtime outputs remain `finite_diagnostic`.
