"""AP19 -- spin-1 Weitzenboeck rung: coefficient 2 -> response power 4.

NARROW CLAIM
------------
Start from the finite SU(2) Yang-Mills curvature of a background plus a
vector fluctuation, extract the quadratic Hessian without inserting a Zeeman
term, and verify that the curvature block has multiplier 2.  One unit comes
from the linearized field-strength norm plus background gauge fixing; the
second comes from the background-curvature x [a_x,a_y] self-interaction term.
The normalized trace-square of the vector remainder is then four times the
spin-1/2 Pauli/Dirac remainder.

HONEST SCOPE
------------
- finite-dimensional SU(2) adjoint toy; constant background; two directional
  components; no continuum and no infinite mode sum;
- this is NOT a full one-loop Yang-Mills beta-function calculation: ghosts,
  longitudinal modes, spacetime heat-kernel factors, and representation
  counting are not reproduced here;
- +11/3 is only reconstructed downstream as 4 - 1/3, using AP11's declared
  screening atom.

Run: pytest ap/ap19_spin1_weizenbock.py -q
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
    """Tr(R^dagger R) per polarization degree of freedom."""
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


def test_downstream_gauge_atom_reconstructs_eleven_thirds_exactly():
    """Bookkeeping only: response 4 minus AP11 screening 1/3."""
    assert F(4, 1) - F(1, 3) == F(11, 3)
