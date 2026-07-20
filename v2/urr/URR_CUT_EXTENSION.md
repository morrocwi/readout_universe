# URR-C — Universal Retention–Cut–Readout Master Extension

**Version:** `0.3.0-cut`  
**Status:** `Dr` architecture over the native URR kernel  
**Finite smoke test:** AP15 (`finite_diagnostic`)  
**Exact finite results:** balance and hidden-elimination identities in their declared scopes  
**Unified DRL + cut + tape action:** `Open`

## 1. Purpose

URR-C generalizes the native system by separating four notions that must not be
collapsed:

\[
\boxed{
\text{existence}
\neq
\text{retention}
\neq
\text{accessibility}
\neq
\text{readability}.
}
\]

A system may retain a state that a particular readout cannot access. A cut may
permit writing in one direction while restricting or eliminating return.
Black-hole language is only one possible interpretation; the same structure
can represent memory, forgetting, secrecy, sensors, absorbing sectors, broken
communication, or append-only records.

The canonical discovery ledger is
[`URR_C_DISCOVERIES.md`](URR_C_DISCOVERIES.md). The machine-readable contract
is [`URR_C_MASTER.yaml`](URR_C_MASTER.yaml).

## 2. Sector decomposition

Let \(\mathsf O_\alpha\) project onto the sector accessible to readout
\(\alpha\):

\[
\mathsf O_\alpha^2=\mathsf O_\alpha.
\]

Define the retained but directly hidden projector

\[
\boxed{\mathsf H_\alpha=I-\mathsf O_\alpha.}
\]

Then

\[
\mathsf H_\alpha^2=\mathsf H_\alpha,
\qquad
\mathsf O_\alpha\mathsf H_\alpha=0.
\]

Define the directed channels

\[
W_{\alpha,n}:\mathsf O_\alpha\mathscr H_T
\longrightarrow
\mathsf H_\alpha\mathscr H_T
\]

and

\[
R_{\alpha,n}:\mathsf H_\alpha\mathscr H_T
\longrightarrow
\mathsf O_\alpha\mathscr H_T.
\]

Here \(W\) writes across the cut and \(R\) returns or reads back across it.
A separate nonnegative tape operator \(\Lambda_{T,\alpha,n}\) writes retained
hidden content into an append-only record.

## 3. Canonical URR-C master architecture

Let

\[
X_n=(\Phi_n,\Psi_n)^\top
\]

be the reader–record DRL state and

\[
\mathbb G_T
=
L_R\otimes I_{\mathcal F}
+
I_{\mathcal R}\otimes C_{\mathcal F}
+
C_{\rm int}
\]

be the native finite grammar.

The balanced directed cut flux is

\[
\boxed{
\begin{aligned}
\mathcal J_{C,\alpha,n}[X]
={}&
\mathsf H_\alpha W_{\alpha,n}\mathsf O_\alpha X
-
\mathsf O_\alpha\Lambda_{W,\alpha,n}\mathsf O_\alpha X
\\
&+
\mathsf O_\alpha R_{\alpha,n}\mathsf H_\alpha X
-
\mathsf H_\alpha
(\Lambda_{R,\alpha,n}+\Lambda_{T,\alpha,n})
\mathsf H_\alpha X.
\end{aligned}
}
\]

The \(\Lambda\) operators balance outflow from the sector that supplies each
directed flux. In the AP15 positive-flow realization they reduce to diagonal
column-sum operators.

The candidate master system is

\[
\boxed{
\begin{gathered}
\delta_R
\Longrightarrow
\mathscr H_T,
\qquad
X_n=(\Phi_n,\Psi_n)^\top,
\qquad
\mathbb G_T
=L_R\otimes I+I\otimes C_{\mathcal F}+C_{\rm int},
\\[1mm]
\mathcal E_{\rm DRL}[X]_n
:=
\frac{\delta S_{\rm DRL}[X;\mathbb G_T,V,J]}{\delta X_n}
=
\mathcal J_{C,\alpha,n}[X_n],
\\[1mm]
\mathcal T_{n+1}
=
\mathcal T_n
\oplus
\Lambda_{T,\alpha,n}\mathsf H_\alpha X_n,
\\[1mm]
r_{\alpha,n}
=
A_\alpha\mathsf O_\alpha X_n-\delta_{\alpha,n},
\\[1mm]
P_{\alpha,n}
=
\Pi_\alpha
\left(
r_{\alpha,n},
A_\alpha\mathsf O_\alpha X_n,
\delta_{\alpha,n}
\right),
\\[1mm]
I_R(P_{\alpha,n}\mid\Pi_\alpha)
=
-\log_2p_{\Pi_\alpha}(P_{\alpha,n})\;\mathrm{rbit}.
\end{gathered}
}
\tag{URR-C Master}
\]

The left-hand side is the native DRL Euler–Lagrange operator. The right-hand
side is a candidate directed flux across a read–write cut. No derivation of
that flux from the DRL action is claimed. The equation is therefore the
canonical native architecture, not yet a unified variational theorem.

## 4. Channel classes

| System | Condition |
|---|---|
| closed | \(W=0, R=0\) |
| reciprocal | \(W\neq0, R\neq0\), often \(R=W^\top\) |
| one-way horizon/sink | \(W\neq0, R=0\) |
| leaky horizon | \(W\neq0, 0<\|R\|\ll\|W\|\) |
| source-like reverse | \(W=0, R\neq0\) |
| append-only record | hidden sector writes to tape with no tape-return edge |

