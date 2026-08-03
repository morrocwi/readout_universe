# URR-C Executed Runs

All numerical results in this file are `finite_diagnostic`. Timings are
intentionally omitted because they are machine-specific unless a timing study
is separately registered.

Exact algebraic identities are recorded in the technical documents and claim
ledger; they are not created by a numerical run.

## Native DRL smoke test

Command:

```bash
python v2/urr/smoke_test.py
```

Recorded result:

```text
verdict: PASS
reader EL residual max: 2.76489942052649e-12
mirror EL residual max: 2.1074461620251839e-13
pairing-charge relative drift: 7.4358593633583325e-06
tape conservation total error: 7.549516567451064e-15
```

Machine-readable record: `v2/urr/results/smoke_report.json`.

## AP13 full FPUT run

```bash
python ap/ap13_urr_fput.py --full \
  --output ap/results/AP13_FPUT_RESULTS_REPRO.json \
  --csv ap/results/AP13_FPUT_RESULTS_REPRO.csv
```

Selected recorded results at `dt=0.01`:

```text
standard final relative state error: 9.230488983027812e-08
standard observed order: 2.0000160195221275
standard max relative energy drift: 2.290795599879658e-07
DRL final relative state error: 2.9895843820460835e-07
DRL observed order: 2.000024997286302
DRL pairing-charge relative drift: 3.292722445071873e-10
```

Canonical record: `ap/results/AP13_FPUT_RESULTS.json`.

## AP14 full DESI DR2 run

```bash
python ap/ap14_urr_desi_dr2.py --full \
  --output ap/results/AP14_DESI_DR2_RESULTS_REPRO.json \
  --csv ap/results/AP14_DESI_DR2_FIT_TABLE_REPRO.csv
```

Selected recorded results:

```text
Omega_m: 0.29746181906755703
h r_d [Mpc]: 101.53977322250158
official central-value differences: -0.00444 sigma, -0.000311 sigma
Lambda-CDM chi2/dof: 10.271041002564871 / 11
CPL best fit: [0.3866058050, 91.24965832, -0.17883402, -2.71667347]
CPL Fisher condition number: 1.1986937389955192e6
```

Canonical record: `ap/results/AP14_DESI_DR2_RESULTS.json`.

## AP15 Read–Write Cut smoke test

```bash
python ap/ap15_read_write_cut.py \
  --output ap/results/AP15_READ_WRITE_CUT_RESULTS.json
```

Recorded result:

```text
verdict: PASS
one-way horizon index: 0.9999999999999973
reciprocal horizon index: 0.4999999999999993
leaky horizon index: 0.9523809523809499
one-way observability rank/nullity: 3 / 4
reciprocal observability rank/nullity: 6 / 1
leaky observability rank/nullity: 6 / 1
one-way final visible quantity: 0.010762744228616037
one-way final hidden quantity: 0.9892372557713833
one-way-with-tape final hidden quantity: 0.6978201445561787
tape final quantity: 0.29141711121520486
max total-retention error: 5.10702591327572e-15
```

Runtime interpretation:

- the finite generator conserves total retained quantity to floating-point
  precision;
- a return channel reduces the recorded dynamical readout null space;
- a one-way cut follows exact visible damping in the declared finite model;
- positive tape writes are append-only;
- these results do not derive black-hole dynamics or the cut from DRL.

Canonical records:

- `ap/results/AP15_READ_WRITE_CUT_RESULTS.json`
- `v2/urr/URR_CUT_EXTENSION.md`
- `v2/urr/URR_C_DISCOVERIES.md`

## AP17 Return Transformation and Physical Readability

```bash
python ap/ap17_return_transformation.py \
  --output ap/results/AP17_RETURN_TRANSFORMATION_RESULTS.json
```

Recorded result:

```text
verdict: PASS
transformed-return rank: 2
distance from identity: 1.222171974564525
noiseless decoder error: 2.289691319182597e-16
Gaussian readable information: 7.825375266365017 rbit
partial-return rank/nullity: 1 / 1
no-return readable information: 0 rbit
echo time: 0.885
echo amplitude: 0.8972693231816911
hidden-elimination max residual: 6.189493362285248e-15
finite-window rank: 1 -> 2 -> 3
```

Runtime interpretation:

- a return map can differ strongly from the identity while a declared decoder
  reconstructs the noiseless encoded input;
