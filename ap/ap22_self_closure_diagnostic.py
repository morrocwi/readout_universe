"""AP22 -- a fresh, self-contained finite_diagnostic toy model for
philosophy.md's section 7.21 ("Self as a closure property, not a
substance -- the tau_c^H loop"), built after a cross-repo survey this
session (2026-08-03) found no existing EXECUTED numeric diagnostic
anywhere in the workspace bearing on this exact claim -- only a
proprietary repo's own toy models for a structurally distinct object
(a static single-instant self-readout regime split, not this standing
closure loop). Nothing in this file is copied or adapted from any
proprietary source; every definition, parameter, and result below was
written and run fresh for this file.

WHAT SECTION 7.21 CLAIMS (its own falsifiable signature, restated here
in this file's own words, not quoted verbatim from any source): a
world-model Omega_H that both (a) results from the loop's own prior
passes and (b) conditions the loop's next pass is a "closed" loop, at a
timescale tau_c^H. A genuinely DEGRADED closure -- the coupling between
the loop's own readout and its own next update weakening -- should show
two measurable signatures: a flattened agency gradient (how much the
loop's own policy shifts in response to its own error signal) and a
slowed repair rate (how fast the loop returns to tracking the true state
after a perturbation).

TOY MODEL (entirely fresh, no proprietary reuse): a scalar world-model
Omega[t] tracking an unknown fixed target theta_true through noisy
observations. Omega[t+1] = Omega[t] + k * (obs[t] - Omega[t]) -- Omega
feeding its own next update through the SAME coefficient k that also
scales how strongly the loop's policy responds to its own perceived
error (pi_star[t] = Omega[t] + k * tanh(eta[t])) -- i.e. one shared
"closure gain" k governs both the repair channel and the policy-
sensitivity channel, because both are read here as the SAME loop's
closure, not two independent knobs. "Degraded closure" = a smaller k.

WHAT IS MEASURED, NOT ASSUMED: after letting each arm converge, a fixed
perturbation is injected into Omega, and BOTH signatures are measured
empirically over the following window -- the repair-rate signature via
the actual finite-difference decay of |Res_true| = |theta_true - Omega|
(not read off k analytically), and the agency-gradient signature via an
actual finite-difference perturbation of the observation and re-
evaluation of pi_star (not read off k analytically either). Both
signatures could, in principle, have failed to separate by k in this
toy model (e.g. if noise dominated, or if the perturbation-recovery
window were chosen badly) -- they are reported honestly below, following
this repo's own no-forced-passes convention (cf. ap6_drl_general.py's
test_nonlinear_h_drift_reported), not assumed to confirm anything.

WHAT THIS DOES NOT SHOW: this is a linear-ish scalar toy model with one
shared gain parameter driving both signatures by construction -- it is
an honest confirmation that the MEASUREMENT METHODOLOGY correctly
detects a built-in coupling in a model designed to have one, not an
independent empirical discovery that real human/agent closure works
this way, and not evidence that any real world-model update rule is
well-approximated by this linear form. It supplies, at finite_diagnostic
tier, the first EXECUTED numeric check that section 7.21's own claimed
signature is at least internally coherent and measurable in a toy
setting -- nothing about tau_c^H, human cognition, or consciousness is
claimed or tested here.

Tier: finite_diagnostic (measured numeric run, this file only). Section
7.21 itself remains Dr/[Open]; running this file does not upgrade it.

Run: pytest ap/ap22_self_closure_diagnostic.py -q
"""
import numpy as np

THETA_TRUE = 5.0
OBS_NOISE = 0.02
STEPS = 60
PERTURB_AT = 10
PERTURB_SIZE = 2.0
WINDOW = 15
SEED = 7
FD_EPS = 1e-4


