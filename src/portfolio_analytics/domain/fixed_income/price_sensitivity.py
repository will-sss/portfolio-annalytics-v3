# SPDX-License-Identifier: MIT

"""Price sensitivity analysis for fixed income instruments."""

from __future__ import annotations

from .models import Bond
from .duration import price, modified_duration, convexity


def price_sensitivity(bond: Bond, yield_to_maturity: float, delta_y: float) -> float:
    """Approximate the change in bond price for a small change in yield.

    This function uses first‑ and second‑order approximations via
    modified duration and convexity:

    .. math::
        \frac{\Delta P}{P} \approx -D_\text{mod} \Delta y + \frac{1}{2} \text{Convexity} (\Delta y)^2

    Parameters
    ----------
    bond:
        The bond instrument.
    yield_to_maturity:
        Current yield to maturity as a decimal.
    delta_y:
        Change in yield (e.g., 0.01 for a 1 percentage point increase).

    Returns
    -------
    float
        Approximate change in price (in currency units per 100 of face value).
    """
    p = price(bond, yield_to_maturity)
    d = modified_duration(bond, yield_to_maturity)
    c = convexity(bond, yield_to_maturity)
    pct_change = -d * delta_y + 0.5 * c * delta_y * delta_y
    return p * pct_change
