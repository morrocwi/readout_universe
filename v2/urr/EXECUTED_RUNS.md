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
