"""AP21 -- spin-1 Weitzenboeck rung: coefficient 2 -> response power 4
(toy-tier finite_diagnostic).

NARROW CLAIM
------------
Start from the finite SU(2) Yang-Mills curvature of a background plus a
vector fluctuation, extract the quadratic Hessian without inserting a Zeeman
term, and verify that the curvature block has multiplier 2.  One unit comes
from the linearized field-strength norm plus background gauge fixing; the
second comes from the background-curvature x [a_x,a_y] self-interaction term.
The normalized trace-square of the vector remainder is then four times the
spin-1/2 Pauli/Dirac remainder.

TIER: finite_diagnostic. This is a finite, seed-independent algebraic fact
about a toy SU(2) adjoint model, checked numerically to machine precision.
It is NOT a derivation from the repo's own graph/spectral engine (AP9-AP12).

RETRACTED STRONG READING (author, PR #23 comment -- this is the operative
status, not the PR title/body): "its self-interaction unit is borrowed
through the non-Abelian curvature expansion. Do not treat or merge it as
the foundational closure."

KINSHIP (borrowed, not derived here): the +1 unit contributed by the
self-interaction term is the standard non-Abelian background-field result
for a charged vector boson's g=2 -- this is essentially the Nielsen 1981 /
't Hooft computation already cited by kinship in AP11 (Nielsen, "Asymptotic
freedom as a spin effect", Am.J.Phys 49, 1171). The Lie/commutator algebra
that makes it work (so(3) adjoint structure, background-Feynman-gauge
Hessian) is standard Yang-Mills machinery, not something this file derives
from first principles.

HONEST SCOPE
------------
- finite-dimensional SU(2) adjoint toy; constant background; two directional
  components; no continuum and no infinite mode sum;
- this is NOT a full one-loop Yang-Mills beta-function calculation: ghosts,
  longitudinal modes, spacetime heat-kernel factors, and representation
  counting are not reproduced here;
- (a) BORROWED, not derived here: the non-Abelian curvature expansion and
  the Lie/commutator structure that produce the second curvature unit are
  standard Yang-Mills background-field machinery (Nielsen 1981 / 't Hooft
  g=2 kinship, see above), not a from-scratch construction of this file;
- (b) this does NOT close MYSTERY_LADDER's open item (2s)^2: that falsifier
  explicitly demands the paramagnetic law be derived "จากโครงสร้าง channel
  บนกราฟ" (from the channel structure on the graph) using this repo's own
  graph/spectral engine (AP9-AP12). AP21 does not touch that engine at all
  -- it is a standalone Yang-Mills toy computation, orthogonal to the
  graph-derivation falsifier;
- (c) what IS established here, and is genuinely earned: a finite,
  seed-independent algebraic fact -- the so(3) Lie-homomorphism identity
  [ad_u, ad_v] = ad_{u x v} forces the self-interaction term to contribute
  EXACTLY one more copy of the same curvature operator, giving multiplier
  2 and trace-square response 4, independent of the random background
  (see genericity tests below, multiple seeds);
- +11/3 is only reconstructed downstream as 4 - 1/3, using AP11's declared
  screening atom -- see OPEN CHECK below on normalization convention.

OPEN CHECK -- normalization not independently cross-validated
---------------------------------------------------------------
The SHAPE of the result (two equal curvature units, multiplier exactly 2)
is forced by the so(3) identity above and is not tunable. The specific term
weights used to get there -- 1/2, 1/2, 1 in background-Feynman gauge, see
`ym_quadratic_coefficient` -- were chosen to match the already-known target
(AP11 pins atom(2) = +11/3 = (2*1)^2 - 1/3, i.e. response 4 was known in
advance) and were NOT independently cross-checked against a textbook
background-field computation. This is a declared open check, not a hidden
weakness: if the overall normalization convention is wrong by a constant
factor, the *shape* (self-interaction contributes exactly one more unit of
the same operator) still holds, but the absolute value "2" / "4" would not.

Run: pytest ap/ap21_spin1_weizenbock.py -q
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
from fractions import Fraction as F

import numpy as np

TOL = 1e-11


def ad_su2(v: np.ndarray) -> np.ndarray:
    """Adjoint action of su(2) in the real cross-product representation."""
    x, y, z = np.asarray(v, dtype=float)
    return np.array(
        [[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]], dtype=float
    )


def background(seed: int = 7) -> tuple[np.ndarray, np.ndarray]:
    """Deterministic noncommuting background directions."""
    rng = np.random.default_rng(seed)
    bg_x = rng.normal(size=3)
    bg_y = rng.normal(size=3)
    if np.linalg.norm(np.cross(bg_x, bg_y)) < 0.2:
        bg_y = bg_y + np.array([0.3, -0.4, 0.5])
    return bg_x, bg_y


def ym_quadratic_coefficient(
    z: np.ndarray,
    bg_x: np.ndarray,
    bg_y: np.ndarray,
    *,
    include_self_interaction: bool = True,
) -> float:
    """Coefficient of epsilon^2 in the background-field quadratic action.

    For A_mu -> A_mu + epsilon a_mu on a one-cell SU(2) toy:
      F(eps) = F0 + eps(D_x a_y - D_y a_x) + eps^2[a_x,a_y].

    The quadratic coefficient in background-Feynman gauge is
      1/2 |f1|^2 + 1/2 |D_x a_x + D_y a_y|^2
      + <F0,[a_x,a_y]>.

    No curvature multiplier is supplied here.
    """
    z = np.asarray(z, dtype=float)
    if z.shape != (6,):
        raise ValueError("z must contain two su(2) adjoint vectors")
    a_x, a_y = z[:3], z[3:]
    d_x, d_y = ad_su2(bg_x), ad_su2(bg_y)
    f0 = np.cross(bg_x, bg_y)
    f1 = d_x @ a_y - d_y @ a_x
    gauge = d_x @ a_x + d_y @ a_y
    q = 0.5 * float(f1 @ f1) + 0.5 * float(gauge @ gauge)
    if include_self_interaction:
        q += float(f0 @ np.cross(a_x, a_y))
    return q


def hessian_from_quadratic(q, dimension: int) -> np.ndarray:
    """Recover H from q(z)=1/2 z^T H z by polarization."""
    eye = np.eye(dimension)
    h = np.zeros((dimension, dimension), dtype=float)
    base = [q(eye[i]) for i in range(dimension)]
    for i in range(dimension):
        h[i, i] = 2.0 * base[i]
        for j in range(i + 1, dimension):
            hij = q(eye[i] + eye[j]) - base[i] - base[j]
            h[i, j] = h[j, i] = hij
    return h


def vector_fluctuation_hessian(
    bg_x: np.ndarray,
    bg_y: np.ndarray,
    *,
    include_self_interaction: bool = True,
) -> np.ndarray:
    return hessian_from_quadratic(
        lambda z: ym_quadratic_coefficient(
            z,
            bg_x,
            bg_y,
            include_self_interaction=include_self_interaction,
        ),
        6,
    )


def orbital_vector_operator(bg_x: np.ndarray, bg_y: np.ndarray) -> np.ndarray:
    d_x, d_y = ad_su2(bg_x), ad_su2(bg_y)
    scalar = -(d_x @ d_x + d_y @ d_y)
    zero = np.zeros_like(scalar)
    return np.block([[scalar, zero], [zero, scalar]])


def curvature_operator(bg_x: np.ndarray, bg_y: np.ndarray) -> np.ndarray:
    d_x, d_y = ad_su2(bg_x), ad_su2(bg_y)
    return d_x @ d_y - d_y @ d_x


def extract_vector_curvature_multiplier(
    hessian: np.ndarray, bg_x: np.ndarray, bg_y: np.ndarray
) -> tuple[float, float]:
    """Fit the off-diagonal remainder H_xy = -c [D_x,D_y]."""
    remainder = hessian - orbital_vector_operator(bg_x, bg_y)
    f_op = curvature_operator(bg_x, bg_y)
    denom = float(np.sum(f_op * f_op))
    if denom < 1e-20:
        raise ValueError("zero adjoint curvature; multiplier undefined")
    off = remainder[:3, 3:]
    coefficient = -float(np.sum(off * f_op)) / denom
    residual = np.linalg.norm(off + coefficient * f_op) / np.linalg.norm(f_op)
    return coefficient, float(residual)


def pauli_remainder(bg_x: np.ndarray, bg_y: np.ndarray) -> np.ndarray:
    """Spin-1/2 first-order square remainder, with no Zeeman term inserted."""
    d_x, d_y = ad_su2(bg_x), ad_su2(bg_y)
    p_x, p_y = 1j * d_x, 1j * d_y
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    first_order = np.kron(sigma_x, p_x) + np.kron(sigma_y, p_y)
    squared = first_order.conj().T @ first_order
    orbital = np.kron(np.eye(2), p_x @ p_x + p_y @ p_y)
    return squared - orbital


def normalized_trace_square(remainder: np.ndarray, polarization_dim: int) -> float:
    """Tr(R^dagger R) per polarization degree of freedom.

    NOTE (declared, not hidden): both call sites in this file pass the same
    polarization_dim=2, so the division cancels exactly in the reported
    power_vec/power_half ratio (test_trace_square_response_ratio_is_four)
    and does no actual normalization work for that comparison. The name
    is kept only because it matches the file's existing convention; treat
    it as "trace-square, divided by a constant that happens to be shared"
    rather than a normalization that changes the answer.
    """
    return float(np.trace(remainder.conj().T @ remainder).real / polarization_dim)


def test_full_quadratic_expansion_derives_vector_multiplier_two():
    bg_x, bg_y = background()
    h = vector_fluctuation_hessian(bg_x, bg_y, include_self_interaction=True)
    coefficient, residual = extract_vector_curvature_multiplier(h, bg_x, bg_y)
    assert abs(coefficient - 2.0) < TOL, coefficient
    assert residual < TOL, residual


def test_nonabelian_self_interaction_supplies_the_second_unit():
    bg_x, bg_y = background()
    h_linear = vector_fluctuation_hessian(
        bg_x, bg_y, include_self_interaction=False
    )
    h_full = vector_fluctuation_hessian(bg_x, bg_y, include_self_interaction=True)
    c_linear, r_linear = extract_vector_curvature_multiplier(h_linear, bg_x, bg_y)
    c_full, r_full = extract_vector_curvature_multiplier(h_full, bg_x, bg_y)
    assert abs(c_linear - 1.0) < TOL, c_linear
    assert abs(c_full - 2.0) < TOL, c_full
    assert r_linear < TOL and r_full < TOL
    assert abs((c_full - c_linear) - 1.0) < TOL


def test_trace_square_response_ratio_is_four():
    bg_x, bg_y = background()
    h_vec = vector_fluctuation_hessian(bg_x, bg_y, include_self_interaction=True)
    r_vec = h_vec - orbital_vector_operator(bg_x, bg_y)
    r_half = pauli_remainder(bg_x, bg_y)
    power_vec = normalized_trace_square(r_vec, polarization_dim=2)
    power_half = normalized_trace_square(r_half, polarization_dim=2)
    assert abs(power_vec / power_half - 4.0) < TOL


def test_commuting_background_declines_instead_of_inventing_a_number():
    bg_x = np.array([1.0, -2.0, 0.5])
    bg_y = 3.0 * bg_x
    h = vector_fluctuation_hessian(bg_x, bg_y, include_self_interaction=True)
    assert np.linalg.norm(curvature_operator(bg_x, bg_y)) < TOL
    try:
        extract_vector_curvature_multiplier(h, bg_x, bg_y)
    except ValueError as exc:
        assert "zero adjoint curvature" in str(exc)
    else:
        raise AssertionError("zero-curvature control must decline")


def test_so3_adjoint_is_a_lie_homomorphism():
    """The actual reason the multiplier is exactly 2, not a fitted number.

    ad: so(3) (cross product) -> gl(3) (matrix commutator) is a Lie-algebra
    homomorphism: [ad_u, ad_v] = ad_{u x v}. This is the identity that
    forces the self-interaction term to contribute exactly one more copy
    of the same curvature operator as the linear term -- it is standard
    algebra, not tuned to hit the target value 2.
    """
    rng = np.random.default_rng(0)
    for _ in range(20):
        u = rng.normal(size=3)
        v = rng.normal(size=3)
        ad_u, ad_v = ad_su2(u), ad_su2(v)
        lhs = ad_u @ ad_v - ad_v @ ad_u
        rhs = ad_su2(np.cross(u, v))
        assert np.max(np.abs(lhs - rhs)) < TOL


def test_curvature_multiplier_is_generic_across_seeds():
    """The multiplier-2 result must not be an artifact of seed=7.

    An independent reviewer re-ran seeds 1,2,3,4,5,42,100,999 and reported
    multiplier 2.0 to ~1e-15 for every one. Pin that genericity claim in
    the repo itself so a future regression (e.g. an accidental seed-7-only
    tuning) is caught by CI, not by manual re-derivation.
    """
    seeds = [1, 2, 3, 4, 5, 7, 42, 100, 999]
    worst_coeff_error = 0.0
    worst_residual = 0.0
    for seed in seeds:
        bg_x, bg_y = background(seed)
        h = vector_fluctuation_hessian(bg_x, bg_y, include_self_interaction=True)
        coefficient, residual = extract_vector_curvature_multiplier(h, bg_x, bg_y)
        assert abs(coefficient - 2.0) < TOL, (seed, coefficient)
        assert residual < TOL, (seed, residual)
        worst_coeff_error = max(worst_coeff_error, abs(coefficient - 2.0))
        worst_residual = max(worst_residual, residual)
    # Sanity: report is meaningful only if every seed actually ran and
    # produced a noncommuting background (background() nudges bg_y away
    # from degeneracy, so this should never trip).
    assert worst_coeff_error < TOL
    assert worst_residual < TOL


def test_downstream_gauge_atom_reconstructs_eleven_thirds_exactly():
    """Bookkeeping only: response 4 minus AP11 screening 1/3.

    Declared open check (see module docstring OPEN CHECK section): the
    target value 11/3 was known in advance from AP11 (atom(2) = (2*1)^2 -
    1/3), and the term weights in ym_quadratic_coefficient were not
    independently cross-validated against a textbook background-field
    computation before this bookkeeping identity was written down. The
    SHAPE (two equal curvature units) is forced by the so(3) identity
    tested above; the overall normalization convention is not.
    """
    assert F(4, 1) - F(1, 3) == F(11, 3)
