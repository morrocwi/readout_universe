"""AP20 -- ordered self-carrier composition forces an equal second curvature term.

TARGET
------
Paper IV measured a plain geometric vector-curvature coupling of one relative
unit. This file asks a narrower question than the original draft: once a
noncommutative ordered channel algebra and self-carrier closure are granted,
does the quadratic expansion require a self-composition contribution equal to
the geometric contribution, without inserting a separate trilinear coefficient?

PREMISES (declared; conditional, not RD4-alone)
------------------------------------------------
A1. Channels compose by one unital bilinear associative product m(x,y).
A2. Circulation/curvature is the exchange-odd order defect
        K(x,y)=m(x,y)-m(y,x).
    This noncommutative/Lie-algebraic structure remains BORROWED.
A3. Self-carrier closure: fluctuations inhabit the same channel algebra as the
    background rather than being external payloads.
A4. Geometric and self terms are evaluated with the SAME invariant quadratic
    load. Its arbitrary overall normalization must cancel in the ratio.

Bilinearity forces
  K(Ax+e ax, Ay+e ay)
   = K0 + e K1 + e^2 K(ax,ay).
Thus no separate coefficient for the quadratic self term is available. In a
finite so(3) representation, the geometric Hessian and the self Hessian carry
the SAME curvature multiplier under every common positive load scaling:

    c_self / c_geo = 1,       (c_geo+c_self)/c_geo = 2.

With Paper IV's convention c_geo=1, this is 1+1=2 and the quadratic response
ratio is 2^2=4. The result is RELATIVE, not an absolute norm normalization.

HONEST SCOPE
------------
- finite-dimensional operator diagnostic; no continuum or infinity;
- the commutator channel algebra, representation, covariant geometric term,
  and self-carrier premise are borrowed/declared, not derived from RD4;
- what is closed conditionally is the absence of an independent trilinear
  coefficient once A1-A4 hold;
- no full +11/3 beta coefficient, ghosts, gauge-group generation, or Standard
  Model claim.

Run: pytest -q ap/ap20_retention_self_interaction.py
PRIVATE / PROPRIETARY (LICENSE EXCEPTIONS) -- do not publish.
"""
from __future__ import annotations

import numpy as np

TOL = 1e-11


def compose(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.asarray(x) @ np.asarray(y)


def order_defect(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return compose(x, y) - compose(y, x)


def ad(v: np.ndarray) -> np.ndarray:
    x, y, z = np.asarray(v, dtype=float)
    return np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]], dtype=float)


def unad(m: np.ndarray) -> np.ndarray:
    m = np.asarray(m, dtype=float)
    return np.array([m[2, 1], m[0, 2], m[1, 0]], dtype=float)


