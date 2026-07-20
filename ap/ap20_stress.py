"""Stress sweep for AP20's normalization-safe relative unit claim.

Run: pytest -q ap/ap20_stress.py
"""
import ap20_retention_self_interaction as ap20


def test_one_hundred_backgrounds_preserve_relative_units_under_three_scales():
    for seed in range(1, 101):
        bg_x, bg_y = ap20.background(seed)
        for scale in (0.1, 1.0, 10.0):
            _, _, ratio, total_ratio, r_geo, r_self = ap20.relative_units(
                bg_x, bg_y, load_scale=scale
            )
            assert abs(ratio - 1.0) < ap20.TOL
            assert abs(total_ratio - 2.0) < ap20.TOL
            assert r_geo < ap20.TOL and r_self < ap20.TOL
