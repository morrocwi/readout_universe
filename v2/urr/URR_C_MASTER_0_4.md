# URR-C 0.4 — Return, Transformation, and Physical Readability Master

**Status:** candidate computational architecture  
**Native DRL:** `derived_narrow`  
**Forced cut extension:** `Dr` / discrete Lagrange-d'Alembert form  
**Linear hidden elimination:** `exact_algebra` in the declared finite model  
**Linear-Gaussian readability:** exact under its declared channel assumptions  
**Unified DRL–cut–tape action:** `Open`

## 1. Why the master system changed

The development followed a sequence of failed collapses:

1. **Readout was initially too close to truth.**  
   The null-space gate established that a reported value depends on a question
   operator and policy.

2. **Reader loss was initially too close to destruction.**  
   AP15 supplied a positive finite-flow counterexample in which the readable
   sector decreased while the combined readable, hidden, and tape quantity was
   conserved.

3. **Unreadability was initially too close to a physical black hole.**  
   AP16 produced blind-sensor and one-way-sink counterexamples. A gravitational
   black hole additionally requires a causal/geometric horizon certificate.

4. **Return was initially too close to return of the original form.**  
   AP17 showed that a return kernel can be far from the identity while a known
   decoder reconstructs the encoded input exactly in the noiseless model.

The upgraded primitive question is therefore:

\[
\boxed{
\text{What was written, how did it evolve, through which channel did it
return, and how much can a declared physical readout reconstruct?}
}
\]

## 2. Typed native spaces

Let the finite native retained space be \(\mathscr H_T\). The reader–record
space is

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

Lift them to the doubled space:

\[
\bar O_\alpha=I_2\otimes O_\alpha,
\qquad
\bar H_\alpha=I_{\mathscr X}-\bar O_\alpha.
\]

This removes the former ambiguity about whether the cut acts on \(\Phi\),
\(\Psi\), or both.

## 3. Native DRL action

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

The native grammar is

\[
\mathbb G_T
=
L_R\otimes I_{\mathcal F}
+
I_{\mathcal R}\otimes C_{\mathcal F}
+
C_{\rm int}.
\]

## 4. Balanced read–write cut

Let

\[
W_{\beta,n}:\operatorname{im}\bar O_\beta
\rightarrow\operatorname{im}\bar H_\beta,
\]

\[
R_{\alpha,n}:\operatorname{im}\bar H_\alpha
\rightarrow\operatorname{im}\bar O_\alpha.
\]

The balanced cut force is

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

The outflow operators are not arbitrary decoration. A declared retention
covector \(\rho\) must satisfy the cut-balance gate

\[
\boxed{\rho^T\mathcal J_{C,n}[X]=0}
\]

when the adapter claims cut conservation. For AP15, \(\rho=\mathbf1\).

## 5. Explicit forced DRL equations

The cut does not replace DRL. It supplies a force to the DRL
Euler–Lagrange equations:

\[
\boxed{
\begin{aligned}
&M\frac{\Phi_{n+1}-2\Phi_n+\Phi_{n-1}}{\Delta t^2}
+D\frac{\Phi_{n+1}-\Phi_{n-1}}{2\Delta t}\\
&\quad
+K\mathbb G_T\Phi_n+\nabla V(\Phi_n)-J_n
=
P_\Phi\mathcal J_{C,n}[X_n],
\end{aligned}
}
\]

\[
\boxed{
\begin{aligned}
&M\frac{\Psi_{n+1}-2\Psi_n+\Psi_{n-1}}{\Delta t^2}
-D\frac{\Psi_{n+1}-\Psi_{n-1}}{2\Delta t}\\
&\quad
+K\mathbb G_T\Psi_n+\nabla^2V(\Phi_n)\Psi_n
=
P_\Psi\mathcal J_{C,n}[X_n].
\end{aligned}
}
\]

This is a **forced discrete variational system**, not yet a derivation of the
cut from one unified action.

Its continuum reader form is telegraph-like:

\[
M\partial_t^2\Phi
+D\partial_t\Phi
+K\mathbb G_T\Phi+\nabla V(\Phi)
=
J+P_\Phi\mathcal J_C.
\]

## 6. Tape types must not be collapsed

### 6.1 Growing injective tape

\[
\boxed{
\mathcal T_{n+1}
=
\mathcal T_n\oplus
E_{T,n}(\bar H X_n),
}
\]

where \(E_{T,n}\) is injective. The tape state space grows.

