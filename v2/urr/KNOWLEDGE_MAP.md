# URR-C Knowledge Map

## 1. Root and doctrine

| Layer | Native object | Canonical source | Status |
|---|---|---|---|
| Root | retained distinction `delta_R` | `v2/INFORMATION_DNA.md` | doctrine/root |
| Quantity | relational projection, not self-property | `v2/DOCTRINE_OF_QUANTITY.md` | doctrine |
| Translation | external problems enter through an explicit lens | `v2/TRANSLATION_PROTOCOL.md` | workflow |
| Claim control | `Th_coqc / exact_algebra / finite_diagnostic / Dr / Open` | claim ledgers | binding |

## 2. Current reading order

```text
URR_NATIVE_SYSTEM.md
    -> v2/urr/URR_CUT_EXTENSION.md       canonical master equation
    -> v2/urr/URR_C_MASTER.yaml          machine-readable contract
    -> v2/urr/URR_C_DISCOVERIES.md       discovery and tier ledger
    -> v2/urr/URR_NATIVE_TECHNICAL_SPEC.md
    -> v2/urr/CLAIM_LEDGER.yaml
    -> executable evidence AP13–AP15
```

## 3. Native mathematical kernel

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

## 4. URR-C master extension

```text
native URR state and DRL
    -> observer/readout projector O_alpha
    -> retained hidden projector H_alpha = I - O_alpha
    -> write channel W_alpha: accessible -> hidden
    -> return channel R_alpha: hidden -> accessible
    -> source-sector outflow balancers Lambda_W and Lambda_R
    -> append-only operator Lambda_T
    -> balanced directed flux J_C
    -> tape retention
    -> readout residual and policy
```

Canonical master:

\[
\boxed{
\begin{gathered}
\delta_R\Longrightarrow\mathscr H_T,
\qquad
X_n=(\Phi_n,\Psi_n)^\top,
\qquad
\mathsf H_\alpha=I-\mathsf O_\alpha,
\\
\frac{\delta S_{\rm DRL}}{\delta X_n}
=\mathcal J_{C,\alpha,n}[X_n],
\\
\mathcal T_{n+1}
=\mathcal T_n\oplus\Lambda_{T,\alpha,n}\mathsf H_\alpha X_n,
\\
r_{\alpha,n}=A_\alpha\mathsf O_\alpha X_n-\delta_{\alpha,n},
\qquad
P_{\alpha,n}=\Pi_\alpha(r_{\alpha,n}).
\end{gathered}
}
\]

Canonical files:

- `v2/urr/URR_CUT_EXTENSION.md`
- `v2/urr/URR_C_MASTER.yaml`
- `v2/urr/URR_C_DISCOVERIES.md`

Status:

- DRL kernel: derived only in declared scopes;
- balanced cut architecture: `Dr`;
- finite flow conservation and elimination: `exact_algebra` in AP15 scope;
- runtime evidence: `finite_diagnostic`;
- unified DRL–cut–tape action: `Open`.

## 5. AP15 reduction graph

```text
balanced cut architecture
    -> positive finite-flow realization q=(q_O,q_H,q_T)
    -> zero generator column sums
       -> exact total retention
    -> set R=0
       -> exact visible damping
       -> hidden readout null space
    -> set R>0
       -> eliminate q_H
       -> memory kernel K_mem(u)=R exp(-Lambda_H u) W
       -> improved dynamical observability
    -> set Lambda_T>0
       -> append-only tape
```

## 6. Discoveries graph

| ID | Discovery | Tier |
|---|---|---|
| D0 | existence, retention, accessibility and readability are distinct | doctrine/definition |
| D1 | readable loss can coexist with exact total retention | exact finite model + `Dr` general reading |
| D2 | one-way write gives exact visible damping in AP15 | exact algebra |
| D3 | return gives an explicit memory kernel | exact algebra in finite linear scope |
| D4 | return edges change observability and nullity | exact recorded matrices + finite diagnostic |
| D5 | append-only tape can retain quantity after hidden working-state change | exact construction + finite diagnostic |
| D6 | horizon-ness is a channel-asymmetry readout | definition + `Dr` |
| D7 | black-hole language is one optional special case | `Dr` |
| D8 | frontier is a unified DRL–cut–tape action or no-go result | `Open` |

Binding details and safe wording:

- `v2/urr/URR_C_DISCOVERIES.md`
- `v2/urr/CLAIM_LEDGER.yaml`

## 7. Evidence graph

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
       - independent-solver cross-check, nonlinear many-body (self-generated ICs)
    -> AP14
       - current correlated inverse-problem adapter
    -> URR-C + AP15
       - balanced cut, retention, memory and observability smoke test
```

Evidence tiers do not flow upward automatically. An AP result is not a theorem,
an exact identity remains limited to its stated model, and a domain adapter
does not become native ontology.

## 8. Benchmark placement

### AP13 — FPUT nonlinear lattice

Purpose: test numerical consistency of the conservative reduction and the
nonlinear DRL reader–record extension against an independent high-order ODE
solver.

Files:

- `ap/AP13_URR_FPUT_SOLVER_CROSSCHECK.md`
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
- reciprocal, leaky, one-way and reverse channel classes;
- horizon/asymmetry index values;
- exact visible damping when `R=0` in the finite linear realization;
- return-memory structure when `R>0`;
- observability rank and null-space changes;
- append-only tape monotonicity.

Files:

- `v2/urr/URR_CUT_EXTENSION.md`
- `v2/urr/URR_C_MASTER.yaml`
- `v2/urr/URR_C_DISCOVERIES.md`
- `ap/AP15_READ_WRITE_CUT.md`
- `ap/ap15_read_write_cut.py`
- `ap/results/AP15_READ_WRITE_CUT_RESULTS.json`

Tier: runtime `finite_diagnostic`; cut architecture `Dr`; unified action
`Open`.

## 9. Novelty boundary

Candidate novelty is restricted to the conjunction of:

1. discrete graph-tensor DRL using the retention metric and antisymmetric
   retention structure;
2. ontic record reading of `Psi` rather than a disposable auxiliary copy;
3. zero-diagonal retention metric as a dynamical form of the Doctrine of
   Quantity;
4. one native AI contract connecting action, residual, readout, null space,
   tier control, and `rbit` conversion;
5. balanced directed write/return cuts, dynamical accessibility, return-memory,
   append-only retention and claim-tier control in the same native architecture.

Not individually novel: graph Laplacians, projectors, doubled-variable methods,
finite differences, Shannon information, Landauer conversion, matrix rank,
covariance-weighted least squares, linear compartment models, observability
matrices, or memory kernels obtained by eliminating hidden variables.

## 10. Open frontier

- derive or reject a unified action realizing DRL, balanced directed cuts and
  injective append-only tape;
- prove or falsify the ontic-record and URR-C conjunction against the full
  literature;
- generalize formal EL equivalence beyond the currently declared scope;
- determine when nonlinear hidden-sector elimination preserves positivity,
  stability and finite retention;
- derive domain-specific `W`, `R`, and projectors from external records rather
  than choosing them by hand;
- obtain external peer review before promoting any novelty claim.
