# AP13 — URR FPUT Independent-Solver Cross-Check

## Benchmark identity

This is an independent-solver cross-check, not a comparison against any
external dataset or published result. Both the URR integrator and the
reference trajectory are computed inside this same script, from the same
self-generated initial condition (`initial_mode()`); the reference trajectory
uses a different, independently-implemented integration algorithm (SciPy's
DOP853, an eighth-order Runge-Kutta) at very tight tolerance so that it can
serve as a high-precision numerical cross-check on the URR recurrence. There
is no external dataset and no literature/experimental comparison here.

This run uses the 32-particle fixed-boundary Fermi–Pasta–Ulam–Tsingou
beta chain. It is a historically important nonlinear many-body benchmark.

The tested Hamiltonian is

\[
H(q,p)=\frac12\sum_i p_i^2+
\frac12\sum_{b=0}^N d_b^2+
\frac{\beta}4\sum_{b=0}^N d_b^4,
\qquad d=Bq.
\]

Configuration:

- moving particles: 32
- nonlinear coefficient: beta = 1.0
- initial total energy: 0.25
- initial excitation: first fixed-boundary normal mode
- cross-check solver: SciPy DOP853, order 8, rtol `1e-12`, atol `1e-14`
  (independently implemented from the URR recurrence; run on the same
  self-generated initial condition, not an external dataset)

This is a solved initial-value benchmark, not a claimed solution of the open
thermodynamic-limit FPUT problem.

## A. Standard conservative FPUT

| dt | final relative state error | trajectory RMS error | max relative energy drift | observed order |
|---:|---:|---:|---:|---:|
| 0.04 | 1.476918e-06 | 2.173489e-06 | 3.665287e-06 |  |
| 0.02 | 3.692237e-07 | 5.434156e-07 | 9.163216e-07 | 2.00002 |
| 0.01 | 9.230489e-08 | 1.358597e-07 | 2.290796e-07 | 2.00002 |
| 0.005 | 2.307679e-08 | 3.396598e-08 | 5.727040e-08 | 1.99996 |

Result: halving the step reduces the final-state error by approximately four,
giving observed order close to 2.

Long-horizon run to T = 1000, URR dt = 0.02:

- first-mode energy-fraction RMSE: 1.253223e-06
- first-mode maximum absolute error: 3.145068e-06
- final relative state error: 1.205460e-04
- URR maximum relative energy drift: 1.172991e-06
- DOP853 maximum relative energy drift: 1.154632e-14
- URR local runtime: 1.2435 s
- DOP853 local runtime: 6.2065 s

Interpretation: the native conservative reduction is accurate and
structure-preserving, but it is not a new state-of-the-art integrator. It is
in the established second-order variational / Störmer-Verlet class.

## B. DRL-specific nonlinear graph test

The same FPUT graph was extended to the reader-record system

\[
\ddot\Phi+D\dot\Phi+L\Phi+\nabla V_4(\Phi)=0,
\]

\[
\ddot\Psi-D\dot\Psi+L\Psi+
\nabla^2V_4(\Phi)\Psi=0.
\]

Damping is heterogeneous across the 32 nodes. The independently-implemented
cross-check solver integrates the full 128-dimensional first-order system.

| dt | final relative state error | trajectory RMS error | pairing-charge relative drift | observed order |
|---:|---:|---:|---:|---:|
| 0.04 | 4.783414e-06 | 5.377586e-07 | 5.268092e-09 |  |
| 0.02 | 1.195854e-06 | 1.344225e-07 | 1.317058e-09 | 2.00000 |
| 0.01 | 2.989584e-07 | 3.360280e-08 | 3.292722e-10 | 2.00002 |
| 0.005 | 7.473684e-08 | 8.400025e-09 | 8.234912e-11 | 2.00005 |

Cross-check DOP853 pairing-charge relative drift:
`2.743031e-17`.

At dt = 0.01:

- final relative state error: 2.989584e-07
- trajectory RMS error: 3.360280e-08
- pairing-charge relative drift: 3.292722e-10
- URR local runtime: 0.1674 s
- cross-check solver local runtime: 1.6699 s

Runtime values are machine-specific finite diagnostics, not universal
performance claims.

## Harness verdict

| Gate | Result |
|---|---|
| independent high-precision cross-check solver (in-script, self-generated ICs) | PASS |
| deterministic initial condition | PASS |
| step-halving convergence | PASS, approximately second order |
| conservative energy diagnostic | PASS |
| nonlinear DRL pairing diagnostic | PASS |
| long-horizon observable comparison | PASS |
| state-of-the-art efficiency claim | NOT CLAIMED |
| proof or external peer validation | NOT PROVIDED |

## Scientific meaning

The benchmark gives strong finite evidence that:

1. the URR recurrence is implemented consistently;
2. its conservative reduction reproduces a recognized nonlinear lattice
   benchmark;
3. the DRL reader-record extension agrees with an independent high-order
   solver;
4. the pairing charge exhibits the predicted cancellation behavior in this
   difficult nonlinear graph case.

It does not show that URR solves every scientific domain, and it does not
settle the open questions surrounding FPUT thermalization.

## Status

```yaml
tier: finite_diagnostic
cross_check_solver: SciPy DOP853 (in-script, independently implemented, self-generated initial conditions)
external_dataset: none
novelty_promotion: forbidden
```
