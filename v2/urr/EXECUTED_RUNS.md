# URR Executed Runs

All results in this file are `finite_diagnostic`. Timings are intentionally
omitted because they are machine-specific unless a timing study is separately
registered.

## Native smoke test

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

Machine-readable record:
`v2/urr/results/smoke_report.json`.

## AP13 full FPUT run

Command:

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

Canonical record:
`ap/results/AP13_FPUT_RESULTS.json`.

## AP14 full DESI DR2 run

Command:

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

Canonical record:
`ap/results/AP14_DESI_DR2_RESULTS.json`.

## Reproduction rule

A rerun may differ in the final few digits because of library, platform, and
optimizer differences. A material change requires:

1. saving the new JSON and CSV;
2. recording package versions and command;
3. comparing against the canonical result;
4. explaining whether the difference is numerical, implementation-related,
   or a genuine falsification.
