# SPDX-License-Identifier: MIT

"""Yield curve construction and interpolation utilities."""

from __future__ import annotations

from typing import List

import numpy as np

from .models import YieldCurvePoint


def interpolate_yield_curve(points: List[YieldCurvePoint], maturities: List[float]) -> List[float]:
    """Linearly interpolate yields for arbitrary maturities.

    Parameters
    ----------
    points:
        Observed points on the yield curve sorted by increasing tenor.
    maturities:
        List of maturities (in years) at which to interpolate yields.

    Returns
    -------
    List[float]
        Interpolated yields corresponding to the requested maturities.
    """
    if not points:
        return [0.0 for _ in maturities]
    # Sort points by tenor
    sorted_points = sorted(points, key=lambda p: p.tenor)
    tenors = np.array([p.tenor for p in sorted_points])
    rates = np.array([p.rate for p in sorted_points])
    interpolated = np.interp(maturities, tenors, rates)
    return interpolated.tolist()


def bootstrap_zero_rates(points: List[YieldCurvePoint]) -> List[YieldCurvePoint]:
    """Placeholder for bootstrapping zero rates from coupon bonds.

    In a full implementation, this function would take a list of coupon
    instruments and derive spot rates.  Here we simply return the input.
    """
    return points
