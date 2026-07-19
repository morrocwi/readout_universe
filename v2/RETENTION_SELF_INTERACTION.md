# Retention Self-Interaction Ratio — AP20

## Question

Paper IV measured the geometric spin ladder

\[
\kappa_{\rm geo}(0,\tfrac12,1)=\{0,1,1\}.
\]

Plain Hodge/1-form geometry therefore supplies one vector-curvature contribution. The target requiring two raised a narrower question: after a noncommutative channel algebra and self-carrier closure are granted, is an additional trilinear coefficient still independent, or is its relative weight forced by the same ordered product?

## Conditional statement

Assume:

1. **One unital ordered composition.** Channels compose by a unital bilinear associative product \(m(x,y)\).
2. **Borrowed commutator curvature.**
   \[
   K(x,y)=m(x,y)-m(y,x).
   \]
   This identifies circulation with the exchange-odd order defect. The noncommutative/Lie-algebraic input remains borrowed; AP20 does not derive it from RD4.
3. **Self-carrier closure.** A channel fluctuation belongs to the same algebra as the background channel, rather than being an external payload.
4. **One common quadratic load.** Geometric and self terms use the same invariant inner product. Its overall normalization is free, so only ratios are claimable.

Bilinearity then gives

\[
\begin{aligned}
K(A_x+\varepsilon a_x,A_y+\varepsilon a_y)
={}&K(A_x,A_y)\\
&+\varepsilon\bigl(K(A_x,a_y)+K(a_x,A_y)\bigr)\\
&+\varepsilon^2K(a_x,a_y).
\end{aligned}
\]

Thus the quadratic self term has polynomial coefficient one relative to the same product expansion; no separate trilinear coefficient is available once assumptions 1–3 hold.

The quadratic load produces two Hessian pieces:

\[
H_{\rm geo},\qquad H_{\rm self}.
\]

Under the same load normalization, AP20 measures

\[
\frac{c_{\rm self}}{c_{\rm geo}}=1,
\qquad
\frac{c_{\rm geo}+c_{\rm self}}{c_{\rm geo}}=2.
\]

Multiplying the common inner product by any positive constant rescales both coefficients equally and leaves these ratios unchanged. In the Paper-IV convention \(c_{\rm geo}=1\), this reads

\[
1_{\rm geo}+1_{\rm self}=2,
\qquad
\left(\frac{c_{\rm total}}{c_{\rm geo}}\right)^2=4.
\]

The number four is therefore a relative response ratio, not an absolute normalization derived by AP20.

## Executed artifacts

- `ap/ap20_retention_self_interaction.py`
- `ap/ap20_symbolic_forcing.py`
- `ap/ap20_stress.py`

They verify:

- the order defect is exchange-odd and obeys Jacobi because it descends from associative composition;
- symbolic generic matrices give the \(\varepsilon^2\) term exactly with coefficient one;
- the geometric and self Hessians have equal curvature multipliers under one common load;
- arbitrary common load rescaling changes the individual coefficients but leaves the ratios \(1\) and \(2\) invariant;
- the ratio survives 100 noncommuting backgrounds at three load scales;
- commutative and external-payload controls remove the self term.

## What AP20 does and does not change

Before AP20, the second contribution was introduced through the standard non-Abelian fluctuation operator.

After AP20, the narrower result is:

> Given borrowed commutator curvature, self-carrier closure and one common quadratic load, the self term is not an additional independently tunable vertex: it is the quadratic term of the same ordered-product expansion and has equal relative curvature weight to the geometric term in the executed finite representation.

AP20 therefore **re-expresses and conditionally constrains** the standard self-interaction structure. It does not remove the Lie-algebra/commutator borrow.

## Honest status

Closed conditionally:

- the polynomial coefficient of the self term;
- the normalization-safe relative equality \(c_{\rm self}/c_{\rm geo}=1\) in the executed finite representation;
- the relative total coupling \(2\) and response ratio \(4\).

Still open:

- why retained distinction forces a noncommutative channel algebra;
- why curvature must be its commutator/order defect;
- why self-carrier closure is selected;
- why the physical representation and gauge group are those required by nature;
- ghost, longitudinal and heat-kernel bookkeeping toward \(+11/3\);
- any Standard Model or RD4-alone derivation.

The first foundational gate is therefore **not fully passed**. AP20 moves its frontier from “where does the second term come from?” to “why must the retention grammar choose commutator curvature and self-carrier closure?”
