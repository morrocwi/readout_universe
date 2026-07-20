# AP16 — Physical Unreadability Classification Smoke Test

**Verdict:** `PASS`  
**Runtime tier:** `finite_diagnostic`  
**Schwarzschild/Painlevé–Gullstrand adapter:** `Dr`

## 1. Tested statement

\[
\text{unreadable}\Longrightarrow\text{physical black hole}.
\]

The smoke test searches for finite counterexamples and separately checks a toy
general-relativistic horizon adapter.

## 2. Shared linear readout equation

\[
\dot x=Ax,
\qquad
y=Cx,
\]

with observability matrix

\[
\boxed{
\mathcal O_C=
\begin{pmatrix}
C\\CA\\\vdots\\CA^{n-1}
\end{pmatrix}.
}
\]

## 3. Recorded cases

| Case | Rank | Maximum visible separation | Horizon certificate | Physical black hole |
|---|---:|---:|---:|---:|
| blind sensor | 1 | 0 | no | no |
| reciprocal thermal memory | 2 | 0.4999995842 | no | no |
| one-way retained sink | 1 | 0 | no | no |
| Schwarzschild PG toy interior | — | outgoing ray moves inward | yes, adapter | yes, adapter |

### 3.1 Blind sensor

Two states differing only in a hidden coordinate produce identical direct
output. Replacing the sensor raises the recorded rank from

\[
1\longrightarrow2.
\]

Unreadability here belongs to the measurement operator, not to a gravitational
horizon.

### 3.2 Reciprocal thermal memory

\[
\dot T_O=-k(T_O-T_H),
\qquad
\dot T_H=k(T_O-T_H).
\]

The hidden initial temperature later changes the visible temperature. The
recorded observability rank is 2 and the maximum visible separation is

\[
0.49999958423564045.
\]

### 3.3 One-way retained sink

\[
\dot q_O=-wq_O,
\qquad
\dot q_H=wq_O.
\]

After the declared time window,

\[
q_O=0.0009118819655545162,
\qquad
q_H=0.9990881180344455,
\]

while

\[
\max_t|q_O+q_H-1|
=1.3322676295501878\times10^{-15}.
\]

A hidden initial difference remains absent from the visible output, yet this
one-way retained sink contains no gravitational metric or horizon certificate.

### 3.4 Schwarzschild outgoing radial null-ray toy adapter

In Painlevé–Gullstrand units \(c=r_s=1\), the outgoing radial branch is

\[
\boxed{
\frac{dr}{dt_{PG}}
=1-\sqrt{\frac{r_s}{r}}.
}
\]

Outside the horizon,

\[
r_0=1.2r_s,
\qquad
\dot r_0=0.0871290708247231>0.
\]

Inside the horizon,

\[
r_0=0.8r_s,
\qquad
\dot r_0=-0.1180339887498949<0,
\]

and the recorded outgoing ray moved inward to the numerical cutoff

\[
0.8r_s\longrightarrow0.05r_s.
\]

This subsection is an external GR adapter, not a derivation of general
relativity from URR-C.

## 4. Gates

```text
blind_sensor_counterexample                  PASS
thermal_hidden_returns                       PASS
one_way_sink_counterexample                  PASS
schwarzschild_inside_outgoing_inward         PASS
```

## 5. Verdict

The universal implication is falsified by finite counterexample:

\[
\boxed{
\text{unreadable}
\centernot\Longrightarrow
\text{physical black hole}.
}
\]

The surviving classification gate is

\[
\boxed{
\text{physical black-hole adapter}
=
\text{one-way causal cut}
\land
\text{geometric horizon certificate}.
}
\]

```yaml
linear counterexamples: finite_diagnostic
Schwarzschild null-ray calculation: finite_diagnostic
GR interpretation: Dr
full black-hole information problem: not_tested
```
