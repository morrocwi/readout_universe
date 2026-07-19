"""AP5 -- the Discrete Retention Lagrangian (DRL), first executed run.

    L^n[X] = (M/2dt) dX^T (G(x)I) dX + (D/2) X^T (Omega(x)I) dX
             - (dt/2) X^T (G(x)(K L_R + k2 I)) X
    X = (Phi, Psi):  reader + RD4-forced record field
    G = [[0,1],[1,0]] retention metric (zero diagonal: quantity = pairing only)
    Omega = [[0,1],[-1,0]] retention symplectic (carries D)

Defined in v2/DISCRETE_RETENTION_LAGRANGIAN.md (registered there first,
2026-07-19). Kinship declared: Bateman 1931 / CTP doubling / discrete
variational integrators -- algebraic ancestry NOT claimed novel; candidate
novelty = graph-tensor form + ontic record + conservation-of-distinction
reading [Open]. TOY TIER: ring graph N=6, uniform M,D,K,k2. Claims: [Dr]
over the finite_diagnostic checks below.

Run: pytest ap/ap5_drl.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
import numpy as np

N, T, DT = 6, 4000, 0.01
M, D, K, K2 = 1.0, 0.35, 1.0, 0.8
L_R = 2 * np.eye(N) - np.roll(np.eye(N), 1, 0) - np.roll(np.eye(N), -1, 0)


def action(Phi, Psi, dt=DT):
    dPhi, dPsi = np.diff(Phi, axis=0), np.diff(Psi, axis=0)
    kin = (M / dt) * np.sum(dPhi * dPsi)
    damp = (D / 2) * np.sum(Phi[:-1] * dPsi - Psi[:-1] * dPhi)
    pot = dt * sum(K * Phi[n] @ L_R @ Psi[n] + K2 * np.sum(Phi[n] * Psi[n])
                   for n in range(len(Phi) - 1))
    return kin + damp - pot


def el_trajectories(damping=D, seed=7, dt=DT, steps=T):
    """Step the exact discrete EL equations of the action above.
    NOTE: the two endpoints in time are boundary data (initial conditions),
    not interior stencil points -- EL residual claims apply to interior n only
    by construction (reviewer note, PR #11)."""
    a_plus = (M / dt**2) * np.eye(N) + (damping / (2 * dt)) * np.eye(N)
    a_minus = (M / dt**2) * np.eye(N) - (damping / (2 * dt)) * np.eye(N)
    a_mid = -2 * (M / dt**2) * np.eye(N) + K * L_R + K2 * np.eye(N)
    Phi, Psi = np.zeros((steps, N)), np.zeros((steps, N))
    rng = np.random.default_rng(seed)
    Phi[0] = rng.normal(size=N); Phi[1] = Phi[0]
    Psi[0] = rng.normal(size=N) * 0.1; Psi[1] = Psi[0]
    ip, im = np.linalg.inv(a_plus), np.linalg.inv(a_minus)
    for n in range(1, steps - 1):
        Phi[n + 1] = ip @ (-(a_mid @ Phi[n]) - a_minus @ Phi[n - 1])  # damped reader
        Psi[n + 1] = im @ (-(a_mid @ Psi[n]) - a_plus @ Psi[n - 1])   # anti-damped record
    return Phi, Psi


def _charge_drift(dt, steps):
    Phi, Psi = el_trajectories(dt=dt, steps=steps)
    def h(n):
        vp = (Phi[n + 1] - Phi[n - 1]) / (2 * dt)
        vs = (Psi[n + 1] - Psi[n - 1]) / (2 * dt)
        return M * vp @ vs + K * Phi[n] @ L_R @ Psi[n] + K2 * Phi[n] @ Psi[n]
    hh = np.array([h(n) for n in range(1, steps - 1, 10)])
    return (hh.max() - hh.min()) / abs(hh.mean())


def readout_energy(Phi, n):
    v = (Phi[n + 1] - Phi[n - 1]) / (2 * DT)
    return 0.5 * M * v @ v + 0.5 * K * Phi[n] @ L_R @ Phi[n] + 0.5 * K2 * Phi[n] @ Phi[n]


def distinction_charge(Phi, Psi, n):
    """Legendre transform of L: the D-terms cancel -- H couples reader to
    record only (zero-diagonal metric G): H = M vP.vS + K P.L_R.S + k2 P.S"""
    vp = (Phi[n + 1] - Phi[n - 1]) / (2 * DT)
    vs = (Psi[n + 1] - Psi[n - 1]) / (2 * DT)
    return M * vp @ vs + K * Phi[n] @ L_R @ Psi[n] + K2 * Phi[n] @ Psi[n]


def test_el_derives_damped_spine_from_action():
    """THE claim: trajectories of the damped spine extremize S -- numeric
    gradient of the action w.r.t. interior field values vanishes at machine
    precision => the dissipative D-term IS variational under RD4 doubling."""
    Phi, Psi = el_trajectories()
    eps, grads = 1e-6, []
    for n in (5, 37, 100, 500, 1500, 3200):
        for i in range(N):
            pp, pm = Psi.copy(), Psi.copy(); pp[n, i] += eps; pm[n, i] -= eps
            grads.append((action(Phi, pp) - action(Phi, pm)) / (2 * eps))
            qp, qm = Phi.copy(), Phi.copy(); qp[n, i] += eps; qm[n, i] -= eps
            grads.append((action(qp, Psi) - action(qm, Psi)) / (2 * eps))
    assert max(abs(g) for g in grads) < 1e-8


def test_reader_dies_record_retains():
    """Readout energy decays essentially to zero while the anti-damped
    adjoint grows FROM ITS OWN initial conditions. NOTE (external critique,
    executed 2026-07-19): the linear EL system decouples Phi and Psi --
    Psi0=0 => Psi stays 0 while Phi still dissipates, so this test shows
    adjoint growth, NOT an information handoff (that reading is [Open];
    see v2 doc, append-only direction)."""
    Phi, Psi = el_trajectories()
    e0, e1 = readout_energy(Phi, 1), readout_energy(Phi, T - 2)
    assert e1 / e0 < 1e-4                      # measured ~8e-7
    assert np.linalg.norm(Psi[T - 2]) > 100 * np.linalg.norm(Psi[1])


def test_conservation_of_distinction():
    """H (reader-record pairing charge) is conserved to <1e-3 relative drift
    over 4000 steps while the readout energy dies completely."""
    Phi, Psi = el_trajectories()
    h = np.array([distinction_charge(Phi, Psi, n) for n in range(1, T - 1, 10)])
    assert abs(h.mean()) > 0.01                # a genuinely nonzero charge
    assert (h.max() - h.min()) / abs(h.mean()) < 1e-3   # measured 1.5e-4


def test_charge_drift_scales_as_dt_squared():
    """Reviewer NIT (PR #11) committed as a test: halving dt shrinks the
    distinction-charge drift ~4x => the residual drift is O(dt^2)
    discretization error, not a broken conservation law."""
    d1 = _charge_drift(DT, T)
    d2 = _charge_drift(DT / 2, 2 * T)
    assert 3.0 < d1 / d2 < 5.0, (d1, d2)


def test_reduction_d_zero_conservative():
    """D=0: reader and record obey the SAME conservative equation, and the
    reader's own energy is conserved -- the standard theory returns."""
    Phi, Psi = el_trajectories(damping=0.0)
    e = np.array([readout_energy(Phi, n) for n in range(1, T - 1, 50)])
    assert (e.max() - e.min()) / e.mean() < 1e-3
