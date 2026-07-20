# AP17 — Return Transformation and Physical Readability Smoke Test

**Version:** `0.4.0-return`  
**Verdict:** `PASS`  
**Tier:** `finite_diagnostic`

## 1. Purpose

AP17 tests the statement

\[
\text{returned form}\neq\text{returned information}.
\]

It asks whether an encoded state can return through a hidden sector in a form
that differs from the original while remaining reconstructable under a
declared decoder and noise model.

## 2. Return kernel

For encoder \(E_\beta\), write channel \(W_\beta\), hidden propagator
\(\mathcal U_H(\tau)\), return channel \(R_\alpha\), and readout \(A_\alpha\),

\[
\boxed{
\mathcal K_{\alpha\leftarrow\beta}(\tau)
=A_\alpha\bar O_\alpha R_\alpha
\mathcal U_H(\tau)
\bar H_\beta W_\beta\bar O_\beta E_\beta.
}
\]

For the linear smoke test,

\[
\boxed{\mathcal U_H(\tau)=e^{F_H\tau}.}
\]

The measured return is

\[
y(\tau)=\mathcal K(\tau)z+\eta.
\]

## 3. Readability

For Gaussian encoded state covariance \(\Sigma_x\) and Gaussian noise
covariance \(\Sigma_\eta\),

\[
\boxed{
I_{\rm read}(\tau)
=\frac12\log_2\det\left[
I+\Sigma_x^{1/2}\mathcal K(\tau)^T\Sigma_\eta^{-1}
\mathcal K(\tau)\Sigma_x^{1/2}
\right].
}
\]

For a full-column-rank kernel, the generalized least-squares decoder is

\[
\boxed{
D_*=(\mathcal K^T\Sigma_\eta^{-1}\mathcal K)^{-1}
\mathcal K^T\Sigma_\eta^{-1}.
}
\]

## 4. Recorded cases

### 4.1 Transformed but reconstructable

The recorded kernel has

\[
\operatorname{rank}\mathcal K=2,
\qquad
\|\mathcal K-I\|_2=1.222171974564525.
\]

Thus its form is substantially different from the identity. Nevertheless,

\[
\|D_*\mathcal K-I\|_2
=2.289691319182597\times10^{-16}.
\]

Under the declared Gaussian policy,

\[
I_{\rm read}=7.825375266365017\ \mathrm{rbit}.
\]

### 4.2 Partial return

\[
\operatorname{rank}\mathcal K=1,
\qquad
\operatorname{nullity}\mathcal K=1.
\]

No full inverse decoder exists; only one encoded direction returns.

### 4.3 No direct return

\[
\mathcal K=0,
\qquad
I_{\rm read}=0.
\]

This is a channel/readout statement and does not establish destruction.

### 4.4 Delayed echo

A cross-coordinate kernel was chosen with

\[
\mathcal K(0)=0.
\]

Its largest recorded magnitude occurs at

\[
\tau_{\rm echo}=0.885,
\qquad
\mathcal K(\tau_{\rm echo})=0.8972693231816911.
\]

This supplies a delayed-return example rather than an immediate read-back.

## 5. Exact hidden-elimination check

For

\[
\dot x_O=F_{OO}x_O+Rx_H,
\qquad
\dot x_H=Wx_O+F_Hx_H,
\]

the full block solution was compared with the reduced Volterra equation using

\[
K_{\rm mem}(t)=Re^{F_Ht}W.
\]

Maximum absolute residual:

\[
6.189493362285248\times10^{-15}.
\]

## 6. Time-window result

With sampled output \(y_k=Cx_k+\eta_k\), define

\[
\mathcal G_L=\begin{pmatrix}C\\CF\\\vdots\\CF^L\end{pmatrix}.
\]

The recorded rank increased from

\[
1\longrightarrow3
\]

as the measurement window increased. A state unreadable from one instantaneous
sample became structurally readable from a longer trajectory.

## 7. Gates

```text
transformed_return_is_not_identity                 PASS
transformed_return_is_full_rank                    PASS
known_decoder_recovers_noiseless_input             PASS
partial_return_is_rank_deficient                   PASS
zero_return_has_zero_information                   PASS
echo_is_delayed                                    PASS
hidden_elimination_identity_matches_full_system    PASS
longer_window_improves_rank                        PASS
```

## 8. Verdict

\[
\boxed{
\text{same returned form}
\not\equiv
\text{same returned information}.
}
\]

A transformed return can remain fully reconstructable. Physical readability
must be judged using typing, rank, conditioning, noise, time window, and a
declared decoding policy—not by \(\|\mathcal K-I\|\) alone.

```yaml
linear_return_kernel: exact_algebra_in_declared_scope
Gaussian_readability: exact_for_declared_linear_Gaussian_channel
runtime: finite_diagnostic
nonlinear_universal_return: Open
all_retained_states_eventually_return: not_claimed
```
