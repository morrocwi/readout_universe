"""AP1 -- Hubble tension read through the RD lens (toy-tier finite_diagnostic).

Claim C-AP1: the CMB acoustic record theta* does NOT identify h by itself;
h_CMB exists only after POSITING closure (flat LCDM, w=-1, standard r_s).
Executed demonstration: a curve in parameter space holds theta* constant to
<1e-3 relative while h sweeps the whole SH0ES<->Planck range.
Consequence [Dr]: h_CMB and h_ladder are different quantities by role
(DOCTRINE_OF_QUANTITY Q3); the tension relocates to the closure posits, and
the load-bearing discarded difference (LTP3) is the sound-horizon calibration.

TOY TIER declared: omega_m held fixed; fitting-formula grammar (Hu & Sugiyama
z*, no full Boltzmann); no error propagation. Frontier convergence: this
reproduces the geometric-degeneracy framing (Efstathiou & Bond 1999; Knox &
Millea 2019) from the lens's own gates.

Run: pytest ap/ap1_hubble_identifiability.py -q
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

C = 299792.458  # km/s

# Planck 2018 fiducial
H0, WB0, WC0 = 0.6736, 0.02237, 0.1200
WM0 = WB0 + WC0
THETA_PLANCK = 1.0411  # 100*theta_star


def z_star(wb, wm):
    """Hu & Sugiyama 1996 last-scattering redshift."""
    g1 = 0.0783 * wb**-0.238 / (1 + 39.5 * wb**0.763)
    g2 = 0.560 / (1 + 21.1 * wb**1.81)
    return 1048 * (1 + 0.00124 * wb**-0.738) * (1 + g1 * wm**g2)


def E(z, h, wm, w=-1.0):
    wr = 2.469e-5 * (1 + 0.2271 * 3.046)
    om, orad = wm / h**2, wr / h**2
    ode = 1.0 - om - orad
    return np.sqrt(orad*(1+z)**4 + om*(1+z)**3 + ode*(1+z)**(3*(1+w)))


def D_M(zs, h, wm, w=-1.0):
    return (C/(100*h)) * quad(lambda z: 1/E(z, h, wm, w), 0, zs, limit=200)[0]


def r_s(zs, h, wb, wm):
    def cs_over_H(z):
        R = 31500 * wb * (2.7255/2.7)**-4 / (1+z)
        return (C/np.sqrt(3*(1+R))) / (100*h*E(z, h, wm))
    return quad(cs_over_H, zs, np.inf, limit=400)[0]


def theta100(h, wb, wm, w=-1.0):
    zs = z_star(wb, wm)
    return 100 * r_s(zs, h, wb, wm) / D_M(zs, h, wm, w)


def test_grammar_sanity_reproduces_planck():
    """Gate W3: the grammar must reproduce the known record before use."""
    th = theta100(H0, WB0, WM0)
    assert abs(th - THETA_PLANCK)/THETA_PLANCK < 0.005, th  # 0.5% fitting-formula gate


def test_closure_on_h_is_identified():
    """Under posits (flat, w=-1, early physics fixed) theta* DOES pin h:
    the h-range Planck<->SH0ES moves theta* by >>Planck precision."""
    spread = theta100(0.73, WB0, WM0) - theta100(0.62, WB0, WM0)
    assert spread > 0.02  # vs Planck sigma(100theta*) ~ 0.0003


def test_closure_off_h_in_null_space():
    """Free ONE posit (w): h sweeps 0.62..0.76 while theta* stays fixed to
    <1e-3 relative => h lies in the null space of the theta* record (LTP4)."""
    th0 = theta100(H0, WB0, WM0)
    for h in (0.62, 0.65, 0.70, 0.73, 0.76):
        w = brentq(lambda w: theta100(h, WB0, WM0, w) - th0, -2.5, -0.3, xtol=1e-6)
        assert abs(theta100(h, WB0, WM0, w) - th0)/th0 < 1e-3
    # and the degeneracy direction is monotone in w (phantom side for high h)
    w73 = brentq(lambda w: theta100(0.73, WB0, WM0, w) - th0, -2.5, -0.3, xtol=1e-6)
    assert w73 < -1.0


def test_rs_recalibration_absorbs_tension():
    """Alternative escape (early-physics route): with w=-1 kept, a percent-level
    r_s shift accommodates h=0.73 at fixed theta* (toy: wm fixed)."""
    th0 = theta100(H0, WB0, WM0)
    zs = z_star(WB0, WM0)
    rs_needed = th0/100 * D_M(zs, 0.73, WM0)
    shift = rs_needed / r_s(zs, H0, WB0, WM0) - 1
    assert -0.05 < shift < -0.005  # small, percent-level, negative
