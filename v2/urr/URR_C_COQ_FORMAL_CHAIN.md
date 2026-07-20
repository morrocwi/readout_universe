# URR-C Coq Formal Chain — Philosophy Root to Master Equation

## Status

This document specifies the first machine-checked chain joining the
formal retained-difference root to the URR-C 0.4 master architecture. As of
2026-07-20, `evidence/URR_C_Foundational_Chain.v` compiles cleanly (coqc
8.20.1, Legion / ANSE.ASIA workstation, git rev
daa2f36274bd2afb466de46c5e6f11220beeba9a; `make verify-urr-coq` exit 0) and
its 7 `Print Assumptions` calls all report "Closed under the global
context" — see the Evidence boundary below for which named theorems that
covers. The interpretive bridges (`Dr`) and open items (`Open`) remain
exactly as conditional as before; only the compiled-mathematics side of the
chain moved from draft to machine-checked.

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
# Evidence-boundary update, 2026-07-20 (tier CORRECTION, not a new proof):
#   coqc: The Coq Proof Assistant, version 8.20.1 compiled with OCaml 5.4.0
#   machine: Legion (ANSE.ASIA workstation)
#   git_rev: daa2f36274bd2afb466de46c5e6f11220beeba9a
#   `make verify-urr-coq` exit 0; evidence/URR_C_Foundational_Chain.v has no
#   Admitted/Axiom/admit./Parameter tokens. Rows below are promoted to
#   Th_coqc ONLY where the named theorem itself appears in a `Print
#   Assumptions` call reporting "Closed under the global context"
#   (F0, F3_lifted_recompose, F4, F5, F6, F7_declared_left_decoder_recovers_message,
#   foundational_master_chain_core). Rows whose named sub-lemma was not
#   individually the target of a `Print Assumptions` call keep a
#   non-Th_coqc label even though they compile as part of the same
#   axiom-free file -- no claim exceeds what was actually printed. The
#   earlier "pending_new_compile" wording was stale: it described a machine
#   that had no coqc, not a property of the proof.
philosophical_interpretation: Dr
RD4_injectivity: Th_coqc
RD_dimension_reflection: compiled_2026-07-20_no_individual_print_assumptions_call  # F1; part of the axiom-free file but not itself a Print Assumptions target
reader_record_product_typing: compiled_2026-07-20_no_individual_print_assumptions_call  # F2; same caveat as above
lifted_readout_split_given_declared_split_laws: Th_coqc  # F3_lifted_recompose: Closed under the global context, coqc 8.20.1, 2026-07-20, rev daa2f36
native_DRL_EL_anchors: Th_coqc_in_existing_scope
native_general_N_D_cancellation: Th_coqc
balanced_cut_total_identity: Th_coqc  # F5_balanced_cut_conserves_declared_total: Closed under the global context, coqc 8.20.1, 2026-07-20, rev daa2f36
append_only_tape_injectivity: Th_coqc  # F6_append_cell_injective: Closed under the global context, coqc 8.20.1, 2026-07-20, rev daa2f36
return_composition: compiled_2026-07-20_no_individual_print_assumptions_call  # F7_return_kernel_is_declared_composition; part of the axiom-free file but not itself a Print Assumptions target
left_decoder_recovery_given_left_inverse: Th_coqc  # F7_declared_left_decoder_recovers_message: Closed under the global context, coqc 8.20.1, 2026-07-20, rev daa2f36
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