### 6.2 Fixed-dimensional accumulator

\[
\boxed{
q_{T,n+1}
=
q_{T,n}+L_{T,n}\bar HX_n.
}
\]

Append-only monotonicity requires a positive state cone and
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

The hidden solution is

\[
x_H(t)
=
e^{F_H(t-t_0)}x_H(t_0)
+
\int_{t_0}^{t}
e^{F_H(t-s)}
\left[Wx_O(s)+B_Hu(s)\right]ds.
\]

Therefore

\[
\boxed{
\begin{aligned}
\dot x_O(t)={}&F_{OO}x_O(t)
+Re^{F_H(t-t_0)}x_H(t_0)\\
&+\int_{t_0}^{t}K_{\rm mem}(t-s)x_O(s)\,ds\\
&+B_Ou(t)
+\int_{t_0}^{t}R e^{F_H(t-s)}B_Hu(s)\,ds,
\end{aligned}
}
\]

where

\[
\boxed{K_{\rm mem}(\tau)=R e^{F_H\tau}W,\qquad \tau\ge0.}
\]

This formula separates four effects: visible dynamics, hidden initial-state
echo, state memory, and hidden-input memory.

## 8. Return–transformation kernel

Let \(z\) be an encoded message or perturbation, with encoder \(E_\beta\).
The future return read by channel \(\alpha\) is

\[
\boxed{
\mathcal K_{\alpha\leftarrow\beta}(\tau)
=
A_\alpha\bar O_\alpha R_\alpha
\mathcal U_H(\tau)
\bar H_\beta W_\beta\bar O_\beta E_\beta.
}
\]

For a linear hidden sector,

\[
\mathcal U_H(\tau)=e^{F_H\tau}.
\]

The channel is causal:

\[
\mathcal K_{\alpha\leftarrow\beta}(\tau)=0
\qquad(\tau<0).
\]

The measured return is

\[
\boxed{
y_{\alpha\leftarrow\beta}(\tau)
=
\mathcal K_{\alpha\leftarrow\beta}(\tau)z+\eta_\alpha.
}
\]

## 9. Form fidelity and information fidelity are different

Comparing \(\mathcal K\) with \(I\) is meaningful only after matching units,
dimensions, encoder, and decoder.

Because \(\mathcal K\) already includes the encoder \(E_\beta\), a transformed
return is reconstructable when a declared decoder \(D\) gives

\[
\boxed{D\mathcal K\approx I}
\]

on the message space.

For full-column-rank \(\mathcal K\) with noise covariance \(\Sigma_\eta\), the
generalized least-squares decoder is

\[
\boxed{
D_*
=
(\mathcal K^T\Sigma_\eta^{-1}\mathcal K)^{-1}
\mathcal K^T\Sigma_\eta^{-1}.
}
\]

Its reconstruction covariance is

\[
\boxed{
\Sigma_{\rm rec}
=
(\mathcal K^T\Sigma_\eta^{-1}\mathcal K)^{-1}.
}
\]

## 10. Physical readability over a time window

For sampled dynamics

\[
x_{k+1}=Fx_k,
\qquad
y_k=Cx_k+\eta_k,
\]

stack \(L+1\) measurements:

\[
Y_L=\mathcal G_Lx_0+N_L,
\]

\[
\boxed{
\mathcal G_L
=
\begin{pmatrix}
C\\CF\\\vdots\\CF^L
\end{pmatrix}.
}
\]

Structural readability is

\[
d_{\rm struct}(L)=\operatorname{rank}\mathcal G_L.
\]

Noise-whitened readability uses the singular values of

\[
\boxed{
\widetilde{\mathcal G}_L
=
\Sigma_N^{-1/2}
\mathcal G_L
\Sigma_x^{1/2}.
}
\]

For a declared threshold \(\kappa\),

\[
d_{\rm readable}^{(\kappa)}(L)
=
\#\{i:\sigma_i(\widetilde{\mathcal G}_L)>\kappa\}.
\]

Under the declared linear-Gaussian model,

\[
\boxed{
I_{\rm read}(L)
=
\frac12\log_2\det\left[
I+
\Sigma_x^{1/2}
\mathcal G_L^T\Sigma_N^{-1}
\mathcal G_L
\Sigma_x^{1/2}
\right]\;\mathrm{rbit}.
}
\]

This is policy-conditioned physical readability, not intrinsic information
independent of apparatus.

## 11. Memory and echo readouts

