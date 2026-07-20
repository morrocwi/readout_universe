# URR-C Coq Formal Chain — Philosophy Root to Master Equation

## Status

This document specifies the first conditional machine-checked chain joining the
formal retained-difference root to the URR-C 0.4 master architecture.

The corresponding Coq source is:

- `evidence/URR_C_Foundational_Chain.v`

The intended build command is:

```bash
make verify-urr-coq
```

## What “from philosophy to equation” can honestly mean

Coq cannot prove an ontological interpretation from no premises. The philosophy
must first be separated into:

1. **formal primitives and axioms**, which Coq can type-check and reason from;
2. **interpretive bridges**, which remain `Dr` until an independently testable
   physical derivation is supplied;
3. **mathematical consequences**, which may receive `Th_coqc` in the exact
   compiled scope.

The formal chain is therefore conditional rather than rhetorical:

```text
Retained distinction formal root
  -> injective distinction theorem
  -> finite typed dimension/index
  -> doubled reader-record state
  -> lifted accessible/hidden split
  -> native DRL action theorem anchors
  -> balanced cut certificate
  -> injective append-only tape
  -> return-transform composition and decoder gate
  -> projected reader and mirror master equations
```

## The formal links

### F0 — Retained distinction root

The existing theorem

```coq
RD4_succ_inj : forall x y : D, succ x = succ y -> x = y
```

is re-exported as `F0_RD4_retained_difference_injective`.

This is the formal content of “a retained distinction does not collapse under
the declared successor constructor.” It is not by itself a theorem that every
physical history is retained.

### F1 — Distinction-reflecting finite dimension

The bridge defines

```coq
rd_dimension d := toNat d
```

and proves that equal formal dimensions reflect equal retained-difference
objects, using the existing `toNat_inj` theorem.

This provides an honest formal index root for finite state spaces without
claiming that arithmetic alone generates physics.

### F2 — Reader-record doubled state

For any carrier `V`,

```coq
RRState V := V * V
```

with exact selectors `P_Phi` and `P_Psi`. Coq proves both beta laws and the eta
law:

```text
P_Phi (Phi,Psi) = Phi
P_Psi (Phi,Psi) = Psi
(P_Phi X, P_Psi X) = X
```

This is the exact typing behind

```text
X_n = (Phi_n, Psi_n)^T.
```

It does not prove that `Psi` has a unique ontic interpretation.

### F3 — Lifted readout split

A `ReadoutSplit` is an adapter obligation containing:

- accessible operator `O`;
- hidden operator `H`;
- idempotence;
- cross-annihilation;
- a declared merge law reconstructing the original state.

The bridge proves that these laws lift componentwise to `RRState V`. This is
the formal typing behind

```text
Obar = I_2 tensor O
Hbar = I - Obar
```

without pretending that the split itself has been derived from DRL.

### F4 — Master equation projects to components

The abstract master equation is represented as

```coq
forall X, E_DRL X = J_C X.
```

Coq proves that this equality implies both projected laws:

```text
P_Phi(E_DRL X) = P_Phi(J_C X)
P_Psi(E_DRL X) = P_Psi(J_C X).
```

This is the formal connection from the compact master equality to the explicit
reader and mirror equations.

### F5 — Exact balanced cut theorem

For the three-sector state `(visible, hidden, tape)`, the cut step is

```text
visible' = visible - write + return
hidden'  = hidden + write - return - tape_write
tape'    = tape + tape_write.
```

Coq proves over integers:

```text
visible' + hidden' + tape'
= visible + hidden + tape.
```

This is exact algebra. Positivity and physical interpretation remain separate
adapter obligations.

### F6 — Append-only tape

For

```coq
append_record tape cell := tape ++ [cell]
```

Coq proves:

- the old history remains a prefix;
- appending to the same history is injective in the new cell;
- distinct new cells produce distinct histories.

This is a direct formal realization of append-only non-overwrite. It does not
prove that a finite-dimensional accumulator is injective.

### F7 — Return-transform and decoder

The return kernel is represented by typed function composition:

```text
A_alpha o O_read o R_alpha o U_H o H_hidden o W_beta o O_write o E_beta.
```

Coq proves the composition unfolds exactly. Under a declared left-inverse
decoder, it proves exact message recovery. Under a declared zero return-readout
map, it proves a zero direct return kernel.

This proves the algebraic gate, not universal physical return.

### F8 — Existing DRL anchors

The bridge imports and aliases the existing machine-checked theorems:

- `T1_el_psi_node1` — reader EL iff damped recurrence, 3-ring scope;
- `T1_el_psi_node2` — second reader node;
- `T1_el_phi_node1` — mirror EL iff anti-damped recurrence;
- `T2_D_cancellation` — 3-ring Legendre D cancellation;
- `general_legendre_D_cancellation` — axiom-free general-N D cancellation.

The new file therefore depends on the original DRL proof objects rather than
merely repeating their names in documentation.

## Evidence boundary

```yaml
philosophical_interpretation: Dr
RD4_injectivity: Th_coqc
RD_dimension_reflection: pending_new_compile
reader_record_product_typing: pending_new_compile
lifted_readout_split_given_declared_split_laws: pending_new_compile
native_DRL_EL_anchors: Th_coqc_in_existing_scope
native_general_N_D_cancellation: Th_coqc
balanced_cut_total_identity: pending_new_compile
append_only_tape_injectivity: pending_new_compile
return_composition: pending_new_compile
left_decoder_recovery_given_left_inverse: pending_new_compile
forced_DRL_cut_physical_bridge: Dr
unified_DRL_cut_tape_action: Open
nonlinear_universal_return: Open
physical_black_hole_derivation: not_claimed
```

## What remains to formalize

1. A general-N Euler-Lagrange theorem, beyond the current 3-ring EL proof.
2. Matrix/vector definitions matching every operator in the YAML contract.
3. A discrete Lagrange-d'Alembert theorem deriving the forced component form.
4. A formal retention covector theorem for general finite matrices.
5. Matrix exponential and convolution identities for hidden elimination.
6. Rank, singular values, and Gaussian log-determinant information, likely using
   MathComp/Coquelicot or a deliberately finite rational surrogate.
7. A unified action or a formal no-go theorem for DRL plus exact injective tape.
8. External semantics connecting formal retained distinction to physical
   ontology; this cannot be obtained from type-checking alone.
