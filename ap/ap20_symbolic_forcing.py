"""Exact symbolic companion for AP20's unit-coefficient expansion.

This test uses generic symbolic 2x2 matrices. It verifies entry-by-entry that
the exchange-odd defect of ONE ordered product has an epsilon^2 coefficient
exactly equal to the defect of the two fluctuations. No random seed or fitted
coefficient is involved.

Run: pytest -q ap/ap20_symbolic_forcing.py
"""
import sympy as sp


def _mat(prefix: str) -> sp.Matrix:
    return sp.Matrix(2, 2, sp.symbols(f"{prefix}0:4"))


def _k(x: sp.Matrix, y: sp.Matrix) -> sp.Matrix:
    return x * y - y * x


def test_symbolic_order_defect_expansion_has_exact_unit_self_coefficient():
    eps = sp.symbols("eps")
    bg_x, bg_y, a_x, a_y = (_mat(p) for p in ("Ax", "Ay", "ax", "ay"))
    full = _k(bg_x + eps * a_x, bg_y + eps * a_y)
    k0 = _k(bg_x, bg_y)
    k1 = _k(bg_x, a_y) + _k(a_x, bg_y)
    k2 = _k(a_x, a_y)

    for i in range(2):
        for j in range(2):
            poly = sp.Poly(sp.expand(full[i, j]), eps)
            assert sp.simplify(poly.coeff_monomial(1) - k0[i, j]) == 0
            assert sp.simplify(poly.coeff_monomial(eps) - k1[i, j]) == 0
            assert sp.simplify(poly.coeff_monomial(eps**2) - k2[i, j]) == 0
            assert poly.degree() <= 2