\[
\boxed{
\tau_{\rm echo}
=
\operatorname*{arg\,max}_{\tau>0}
I_{\rm read}(\tau)
}
\]

for a declared observation protocol.

For threshold \(I_*\),

\[
\boxed{
\tau_{\rm mem}^{(I_*)}
=
\sup\{\tau:I_{\rm read}(\tau)\ge I_*\}.
}
\]

A later peak is an echo. A monotone decrease is fading memory. Rank loss is
structural loss under the declared channel. Small singular values are practical
unreadability under noise.

## 12. Classification gates

| Class | Mathematical gate |
|---|---|
| same-form return | typed \(\mathcal K\approx I\) |
| transformed but reconstructable | full column rank and acceptable \(\Sigma_{\rm rec}\) |
| partial return | \(0<\operatorname{rank}\mathcal K<\dim z\) |
| echo | delayed local maximum of \(I_{\rm read}(\tau)\) |
| no direct return | \(\mathcal K=0\) for the declared channel |
| practically unreadable | all whitened singular values below threshold |
| structurally unreadable | encoded direction lies in \(\ker\mathcal G_L\) |
| physical black-hole adapter | one-way causal cut plus geometric horizon certificate |

A finite observation of zero return does not prove permanent inaccessibility.
A native \(R=0\) parameter does not certify a gravitational event horizon.

## 13. Stability and well-posedness gates

For a finite linear hidden sector:

\[
\alpha_H=\max\Re\lambda(F_H).
\]

- \(\alpha_H<0\): asymptotically decaying hidden propagator;
- \(\alpha_H=0\): persistent or oscillatory memory is possible;
- \(\alpha_H>0\): growing return; finite horizon or nonlinear saturation must be
  declared.

Because nonnormal systems can grow transiently even when
\(\alpha_H<0\), also report

\[
g_H(T)=\sup_{0\le\tau\le T}\|e^{F_H\tau}\|.
\]

## 14. Nonlinear extension

For

\[
\dot x_H=f_H(x_H,x_O,u),
\]

the exact return is generally a nonlinear response functional, not a matrix
kernel. Along a declared trajectory, define the tangent propagator

\[
\partial_tU_H(t,s)
=
\left.\frac{\partial f_H}{\partial x_H}\right|_{x(t)}
U_H(t,s),
\qquad
U_H(s,s)=I.
\]

Then

\[
\mathcal K_{\rm tangent}(t,s)
=
A(t)R(t)U_H(t,s)W(s)E(s)
\]

is only a local linearization. Universal nonlinear return remains `Open`.

## 15. Upgraded master box

\[
\boxed{
\begin{gathered}
\delta_R\Rightarrow
\mathscr H_T\Rightarrow
\mathscr X_T=(\mathscr H_T\oplus\mathscr H_T),
\\
\mathbb G_T=L_R\otimes I+I\otimes C_{\mathcal F}+C_{\rm int},
\\
\mathcal E_{\rm DRL}[X]_n=\mathcal J_{C,n}[X_n],
\\
\mathcal T_{n+1}=\mathcal T_n\oplus E_{T,n}(\bar HX_n),
\\
\mathcal K_{\alpha\leftarrow\beta}(\tau)
=
A_\alpha\bar O_\alpha R_\alpha
\mathcal U_H(\tau)
\bar H_\beta W_\beta\bar O_\beta E_\beta,
\\
Y_L=\mathcal G_Lx_0+N_L,
\\
I_{\rm read}(L)
=
\frac12\log_2\det\left[
I+
\Sigma_x^{1/2}
\mathcal G_L^T\Sigma_N^{-1}
\mathcal G_L\Sigma_x^{1/2}
\right]\;\mathrm{rbit},
\\
P_{\alpha,n}
=
\Pi_\alpha(Y_L,\delta_{\alpha},\Sigma_N,\text{decoder},\text{threshold}).
\end{gathered}
}
\]

## 16. Binding claim boundary

```yaml
native_DRL: derived_narrow
forced_DRL_cut_equations: Dr
cut_balance: requires declared retention covector and certificate
linear_hidden_elimination: exact_algebra_in_declared_scope
linear_return_kernel: exact_algebra_in_declared_scope
linear_Gaussian_readability: exact_under_declared_distribution
AP17_runtime: finite_diagnostic
nonlinear_return_kernel: local_linearization_only
unified_DRL_cut_tape_action: Open
all_retained_states_eventually_return: not_claimed
physical_black_hole_from_native_cut_alone: not_claimed
```
