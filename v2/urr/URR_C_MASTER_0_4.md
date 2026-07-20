# URR-C 0.4 — Return, Transformation, and Physical Readability Master

**Status:** candidate computational architecture  
**Native DRL:** `derived_narrow`  
**Forced cut extension:** `Dr` / discrete Lagrange-d'Alembert form  
**Linear hidden elimination:** `exact_algebra` in the declared finite model  
**Linear-Gaussian readability:** exact under its declared channel assumptions  
**Unified DRL–cut–tape action:** `Open`

## 1. Development path

The upgraded system follows four counterexamples:

1. a readout is not truth because different retained states can share one output;
2. readable loss is not destruction because AP15 conserves total positive flow;
3. unreadability is not automatically a physical black hole because blind
   sensors and one-way sinks supply counterexamples;
4. return of information is not return of the original form because AP17
   reconstructs an encoded input through a non-identity return map.

The canonical question is therefore

\[
\boxed{
\text{what was written, how did it evolve, how did it return, and how much can a declared readout reconstruct?}
}
\]

## 2. Typed spaces

Let \(\mathscr H_T\) be the finite retained space and

\[
\mathscr X_T=\mathscr H_T\oplus\mathscr H_T,
\qquad
X_n=(\Phi_n,\Psi_n)^T.
\]

Define component selectors

\[
P_\Phi=(I,0),
\qquad
P_\Psi=(0,I).
\]

For readout \(\alpha\),

\[
O_\alpha^2=O_\alpha,
\qquad
H_\alpha=I-O_\alpha.
\]

Lift the projectors to the doubled reader–record space:

\[
\boxed{
\bar O_\alpha=I_2\otimes O_\alpha,
\qquad
\bar H_\alpha=I_{\mathscr X}-\bar O_\alpha.
}
\]

## 3. Native DRL

The native grammar is

\[
\mathbb G_T
=L_R\otimes I_{\mathcal F}
+I_{\mathcal R}\otimes C_{\mathcal F}
+C_{\rm int}.
\]

The action is

\[
S_{\rm DRL}[X]=\sum_n\mathbb L^n
\]

with

\[
\begin{aligned}
\mathbb L^n={}&
\frac{1}{\Delta t}\Delta\Phi_n^T M\Delta\Psi_n
+\frac12\left(
\Phi_n^TD\Delta\Psi_n-\Psi_n^TD\Delta\Phi_n
\right)\\
&-\Delta t\left[
K\Phi_n^T\mathbb G_T\Psi_n
+\Psi_n^T\nabla V(\Phi_n)-J_n^T\Psi_n
\right].
\end{aligned}
\]

## 4. Balanced cut force

Let

\[
W_{\beta,n}:\operatorname{im}\bar O_\beta
\to\operatorname{im}\bar H_\beta,
\qquad
R_{\alpha,n}:\operatorname{im}\bar H_\alpha
\to\operatorname{im}\bar O_\alpha.
\]

Define

\[
\boxed{
\begin{aligned}
\mathcal J_{C,n}[X]={}&
\bar H W_n\bar OX
-\bar O\Lambda_{W,n}\bar OX\\
&+\bar OR_n\bar HX
-\bar H(\Lambda_{R,n}+\Lambda_{T,n})\bar HX.
\end{aligned}
}
\]

A claimed cut balance requires a declared retention covector \(\rho\):

\[
\boxed{\rho^T\mathcal J_{C,n}[X]=0.}
\]

AP15 uses \(\rho=\mathbf1\) in its positive-flow realization. This
certificate is not automatic for the signed doubled DRL state.

## 5. Explicit forced DRL equations

The cut does not replace DRL. It acts as a force on the two DRL equations:

\[
\boxed{
\begin{aligned}
&M\frac{\Phi_{n+1}-2\Phi_n+\Phi_{n-1}}{\Delta t^2}
+D\frac{\Phi_{n+1}-\Phi_{n-1}}{2\Delta t}\\
&\quad+K\mathbb G_T\Phi_n+\nabla V(\Phi_n)-J_n
=P_\Phi\mathcal J_{C,n}[X_n],
\end{aligned}
}
\]

\[
\boxed{
\begin{aligned}
&M\frac{\Psi_{n+1}-2\Psi_n+\Psi_{n-1}}{\Delta t^2}
-D\frac{\Psi_{n+1}-\Psi_{n-1}}{2\Delta t}\\
&\quad+K\mathbb G_T\Psi_n+\nabla^2V(\Phi_n)\Psi_n
=P_\Psi\mathcal J_{C,n}[X_n].
\end{aligned}
}
\]

