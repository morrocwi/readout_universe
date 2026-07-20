# URR-C — Universal Retention–Cut Extension

**Status:** `Dr` architecture over the native URR kernel  
**Finite smoke test:** AP15 (`finite_diagnostic`)  
**Unified DRL + cut action:** `Open`

## 1. Purpose

URR-C generalizes the native system by separating four notions that must not be
collapsed:

\[
\text{existence}\neq\text{retention}\neq\text{accessibility}\neq\text{readability}.
\]

A system may retain a state that a particular readout cannot access.  A cut may
permit writing in one direction while restricting or eliminating return.
Black-hole language is only one possible interpretation; the same structure
can represent memory, forgetting, secrecy, sensors, absorbing sectors, broken
communication, or append-only records.

## 2. Master architecture

Let \(\mathsf O_\alpha\) project onto the sector accessible to readout
\(\alpha\), and let

\[
\mathsf H_\alpha=I-\mathsf O_\alpha
\]

project onto the retained but hidden sector.  Define

\[
W_\alpha:\mathsf O_\alpha\mathscr H_T\to
\mathsf H_\alpha\mathscr H_T
\]

as the write operator and

\[
R_\alpha:\mathsf H_\alpha\mathscr H_T\to
\mathsf O_\alpha\mathscr H_T
\]

as the return/read-back operator.

The candidate master system is

\[
\boxed{
\begin{gathered}
\delta_R\Longrightarrow\mathscr H_T,
\qquad
X_n=(\Phi_n,\Psi_n)^\top,
\qquad
\mathbb G_T=L_R\otimes I+I\otimes C_{\mathcal F}+C_{\rm int},
\\[1mm]
\frac{\delta S_{\rm DRL}[X;\mathbb G_T,V,J]}{\delta X_n}
=
\mathcal C_{\alpha,n}X_n,
\\[1mm]
\mathcal C_{\alpha,n}
=
\mathsf H_\alpha W_{\alpha,n}\mathsf O_\alpha
+
\mathsf O_\alpha R_{\alpha,n}\mathsf H_\alpha,
\\[1mm]
\mathcal T_{n+1}
=
\mathcal T_n\oplus
\mathsf H_\alpha W_{\alpha,n}\mathsf O_\alpha X_n,
\\[1mm]
P_{\alpha,n}
=
\Pi_\alpha\!
\left(A_\alpha\mathsf O_\alpha X_n-\delta_{\alpha,n}\right),
\\[1mm]
I_R(P_{\alpha,n}\mid\Pi_\alpha)
=-\log_2p_{\Pi_\alpha}(P_{\alpha,n})\;\mathrm{rbit}.
\end{gathered}
}
\]

The left-hand side is the native DRL dynamics.  The right-hand side is a
candidate directed flux across a read–write cut.  No derivation of that cut
term from the DRL action is claimed.

## 3. Channel classes

| System | Condition |
|---|---|
| closed | \(W=0, R=0\) |
| reciprocal | \(W\neq0, R\neq0\), often \(R=W^\top\) |
| one-way horizon/sink | \(W\neq0, R=0\) |
| leaky horizon | \(W\neq0, 0<\|R\|\ll\|W\|\) |
| source-like reverse | \(W=0, R\neq0\) |
| append-only record | hidden sector writes to tape with no return |

## 4. Horizon index

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

This is a readout, not an observer-independent essence.

## 5. Finite retained-flow realization

AP15 tests a linear positive retained-flow model with readable state \(q_O\),
hidden state \(q_H\), and tape \(q_T\):

\[
\dot q_O
=-\operatorname{diag}(\mathbf1^\top W)q_O+Rq_H,
\]

\[
\dot q_H
=Wq_O-\operatorname{diag}(\mathbf1^\top R+\ell)q_H,
\]

\[
\dot q_T=\ell^\top q_H.
\]

The generator has zero column sums, so

\[
\frac{d}{dt}
\left(\mathbf1^\top q_O+\mathbf1^\top q_H+q_T\right)=0
\]

exactly in this finite model.

## 6. Hidden-sector elimination

For the no-tape case, write

\[
\dot q_H=Wq_O-\Lambda_Hq_H,
\qquad
\Lambda_H=\operatorname{diag}(\mathbf1^\top R).
\]

Then

\[
q_H(t)=e^{-\Lambda_Ht}q_H(0)
+\int_0^t e^{-\Lambda_H(t-s)}Wq_O(s)\,ds.
\]

Substituting into the visible equation gives

\[
\boxed{
\dot q_O(t)
=-\Lambda_Oq_O(t)
+Re^{-\Lambda_Ht}q_H(0)
+\int_0^t Re^{-\Lambda_H(t-s)}Wq_O(s)\,ds,
}
\]

where \(\Lambda_O=\operatorname{diag}(\mathbf1^\top W)\).
Thus \(R=0\) yields exact visible damping, while \(R>0\) yields a return-memory
kernel.  This is an algebraic result for the finite realization, not a
universal theorem about every physical system.

## 7. Observability

For direct readout

\[
y=Cq,
\qquad C=(I_O,0_H,0_T),
\]

the observability matrix is

\[
\mathcal O_C=(C^\top,(CA)^\top,\ldots,(CA^{d-1})^\top)^\top.
\]

AP15 checks that reciprocal return makes the hidden sector dynamically
observable, while a one-way cut leaves hidden retained directions in the
readout null space.  The append-only tape remains unobservable because it has
no return channel.

## 8. Claim boundary

```yaml
finite_model_conservation: exact_algebra
hidden_elimination_identity: exact_algebra
runtime_checks: finite_diagnostic
read_write_cut_interpretation: Dr
unified_DRL_cut_action: Open
black_hole_derivation: not_claimed
universal_linearity: not_claimed
```

Canonical executable evidence:

- `ap/AP15_READ_WRITE_CUT.md`
- `ap/ap15_read_write_cut.py`
- `ap/results/AP15_READ_WRITE_CUT_RESULTS.json`
