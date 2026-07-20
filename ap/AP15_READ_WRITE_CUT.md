# AP15 — Universal Retention–Cut Smoke Test

**Status:** `finite_diagnostic`  
**Read–Write Cut interpretation:** `Dr`  
**Unified DRL + cut mechanism:** `Open`

## 1. Purpose

AP15 removes the black-hole-specific language and tests the general structure
behind it:

> a retained system may permit writing across a cut while preventing or
> limiting return readout.

The cut is not assumed to be gravitational. It can represent memory,
forgetting, secrecy, a sensor boundary, an absorbing subsystem, a failed
return channel, a horizon, or any other asymmetric retained relation.

## 2. Finite retained-flow realization

Split the retained state into

\[
q=(q_O,q_H,q_T)^\top,
\]

where \(q_O\) is readable, \(q_H\) is retained but hidden from the direct
readout, and \(q_T\) is an append-only tape.

Let

\[
W:\mathscr H_O\to\mathscr H_H
\]

be the write operator,

\[
R:\mathscr H_H\to\mathscr H_O
\]

the return/read-back operator, and \(\ell\ge0\) the tape-write rate.

The smoke-test equations are

\[
\boxed{
\dot q_O=-\operatorname{diag}(\mathbf1^\top W)q_O+Rq_H
}
\]

\[
\boxed{
\dot q_H=Wq_O-\operatorname{diag}(\mathbf1^\top R+\ell)q_H
}
\]

\[
\boxed{
\dot q_T=\ell^\top q_H.
}
\]

The generator has zero column sums, hence

\[
\boxed{
\frac{d}{dt}
\left(\mathbf1^\top q_O+\mathbf1^\top q_H+q_T\right)=0.
}
\]

This conservation statement is exact for this finite model.

## 3. Relation to URR-C

The candidate native extension is

\[
\boxed{
\begin{gathered}
\delta_R\Longrightarrow\mathscr H_T,
\qquad X=(\Phi,\Psi)^\top,
\\
\frac{\delta S_{\rm DRL}}{\delta X}
=
\mathcal C_\alpha X,
\\
\mathcal C_\alpha
=
\mathsf H_\alpha W_\alpha\mathsf O_\alpha
+
\mathsf O_\alpha R_\alpha\mathsf H_\alpha,
\\
P_\alpha
=
\Pi_\alpha(A_\alpha\mathsf O_\alpha X-\delta_\alpha).
\end{gathered}
}
\]

AP15 does **not** claim that the retained-flow generator has been derived from
\(S_{\rm DRL}\). It is a finite smoke-test realization of the cut layer.

## 4. Exact elimination and memory

For the no-tape case,

\[
\dot q_H=Wq_O-\Lambda_Hq_H,
\qquad
\Lambda_H=\operatorname{diag}(\mathbf1^\top R),
\]

so

\[
q_H(t)=e^{-\Lambda_Ht}q_H(0)
+\int_0^t e^{-\Lambda_H(t-s)}Wq_O(s)\,ds.
\]

Substitution gives

\[
\boxed{
\dot q_O(t)
=-\Lambda_Oq_O(t)
+Re^{-\Lambda_Ht}q_H(0)
+\int_0^t Re^{-\Lambda_H(t-s)}Wq_O(s)\,ds
}
\]

with

\[
\Lambda_O=\operatorname{diag}(\mathbf1^\top W).
\]

Therefore:

- \(R=0\) gives exact visible damping with no return;
- \(R>0\) gives a return-memory kernel;
- weak \(R\) gives a leaky horizon;
- \(R=W^\top\) gives a reciprocal cut.

This is an algebraic result for the finite linear realization, not a universal
physics theorem.

## 5. Horizon index

\[
\boxed{
\chi_\alpha
=
\frac{\|W_\alpha\|}
{\|W_\alpha\|+\|R_\alpha\|+\varepsilon}.
}
\]

| Value | Reading |
|---:|---|
| \(\chi\approx0.5\) | reciprocal channel |
| \(0.5<\chi<1\) | asymmetric/leaky cut |
| \(\chi\to1\) | write enabled, return disabled |
| \(\chi\to0\) | source-like reverse channel |

The index is a readout, not an observer-independent essence.

## 6. Dynamical observability

Let the direct readout observe only \(q_O\):

\[
y=Cq,
\qquad C=(I_O,0_H,0_T).
\]

The finite observability matrix is

\[
\mathcal O_C=(C^\top,(CA)^\top,\ldots,(CA^{d-1})^\top)^\top.
\]

The test checks that reciprocal return makes hidden states dynamically
observable, while a one-way cut leaves the hidden sector structurally
unobservable. The append-only tape remains unobservable because it has no
return channel.

Thus

\[
\boxed{\text{directly unreadable}\neq\text{destroyed}.}
\]

## 7. Tested cases

1. closed control: \(W=R=0\);
2. reciprocal cut: \(W\neq0, R=W^\top\);
3. one-way horizon: \(W\neq0, R=0\);
4. leaky horizon: \(W\neq0, 0<R\ll W\);
5. one-way horizon with append-only tape;
6. source-like reverse channel: \(W=0, R\neq0\).

## 8. Recorded result

```text
verdict: PASS
one-way horizon index: 0.9999999999999973
reciprocal horizon index: 0.4999999999999993
leaky horizon index: 0.9523809523809499
one-way observability nullity: 4
reciprocal observability nullity: 1
one-way final visible quantity: 0.010762744228616037
one-way final hidden quantity: 0.9892372557713833
tape final quantity: 0.29141711121520486
max total-retention error: 5.10702591327572e-15
```

## 9. Binding claim boundary

```yaml
finite_model_conservation: exact_algebra
hidden_elimination_identity: exact_algebra
runtime_checks: finite_diagnostic
read_write_cut_interpretation: Dr
unified_DRL_cut_action: Open
black_hole_derivation: not_claimed
universal_linearity: not_claimed
```

## 10. Run

```bash
python ap/ap15_read_write_cut.py \
  --output ap/results/AP15_READ_WRITE_CUT_RESULTS.json
```