The continuum reader form remains telegraph-like:

\[
\boxed{
M\partial_t^2\Phi+D\partial_t\Phi
+K\mathbb G_T\Phi+\nabla V(\Phi)
=J+P_\Phi\mathcal J_C.
}
\]

This is presently a forced discrete variational architecture, not a derivation
of the cut from one unified action.

## 6. Tape types

A growing injective tape is

\[
\boxed{
\mathcal T_{n+1}=\mathcal T_n\oplus E_{T,n}(\bar HX_n),
}
\]

where \(E_{T,n}\) is injective and the tape space grows.

A fixed-dimensional accumulator is

\[
\boxed{
q_{T,n+1}=q_{T,n}+L_{T,n}\bar HX_n.
}
\]

It is append-only only after declaring a positive cone and checking
\(L_{T,n}\bar HX_n\ge0\). An accumulator is not automatically an injective
record.

## 7. Linear hidden elimination

For a continuous linear adapter,

\[
\dot x_O=F_{OO}x_O+Rx_H+B_Ou,
\]

\[
\dot x_H=Wx_O+F_Hx_H+B_Hu,
\]

\[
y=Cx_O+\eta.
\]

The hidden state is

\[
\begin{aligned}
x_H(t)={}&e^{F_H(t-t_0)}x_H(t_0)\\
&+\int_{t_0}^{t}e^{F_H(t-s)}[Wx_O(s)+B_Hu(s)]\,ds.
\end{aligned}
\]

Substitution gives

\[
\boxed{
\begin{aligned}
\dot x_O(t)={}&F_{OO}x_O(t)
+Re^{F_H(t-t_0)}x_H(t_0)\\
&+\int_{t_0}^{t}K_{\rm mem}(t-s)x_O(s)\,ds\\
&+B_Ou(t)
+\int_{t_0}^{t}Re^{F_H(t-s)}B_Hu(s)\,ds,
\end{aligned}
}
\]

where

\[
\boxed{K_{\rm mem}(\tau)=Re^{F_H\tau}W,\qquad\tau\ge0.}
\]

This separates visible dynamics, an initial-hidden echo, state memory, and
hidden-input memory.

## 8. Return–transformation kernel

Let \(z\) be encoded by \(E_\beta\). Define

\[
\boxed{
\mathcal K_{\alpha\leftarrow\beta}(\tau)
=A_\alpha\bar O_\alpha R_\alpha
\mathcal U_H(\tau)
\bar H_\beta W_\beta\bar O_\beta E_\beta.
}
\]

For a linear hidden sector,

\[
\mathcal U_H(\tau)=e^{F_H\tau}.
\]

Causality requires

\[
\mathcal K_{\alpha\leftarrow\beta}(\tau)=0
\qquad(\tau<0).
\]

The returned measurement is

\[
\boxed{
y_{\alpha\leftarrow\beta}(\tau)
=\mathcal K_{\alpha\leftarrow\beta}(\tau)z+\eta_\alpha.
}
\]

## 9. Reconstructability

A transformed return need not resemble its input. Reconstruction requires a
declared decoder \(D\):

\[
\boxed{D\mathcal K E\approx I}
\]

on the encoded subspace.

For full-column-rank \(\mathcal K\) and noise covariance \(\Sigma_\eta\),

\[
\boxed{
D_*=(\mathcal K^T\Sigma_\eta^{-1}\mathcal K)^{-1}
\mathcal K^T\Sigma_\eta^{-1},
}
\]

\[
\boxed{
\Sigma_{\rm rec}
=(\mathcal K^T\Sigma_\eta^{-1}\mathcal K)^{-1}.
}
\]

Therefore \(\|\mathcal K-I\|\) alone is not an information-loss measure.

## 10. Physical readability over a time window

For

\[
x_{k+1}=Fx_k,
\qquad
y_k=Cx_k+\eta_k,
\]

stack \(L+1\) samples:

\[
Y_L=\mathcal G_Lx_0+N_L,
\]

\[
\boxed{
\mathcal G_L=
\begin{pmatrix}
C\\CF\\\vdots\\CF^L
\end{pmatrix}.
}
\]

Structural readability is

\[
d_{\rm struct}(L)=\operatorname{rank}\mathcal G_L.
\]

Noise-whitened readability uses

\[
\boxed{
\widetilde{\mathcal G}_L
=\Sigma_N^{-1/2}\mathcal G_L\Sigma_x^{1/2}.
}
\]

For threshold \(\kappa\),

\[
d_{\rm readable}^{(\kappa)}(L)
=\#\{i:\sigma_i(\widetilde{\mathcal G}_L)>\kappa\}.
\]

