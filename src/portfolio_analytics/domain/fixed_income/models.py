# SPDX-License-Identifier: MIT

"""Fixed income-specific domain models."""

from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class Bond(BaseModel):
    """Represents a fixed income instrument."""

    isin: str = Field(..., description="International Securities Identification Number")
    issuer: Optional[str] = Field(None, description="Issuer name")
    coupon_rate: float = Field(..., description="Annual coupon rate as a decimal (e.g., 0.05 for 5%)")
    coupon_frequency: int = Field(
        ..., description="Number of coupon payments per year (e.g., 2 for semi‑annual)"
    )
    maturity_date: date = Field(..., description="Bond maturity date")
    face_value: float = Field(100.0, description="Face value or principal amount")
    price: Optional[float] = Field(None, description="Current price per 100 of face value")


class YieldCurvePoint(BaseModel):
    """Represents a single point on a yield curve."""

    tenor: float = Field(..., description="Time to maturity in years")
    rate: float = Field(..., description="Yield as a decimal (e.g., 0.03 for 3%)")


class DurationMetrics(BaseModel):
    """Holds duration and convexity measures for a bond."""

    macaulay_duration: Optional[float] = Field(None, description="Macaulay duration in years")
    modified_duration: Optional[float] = Field(None, description="Modified duration in years")
    convexity: Optional[float] = Field(None, description="Convexity of the bond price")
