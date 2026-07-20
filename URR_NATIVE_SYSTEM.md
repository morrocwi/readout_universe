# URR Native System — Entry Point

This file is the root-level entry point for the native
**Universal Retention–Readout System (URR)** calculation layer added on top of
the existing Readout Universe philosophy and logic corpus.

## Start here

1. [`v2/urr/README.md`](v2/urr/README.md) — package purpose and commands.
2. [`v2/urr/KNOWLEDGE_MAP.md`](v2/urr/KNOWLEDGE_MAP.md) — dependency and evidence map.
3. [`v2/urr/URR_NATIVE_TECHNICAL_SPEC.md`](v2/urr/URR_NATIVE_TECHNICAL_SPEC.md) — native equations, pseudocode, DAG and claim boundaries.
4. [`v2/urr/urr_system_spec.yaml`](v2/urr/urr_system_spec.yaml) — machine-readable system contract.
5. [`v2/urr/urr_reference_runner.py`](v2/urr/urr_reference_runner.py) — executable reference runner.
6. [`v2/urr/CLAIM_LEDGER.yaml`](v2/urr/CLAIM_LEDGER.yaml) — novelty and evidence ledger.
7. [`v2/urr/EXECUTED_RUNS.md`](v2/urr/EXECUTED_RUNS.md) — canonical run records.

## External benchmark adapters

- [AP13 — nonlinear FPUT external benchmark](ap/AP13_URR_FPUT_EXTERNAL_BENCHMARK.md)
- [AP14 — DESI DR2 correlated BAO inverse benchmark](ap/AP14_URR_DESI_DR2_COSMOLOGY_BENCHMARK.md)

AP13 and AP14 are executable finite diagnostics. AP14's cosmology equations
are an external `Dr` readout adapter, not a derivation of cosmology from URR.

## Core boundary

The native kernel contains retained distinction, finite relational grammar,
reader–record DRL dynamics, explicit readout, identifiability gates, claim
tiers, and the native information unit `rbit`.

Quantum postulates, relativity postulates, and other domain theories are not
part of the native kernel. External adapters do not inherit native evidence
tiers automatically.
