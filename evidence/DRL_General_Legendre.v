(* ===================================================================== *)
(*  DRL_General_Legendre.v -- GENERAL-N Legendre D-cancellation for the   *)
(*  Discrete Retention Lagrangian (2026-07-19, closes the "Coq general-N" *)
(*  half of the conservation structure; see v2/DISCRETE_RETENTION_        *)
(*  LAGRANGIAN.md and ap/ap6_drl_general.py / ap/ap8_h_quartic.py).       *)
(*                                                                        *)
(*  WHAT IT PROVES: for ANY number of nodes (list-indexed), ANY per-node  *)
(*  masses M_i and dampings D_i (heterogeneous), ANY graph coupling GB    *)
(*  (abstract term -- covers K Phi.Lw.Psi for every weighted graph), and  *)
(*  ANY per-node non-D coupling w_i (abstract -- covers the quadratic     *)
(*  k2 q r, the quartic Psi.gradV(Phi) of AP8's H_nl, and forcing -J.Psi),*)
(*  the discrete Legendre transform of the DRL Lagrangian is EXACTLY the  *)
(*  D-free pairing:                                                       *)
(*      H  =  sum_i M_i vq_i vr_i  +  GB  +  sum_i w_i                    *)
(*  i.e. the damping tensor drops out of the conserved-charge STRUCTURE   *)
(*  at full generality, by list induction + per-node ring identity.       *)
(*                                                                        *)
(*  WHAT IT DOES NOT PROVE: (a) the general-N EL-identity (stationarity   *)
(*  <-> damped recurrence) -- that remains at 3-ring scope                *)
(*  (DRL_Discrete.v / solver InfoRetentionLagrangian_attempt.v);          *)
(*  (b) conservation ALONG trajectories (dH/dt=0 needs the EL equations;  *)
(*  hand-derived + numerics ap6/ap8, reviewer-re-derived PR #15);         *)
(*  (c) anything about D<>0 exact discrete conservation (O(dt^2) drift    *)
(*  measured, not claimed away).                                          *)
(*                                                                        *)
(*  Over Q, axiom-free target (check Print Assumptions).                  *)
(* ===================================================================== *)

Require Import QArith.
Require Import List.
Import ListNotations.

Open Scope Q_scope.

(* one node's data: mass, damping, positions (q,r), velocities (vq,vr),
   and w = the node's arbitrary non-D coupling term (potential/forcing). *)
Record node := mkNode { nM : Q; nD : Q; nq : Q; nr : Q; nvq : Q; nvr : Q; nw : Q }.

(* per-node Lagrangian piece: M vq vr + (D/2)(q vr - r vq) - w  *)
Definition Lnode (x : node) : Q :=
  nM x * (nvq x * nvr x)
  + (nD x / (2#1)) * (nq x * nvr x - nr x * nvq x)
  - nw x.

(* per-node momenta (coefficients of the velocities in Lnode) *)
Definition p_phi (x : node) : Q := nM x * nvr x - (nD x / (2#1)) * nr x.
Definition p_psi (x : node) : Q := nM x * nvq x + (nD x / (2#1)) * nq x.

(* per-node Legendre piece and the D-free target piece *)
Definition legendre_node (x : node) : Q :=
  p_phi x * nvq x + p_psi x * nvr x - Lnode x.
Definition pairing_node (x : node) : Q :=
  nM x * (nvq x * nvr x) + nw x.

Fixpoint qsum (f : node -> Q) (l : list node) : Q :=
  match l with
  | [] => 0
  | x :: t => f x + qsum f t
  end.

(* full Lagrangian over any node list, with GB = arbitrary graph coupling
   (enters with no D anywhere -- covers K Phi.Lw.Psi on any weighted graph) *)
Definition Lfull (l : list node) (GB : Q) : Q := qsum Lnode l - GB.

(* full Legendre transform *)
Definition Hfull (l : list node) (GB : Q) : Q :=
  qsum (fun x => p_phi x * nvq x + p_psi x * nvr x) l - Lfull l GB.

(* ---- per-node identity: the D-terms cancel nodewise ---- *)
Lemma legendre_node_D_free :
  forall x : node, legendre_node x == pairing_node x.
Proof.
  intro x. unfold legendre_node, pairing_node, Lnode, p_phi, p_psi. field.
Qed.

(* qsum respects pointwise-== functions (needed for setoid Q) *)
Lemma qsum_ext :
  forall (f g : node -> Q) (l : list node),
  (forall x, f x == g x) -> qsum f l == qsum g l.
Proof.
  intros f g l Hfg. induction l as [| x t IH]; simpl.
  - reflexivity.
  - rewrite (Hfg x). rewrite IH. reflexivity.
Qed.

(* qsum is additive over pointwise sums/differences *)
Lemma qsum_sub :
  forall (f g : node -> Q) (l : list node),
  qsum (fun x => f x - g x) l == qsum f l - qsum g l.
Proof.
  intros f g l. induction l as [| x t IH]; simpl.
  - ring.
  - rewrite IH. ring.
Qed.

(* ===================================================================== *)
(*  THE THEOREM: general-N, heterogeneous, arbitrary-graph,               *)
(*  arbitrary-potential Legendre D-cancellation.                          *)
(* ===================================================================== *)
Theorem general_legendre_D_cancellation :
  forall (l : list node) (GB : Q),
  Hfull l GB == qsum pairing_node l + GB.
Proof.
  intros l GB. unfold Hfull, Lfull.
  assert (Hstep :
    qsum (fun x => p_phi x * nvq x + p_psi x * nvr x) l - qsum Lnode l
    == qsum pairing_node l).
  { rewrite <- qsum_sub.
    apply qsum_ext. intro x.
    unfold pairing_node.
    assert (Hx := legendre_node_D_free x).
    unfold legendre_node, pairing_node in Hx.
    rewrite <- Hx. ring. }
  rewrite <- Hstep. ring.
Qed.

(* Sanity corollary: with all w_i == 0 and GB == 0 the pairing reduces to
   the pure kinetic reader-record pairing (zero-diagonal metric alone). *)
Corollary kinetic_only_case :
  forall l : list node,
  (forall x, In x l -> nw x == 0) ->
  Hfull l 0 == qsum (fun x => nM x * (nvq x * nvr x)) l.
Proof.
  intros l Hw.
  rewrite (general_legendre_D_cancellation l 0).
  assert (Hp : qsum pairing_node l
               == qsum (fun x => nM x * (nvq x * nvr x)) l).
  { induction l as [| x t IH]; simpl.
    - reflexivity.
    - unfold pairing_node at 1. rewrite (Hw x (or_introl eq_refl)).
      rewrite IH.
      + ring.
      + intros y Hy. apply Hw. right. exact Hy. }
  rewrite Hp. ring.
Qed.

Print Assumptions general_legendre_D_cancellation.
Print Assumptions kinetic_only_case.
