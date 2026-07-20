# URR Knowledge Map

## 1. Root and doctrine

| Layer | Native object | Canonical source | Status |
|---|---|---|---|
| Root | retained distinction `delta_R` | `v2/INFORMATION_DNA.md` | doctrine/root |
| Quantity | relational projection, not self-property | `v2/DOCTRINE_OF_QUANTITY.md` | doctrine |
| Translation | external problems enter through an explicit lens | `v2/TRANSLATION_PROTOCOL.md` | workflow |
| Claim control | `Th_coqc / finite_diagnostic / Dr / Open` | root README and claim ledgers | binding |

## 2. Native mathematical kernel

```text
retained distinctions
    -> finite retained relation/history structure
    -> L_R and finite internal fiber
    -> universal grammar G_T
    -> reader-record state X=(Phi,Psi)
    -> Discrete Retention Lagrangian
    -> Euler-Lagrange recurrences
    -> explicit readout A_alpha
    -> residual and null-space diagnostics
    -> policy Pi_alpha
    -> finite reported readout P_alpha
```

Canonical files:

- `v2/urr/URR_NATIVE_TECHNICAL_SPEC.md`
- `v2/urr/urr_system_spec.yaml`
- `v2/urr/urr_reference_runner.py`

## 3. URR-C extension

```text
native URR state and DRL
    -> observer/readout projector O_alpha
    -> retained hidden projector H_alpha = I - O_alpha
    -> write channel W_alpha: visible -> hidden
    -> return channel R_alpha: hidden -> visible
    -> directed Read-Write Cut C_alpha
    -> horizon/asymmetry readout chi_alpha
    -> hidden-sector elimination
    -> visible damping or return-memory kernel
    -> dynamical observability and null-space test
```

Canonical source:

- `v2/urr/URR_CUT_EXTENSION.md`

Status:

- cut architecture: `Dr`;
- finite linear conservation and elimination identity: exact algebra in the
  declared AP15 model;
- runtime evidence: `finite_diagnostic`;
- derivation of the cut from the DRL action: `Open`.

## 4. Evidence graph

```text
DRL philosophy/definition
    -> evidence/DRL_Discrete.v
       - finite-scope EL equivalence
       - D-cancellation identity
    -> evidence/DRL_General_Legendre.v
       - general-N pairing structure
    -> v2/urr/smoke_test.py
       - executable finite diagnostic
    -> AP13
       - external nonlinear many-body oracle
    -> AP14
       - current correlated inverse-problem adapter
    -> URR-C + AP15
       - directed cut, memory and observability smoke test
```

Evidence tiers do not flow upward automatically. In particular, an AP result
is not a theorem and a domain adapter does not become native ontology.

## 5. Benchmark placement

### AP13 — FPUT nonlinear lattice

Purpose: test numerical consistency of the conservative reduction and the
nonlinear DRL reader–record extension against an independent high-order ODE
solver.

Files:

- `ap/AP13_URR_FPUT_EXTERNAL_BENCHMARK.md`
- `ap/ap13_urr_fput.py`
- `ap/results/AP13_FPUT_RESULTS.json`
- `ap/results/AP13_FPUT_RESULTS.csv`

Tier: `finite_diagnostic`.

### AP14 — DESI DR2 correlated BAO inverse problem

Purpose: test whether the URR readout/residual discipline can host a hard,
current, covariance-aware inference task while preserving identifiability and
claim boundaries.

Files:

- `ap/AP14_URR_DESI_DR2_COSMOLOGY_BENCHMARK.md`
- `ap/ap14_urr_desi_dr2.py`
- `ap/results/AP14_DESI_DR2_RESULTS.json`
- `ap/results/AP14_DESI_DR2_FIT_TABLE.csv`
- `ap/data/DESI_DR2_BAO_COVARIANCE.txt`

Tier: numerical result `finite_diagnostic`; cosmology adapter `Dr`.

### AP15 — Universal Retention–Cut smoke test

Purpose: test a general read–write cut without assuming a black hole or any
other external physical theory.

The model separates readable, hidden and append-only sectors and checks:

- total retained-quantity conservation;
- reciprocal, leaky and one-way channel classes;
- horizon index values;
- exact visible damping when `R=0` in the finite linear realization;
- return-memory structure when `R>0`;
- observability rank and null-space changes;
- append-only tape monotonicity.

Files:

- `v2/urr/URR_CUT_EXTENSION.md`
- `ap/AP15_READ_WRITE_CUT.md`
- `ap/ap15_read_write_cut.py`
- `ap/results/AP15_READ_WRITE_CUT_RESULTS.json`

Tier: runtime `finite_diagnostic`; cut architecture `Dr`; unified DRL+cut
action `Open`.

## 6. Novelty boundary

Candidate novelty is restricted to the conjunction of:

1. discrete graph-tensor DRL using the retention metric and antisymmetric
   retention structure;
2. ontic record reading of `Psi` rather than a disposable auxiliary copy;
3. zero-diagonal retention metric as a dynamical form of the Doctrine of
   Quantity;
4. one native AI contract connecting action, residual, readout, null space,
   tier control, and `rbit` conversion;
5. URR-C's conjunction of retained accessibility, separate write and return
   channels, dynamical readout null spaces, and append-only retention.

Not individually novel: graph Laplacians, doubled-variable methods, finite
differences, Shannon information, Landauer conversion, matrix rank,
covariance-weighted least squares, linear compartment models, observability
matrices, or memory kernels obtained by eliminating hidden variables.

## 7. Open frontier

- derive or reject a unified action that realizes DRL, directed cuts and
  injective append-only tape;
- prove or falsify the ontic-record and URR-C conjunction against the full
  literature;
- generalize formal EL equivalence beyond the currently declared scope;
- determine when nonlinear hidden-sector elimination preserves positivity,
  stability and finite retention;
- design domain adapters with external records and explicit falsifiers;
- obtain an external peer review before promoting any novelty claim.
