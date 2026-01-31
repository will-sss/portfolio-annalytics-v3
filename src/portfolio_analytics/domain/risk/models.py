# SPDX-License-Identifier: MIT

"""Risk analytics domain models."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class VaRResult(BaseModel):
    """Value at Risk result container."""

    confidence_level: float = Field(..., description="Confidence level (e.g., 0.95)")
    value_at_risk: float = Field(..., description="Value at risk in currency units")
    method: str = Field(..., description="Method used (historical, parametric, Monte Carlo)")
    horizon: int = Field(..., description="Time horizon in days")


class DrawdownStats(BaseModel):
    """Maximum drawdown and related statistics."""

    max_drawdown: float = Field(..., description="Maximum drawdown as a decimal (e.g., -0.2)")
    start_date: Optional[str] = Field(None, description="Start date of the worst drawdown period")
    end_date: Optional[str] = Field(None, description="End date of the worst drawdown period")
    recovery_date: Optional[str] = Field(None, description="Date when the portfolio recovered")


class CorrelationMatrix(BaseModel):
    """Correlation matrix for a set of instruments."""

    instruments: List[str] = Field(..., description="List of instrument identifiers")
    matrix: List[List[float]] = Field(
        ..., description="2D symmetric matrix of pairwise correlations"
    )
