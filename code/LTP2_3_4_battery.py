"""
LTP2 + LTP3 + LTP4 -- Universal Philosophy & Logic (UPL) test battery, release 2
Engine: same residual-flow core as LTP1 (Aeps=delta, V=1/2r^TWr, eps=-LambdaA^TW r)

LTP2  sorites_as_threshold      -> would lift L-10 [Wf]->[Dr]
LTP3  bounded_quantification    -> would lift L-05 [Dr]->[Dr-anchored]
LTP4  rank_deficiency_goedel    -> would lift L-11 [Cj]->[Dr] (structural analogy only)
"""

import numpy as np
rng = np.random.default_rng(7)
results = []

def add(name, ok, detail): results.append((name, ok, detail))

# =====================================================================
# LTP2 -- SORITES AS RETENTION-THRESHOLD ARTIFACT
# World-side: graded quantity g(n) (e.g. "heapness" vs grains n), smooth.
# Knower-side readout: binary predicate H(n) = [g(n) >= Pi].
# Claims to verify:
#  C1: graded level obeys TOLERANCE: |g(n)-g(n-1)| < tol for all n (no jump in the world)
#  C2: binary readout has EXACTLY ONE discontinuity, located at Pi-crossing
#      -> the "paradoxical step" exists only in the projection
#  C3: moving Pi moves the flip point but leaves g(n) untouched
#      -> the paradox lives in the readout operator, not in the world
# =====================================================================
n_grid = np.arange(1, 10001)
g = 1.0 - np.exp(-n_grid / 1500.0)          # smooth graded "heapness"
tol = np.max(np.abs(np.diff(g)))
c1 = tol < 1e-3                              # world-side tolerance holds

def flips(Pi):
    H = (g >= Pi).astype(int)
    d = np.diff(H)
    return np.flatnonzero(d != 0)

f_05 = flips(0.5); f_08 = flips(0.8)
c2 = (len(f_05) == 1)
c3 = (len(f_08) == 1) and (f_08[0] != f_05[0]) and np.allclose(g, 1.0 - np.exp(-n_grid/1500.0))
add("LTP2-C1 world-side tolerance (graded g smooth)", c1, f"max step |Deltag|={tol:.2e} < 1e-3")
add("LTP2-C2 binary readout has exactly ONE forced jump", c2, f"flip at n={f_05[0]+1} for Pi=0.5 (count={len(f_05)})")
add("LTP2-C3 paradox tracks Pi, not the world", c3, f"Pi=0.5->flip n={f_05[0]+1}; Pi=0.8->flip n={f_08[0]+1}; g unchanged")
# Reading: 'tolerance principle' (heap(n)->heap(n-1)) is TRUE of g, FALSE of H exactly
# at one Pi-determined point => sorites = projection artifact of retention threshold Pi. [Dr]

# =====================================================================
# LTP3 -- BOUNDED QUANTIFICATION (inference over S_A  proper-subset-of  Delta)
# Full grammar: 3 constraints over 4 propositions (as LTP1).
# Salient sub-grammar: knower attends only to constraints {1,2} (drops row 3).
# Case A: dropped constraint NOT load-bearing for query q=(b1-b2)  -> bounded ~= full
# Case B: query q'=(b3-b4) DEPENDS on dropped row                  -> bounded diverges
# Pass: divergence occurs IFF the discarded difference is load-bearing.
# =====================================================================
A_full = np.array([[1.,-1.,0.,0.],[0.,1.,-1.,0.],[0.,0.,1.,-1.]])
A_sal  = A_full[:2]                          # salience-selected grammar
d_full = np.array([1.0, 0.5, -0.3])
d_sal  = d_full[:2]

def settle(A, d, T=80.0, dt=0.01):
    n = A.shape[1]; eps = np.zeros(n); W = np.eye(A.shape[0]); Lam = 0.8*np.eye(n)
    for k in range(int(T/dt)):
        r = A @ eps - d
        eps = eps - dt * (Lam @ (A.T @ W @ r))
    return eps

e_full = settle(A_full, d_full)
e_sal  = settle(A_sal,  d_sal)
qA_full, qA_sal = e_full[0]-e_full[1], e_sal[0]-e_sal[1]     # b1-b2
qB_full, qB_sal = e_full[2]-e_full[3], e_sal[2]-e_sal[3]     # b3-b4
caseA_ok = abs(qA_full - qA_sal) < 1e-3                       # agree when not load-bearing
caseB_div = abs(qB_full - qB_sal) > 0.25                      # diverge when load-bearing
add("LTP3-A bounded inference ~= full when discard is idle", caseA_ok,
    f"(b1-b2): full={qA_full:+.3f} vs bounded={qA_sal:+.3f}")
add("LTP3-B bounded inference diverges when discard is load-bearing", caseB_div,
    f"(b3-b4): full={qB_full:+.3f} vs bounded={qB_sal:+.3f} (bounded knower has NO access to this difference)")
# Reading: 'forall ' of a finite knower quantifies over S_A; validity is relative to whether
# discarded differences are load-bearing for the query -- exactly L-05. [Dr-anchored]

# =====================================================================
# LTP4 -- RANK DEFICIENCY => TRUE-BUT-UNREACHABLE (Goedel-flavored, STRUCTURAL ANALOGY ONLY)
# A_full above has rank 3 < n=4: null(A) = span(1,1,1,1).
# Two distinct world-configurations theta1 != theta2 differing along the null space
# produce IDENTICAL records delta = Atheta, hence identical residual dynamics forever.
# Checks:
#  C1: theta1 != theta2 (a real difference exists)
#  C2: Atheta1 == Atheta2 exactly (records identical) => no admissible inference separates them
#  C3: Fisher matrix J^T J is singular (identifiability statement, RUSC-style)
# =====================================================================
theta1 = np.array([0.7, -0.3, 0.2, 0.5])
theta2 = theta1 + 1.3*np.ones(4)             # shift along null space
c1 = not np.allclose(theta1, theta2)
c2 = np.allclose(A_full@theta1, A_full@theta2, atol=1e-12)
F = A_full.T @ A_full
c3 = np.linalg.matrix_rank(F) < 4 and abs(np.linalg.det(F)) < 1e-10
add("LTP4-C1 a genuine world-difference exists", c1, f"||theta1-theta2||={np.linalg.norm(theta1-theta2):.3f}")
add("LTP4-C2 records are identical => difference inaccessible-admissible", c2,
    "Atheta1 == Atheta2 exactly; every inference trajectory coincides")
add("LTP4-C3 Fisher rank-deficient (identifiability, not mysticism)", c3,
    f"rank(A^TA)={np.linalg.matrix_rank(F)}/4, det={np.linalg.det(F):.1e}")
# Reading: 'true but unprovable-from-records' realized as null-space truth. This is a
# STRUCTURAL ANALOGY to incompleteness (self-reference NOT constructed here) -- the honest
# lift is L-11 [Cj]->[Dr] as identifiability reading, with the formal Goedel bridge still Open.

print("LTP2-LTP4 battery")
print("="*84)
ok = True
for nm, p, dt_ in results:
    ok &= p; print(f"[{'PASS' if p else 'FAIL'}] {nm}\n        {dt_}")
print("="*84)
print("SUITE:", ("PASS 8/8 -- lifts: L-10->[Dr], L-05->[Dr-anchored], L-11->[Dr as identifiability; "
                 "Goedel formal bridge remains Open]") if ok else "FAIL")