def channel_bracket(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Borrowed Lie bracket represented as the order defect of one product."""
    return unad(order_defect(ad(u), ad(v)))


def curvature_coefficients(bg_x, bg_y, a_x, a_y):
    k0 = channel_bracket(bg_x, bg_y)
    k1 = channel_bracket(bg_x, a_y) + channel_bracket(a_x, bg_y)
    k2 = channel_bracket(a_x, a_y)
    return k0, k1, k2


def full_curvature(eps, bg_x, bg_y, a_x, a_y):
    return channel_bracket(bg_x + eps * a_x, bg_y + eps * a_y)


def hessian_from_quadratic(q, dimension: int) -> np.ndarray:
    eye = np.eye(dimension)
    h = np.zeros((dimension, dimension), dtype=float)
    base = [q(eye[i]) for i in range(dimension)]
    for i in range(dimension):
        h[i, i] = 2.0 * base[i]
        for j in range(i + 1, dimension):
            hij = q(eye[i] + eye[j]) - base[i] - base[j]
            h[i, j] = h[j, i] = hij
    return h


def geometric_hessian(bg_x, bg_y, load_scale: float = 1.0) -> np.ndarray:
    """Geometric/background-gauge quadratic term, under one common load scale."""
    d_x, d_y = ad(bg_x), ad(bg_y)

    def q_geo(z):
        a_x, a_y = z[:3], z[3:]
        k1 = d_x @ a_y - d_y @ a_x
        gauge = d_x @ a_x + d_y @ a_y
        return load_scale * (0.5 * float(k1 @ k1) + 0.5 * float(gauge @ gauge))

    return hessian_from_quadratic(q_geo, 6)


def self_interaction_hessian(bg_x, bg_y, load_scale: float = 1.0) -> np.ndarray:
    """Forced cross term <K0,K(ax,ay)> under the SAME load scale."""
    k0 = channel_bracket(bg_x, bg_y)

    def q_self(z):
        a_x, a_y = z[:3], z[3:]
        return load_scale * float(k0 @ channel_bracket(a_x, a_y))

    return hessian_from_quadratic(q_self, 6)


def curvature_operator(bg_x, bg_y) -> np.ndarray:
    return order_defect(ad(bg_x), ad(bg_y))


def extract_curvature_multiplier(hessian, bg_x, bg_y):
    k_op = curvature_operator(bg_x, bg_y)
    denom = float(np.sum(k_op * k_op))
    if denom < 1e-20:
        raise ValueError("zero order defect; multiplier undefined")
    off = hessian[:3, 3:]
    coefficient = -float(np.sum(off * k_op)) / denom
    residual = np.linalg.norm(off + coefficient * k_op) / np.linalg.norm(k_op)
    return coefficient, float(residual)


def relative_units(bg_x, bg_y, load_scale: float = 1.0):
    c_geo, r_geo = extract_curvature_multiplier(
        geometric_hessian(bg_x, bg_y, load_scale), bg_x, bg_y
    )
    c_self, r_self = extract_curvature_multiplier(
        self_interaction_hessian(bg_x, bg_y, load_scale), bg_x, bg_y
    )
    if abs(c_geo) < 1e-20:
        raise ValueError("zero geometric reference unit")
    return c_geo, c_self, c_self / c_geo, (c_geo + c_self) / c_geo, r_geo, r_self


def background(seed: int = 20):
    rng = np.random.default_rng(seed)
    bg_x = rng.normal(size=3)
    bg_y = rng.normal(size=3)
    if np.linalg.norm(curvature_operator(bg_x, bg_y)) < 0.2:
        bg_y += np.array([0.3, -0.4, 0.5])
    return bg_x, bg_y


def test_no_op_identity_fixes_product_but_not_load_normalization():
    rng = np.random.default_rng(3)
    x = rng.normal(size=(3, 3))
    identity = np.eye(3)
    assert np.linalg.norm(compose(identity, x) - x) < TOL
    assert np.linalg.norm(compose(x, identity) - x) < TOL
    bg_x, bg_y = background()
    c1 = relative_units(bg_x, bg_y, load_scale=0.3)
    c2 = relative_units(bg_x, bg_y, load_scale=7.0)
    assert abs(c1[0] - c2[0]) > 1.0
    assert abs(c1[2] - 1.0) < TOL and abs(c2[2] - 1.0) < TOL
    assert abs(c1[3] - 2.0) < TOL and abs(c2[3] - 2.0) < TOL


def test_order_defect_is_exchange_odd_and_jacobi_follows_from_composition():
    rng = np.random.default_rng(7)
    x, y, z = (rng.normal(size=(3, 3)) for _ in range(3))
    assert np.linalg.norm(order_defect(x, y) + order_defect(y, x)) < TOL
    jacobi = (
        order_defect(x, order_defect(y, z))
        + order_defect(y, order_defect(z, x))
        + order_defect(z, order_defect(x, y))
    )
    assert np.linalg.norm(jacobi) < TOL


def test_bilinearity_forces_quadratic_term_with_unit_polynomial_coefficient():
    rng = np.random.default_rng(11)
    bg_x, bg_y = background()
    a_x, a_y = rng.normal(size=3), rng.normal(size=3)
    k0, k1, k2 = curvature_coefficients(bg_x, bg_y, a_x, a_y)
    for eps in (-0.7, -0.2, 0.3, 0.9):
        assert np.linalg.norm(
            full_curvature(eps, bg_x, bg_y, a_x, a_y)
            - (k0 + eps * k1 + eps**2 * k2)
        ) < TOL


def test_self_and_geometric_terms_have_equal_relative_curvature_weight():
    bg_x, bg_y = background()
    c_geo, c_self, ratio, total_ratio, r_geo, r_self = relative_units(bg_x, bg_y)
    assert abs(c_geo - 1.0) < TOL  # convention at load_scale=1, not absolute physics
    assert abs(c_self - 1.0) < TOL
    assert abs(ratio - 1.0) < TOL
    assert abs(total_ratio - 2.0) < TOL
    assert r_geo < TOL and r_self < TOL


def test_common_load_rescaling_cancels_from_the_claimed_ratios():
    bg_x, bg_y = background()
    for scale in (0.05, 0.2, 1.0, 3.7, 20.0):
        _, _, ratio, total_ratio, r_geo, r_self = relative_units(
            bg_x, bg_y, load_scale=scale
        )
        assert abs(ratio - 1.0) < TOL
        assert abs(total_ratio - 2.0) < TOL
        assert r_geo < TOL and r_self < TOL


def test_commutative_and_external_payload_controls_kill_self_term():
    x = np.diag([1.0, 2.0, -1.0])
    y = np.diag([3.0, -4.0, 0.5])
    assert np.linalg.norm(order_defect(x, y)) < TOL

    bg_x, bg_y = background()
    rng = np.random.default_rng(19)
    a_x, a_y = rng.normal(size=3), rng.normal(size=3)
    k0 = channel_bracket(bg_x, bg_y)
    k1 = channel_bracket(bg_x, a_y) + channel_bracket(a_x, bg_y)

    def external_payload_curvature(eps):
        return k0 + eps * k1

    h = 0.25
    second = (
        external_payload_curvature(h)
        - 2 * external_payload_curvature(0.0)
        + external_payload_curvature(-h)
    ) / h**2
    assert np.linalg.norm(second) < TOL


def test_relative_coupling_two_has_quadratic_response_ratio_four():
    bg_x, bg_y = background()
    _, _, ratio, total_ratio, _, _ = relative_units(bg_x, bg_y)
    assert abs(ratio - 1.0) < TOL
    assert abs(total_ratio**2 - 4.0) < TOL
