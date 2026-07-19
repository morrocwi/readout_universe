"""
LTP1 -- Logic as Residual Flow (Universal Philosophy & Logic, canon v0.2)
Reuses the MVS engine from yaoharee-proposal (Aeps=delta, V=1/2r^TWr, eps=-LambdaA^TW r)
but reads it at the LOGIC tau_c:

  A  = logical grammar (relational Jacobian; A2-admissible transport)
  eps  = belief-state deviation of a finite knower
  delta  = world-resistance readout (theta via record operator; noisy, time-varying)
  r  = Aeps-delta  = residual = "incoherence of the belief state w.r.t. evidence"

Three checks (pass criteria stated up front, MVS-style):

  C1 CONVERGENCE   : constant delta => V(t) monotone v, r -> r_min (inference = Lyapunov descent)
  C2 DEFEASIBILITY : delta changes at t_s (new evidence) => a previously "concluded" proposition
                     REVISES (non-monotonic revision) and V re-descends (ISS tracking)
  C3 IRREDUCIBLE eps : noisy delta(t) (eta>0 floor) => V never reaches 0; time-averaged residual
                     bounded AWAY from 0  (operational face of eps_tot > 0, Theorem step 24)

If C1 fails  -> L-04 (inference as path) breaks.
If C2 fails  -> L-06 (defeasibility theorem) breaks.
If C3 gives V->0 exactly under noise -> universal falsifier fires (eps_tot=0).
"""

import numpy as np

rng = np.random.default_rng(42)

# --- grammar: 4 propositions, 3 relational constraints (rank-deficient on purpose:
#     a finite knower's grammar underdetermines the world -> A4 accessibility) ---
A = np.array([
    [1.0, -1.0,  0.0,  0.0],   # b1 - b2 should match evidence e1
    [0.0,  1.0, -1.0,  0.0],   # b2 - b3 should match evidence e2
    [0.0,  0.0,  1.0, -1.0],   # b3 - b4 should match evidence e3
])
m, n = A.shape
W   = np.eye(m)          # A5 admissibility: positive metric
Lam = 0.8 * np.eye(n)    # transport rate

def V_of(r):  return 0.5 * r @ W @ r

def run(delta_fn, T=60.0, dt=0.01, eps0=None):
    eps = np.zeros(n) if eps0 is None else eps0.copy()
    ts, Vs, epss = [], [], []
    steps = int(T/dt)
    for k in range(steps):
        t = k*dt
        d = delta_fn(t)
        r = A @ eps - d
        eps = eps - dt * (Lam @ (A.T @ W @ r))
        ts.append(t); Vs.append(V_of(A@eps - d)); epss.append(eps.copy())
    return np.array(ts), np.array(Vs), np.array(epss)

report = []

# ---------- C1: constant evidence -> inference converges ----------
d0 = np.array([1.0, 0.5, -0.3])
ts, Vs, epss = run(lambda t: d0)
mono_viol = int(np.sum(np.diff(Vs) > 1e-12))
c1_pass = (Vs[-1] < 1e-8) and (mono_viol == 0)
report.append(("C1 convergence (inference = Lyapunov descent)",
               c1_pass, f"V(0)={Vs[0]:.4f} -> V(end)={Vs[-1]:.2e}; monotonicity violations={mono_viol}"))

# ---------- C2: evidence flips mid-run -> conclusion revises ----------
d1 = np.array([-1.0, 0.5, -0.3])          # e1 flips sign at t_s = 30
def delta_switch(t): return d0 if t < 30.0 else d1
ts, Vs, epss = run(delta_switch)
i_pre  = int(29.9/0.01)                    # settled conclusion before switch
i_post = -1                                # settled conclusion after re-descent
concl_pre  = epss[i_pre,0]  - epss[i_pre,1]    # the "b1-b2" judgment
concl_post = epss[i_post,0] - epss[i_post,1]
jump = Vs[int(30.0/0.01)+1]                # V spikes when world resists
c2_pass = (abs(concl_pre - 1.0) < 1e-3) and (abs(concl_post + 1.0) < 1e-3) and (jump > 0.1) and (Vs[-1] < 1e-6)
report.append(("C2 defeasibility (non-monotonic revision under new resistance)",
               c2_pass, f"judgment(b1-b2): {concl_pre:+.3f} -> {concl_post:+.3f}; V spike at switch={jump:.3f}; V(end)={Vs[-1]:.2e}"))

# ---------- C3: noisy world -> residual floor never zero ----------
def delta_noisy(t):
    return d0 + 0.15*np.sin(3.0*t)*np.array([1,0,0]) + 0.05*rng.standard_normal(m)
ts, Vs, epss = run(delta_noisy, T=120.0)
V_tail = Vs[len(Vs)//2:]                   # discard transient
floor  = V_tail.mean()
c3_pass = floor > 1e-4                     # bounded away from zero
report.append(("C3 irreducible residual (operational eps_tot > 0)",
               c3_pass, f"time-averaged V over tail = {floor:.5f} (must be > 0); min V in tail = {V_tail.min():.5f}"))

print("LTP1 -- Logic as Residual Flow  (engine: yaoharee-proposal MVS / Aeps=delta)")
print("="*78)
ok = True
for name, p, detail in report:
    ok &= p
    print(f"[{'PASS' if p else 'FAIL'}] {name}\n       {detail}")
print("="*78)
print("SUITE:", "PASS 3/3 -- L-04, L-06, step-24 operational anchors delivered (T_op)" if ok else "FAIL")
