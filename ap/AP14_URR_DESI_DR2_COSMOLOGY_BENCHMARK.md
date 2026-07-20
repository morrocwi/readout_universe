# AP14 — URR–DESI DR2 Hard Cosmology Benchmark

## 1. Problem

This benchmark treats cosmology as an **external readout adapter** of the native
Universal Retention–Readout System. It does not insert cosmology into the URR
kernel.

The retained record is the 13-component DESI DR2 BAO vector

\[
\delta =
\left(D_V/r_d, D_M/r_d, D_H/r_d, \ldots\right),
\]

covering redshifts from 0.295 to 2.33 with the published non-diagonal
covariance matrix \(C\).

For parameters \(\theta\), the external readout operator produces

\[
\widehat\delta=A_{\rm cosmo}(\theta),
\qquad
r(\theta)=A_{\rm cosmo}(\theta)-\delta,
\]

and the native residual obstruction is

\[
2V(\theta)=\chi^2(\theta)=r^\top C^{-1}r.
\]

The flat-universe readouts are

\[
\frac{D_H(z)}{r_d}
=
\frac{c}{100(h r_d)E(z)},
\]

\[
\frac{D_M(z)}{r_d}
=
\frac{c}{100(h r_d)}\int_0^z\frac{dz'}{E(z')},
\]

\[
\frac{D_V(z)}{r_d}
=
\left[z\frac{D_H}{r_d}
\left(\frac{D_M}{r_d}\right)^2\right]^{1/3}.
\]

Two adapters are tested:

1. flat \(\Lambda\)CDM: \(\theta=(\Omega_m,h r_d)\);
2. CPL \(w_0w_a\)CDM:
   \(\theta=(\Omega_m,h r_d,w_0,w_a)\).

For CPL,

\[
E^2(z)=\Omega_m(1+z)^3+
(1-\Omega_m)(1+z)^{3(1+w_0+w_a)}
\exp\left[-\frac{3w_a z}{1+z}\right].
\]

## 2. Flat Lambda-CDM reproduction test

Our independent result is

\[
\boxed{
\Omega_m=0.29746182\pm0.00857550
}
\]

and

\[
\boxed{
h r_d=101.53977322\pm0.73276161\ \mathrm{Mpc}
}.
\]

The parameter correlation is

\[
\rho(\Omega_m,h r_d)=-0.923401.
\]

Fit quality:

- chi-square = 10.27104100
- degrees of freedom = 11
- goodness-of-fit p = 0.506184

The official DESI DR2 paper quotes

\[
\Omega_m=0.2975\pm0.0086,
\qquad
h r_d=(101.54\pm0.73)\ \mathrm{Mpc}.
\]

Difference between our implementation and the quoted central values:

- Omega_m: -3.81809324e-05 = -0.004440 quoted sigma
- h r_d: -2.26777498e-04 Mpc = -0.000311 quoted sigma

This is a successful external reproduction test.

## 3. CPL dynamical-dark-energy stress test

Five independent differential-evolution seeds converged to the same basin.

Best fit:

\[
\boxed{
(\Omega_m,h r_d,w_0,w_a)
=
(0.386606,
91.249658,
-0.178834,
-2.716673)
}
\]

with

\[
\chi^2_{\rm CPL}=5.61860003.
\]

The raw improvement is

\[
\Delta\chi^2
=
\chi^2_{\Lambda\rm CDM}-\chi^2_{\rm CPL}
=
4.65244097.
\]

For two extra parameters, the likelihood-ratio reference p-value is

\[
p=0.097664.
\]

Information criteria:

| Model | chi-square | AIC | BIC |
|---|---:|---:|---:|
| flat Lambda-CDM | 10.271041 | 14.271041 | 15.400940 |
| CPL w0wa | 5.618600 | 13.618600 | 15.878397 |

The CPL best fit lies in the same qualitative quadrant emphasized by DESI:

\[
w_0>-1,\qquad w_a<0.
\]

However, the local Fisher condition number is

\[
\kappa(F)=1.198694\times10^6,
\]

showing severe BAO-only degeneracy. Therefore the correct URR verdict is:

```text
BETTER RAW FIT, BUT NOT A STANDALONE DISCOVERY.
```

The local errors are not a substitute for a full posterior.

## 4. Why this is a hard test

This run combines:

- 13 correlated measurements;
- six transverse/longitudinal covariance blocks;
- nonlinear distance integrals;
- a global four-parameter search;
- multi-start basin verification;
- local identifiability analysis;
- covariance whitening;
- nested-model and information-criterion comparisons;
- direct reproduction of an official collaboration result.

## 5. Harness result

| Gate | Result |
|---|---|
| Official public data vector | PASS |
| Official covariance | PASS |
| Independent implementation | PASS |
| Reproduces published Lambda-CDM parameters | PASS |
| Multi-start global CPL fit | PASS |
| Residual covariance handled | PASS |
| Identifiability reported | PASS |
| Full DESI CMB/SN likelihood reproduced | NOT CLAIMED |
| Cosmology derived from URR | NOT CLAIMED |

## 6. Scientific interpretation

This benchmark demonstrates that the URR readout/residual architecture can
host a real current cosmological inference problem without changing the native
kernel.

Its strongest result is not that URR predicts dark energy. It is that the same
native discipline correctly separates:

1. **record** — the DESI distance vector;
2. **operator** — the chosen cosmology adapter;
3. **residual** — covariance-weighted model-data mismatch;
4. **null space** — the highly degenerate CPL directions;
5. **policy** — the model-comparison rule;
6. **claim tier** — finite diagnostic, not theorem.

## 7. Claim status

```yaml
tier: finite_diagnostic
external_adapter: Dr
core_modified: false
verdict: PASS
```

This is a serious external benchmark, not evidence that the complete
cosmological model has been derived from retained distinction alone.