- a rank-deficient return preserves only a subspace;
- a zero return kernel gives zero readable information under the declared
  linear-Gaussian channel;
- a hidden cross-coordinate response can produce a delayed echo;
- a longer observation window can turn an instantaneous null direction into a
  dynamically observable direction;
- the full block dynamics and exact hidden-elimination memory identity agree to
  floating-point precision.

Canonical records:

- `ap/AP17_RETURN_TRANSFORMATION_READABILITY.md`
- `ap/ap17_return_transformation.py`
- `ap/results/AP17_RETURN_TRANSFORMATION_RESULTS.json`
- `v2/urr/URR_C_MASTER_0_4.md`
- `v2/urr/URR_C_MASTER_0_4.yaml`

## AP18 Two-Capacitor RC Memory Cell

```bash
python ap/ap18_rc_memory_cell.py \
  --output ap/results/AP18_RC_MEMORY_CELL_RESULTS.json
```

Recorded result:

```text
verdict: PASS
numerical vs matrix exponential: 5.062616992290714e-13 V
matrix exponential vs closed form: 3.108624468950438e-14 V
relative charge-retention error: 1.0842021724855044e-15
relative energy-accounting error: 1.6666663917030977e-07
hidden-elimination residual: 5.2081678081350447e-08 V/s
visible-only observability rank: 2
maximum hidden-to-visible signal: 0.49997730003511887 V
```

Runtime interpretation:

- the ideal two-capacitor circuit maps directly to the declared linear
  visible-hidden adapter;
- total charge is the retained functional in this model;
- capacitor-stored electrical energy decreases while resistor heat accounts for
  the loss;
- eliminating the second capacitor produces the declared exponential memory
  kernel;
- two histories that are identical in the visible snapshot can become
  distinguishable through the later visible voltage trace;
- this is a numerical ideal-circuit execution, not a hardware measurement and
  not a test of the inertial DRL term.

Canonical records:

- `ap/AP18_RC_MEMORY_CELL.md`
- `ap/ap18_rc_memory_cell.py`
- `ap/results/AP18_RC_MEMORY_CELL_RESULTS.json`
## URR-C foundational chain — Coq compile, 2026-07-20

Note on scope: this file's header restricts it to `finite_diagnostic` numerical
runs; a `coqc` compile is a `Th_coqc`-tier machine check, not a numerical
result. This entry is a pointer only — the canonical dated executed-run row
lives in `docs/VERIFIED_RUNS.md` ("2026-07-20 — development workstation
(ANSE.ASIA workstation, Coq 8.20.1) — URR-C foundational chain compiles"), per that
file's own rule that a `Th_coqc` claim must have a dated run recorded there.

```bash
make verify-urr-coq
```

Recorded result (development workstation, coqc 8.20.1, git rev
`daa2f36274bd2afb466de46c5e6f11220beeba9a`):

```text
exit code: 0
Print Assumptions (URR_C_Foundational_Chain.v, 7/7 Closed under the global context):
  F0_RD4_retained_difference_injective
  F3_lifted_recompose
  F4_master_implies_component_equations
  F5_balanced_cut_conserves_declared_total
  F6_append_cell_injective
  F7_declared_left_decoder_recovers_message
  foundational_master_chain_core
Admitted/Axiom/admit./Parameter scan of URR_C_Foundational_Chain.v: no matches
```

This is a tier CORRECTION of the manifest in `v2/urr/URR_C_COQ_FORMAL_CHAIN.yaml`
and `v2/urr/URR_C_COQ_FORMAL_CHAIN.md`, not a new proof — no new theorem or
physics was added. The manifest previously read `machine_checked_now: false`
because the machine that drafted it had no coqc available, not because the
proof failed.

Canonical records:

- `docs/VERIFIED_RUNS.md`
- `v2/urr/URR_C_COQ_FORMAL_CHAIN.yaml`
- `v2/urr/URR_C_COQ_FORMAL_CHAIN.md`

## Evidence-tier rule

```text
exact_algebra in a declared model
    != finite_diagnostic execution
    != Dr interpretation
    != unrestricted theorem about nature
```

## Reproduction rule

A material rerun change requires:

1. saving the new machine-readable artifacts;
2. recording package versions and the command;
3. comparing against the canonical result;
4. explaining whether the change is numerical, implementation-related, or a
   genuine falsification.
