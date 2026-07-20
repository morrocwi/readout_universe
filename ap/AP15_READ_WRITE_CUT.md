# AP15 — Universal Retention–Cut Smoke Test

**Status:** `finite_diagnostic`  
**Read–Write Cut interpretation:** `Dr`  
**Exact algebra:** finite positive-flow balance and finite linear elimination  
**Unified DRL + cut + tape mechanism:** `Open`

## 1. Purpose

AP15 removes the black-hole-specific language and tests the general structure
behind it:

> a retained system may permit writing across a cut while preventing or
> limiting return readout.

The cut is not assumed to be gravitational. It can represent memory,
forgetting, secrecy, a sensor boundary, an absorbing subsystem, a failed
return channel, a horizon, or any other asymmetric retained relation.

Canonical architecture and discovery ledgers:

- `v2/urr/URR_CUT_EXTENSION.md`
- `v2/urr/URR_C_MASTER.yaml`
- `v2/urr/URR_C_DISCOVERIES.md`

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

The negative diagonal terms are not optional decoration. They balance the
quantity written out of the source sector. The generator therefore has zero
column sums, hence

\[
\boxed{
\frac{d}{dt}
\left(\mathbf1^\top q_O+\mathbf1^\top q_H+q_T\right)=0.
}
\]

This conservation statement is exact for this finite positive-flow model.

## 3. Relation to the canonical URR-C master equation

Let \(\mathsf O_\alpha\) project onto the directly readable sector and
\(\mathsf H_\alpha=I-\mathsf O_\alpha\) onto the retained hidden sector.
The balanced candidate cut flux is

\[
\boxed{
\begin{aligned}
\mathcal J_{C,\alpha}[X]
={}&
\mathsf H_\alpha W_\alpha\mathsf O_\alpha X
-
\mathsf O_\alpha\Lambda_{W,\alpha}\mathsf O_\alpha X
\\
&+
\mathsf O_\alpha R_\alpha\mathsf H_\alpha X
-
\mathsf H_\alpha
(\Lambda_{R,\alpha}+\Lambda_{T,\alpha})
\mathsf H_\alpha X.
\end{aligned}
}
\]

The canonical master architecture is

\[
\boxed{
\begin{gathered}
\delta_R\Longrightarrow\mathscr H_T,
\qquad
X=(\Phi,\Psi)^\top,
\\
\frac{\delta S_{\rm DRL}}{\delta X}
=\mathcal J_{C,\alpha}[X],
\\
\mathcal T_{n+1}
=\mathcal T_n\oplus\Lambda_{T,\alpha}\mathsf H_\alpha X_n,
\\
r_\alpha=A_\alpha\mathsf O_\alpha X-\delta_\alpha,
\qquad
P_\alpha=\Pi_\alpha(r_\alpha).
\end{gathered}
}
\]

AP15 does **not** claim that the retained-flow generator or the balanced cut
operator has been derived from \(S_{\rm DRL}\). It is a finite smoke-test
realization of the new cut layer.

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
+\int_0^t K_{\rm mem}(t-s)q_O(s)\,ds
}
\]

with

\[
\boxed{
K_{\rm mem}(u)=Re^{-\Lambda_Hu}W,
\qquad
\Lambda_O=\operatorname{diag}(\mathbf1^\top W).
}
\]

Therefore:

- \(R=0\) gives exact visible damping with no return in this finite model;
- \(R>0\) gives a return-memory kernel;
- weak \(R\) gives a leaky cut;
- \(R=W^\top\) gives a reciprocal cut.

This is an algebraic result for the finite linear realization, not a universal
physics theorem.

## 5. Horizon/asymmetry index

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

For the recorded AP15 matrices:

| Case | Rank | Nullity |
|---|---:|---:|
| reciprocal | 6 | 1 |
| leaky | 6 | 1 |
| one-way | 3 | 4 |

Reciprocal and leaky return expose the three hidden working directions through
their future influence on the readable sector. The append-only tape remains
unobservable because it has no return edge. The one-way cut leaves the hidden
working directions and tape in the dynamical readout null space.

Thus

\[
\boxed{\text{directly unreadable}\neq\text{destroyed}.}
\]

## 7. Append-only tape result

For nonnegative hidden quantity and \(\ell\ge0\),

\[
\dot q_T=\ell^\top q_H\ge0.
\]

The hidden working sector itself need not grow monotonically because it can
write onward into the tape. In the recorded case,

\[
q_O=0.0107627442,
\qquad
q_H=0.6978201446,
\qquad
q_T=0.2914171112
\]

at the final time.

## 8. Tested cases

1. closed control: \(W=R=0\);
2. reciprocal cut: \(W\neq0, R=W^\top\);
3. one-way cut: \(W\neq0, R=0\);
4. leaky cut: \(W\neq0, 0<R\ll W\);
5. one-way cut with append-only tape;
6. source-like reverse channel: \(W=0, R\neq0\).

## 9. Recorded result

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

## 10. Discoveries supported by this artifact

AP15 supports the following only at the tiers recorded in
`v2/urr/URR_C_DISCOVERIES.md`:

1. readable loss can coexist with exact total retention;
2. a one-way cut gives visible damping in the finite flow realization;
3. a return channel gives a memory kernel;
4. return changes observability and nullity;
5. append-only tape can remain retained outside direct readout;
6. horizon-ness can be represented as channel asymmetry;
7. black-hole language is only one optional special-case interpretation.

## 11. Binding claim boundary

```yaml
finite_model_conservation: exact_algebra
hidden_elimination_identity: exact_algebra
R_zero_visible_damping: exact_algebra_in_AP15_scope
runtime_checks: finite_diagnostic
read_write_cut_interpretation: Dr
balanced_cut_flux_from_DRL_action: Open
unified_DRL_cut_tape_action: Open
black_hole_derivation: not_claimed
universal_linearity: not_claimed
```

## 12. Run

```bash
python ap/ap15_read_write_cut.py \
  --output ap/results/AP15_READ_WRITE_CUT_RESULTS.json
```
