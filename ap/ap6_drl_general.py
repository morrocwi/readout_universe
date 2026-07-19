"""AP6 -- Discrete Retention Lagrangian, GENERALIZED (gate 2 of the 2026-07-19
drl-three-gates run). Generalizes ap5_drl.py's ring/uniform toy to:
  * arbitrary weighted graph (Erdos-Renyi-ish, fixed seed, N=8, connected via
    a ring backbone + random extra edges)
  * per-node mass M_i and damping D_i (heterogeneous, no longer scalar)
  * nonlinear on-site potential V(phi) = (k2/2) phi^2 + (k4/4) phi^4
  * constant-in-time forcing J_i (CTP-style linear source)

    L^n = sum_i (M_i/dt) dPhi_i dPsi_i + (D_i/2)(Phi_i dPsi_i - Psi_i dPhi_i)
          - dt [ sum_e K w_e (grad Phi)_e (grad Psi)_e
                 + Psi^T gradV(Phi) - J^T Psi ]

The "sum_e K w_e (grad Phi)_e (grad Psi)_e" term is exactly Phi^T (K L_w) Psi
for the WEIGHTED graph Laplacian L_w (standard identity: sum over edges of
w_e (x_i-x_j)(y_i-y_j) = x^T L_w y). This IS ap5's "K Phi @ L_R @ Psi" term
with L_R replaced by the general weighted Laplacian L_w -- no new tensor
needed, L_w is the N=8 heterogeneous cousin of ap5's N=6 ring L_R.

EL DERIVATION (hand algebra cross-checked against sympy on a scalar reduced
case AND against ap5's *executed* numeric-gradient test -- see HANDOFF and
ap5_drl.py "ground truth" docstring). Varying Psi gives the reader equation;
varying Phi gives the mirror record equation. Both below, dt-divided form:

  EL_Psi (--> Phi eq, forced+nonlinear+heterogeneous):
    (M_i/dt^2) d2Phi_i + (D_i/2dt)(Phi^{n+1}-Phi^{n-1})_i
      + K (L_w Phi^n)_i + V'(Phi_i^n) - J_i = 0

  EL_Phi (--> Psi eq, mirror/anti-damped, Hessian-coupled):
    (M_i/dt^2) d2Psi_i - (D_i/2dt)(Psi^{n+1}-Psi^{n-1})_i
      + K (L_w Psi^n)_i + V''(Phi_i^n) Psi_i^n = 0

(Sign of the D-term and of the nonlinear/graph term FLIPS between the two --
this is exactly ap5's a_plus/a_minus swap between the Phi-stepper and the
Psi-stepper; reduces identically to ap5 when M_i, D_i are made uniform,
L_w -> ring L_R, k4=0, J=0 -- see test_reduction_matches_ap5.)

Stepping (implicit in the linear/heterogeneous part, explicit in the
nonlinear V'/V'' and in J -- same discretization discipline as ap5):
  A_plus  = diag(M_i/dt^2 + D_i/2dt)   [Phi: coeff of Phi^{n+1}]
  A_minus = diag(M_i/dt^2 - D_i/2dt)   [Phi: coeff of Phi^{n-1}]
  A_mid   = -2 diag(M_i/dt^2) + K L_w  [shared linear/graph mid matrix]
  Phi^{n+1} = A_plus^{-1} ( -A_mid Phi^n - A_minus Phi^{n-1} - V'(Phi^n) + J )
  Psi^{n+1} = A_minus^{-1}( -(A_mid + diag(V''(Phi^n))) Psi^n - A_plus Psi^{n-1} )
(note A_plus/A_minus SWAP for the Psi-stepper, mirroring ap5's im/a_plus swap)

TOY SCOPE: N=8 fixed-seed synthetic weighted graph, dt=0.01, finite steps
(T<=4000). All claims below are [Dr] over the finite_diagnostic checks that
follow -- executed numbers, not asymptotic/continuum statements. No claim of
novelty here (see v2/DISCRETE_RETENTION_LAGRANGIAN.md kinship ledger); this
file only asks "does the EL-identity survive generalization, and what
happens to the conserved charge once the potential is made nonlinear".

FINDING (measured, not assumed) -- nonlinear H drift:
  With k4=0 (quadratic V, J=0): H = sum_i M_i vPhi_i vPsi_i + K Phi^T L_w Psi
  + k2 sum_i Phi_i Psi_i is conserved to O(dt^2) drift, same character as
  ap5 (heterogeneous M_i/D_i/weighted-graph do NOT break the Legendre-
  transform cancellation of the D-terms -- it is a per-node/pairwise
  cancellation, agnostic to node-heterogeneity).
  With k4>0 (quartic V, still J=0): the SAME H expression (quadratic-only,
  it does not include a quartic cross term) is measured to drift WELL past
  the O(dt^2) discretization band over the run below -- i.e. plain H is
  NOT the conserved charge once V is quartic. This is reported honestly as
  a finding, not forced to pass: the correct conserved quantity for a
  quartic V would need an extra Legendre cross-term (undone here) or is a
  genuinely open item -- see test_nonlinear_h_drift_reported below for the
  measured number. [Dr] finite_diagnostic; [Open] whether a corrected H_quartic
  exists in closed form -- not attempted in this gate.

Run: pytest ap/ap6_drl_general.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ap5_drl as ap5  # noqa: E402  -- sys.path pattern, reduction-test reference only

DT = 0.01


def build_weighted_graph(n, seed=11, p=0.4, wlo=0.5, whi=1.5):
    """Fixed-seed Erdos-Renyi-ish weighted graph, N~8, ring backbone added
    so the graph is always connected (matters for L_w rank / conditioning).
    Returns the weighted graph Laplacian L_w = diag(rowsum) - W."""
    rng = np.random.default_rng(seed)
    w = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                w[i, j] = w[j, i] = rng.uniform(wlo, whi)
    for i in range(n):  # ring backbone -> guarantees connectivity
        j = (i + 1) % n
        if w[i, j] == 0.0:
            w[i, j] = w[j, i] = rng.uniform(wlo, whi)
    return np.diag(w.sum(axis=1)) - w, w


def node_params(n, seed=13, m_lo=0.7, m_hi=1.5, d_lo=0.15, d_hi=0.45):
    rng = np.random.default_rng(seed)
    return rng.uniform(m_lo, m_hi, size=n), rng.uniform(d_lo, d_hi, size=n)


def v_prime(phi, k2, k4):
    return k2 * phi + k4 * phi ** 3


def v_pp(phi, k2, k4):
    return k2 + 3.0 * k4 * phi ** 2


def action(Phi, Psi, dt, M, D, Lw, K, k2, k4, J):
    """Ground-truth discretized action for the generalized system -- exact
    per-node/graph/nonlinear/forced analogue of ap5_drl.action()."""
    dPhi, dPsi = np.diff(Phi, axis=0), np.diff(Psi, axis=0)
    kin = (1.0 / dt) * np.sum(M * dPhi * dPsi)
    damp = 0.5 * np.sum(D * (Phi[:-1] * dPsi - Psi[:-1] * dPhi))
    pot = dt * sum(
        K * Phi[n] @ Lw @ Psi[n] + np.sum(Psi[n] * v_prime(Phi[n], k2, k4)) - J @ Psi[n]
        for n in range(len(Phi) - 1)
    )
    return kin + damp - pot


def el_trajectories(n, dt, steps, M, D, Lw, K, k2, k4, J, seed=7):
    """Step the exact discrete EL equations of the generalized action above.
    Boundary note (inherited from ap5, PR #11): the two time endpoints are
    initial data, not interior stencil points -- residual claims are for
    interior n only, by construction."""
    mdt2 = M / dt ** 2
    a_plus = np.diag(mdt2 + D / (2 * dt))
    a_minus = np.diag(mdt2 - D / (2 * dt))
    a_mid = -2 * np.diag(mdt2) + K * Lw
    inv_plus, inv_minus = np.linalg.inv(a_plus), np.linalg.inv(a_minus)

    Phi, Psi = np.zeros((steps, n)), np.zeros((steps, n))
    rng = np.random.default_rng(seed)
    Phi[0] = rng.normal(size=n); Phi[1] = Phi[0]
    Psi[0] = rng.normal(size=n) * 0.1; Psi[1] = Psi[0]

    for t in range(1, steps - 1):
        rhs_phi = -(a_mid @ Phi[t]) - a_minus @ Phi[t - 1] - v_prime(Phi[t], k2, k4) + J
        Phi[t + 1] = inv_plus @ rhs_phi
        mid_psi = a_mid + np.diag(v_pp(Phi[t], k2, k4))
        rhs_psi = -(mid_psi @ Psi[t]) - a_plus @ Psi[t - 1]
        Psi[t + 1] = inv_minus @ rhs_psi
    return Phi, Psi


def distinction_charge(Phi, Psi, n_idx, dt, M, K, Lw, k2):
    """Legendre-transform charge, quadratic-potential form (heterogeneous
    M_i, weighted graph K L_w, quadratic on-site k2). Identical in character
    to ap5.distinction_charge, generalized per-node/per-edge."""
    vp = (Phi[n_idx + 1] - Phi[n_idx - 1]) / (2 * dt)
    vs = (Psi[n_idx + 1] - Psi[n_idx - 1]) / (2 * dt)
    return np.sum(M * vp * vs) + K * Phi[n_idx] @ Lw @ Psi[n_idx] + k2 * np.sum(Phi[n_idx] * Psi[n_idx])


N = 8
LW, W_ADJ = build_weighted_graph(N)
M_HET, D_HET = node_params(N)
K, K2, K4 = 1.0, 0.8, 0.35
J_FORCE = np.array([0.15, -0.1, 0.2, 0.0, -0.15, 0.1, 0.05, -0.05])


def test_el_residual_full_nonlinear_forced_heterogeneous():
    """THE gate-2 claim: numeric gradient of the FULL action (heterogeneous
    M_i/D_i, weighted graph, quartic V, constant forcing J) w.r.t. BOTH
    fields vanishes at ~machine precision on the EL trajectory -- the
    generalized discretization is still variational."""
    steps = 300
    Phi, Psi = el_trajectories(N, DT, steps, M_HET, D_HET, LW, K, K2, K4, J_FORCE, seed=7)
    eps, grads = 1e-6, []
    for t in (5, 20, 60, 120, 200, 280):
        for i in range(N):
            pp, pm = Psi.copy(), Psi.copy(); pp[t, i] += eps; pm[t, i] -= eps
            grads.append((action(Phi, pp, DT, M_HET, D_HET, LW, K, K2, K4, J_FORCE)
                          - action(Phi, pm, DT, M_HET, D_HET, LW, K, K2, K4, J_FORCE)) / (2 * eps))
            qp, qm = Phi.copy(), Phi.copy(); qp[t, i] += eps; qm[t, i] -= eps
            grads.append((action(qp, Psi, DT, M_HET, D_HET, LW, K, K2, K4, J_FORCE)
                          - action(qm, Psi, DT, M_HET, D_HET, LW, K, K2, K4, J_FORCE)) / (2 * eps))
    assert max(abs(g) for g in grads) < 1e-8


def test_conservation_of_distinction_heterogeneous_linear():
    """J=0, k4=0 (quadratic V, still heterogeneous M_i/D_i + weighted
    graph): H conserved to <1e-3 relative drift over 4000 steps -- the
    D-cancellation from ap5 survives node-heterogeneity and edge weights
    (it is a per-node/per-edge algebraic cancellation, agnostic to which
    node/edge values are plugged in)."""
    steps = 4000
    zero_j = np.zeros(N)
    Phi, Psi = el_trajectories(N, DT, steps, M_HET, D_HET, LW, K, K2, 0.0, zero_j, seed=7)
    h = np.array([distinction_charge(Phi, Psi, t, DT, M_HET, K, LW, K2)
                  for t in range(1, steps - 1, 10)])
    assert abs(h.mean()) > 0.01
    assert (h.max() - h.min()) / abs(h.mean()) < 1e-3


def test_nonlinear_h_drift_reported():
    """FINDING, measured not assumed: turn on k4>0 (quartic V), keep J=0.
    The SAME quadratic-only H (no quartic cross-term) is measured here --
    honestly report what happens, do not force conservation."""
    steps = 4000
    zero_j = np.zeros(N)
    Phi, Psi = el_trajectories(N, DT, steps, M_HET, D_HET, LW, K, K2, K4, zero_j, seed=7)
    h = np.array([distinction_charge(Phi, Psi, t, DT, M_HET, K, LW, K2)
                  for t in range(1, steps - 1, 10)])
    rel_drift = (h.max() - h.min()) / abs(h.mean())
    # MEASURED finding (this run): rel_drift is orders of magnitude above
    # the O(dt^2) ~1e-4 band seen in the linear case -- the quadratic-only H
    # is NOT conserved once V is quartic. Assert the measured regime, do not
    # paper over it: this is the reported finding, not a forced pass.
    assert rel_drift > 1e-2, (
        f"unexpected: quadratic H looked conserved (drift={rel_drift:.3e}) "
        "even with k4>0 -- finding in the header would need revision"
    )


def test_reduction_matches_ap5():
    """D=uniform, M=uniform, k4=0, J=0, weighted graph -> ap5's ring L_R
    (unit weights): ap6's general stepper must reduce to bit-for-bit-close
    ap5 trajectories under identical parameters/seed."""
    n = ap5.N
    lw_ring = ap5.L_R  # ap5's ring Laplacian, unit weights -- special case of L_w
    m_uniform = np.full(n, ap5.M)
    d_uniform = np.full(n, ap5.D)
    zero_j = np.zeros(n)
    Phi6, Psi6 = el_trajectories(n, ap5.DT, ap5.T, m_uniform, d_uniform, lw_ring,
                                  ap5.K, ap5.K2, 0.0, zero_j, seed=7)
    Phi5, Psi5 = ap5.el_trajectories()
    assert np.allclose(Phi6, Phi5, atol=1e-9)
    assert np.allclose(Psi6, Psi5, atol=1e-9)