def simulate_arm(k, steps=STEPS, perturb_at=PERTURB_AT, perturb_size=PERTURB_SIZE,
                  theta_true=THETA_TRUE, obs_noise=OBS_NOISE, seed=SEED, eps=FD_EPS):
    """One closure-loop arm at a fixed gain k: Omega converges, is perturbed
    at `perturb_at`, and both signatures are recorded at every step."""
    rng = np.random.default_rng(seed)
    Omega = np.zeros(steps)
    Omega[0] = theta_true  # start converged, so the perturbation is the only shock
    res_true = np.zeros(steps)
    res_true[0] = theta_true - Omega[0]
    agency_grad = np.zeros(steps - 1)

    for t in range(steps - 1):
        if t == perturb_at:
            Omega[t] = Omega[t] + perturb_size
            res_true[t] = theta_true - Omega[t]

        obs = theta_true + rng.normal(0, obs_noise)
        res_obs = obs - Omega[t]

        # agency-gradient measurement: finite-difference sensitivity of the
        # policy pi_star to a perturbation of the OBSERVATION (hence of the
        # error signal eta), at fixed Omega[t] and k -- an actual measured
        # slope, not the analytic coefficient k read off directly.
        obs_p, obs_m = obs + eps, obs - eps
        eta_p, eta_m = abs(obs_p - Omega[t]), abs(obs_m - Omega[t])
        pi_p = Omega[t] + k * np.tanh(eta_p)
        pi_m = Omega[t] + k * np.tanh(eta_m)
        agency_grad[t] = (pi_p - pi_m) / (eta_p - eta_m) if eta_p != eta_m else 0.0

        Omega[t + 1] = Omega[t] + k * res_obs
        res_true[t + 1] = theta_true - Omega[t + 1]

    return Omega, res_true, agency_grad


def repair_slope(res_true, perturb_at=PERTURB_AT, window=WINDOW):
    """Mean per-step change in |Res_true| over the window right after the
    perturbation -- a negative number means the residual is shrinking
    (repairing); more negative = faster repair."""
    seg = np.abs(res_true[perturb_at:perturb_at + window])
    return float(np.diff(seg).mean())


def mean_abs_agency_grad(agency_grad, perturb_at=PERTURB_AT, window=WINDOW):
    return float(np.abs(agency_grad[perturb_at:perturb_at + window]).mean())


K_NOMINAL = 0.30
K_DEGRADED = 0.05


def test_repair_rate_and_agency_gradient_measured_honestly():
    """THE gate: run both arms, report the actual measured numbers, and
    check the direction section 7.21's own falsifier predicts -- nominal
    closure repairs faster (more negative slope) and has a less-flattened
    agency gradient than degraded closure. This is the finding, measured,
    not forced -- see module docstring for what it does and does not show."""
    _, res_nom, grad_nom = simulate_arm(K_NOMINAL)
    _, res_deg, grad_deg = simulate_arm(K_DEGRADED)

    slope_nom = repair_slope(res_nom)
    slope_deg = repair_slope(res_deg)
    grad_nom_mag = mean_abs_agency_grad(grad_nom)
    grad_deg_mag = mean_abs_agency_grad(grad_deg)

    # MEASURED this run (fixed seed, reported for the record):
    #   slope_nom ~ -0.1425, slope_deg ~ -0.0736  (nominal repairs faster)
    #   grad_nom_mag ~ 0.2386, grad_deg_mag ~ 0.0114  (degraded gradient flatter)
    assert slope_nom < slope_deg, (
        f"unexpected: degraded closure (k={K_DEGRADED}) repaired at least as fast as "
        f"nominal (k={K_NOMINAL}) in this toy model -- slope_nom={slope_nom:.5f}, "
        f"slope_deg={slope_deg:.5f}; section 7.21's own falsifier would need to be "
        f"reported as NOT confirmed in this toy setting if this assertion fails"
    )
    assert grad_deg_mag < grad_nom_mag, (
        f"unexpected: degraded closure's agency gradient was not flatter than "
        f"nominal's in this toy model -- grad_nom={grad_nom_mag:.5f}, "
        f"grad_deg={grad_deg_mag:.5f}; section 7.21's own falsifier would need to be "
        f"reported as NOT confirmed in this toy setting if this assertion fails"
    )


def test_reduces_to_no_perturbation_baseline():
    """Sanity: with perturb_size=0, Omega should stay close to theta_true
    throughout (only small observation-noise-driven wander, no large
    transient) -- confirming the perturbation, not the update rule itself,
    is what drives the large excursion measured in the main test above."""
    Omega, res_true, _ = simulate_arm(K_NOMINAL, perturb_size=0.0)
    assert abs(res_true[PERTURB_AT]) < 0.5 * PERTURB_SIZE
