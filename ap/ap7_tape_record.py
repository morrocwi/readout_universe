"""AP7 -- append-only tape record model, re-executed IN THIS REPO.

Origin: external critique of DRL (2026-07-19) verified by execution (the
linear DRL pair decouples; handoff was [Open]). This implements the tape
model under OUR discipline and quantitatively bridges it to DRL.

KINSHIP LEDGER (mandatory, declared BEFORE any novelty talk):
- Repeated-interaction / collision models of open systems (fresh ancilla per
  step; review: Ciccarello et al., Phys. Rep. 954 (2022), arXiv:2106.11974)
- Sz.-Nagy unitary dilation of a contraction (1953): our B_gamma rotation
  into a fresh cell IS a dilation of the contraction sqrt(1-gamma)*C
- Landauer 1961 / Bennett 1982: erasure vs reversible record-keeping tape
=> the MAP is standard-ancestry and POSITED (no action). Candidate-new layer
is only the RD-reading (tape = RD6-7 concatenation realizing RD4 injectivity)
and the quantitative bridge to the variational DRL layer below [Open].

Model (phase state z=(u,w): normal-mode scaled coords so conservative step C
is exactly orthogonal): per step z~ = C z ; then rotate with a fresh cell
b=0: z' = sqrt(1-g) z~, rho = -sqrt(g) z~ ; tape Psi_{n+1} = Psi_n (+) rho.

Claims tested (all executed):
 T1 additive exact conservation: Q(z_n) + sum_j Q(rho_j) = Q(z_0)
 T2 RD4 injectivity + full reversibility (reconstruct z_0 from z_N + tape)
 T3 Pi-window: nearby histories become Pi-indistinguishable in readout while
    the tape retains ~the full initial distinction  [re-execution of the
    external [SimulatedData] claim -- admitted only via THIS run]
 T4 bridge to DRL: with gamma = 1 - exp(-(D/M) dt), the tape energy envelope
    matches ap5's damped-spine readout-energy decay (underdamped uniform case)
Tier: finite_diagnostic (toy: ring N=6); interpretations [Dr].

Run: pytest ap/ap7_tape_record.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ap5_drl as drl

N, DT, GAMMA, STEPS = 6, 0.01, 0.02, 1200
M, K, K2 = drl.M, drl.K, drl.K2
A_SPD = K * drl.L_R + K2 * np.eye(N)          # SPD stiffness (ring + mass term)
_LAM, _V = np.linalg.eigh(A_SPD)
_OMEGA = np.sqrt(_LAM / M)


def to_scaled(phi, vel):
    """(phi, vel) -> z=(u,w) normal-mode scaled coords; Q(z)=|z|^2/2 = energy."""
    q, p = _V.T @ phi, _V.T @ vel
    return np.concatenate([np.sqrt(_LAM) * q, np.sqrt(M) * p])


def from_scaled(z):
    u, w = z[:N], z[N:]
    return _V @ (u / np.sqrt(_LAM)), _V @ (w / np.sqrt(M))


def C_step(z, dt=DT):
    """Exact conservative evolution: rotation by omega_k dt per mode (orthogonal)."""
    u, w = z[:N].copy(), z[N:].copy()
    c, s = np.cos(_OMEGA * dt), np.sin(_OMEGA * dt)
    return np.concatenate([c * u + s * w, -s * u + c * w])


def tape_run(z0, gamma=GAMMA, steps=STEPS):
    z, tape = z0.copy(), []
    sq1, sqg = np.sqrt(1 - gamma), np.sqrt(gamma)
    for _ in range(steps):
        zt = C_step(z)
        z, rho = sq1 * zt, -sqg * zt
        tape.append(rho)
    return z, tape


def Q(v):
    return 0.5 * float(v @ v)


def _z0(seed=7):
    rng = np.random.default_rng(seed)
    return to_scaled(rng.normal(size=N), rng.normal(size=N))


def test_t1_additive_exact_conservation():
    z0 = _z0()
    zf, tape = tape_run(z0)
    total = Q(zf) + sum(Q(r) for r in tape)
    assert abs(total - Q(z0)) / Q(z0) < 1e-12          # machine precision, ADDITIVE
    assert Q(zf) / Q(z0) < 1e-9                        # readout genuinely dissipated
    # and the decay law is exact: (1-gamma)^n
    assert abs(Q(zf) / Q(z0) - (1 - GAMMA) ** STEPS) / (1 - GAMMA) ** STEPS < 1e-9


def test_t2_rd4_injectivity_and_reversibility():
    """Reconstruct z_0 exactly from (z_N, tape): successor is injective on the
    full state -- RD4 realized in dynamics, not interpretation."""
    z0 = _z0()
    zf, tape = tape_run(z0)
    sq1, sqg = np.sqrt(1 - GAMMA), np.sqrt(GAMMA)
    z = zf.copy()
    for rho in reversed(tape):
        zt = sq1 * z - sqg * rho                       # B^T inverse (orthogonal)
        b_rec = sqg * z + sq1 * rho                    # must recover the blank cell
        assert np.abs(b_rec).max() < 1e-10
        z = C_step(zt, dt=-DT)                         # exact inverse rotation
    assert np.abs(z - z0).max() < 1e-9
    # injectivity: perturb history at step k -> tapes differ from k onward
    z0b = z0 + 1e-3 * np.eye(2 * N)[0]
    _, tb = tape_run(z0b)
    ta = tape
    first_diff = next(i for i, (a, b) in enumerate(zip(ta, tb)) if np.abs(a - b).max() > 0)
    assert first_diff == 0
    assert all(np.abs(a - b).max() > 0 for a, b in zip(ta[0:], tb[0:]))


def test_t3_pi_window_vs_tape_retention():
    """Two nearby histories: readout difference collapses below a Pi
    resolution while the TAPE retains ~the whole initial distinction.
    (Re-execution of the external claim under our harness.)"""
    z0a = _z0()
    z0b = z0a + 1e-2 * np.eye(2 * N)[3]
    za, ta = tape_run(z0a)
    zb, tb = tape_run(z0b)
    d_readout = np.abs(za - zb).max()
    d_tape = np.sqrt(sum(float((x - y) @ (x - y)) for x, y in zip(ta, tb)))
    assert d_readout < 1e-6                            # below a 1e-6 Pi resolution
    assert abs(d_tape - 1e-2) / 1e-2 < 0.05            # tape keeps ~full distinction
    # (norm preserved: contraction+cells is jointly orthogonal per step)


def test_t4_bridge_tape_envelope_matches_drl_spine():
    """The two layers meet: choose gamma_dt = 1-exp(-(D/M) dt). Then the tape
    energy envelope reproduces ap5's damped-spine readout-energy decay
    (underdamped uniform-damping case) to a few percent over 4000 steps."""
    gamma_dt = 1 - np.exp(-(drl.D / drl.M) * drl.DT)
    Phi, _ = drl.el_trajectories()
    e_drl_0 = drl.readout_energy(Phi, 1)
    e_drl_f = drl.readout_energy(Phi, drl.T - 2)
    drl_factor = e_drl_f / e_drl_0
    tape_factor = (1 - gamma_dt) ** (drl.T - 3)
    # compare decay EXPONENTS (envelope rates), the honest like-for-like:
    r_drl = np.log(drl_factor) / (drl.T - 3)
    r_tape = np.log(tape_factor) / (drl.T - 3)
    assert abs(r_drl - r_tape) / abs(r_tape) < 0.05    # <5% rate mismatch