A black-hole-like readout is only the one-way limiting class. It is not the
root ontology of URR-C.

## 5. Horizon/asymmetry index

Define the policy-dependent readout

\[
\boxed{
\chi_\alpha
=
\frac{\|W_\alpha\|}
{\|W_\alpha\|+\|R_\alpha\|+\varepsilon}.
}
\]

- \(\chi\approx1/2\): reciprocal channel;
- \(1/2<\chi<1\): asymmetric or leaky cut;
- \(\chi\to1\): write enabled, return disabled;
- \(\chi\to0\): source-like reverse channel.

This value depends on the sector decomposition, norm, and readout policy. It is
a readout, not an observer-independent substance.

## 6. Exact positive finite-flow realization

AP15 tests a linear nonnegative retained-flow model with readable state
\(q_O\), hidden state \(q_H\), and tape \(q_T\):

\[
\boxed{
\dot q_O
=-\operatorname{diag}(\mathbf1^\top W)q_O+Rq_H,
}
\]

\[
\boxed{
\dot q_H
=Wq_O-\operatorname{diag}(\mathbf1^\top R+\ell)q_H,
}
\]

\[
\boxed{\dot q_T=\ell^\top q_H.}
\]

The generator has zero column sums, so

\[
\boxed{
\frac{d}{dt}
\left(
\mathbf1^\top q_O
+
\mathbf1^\top q_H
+
q_T
\right)=0
}
\]

exactly in this finite model.

This proves neither universal linearity nor a physical law for every domain.
It supplies an exact realization of the architectural statement that readable
loss can coexist with retained total quantity.

## 7. Hidden-sector elimination and memory

For the finite linear no-tape case, write

\[
\dot q_H=Wq_O-\Lambda_Hq_H,
\qquad
\Lambda_H=\operatorname{diag}(\mathbf1^\top R).
\]

Then

\[
q_H(t)
=e^{-\Lambda_Ht}q_H(0)
+
\int_0^t e^{-\Lambda_H(t-s)}Wq_O(s)\,ds.
\]

Substitution into the visible equation gives

\[
\boxed{
\dot q_O(t)
=-\Lambda_Oq_O(t)
+Re^{-\Lambda_Ht}q_H(0)
+
\int_0^t K_{\rm mem}(t-s)q_O(s)\,ds,
}
\]

where

\[
\boxed{
K_{\rm mem}(u)=Re^{-\Lambda_Hu}W,
\qquad
\Lambda_O=\operatorname{diag}(\mathbf1^\top W).
}
\]

Thus

\[
R=0
\Longrightarrow
\text{exact visible damping in the finite model},
\]

while

\[
R>0
\Longrightarrow
\text{return-memory kernel}.
\]

This is exact algebra for the declared finite linear realization. Nonlinear
hidden-sector elimination remains open.

## 8. Observability

For direct readout

\[
y=Cq,
\qquad
C=(I_O,0_H,0_T),
\]

the observability matrix is

\[
\mathcal O_C
=
(C^\top,(CA)^\top,\ldots,(CA^{d-1})^\top)^\top.
\]

AP15 found:

| Case | Rank | Nullity |
|---|---:|---:|
| reciprocal | 6 | 1 |
| leaky | 6 | 1 |
| one-way | 3 | 4 |

Reciprocal or leaky return makes the three hidden working directions
dynamically observable in the recorded example. The append-only tape remains
unobservable because it has no return edge. A one-way cut leaves both the
hidden directions and tape in the dynamical readout null space.

\[
\boxed{
\text{directly unreadable}
\neq
\text{destroyed}.
}
\]

## 9. AP15 executed result

The canonical run reports:

```text
verdict                           PASS
one-way horizon index            0.9999999999999973
reciprocal horizon index         0.4999999999999993
leaky horizon index              0.9523809523809499
one-way observability nullity    4
reciprocal observability nullity 1
one-way final visible            0.010762744228616037
one-way final hidden             0.9892372557713833
append-only tape final           0.29141711121520486
maximum total-retention error    5.10702591327572e-15
```

These numbers are `finite_diagnostic`, not proof beyond the configured model.

## 10. Discoveries added to the system

1. existence, retention, accessibility, and readability are distinct;
2. readable loss can be realized as retained cross-cut flux;
3. a one-way cut gives exact visible damping in the finite flow realization;
4. a return channel gives an explicit memory kernel;
5. return edges change dynamical observability and nullity;
6. append-only tape can retain quantity after the hidden working state changes;
7. horizon-ness is a channel-asymmetry readout rather than a new substance;
8. black-hole language is one special case, not the master primitive;
9. the sharpened open problem is a unified DRL–cut–tape action.

The exact tier and falsifier of each item are recorded in
[`URR_C_DISCOVERIES.md`](URR_C_DISCOVERIES.md).

## 11. Claim boundary

```yaml
native_DRL: derived_narrow
finite_flow_conservation: exact_algebra_in_declared_scope
hidden_elimination_memory_identity: exact_algebra_in_declared_scope
AP15_runtime: finite_diagnostic
read_write_cut_interpretation: Dr
horizon_index: definition_plus_Dr
unified_DRL_cut_tape_action: Open
black_hole_derivation: not_claimed
universal_linearity: not_claimed
```

Canonical executable evidence:

- `v2/urr/URR_C_MASTER.yaml`
- `v2/urr/URR_C_DISCOVERIES.md`
- `ap/AP15_READ_WRITE_CUT.md`
- `ap/ap15_read_write_cut.py`
- `ap/results/AP15_READ_WRITE_CUT_RESULTS.json`
