# SPDX-License-Identifier: MIT

"""Shared domain models."""

from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class Instrument(BaseModel):
    """A base class for any financial instrument."""

    symbol: str = Field(..., description="Ticker symbol or unique identifier")
    name: Optional[str] = Field(None, description="Human‑readable name of the instrument")

    class Config:
        arbitrary_types_allowed = True


class TimeSeries(BaseModel):
    """A generic time series of values with dates."""

    dates: list[date]
    values: list[float]

    @property
    def latest(self) -> Optional[float]:
        """Return the most recent value or ``None`` if the series is empty."""
        return self.values[-1] if self.values else None
