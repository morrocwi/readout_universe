(* ===================================================================== *)
(*  RetentionLoopClosureMonotone.v -- a fresh, self-contained scaffold     *)
(*  toward philosophy.md's Section 7.21 (Self as a closure property, not  *)
(*  a substance -- the tau_c^H loop), built after a cross-repo survey     *)
(*  this session (2026-08-03) found no existing formalization of the      *)
(*  STANDING, MULTI-PASS closure claim itself anywhere in the workspace   *)
(*  -- only two structurally distinct siblings already named in           *)
(*  philosophy.md Section 7.21 (paradoxes.md Section 6's point-in-time    *)
(*  Origination construction; a proprietary repo's static single-instant  *)
(*  self-readout row_n(L_R)x). Nothing here is copied from any            *)
(*  proprietary source -- every definition and proof below is written     *)
(*  fresh for this file. The generic own-output-feeds-own-next-input      *)
(*  accumulator shape is independently reminiscent of the author's own    *)
(*  information-discrete-math skill (github.com/morrocwi/                 *)
(*  information-discrete-math, MIT, same author), whose IDM_Reduction.v   *)
(*  states a generic fold accumulator with the same next-state-built-     *)
(*  from-prior-state shape for an unrelated purpose (branch-kernel        *)
(*  reduction) -- credited here as a design/vocabulary precedent, no code *)
(*  is Required or copied from it.                                        *)
(*                                                                        *)
(*  WHAT THIS FILE PROVES: for ANY discrete update map U : Q -> Q that is *)
(*  a contraction toward a fixed point xstar (|U(x)-xstar| <= c*|x-xstar|,*)
(*  0<=c<1), the orbit x0, U(x0), U(U(x0)), ... converges toward xstar at *)
(*  a rate bounded by c^n (orbit_contracts) -- and, separately, that this *)
(*  bound is MONOTONE in the contraction ratio c: a weaker contraction    *)
(*  (larger c, closer to 1) never gives a tighter guaranteed bound at any *)
(*  fixed step count than a stronger one (degraded_closure_bound_monotone)*)
(*  -- i.e. more degraded closure implies a provably worse worst-case     *)
(*  convergence guarantee at every step, axiom-free, over Q.              *)
(*                                                                        *)
(*  WHAT THIS FILE DOES NOT PROVE, stated as plainly as Section 7.21's    *)
(*  own honesty-boundary discipline requires: (1) that any real update    *)
(*  rule for a world-model Omega_H (Section 7.21's own notation) actually *)
(*  IS a contraction map of this shape -- that identification is not     *)
(*  attempted here and remains exactly as open as Section 7.21 already   *)
(*  states; (2) anything about human agency, consciousness, the felt-     *)
(*  quality hard problem, or tau_c^H specifically -- this file never uses *)
(*  those words in a definition, only in this header, to state the        *)
(*  motivating connection; (3) that degraded closure in the real-world    *)
(*  sense Section 7.21 gestures at (sleep, anesthesia) corresponds to     *)
(*  "a larger c" in any measured, cited sense -- that mapping, if ever    *)
(*  attempted, would need its own finite_diagnostic or empirical work,    *)
(*  not this abstract result. This file supplies formal vocabulary and a  *)
(*  monotonicity proof pattern only -- a scaffold, not a closure of       *)
(*  Section 7.21's Dr/[Open] tier.                                        *)
(*                                                                        *)
(*  Over Q, axiom-free (check Print Assumptions).                        *)
(* ===================================================================== *)

Require Import QArith Qabs Lqa.

Open Scope Q_scope.

(* ============================ Qpow_nat ============================== *)
(* nat-indexed rational power, hand-rolled (matches the convention        *)
(* already used elsewhere in this repo's own evidence/ files, e.g.        *)
(* DRL_Hidden_Elimination_Convolution.v's Kmem). *)
Fixpoint Qpow_nat (q : Q) (n : nat) : Q :=
  match n with
  | O => 1
  | S k => q * Qpow_nat q k
  end.

Lemma Qpow_nat_nonneg : forall c n, 0 <= c -> 0 <= Qpow_nat c n.
Proof.
  intros c n Hc. induction n as [|k IH]; simpl.
  - lra.
  - apply Qmult_le_0_compat; assumption.
Qed.

Lemma Qpow_nat_monotone : forall c1 c2 n,
  0 <= c1 -> c1 <= c2 -> Qpow_nat c1 n <= Qpow_nat c2 n.
Proof.
  intros c1 c2 n Hc1 Hc12. induction n as [|k IH]; simpl.
  - lra.
  - assert (Hc2 : 0 <= c2) by lra.
    assert (H1 : c1 * Qpow_nat c1 k <= c2 * Qpow_nat c1 k).
    { apply Qmult_le_compat_r; [exact Hc12 | apply Qpow_nat_nonneg; exact Hc1]. }
    assert (H2 : c2 * Qpow_nat c1 k <= c2 * Qpow_nat c2 k).
    { rewrite (Qmult_comm c2 (Qpow_nat c1 k)), (Qmult_comm c2 (Qpow_nat c2 k)).
      apply Qmult_le_compat_r; [exact IH | exact Hc2]. }
    apply (Qle_trans _ _ _ H1 H2).
Qed.

(* ======================== The closure orbit ========================= *)
Section ClosureOrbit.

(* U is the abstract "one loop pass" map: apply U to a state and read off
   the next state. This is exactly Section 7.21's own vocabulary -- "Omega_H
   both (a) results from the loop's own prior passes and (b) conditions the
   loop's next pass" -- rendered as the single fact that orbit(n+1) is
   literally U applied to orbit(n), no external step-index dependence. *)
Variable U : Q -> Q.
Variable xstar : Q.
Hypothesis fixed_point : U xstar == xstar.
Variable c : Q.
Hypothesis c_nonneg : 0 <= c.
Hypothesis contraction : forall x, Qabs (U x - xstar) <= c * Qabs (x - xstar).

Fixpoint orbit (x0 : Q) (n : nat) : Q :=
  match n with
  | O => x0
  | S k => U (orbit x0 k)
  end.

(* THE MAIN CONVERGENCE BOUND: the orbit's distance to the fixed point
   after n passes is bounded by c^n times the initial distance -- a
   standard iterated-contraction estimate, proved here from first
   principles over Q, not assumed. *)
Theorem orbit_contracts : forall x0 n,
  Qabs (orbit x0 n - xstar) <= Qpow_nat c n * Qabs (x0 - xstar).
Proof.
  intros x0 n. induction n as [|k IH]; simpl.
  - ring_simplify. apply Qle_refl.
  - eapply Qle_trans.
    + apply contraction.
    + assert (Heq : c * Qpow_nat c k * Qabs (x0 - xstar)
                    == c * (Qpow_nat c k * Qabs (x0 - xstar))) by ring.
      rewrite Heq.
      rewrite (Qmult_comm c (Qabs (orbit x0 k - xstar))).
      rewrite (Qmult_comm c (Qpow_nat c k * Qabs (x0 - xstar))).
      apply Qmult_le_compat_r; [exact IH | exact c_nonneg].
Qed.

End ClosureOrbit.

(* ================ Degraded-closure monotonicity theorem ============= *)
(* THE NO-GO-SHAPED POSITIVE RESULT: for ANY two contraction ratios
   0<=c1<=c2 and ANY nonnegative initial distance d0, the guaranteed
   convergence bound at every fixed step count n is monotone in the
   ratio -- a weaker/more-degraded contraction (larger c) never produces
   a tighter guaranteed bound than a stronger one, at any step. This is
   the formal shape of Section 7.21's own falsifiable prediction ("a
   genuinely degraded closure should show a measurably slowed repair
   rate") -- restated here as an abstract, unconditional monotonicity
   fact about contraction bounds, not as a claim about any specific
   Omega_H update rule. *)
Theorem degraded_closure_bound_monotone :
  forall c1 c2 d0 n,
  0 <= c1 -> c1 <= c2 -> 0 <= d0 ->
  Qpow_nat c1 n * d0 <= Qpow_nat c2 n * d0.
Proof.
  intros c1 c2 d0 n Hc1 Hc12 Hd0.
  apply Qmult_le_compat_r; [apply Qpow_nat_monotone; assumption | assumption].
Qed.

(* ===================================================================== *)
(*  Non-vacuousness: a concrete contraction U x = (1#2)*x, fixed point 0, *)
(*  ratio c=1#2 -- explicit orbit values match the closed-form bound      *)
(*  exactly (equality, not just the inequality the abstract theorem       *)
(*  guarantees), confirming orbit_contracts is invocable and non-trivial. *)
(* ===================================================================== *)

Section ConcreteWitness.

Definition Uc (x : Q) : Q := (1#2) * x.

Lemma Uc_fixed_point : Uc 0 == 0.
Proof. unfold Uc. ring. Qed.

Lemma Uc_contraction : forall x, Qabs (Uc x - 0) <= (1#2) * Qabs (x - 0).
Proof.
  intro x. unfold Uc.
  assert (Heq : (1 # 2) * x - 0 == (1#2) * (x - 0)) by ring.
  rewrite Heq, Qabs_Qmult.
  apply Qle_refl.
Qed.

Example concrete_orbit_three_steps :
  orbit Uc (1#2) 3 == (1#2) * ((1#2) * ((1#2) * (1#2))).
Proof. reflexivity. Qed.

Example concrete_bound_matches_exactly :
  Qabs (orbit Uc (1#2) 3 - 0) == Qpow_nat (1#2) 3 * Qabs ((1#2) - 0).
Proof. reflexivity. Qed.

Example concrete_orbit_contracts_invocable :
  Qabs (orbit Uc (1#2) 3 - 0) <= Qpow_nat (1#2) 3 * Qabs ((1#2) - 0).
Proof.
  apply orbit_contracts.
  - discriminate.
  - exact Uc_contraction.
Qed.

Example concrete_degraded_ratio_worse :
  Qpow_nat (1#2) 5 * (3#1) <= Qpow_nat (9#10) 5 * (3#1).
Proof.
  apply degraded_closure_bound_monotone; discriminate.
Qed.

End ConcreteWitness.

Print Assumptions Qpow_nat_nonneg.
Print Assumptions Qpow_nat_monotone.
Print Assumptions orbit_contracts.
Print Assumptions degraded_closure_bound_monotone.
Print Assumptions concrete_orbit_contracts_invocable.
Print Assumptions concrete_degraded_ratio_worse.
