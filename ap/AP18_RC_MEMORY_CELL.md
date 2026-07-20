# AP18 — Two-Capacitor RC Memory Cell

**Version:** `0.1.1`  
**Verdict:** `PASS`  
**Tier:** `finite_diagnostic`

## Declared ideal circuit

\[
C_1\dot V_1=-\frac{V_1-V_2}R,
\qquad
C_2\dot V_2=+\frac{V_1-V_2}R.
\]

Parameters:

\[
R=10000\,\Omega,\qquad
C_1=C_2=0.0001\,\mathrm{F},
\]

\[
V_1(0)=5.0\,\mathrm{V},\qquad
V_2(0)=0.0\,\mathrm{V}.
\]

For equal capacitances,

\[
V_1(t)=2.5+2.5e^{-2t/(RC)},
\qquad
V_2(t)=2.5-2.5e^{-2t/(RC)}.
\]

\[
\tau_{\rm diff}=\frac{RC}2=0.500000\,\mathrm{s}.
\]

## URR-C adapter

\[
x_O=V_1,\qquad x_H=V_2,
\]

\[
F_{OO}=-\frac1{RC_1},
\quad
R_{\rm return}=\frac1{RC_1},
\quad
W=\frac1{RC_2},
\quad
F_H=-\frac1{RC_2}.
\]

\[
K_{\rm mem}(\tau)
=
\frac1{R^2C_1C_2}e^{-\tau/(RC_2)}.
\]

## Recorded results

| Test | Result |
|---|---:|
| numerical vs matrix exponential | 5.063e-13 V |
| matrix exponential vs closed form | 3.109e-14 V |
| relative charge-retention error | 1.084e-15 |
| relative energy-accounting error | 1.667e-07 |
| hidden-elimination residual | 5.208e-08 V/s |
| observability rank | 2 |
| maximum hidden-to-visible signal | 0.499977 V |

## Retention and dissipation

\[
Q_{\rm total}=C_1V_1+C_2V_2=0.0005\,\mathrm{C}
\]

is retained in the declared ideal circuit.

\[
E_0=1.250000\,\mathrm{mJ},
\qquad
E_\infty=0.625000\,\mathrm{mJ},
\]

\[
E_R=E_0-E_\infty=0.625000\,\mathrm{mJ}.
\]

Thus the retained functional is total charge, not capacitor-stored electrical
energy.

## Hidden-state readability

Two histories have the same visible initial value \(V_1(0)=0\), but hidden
initial values \(V_2(0)=0\) and \(V_2(0)=1\) V.

\[
\Delta y(0)=0,
\qquad
\max_t|\Delta V_1(t)|=0.499977\,\mathrm{V}.
\]

\[
\mathcal O_2=
\begin{pmatrix}
1&0\\
-1&1
\end{pmatrix},
\qquad
\operatorname{rank}\mathcal O_2=2,
\qquad
\det\mathcal O_2=1.
\]

A hidden initial distinction that is invisible in one snapshot becomes
readable through the time history.

## Gates

```json
{
  "numerical_matches_matrix_exponential": true,
  "matrix_exponential_matches_closed_form": true,
  "total_charge_conserved": true,
  "capacitor_plus_resistor_energy_balanced": true,
  "hidden_elimination_matches_full_system": true,
  "hidden_initial_state_becomes_visible": true,
  "two_sample_observability_full_rank": true
}
```

## Claim boundary

```yaml
linear_circuit_solution: exact_algebra_in_declared_ideal_model
runtime: finite_diagnostic
hardware_validation: not_yet_executed
drl_inertial_term: not_tested
ontic_Psi_record: not_tested
unified_DRL_cut_tape_action: Open
```
