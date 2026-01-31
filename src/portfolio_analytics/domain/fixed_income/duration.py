# SPDX-License-Identifier: MIT

"""Bond pricing, duration and convexity calculations."""

from __future__ import annotations

from math import pow
from typing import List

from .models import Bond
from datetime import date


def price(bond: Bond, yield_to_maturity: float) -> float:
    """Compute the clean price of a fixed coupon bond.

    Parameters
    ----------
    bond:
        The bond instrument.
    yield_to_maturity:
        Annualised yield to maturity as a decimal (e.g., 0.04 for 4%).

    Returns
    -------
    float
        Present value of the bond's future cash flows per 100 of face value.
    """
    # Compute number of periods until maturity
    today = date.today()
    years_to_maturity = max((bond.maturity_date - today).days / 365.0, 0.0)
    n = bond.coupon_frequency
    total_periods = max(int(round(years_to_maturity * n)), 1)
    y = yield_to_maturity / n
    coupon = bond.coupon_rate * bond.face_value / n
    pv_coupons = sum(coupon / pow(1 + y, t) for t in range(1, total_periods + 1))
    pv_face = bond.face_value / pow(1 + y, total_periods)
    return pv_coupons + pv_face


def macaulay_duration(bond: Bond, yield_to_maturity: float) -> float:
    """Approximate the Macaulay duration of a bond.

    This implementation assumes fixed coupon payments at regular intervals
    and ignores day count conventions.  It should be refined for production use.
    """
    price_val = price(bond, yield_to_maturity)
    n = bond.coupon_frequency
    total_periods = max(int(round(max((bond.maturity_date - date.today()).days / 365.0, 0.0) * n)), 1)
    y = yield_to_maturity / n
    coupon = bond.coupon_rate * bond.face_value / n
    duration = sum(
        (t * coupon) / pow(1 + y, t) for t in range(1, total_periods + 1)
    )
    duration += total_periods * bond.face_value / pow(1 + y, total_periods)
    return duration / price_val if price_val else 0.0


def modified_duration(bond: Bond, yield_to_maturity: float) -> float:
    """Compute the modified duration of a bond."""
    macaulay = macaulay_duration(bond, yield_to_maturity)
    n = bond.coupon_frequency
    return macaulay / (1 + yield_to_maturity / n)


def convexity(bond: Bond, yield_to_maturity: float) -> float:
    """Compute the convexity of a bond."""
    price_val = price(bond, yield_to_maturity)
    n = bond.coupon_frequency
    total_periods = max(int(round(max((bond.maturity_date - date.today()).days / 365.0, 0.0) * n)), 1)
    y = yield_to_maturity / n
    coupon = bond.coupon_rate * bond.face_value / n
    conv = sum(
        (t * (t + 1)) * coupon / pow(1 + y, t + 2)
        for t in range(1, total_periods + 1)
    )
    conv += total_periods * (total_periods + 1) * bond.face_value / pow(1 + y, total_periods + 2)
    return conv / price_val if price_val else 0.0
