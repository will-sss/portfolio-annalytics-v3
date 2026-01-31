# SPDX-License-Identifier: MIT

"""Portfolio-specific domain models."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from ..common.models import Instrument


class Constraint(BaseModel):
    """Represents a portfolio constraint.

    Constraints include minimum and maximum weights for sectors or instruments,
    turnover limits, leverage limits, etc.  They are intentionally generic
    to allow for extension as new constraint types are introduced.
    """

    name: str
    lower_bound: float = 0.0
    upper_bound: float = 1.0


class Holding(BaseModel):
    """Represents a holding in a portfolio."""

    instrument: Instrument
    quantity: float = Field(..., description="Number of units held")
    weight: Optional[float] = Field(
        None, description="Weight of the holding in the portfolio (0–1)"
    )


class Portfolio(BaseModel):
    """Represents an investment portfolio."""

    holdings: List[Holding]
    constraints: List[Constraint] = Field(default_factory=list)

    @property
    def total_value(self) -> float:
        """Compute the total market value of the portfolio if weights are absent."""
        return sum(h.quantity for h in self.holdings)
