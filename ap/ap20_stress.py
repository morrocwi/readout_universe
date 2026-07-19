"""Seed sweep for AP20's Hessian self-interaction unit.

Run: pytest -q ap/ap20_stress.py
"""
import ap20_retention_self_interaction as ap20


def test_one_hundred_noncommuting_backgrounds_return_the_same_unit():
    coefficients = []
    residuals = []
    for seed in range(1, 101):
        bg_x, bg_y = ap20.background(seed)
        h_self = ap20.self_interaction_hessian(bg_x, bg_y)
        coefficient, residual = ap20.extract_extra_unit(h_self, bg_x, bg_y)
        coefficients.append(coefficient)
        residuals.append(residual)

    assert max(abs(c - 1.0) for c in coefficients) < ap20.TOL
    assert max(residuals) < ap20.TOL
