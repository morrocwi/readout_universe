# AP14 — URR–DESI DR2 Hard Cosmology Benchmark

## 0. Data provenance

The 13-component compressed BAO distance vector (`DATA` in `ap14_urr_desi_dr2.py`,
also duplicated in `ap/data/DESI_DR2_BAO_COVARIANCE.txt`) is transcribed from:

> DESI Collaboration, "DESI DR2 Results II: Measurements of Baryon Acoustic
> Oscillations and Cosmological Constraints," arXiv:2503.14738 (2025),
> Table IV ("Constraints on the BAO scaling parameters and distance ratios"),
> Section III.1.

Verification performed for this note: every one of the 13 `D_V/r_d`,
`D_M/r_d`, `D_H/r_d` values in the script (e.g. `7.94167639` for BGS
`z=0.295`, `38.988973961958784` for Lyα `D_M/r_d` at `z=2.33`) matches the
paper's Table IV central values to the precision quoted there (3 decimal
places). The per-bin `D_M`/`D_H` correlation coefficients `r_M,H` quoted in
Table IV (e.g. `-0.459` for LRG1) are consistent with the off-diagonal
covariance blocks used here once reconstructed at full precision
(`corr = cov_offdiag / sqrt(var_DM * var_DH)`), so the covariance matrix in
this script is a full-precision reconstruction of Table IV's quoted
sigmas and correlation coefficients, not an independently-sourced
covariance table.

The `official` flat-ΛCDM comparison values in `fit_lcdm()`
(`Omega_m = 0.2975 +/- 0.0086`, `h*r_d = 101.54 +/- 0.73` Mpc) match the
DESI-BAO-alone flat-ΛCDM constraint reported in the same paper's Section VI
cosmology-constraints discussion (external secondary sources corroborate
these exact central values and a `chi2/dof = 10.2/(13-2)` for the BAO-only
fit, consistent with this script's own `chi2=10.271`, `dof=11`). The precise
table number inside Section VI for that specific BAO-alone row was not
independently pinned down in this pass — flag this as a **TODO for the
founder**: confirm the exact table/row (likely one of the ΛCDM parameter
tables in Section VI) and record it here.

Because the raw distance-vector match (Table IV) is exact to quoted
precision while the flat-ΛCDM comparison numbers are strongly corroborated
but not yet pinned to an exact table row, the harness gate below is worded
as "data vector: cited (Table IV)" rather than an unqualified "official ...
PASS", and the comparison-fit gate is worded as "corroborated, table row
unconfirmed."

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

This is a successful reproduction of the DESI DR2 BAO-alone flat-LCDM
constraint quoted in the source paper (see §0 for the citation and the
table-number caveat on this specific comparison row).

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
| Public data vector cited (arXiv:2503.14738, Table IV; numbers verified to quoted precision) | PASS |
| Covariance reconstructed from Table IV sigmas + r_M,H at full precision (not an independently-sourced covariance table) | PASS |
| Independent implementation | PASS |
| Reproduces DESI-BAO-alone flat-LCDM parameters (values corroborated; exact Section VI table row unconfirmed — TODO founder) | CORROBORATED, TABLE ROW TODO |
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
data_provenance:
  distance_vector: "arXiv:2503.14738 Table IV, verified to quoted precision"
  covariance: "reconstructed from Table IV sigmas + r_M,H, not independently sourced"
  lcdm_comparison_row: "corroborated, exact Section VI table number TODO (founder)"
```

This is a serious benchmark against a cited public data vector (see §0), not
evidence that the complete cosmological model has been derived from retained
distinction alone.
