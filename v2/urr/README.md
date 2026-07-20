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
3. [`urr_system_spec.yaml`](urr_system_spec.yaml) — machine-readable contract.
4. [`urr_reference_runner.py`](urr_reference_runner.py) — executable reference implementation.
5. [`example_ring.yaml`](example_ring.yaml) — smallest complete runnable example.
6. [`CLAIM_LEDGER.yaml`](CLAIM_LEDGER.yaml) — novelty, evidence and non-claims.
7. [`EXECUTED_RUNS.md`](EXECUTED_RUNS.md) — recorded commands and numerical outputs.
8. AP13 and AP14 in [`../../ap/`](../../ap/) — external benchmark adapters.

## Native equation

\[
\delta_R\to\mathscr H_T\to\mathbb G_T\to
X_n=(\Phi_n,\Psi_n)^\top\to S_{\rm DRL}\to
(A_\alpha,\Pi_\alpha)\to P_\alpha.
\]

The state equation is generated from the discrete action in the technical
specification. A reported value is always a readout and never silently
promoted to truth.

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
- AP13 is an external numerical benchmark.
- AP14 uses cosmology as a `Dr` readout adapter; cosmology is not derived from
  URR.
- All runtime outputs remain `finite_diagnostic`.
