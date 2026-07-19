"""AP3 -- DESI DR2 "evolving dark energy" through the RD lens
(toy-tier finite_diagnostic; blind trial #3, 2026-07-19).

Paper: DESI DR2 BAO (arXiv:2503.14738) -- w0waCDM preferred over LCDM at
3.1 sigma (BAO+CMB) to 2.8-4.2 sigma (+SNe, sample-dependent); the paper
itself states the driver is a 2.3-sigma tension between BAO- and CMB-inferred
parameters under LCDM.

Lens verdict (gates executed via lens.run_gates, 2026-07-19):
- G3 FLAG: 'Omega_m' arrives through TWO chains (BAO+LCDM closure vs
  CMB+LCDM closure) -- different quantities by role forced equal; the 2.3
  sigma "tension" is the clash of that forced identification (same structure
  as AP1's h_CMB vs h_ladder).
- G4 FLAG: DESI DR2 = new readout policy (14M spectra, new pipeline);
  forward-model before reading world-change.
- G5 FLAG: >=4 hypothesis directions (quintessence / phantom-crossing /
  modified gravity / systematics) on a lower-dimensional record.
- Micro-check below: the preferred CPL direction is NEAR-NULL within BAO
  observables once (h, omega_m) compensate -- the "evolution" signal lives in
  the cross-chain combination, not inside BAO.

TOY TIER declared: approximate headline best-fit (w0=-0.752, wa=-0.86);
r_s(z_star) used as an r_drag proxy (common scaling); 5 effective z-bins,
no covariance; full-likelihood behavior is the declared falsifier
(if BAO-alone with free h, Omega_m prefers CPL at >~2 sigma, the
cross-chain-artifact reading DIES).

Run: pytest ap/ap3_desi_mirage.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ap1_hubble_identifiability import C, E as E_lcdm, r_s, z_star  # verified grammar (AP1)

H0, WM0 = 0.6736, 0.14237
W0, WA = -0.752, -0.86                      # DESI DR2 approx headline (declared toy)
Z_BAO = [0.51, 0.71, 0.93, 1.32, 2.33]      # DESI effective redshifts (approx)


def E_cpl(z, h, wm, w0, wa):
    wr = 2.469e-5 * (1 + 0.2271 * 3.046)
    om, orr = wm / h**2, wr / h**2
    ode = 1 - om - orr
    de = (1 + z)**(3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
    return np.sqrt(orr * (1 + z)**4 + om * (1 + z)**3 + ode * de)


def bao_observables(Efn, h, wm, *de):
    """The 10 BAO readouts: (D_M/r_d, D_H/r_d) at the 5 effective redshifts."""
    rd = r_s(z_star(0.02237, wm), h, 0.02237, wm)
    out = []
    for z in Z_BAO:
        dm = (C / 100.0 / h) * quad(lambda x: 1 / Efn(x, h, wm, *de), 0, z, limit=200)[0]
        dh = C / (100.0 * h * Efn(z, h, wm, *de))
        out += [dm / rd, dh / rd]
    return np.array(out)


def test_grammar_sanity():
    """E(0)=1 for both grammars; CPL reduces to LCDM at (w0,wa)=(-1,0)."""
    assert abs(E_lcdm(0.0, H0, WM0) - 1) < 1e-9
    assert abs(E_cpl(0.0, H0, WM0, -1.0, 0.0) - 1) < 1e-9
    for z in (0.5, 2.0):
        assert abs(E_cpl(z, H0, WM0, -1.0, 0.0) / E_lcdm(z, H0, WM0) - 1) < 1e-12


def test_pivot_rotation_structure():
    """The best-fit w(z) crosses -1 near z~0.4: data pin w(pivot)~-1; the
    claimed 'evolution' is the weakly-constrained slope direction."""
    zg = np.linspace(0.01, 3, 600)
    wz = W0 + WA * zg / (1 + zg)
    zp = zg[np.argmin(np.abs(wz + 1))]
    assert 0.3 < zp < 0.6, zp


def test_near_null_within_bao():
    """With (h, omega_m) compensating, the DESI best-fit CPL differs from
    LCDM by <0.7% across ALL 10 BAO observables (measured 0.50%) -- at the
    per-bin precision floor => near-null direction within BAO alone."""
    ref = bao_observables(E_lcdm, H0, WM0)

    def cost(p):
        return np.max(np.abs(bao_observables(E_cpl, p[0], p[1], W0, WA) / ref - 1))

    r = minimize(cost, [0.66, 0.148], method="Nelder-Mead",
                 options={"xatol": 1e-4, "fatol": 1e-5})
    assert r.fun < 0.007, r.fun
    # and the direction is NOT exactly null -- there is a real sub-percent
    # residual, which is where any genuine BAO-side signal must live
    assert r.fun > 0.001, r.fun


def test_single_param_compensation_insufficient():
    """Omega_m alone cannot absorb the difference (~1.5% D_M residual):
    the near-nullness genuinely needs h to move too -- i.e. the CPL
    preference trades directly against the h/Omega_m chain assignments."""
    from scipy.optimize import minimize_scalar

    def cost(wm2):
        return max(abs(
            (C / 100.0 / H0) * quad(lambda x: 1 / E_cpl(x, H0, wm2, W0, WA), 0, z, limit=200)[0]
            / ((C / 100.0 / H0) * quad(lambda x: 1 / E_lcdm(x, H0, WM0), 0, z, limit=200)[0]) - 1)
            for z in Z_BAO)
    r = minimize_scalar(cost, bounds=(0.13, 0.16), method="bounded")
    assert r.fun > 0.01, r.fun