Under the declared linear-Gaussian model,

\[
\boxed{
I_{\rm read}(L)
=\frac12\log_2\det\left[
I+\Sigma_x^{1/2}\mathcal G_L^T\Sigma_N^{-1}
\mathcal G_L\Sigma_x^{1/2}
\right]\;\mathrm{rbit}.
}
\]

## 11. Memory and echo

\[
\boxed{
\tau_{\rm echo}
=\operatorname*{arg\,max}_{\tau>0}I_{\rm read}(\tau),
}
\]

\[
\boxed{
\tau_{\rm mem}^{(I_*)}
=\sup\{\tau:I_{\rm read}(\tau)\ge I_*\}.
}
\]

A delayed maximum is an echo. Rank loss is structural unreadability. Small
noise-whitened singular values are practical unreadability.

## 12. Classification gates

| Class | Gate |
|---|---|
| same-form return | typed \(\mathcal K\approx I\) |
| transformed but reconstructable | full column rank and acceptable \(\Sigma_{\rm rec}\) |
| partial return | \(0<\operatorname{rank}\mathcal K<\dim z\) |
| echo | delayed local maximum of \(I_{\rm read}(\tau)\) |
| no direct return | \(\mathcal K=0\) for the declared channel |
| practically unreadable | whitened singular values below threshold |
| structurally unreadable | encoded direction lies in \(\ker\mathcal G_L\) |
| physical black-hole adapter | one-way causal cut plus geometric horizon certificate |

A finite observation of zero return does not prove permanent inaccessibility.
A native \(R=0\) parameter does not certify a gravitational event horizon.

## 13. Stability gates

\[
\alpha_H=\max\Re\lambda(F_H).
\]

- \(\alpha_H<0\): asymptotically decaying hidden propagation;
- \(\alpha_H=0\): persistent or oscillatory memory is possible;
- \(\alpha_H>0\): growing return; a finite horizon or saturation model is
  required.

Also report transient growth

\[
\boxed{
g_H(T)=\sup_{0\le\tau\le T}\|e^{F_H\tau}\|}
\]

because a nonnormal system can grow transiently despite stable eigenvalues.

## 14. Nonlinear extension

For

\[
\dot x_H=f_H(x_H,x_O,u),
\]

the exact return is a nonlinear response functional. Along a trajectory,

\[
\partial_tU_H(t,s)
=\left.\frac{\partial f_H}{\partial x_H}\right|_{x(t)}U_H(t,s),
\qquad
U_H(s,s)=I,
\]

and

\[
\mathcal K_{\rm tangent}(t,s)
=A(t)R(t)U_H(t,s)W(s)E(s)
\]

is only a local linearization.

## 15. Upgraded master box

\[
\boxed{
\begin{gathered}
\delta_R\Rightarrow\mathscr H_T
\Rightarrow\mathscr X_T=(\mathscr H_T\oplus\mathscr H_T),\\
\mathbb G_T=L_R\otimes I+I\otimes C_{\mathcal F}+C_{\rm int},\\
\mathcal E_{\rm DRL}[X]_n=\mathcal J_{C,n}[X_n],\\
\mathcal T_{n+1}=\mathcal T_n\oplus E_{T,n}(\bar HX_n),\\
\mathcal K_{\alpha\leftarrow\beta}(\tau)
=A_\alpha\bar O_\alpha R_\alpha\mathcal U_H(\tau)
\bar H_\beta W_\beta\bar O_\beta E_\beta,\\
Y_L=\mathcal G_Lx_0+N_L,\\
I_{\rm read}(L)
=\frac12\log_2\det\left[
I+\Sigma_x^{1/2}\mathcal G_L^T\Sigma_N^{-1}
\mathcal G_L\Sigma_x^{1/2}
\right]\;\mathrm{rbit},\\
P_{\alpha,n}
=\Pi_\alpha(Y_L,\delta_\alpha,\Sigma_N,
\text{decoder},\text{threshold}).
\end{gathered}
}
\]

## 16. Binding claim boundary

```yaml
native_DRL: derived_narrow
forced_DRL_cut_equations: Dr
cut_balance: requires_declared_retention_covector_and_certificate
linear_hidden_elimination: exact_algebra_in_declared_scope
linear_return_kernel: exact_algebra_in_declared_scope
linear_Gaussian_readability: exact_under_declared_distribution
AP17_runtime: finite_diagnostic
nonlinear_return_kernel: local_linearization_only
unified_DRL_cut_tape_action: Open
all_retained_states_eventually_return: not_claimed
physical_black_hole_from_native_cut_alone: not_claimed
```
