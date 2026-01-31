# SPDX-License-Identifier: MIT

"""Equity-specific domain models.

These Pydantic models describe the structure of equity data used throughout
the platform.  They are intentionally generic so they can be instantiated
from different data sources (Yahoo Finance, EDGAR, Alpha Vantage).
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from ..common.models import Instrument


class Equity(Instrument):
    """Represents a publicly traded equity instrument."""

    sector: Optional[str] = Field(None, description="Sector classification")
    industry: Optional[str] = Field(None, description="Industry classification")
    country: Optional[str] = Field(None, description="Country of domicile")
    market_cap: Optional[float] = Field(None, description="Market capitalisation in USD")


class EquityFundamentals(BaseModel):
    """Fundamental metrics for an equity over a historical window."""

    equity: Equity
    revenue_cagr: Optional[float] = Field(
        None, description="Compound annual growth rate of revenue over the analysis window"
    )
    net_margin: Optional[float] = Field(None, description="Average net profit margin")
    operating_margin: Optional[float] = Field(
        None, description="Average operating profit margin"
    )
    cfo_to_ni: Optional[float] = Field(
        None, description="Ratio of operating cash flow to net income"
    )
    leverage_ratio: Optional[float] = Field(
        None, description="Debt‑to‑equity ratio or similar leverage metric"
    )
    lifecycle: Optional[str] = Field(
        None, description="Lifecycle stage classification (Growth/Mature/Defensive)"
    )


class EquityRatios(BaseModel):
    """Financial ratios computed from fundamentals and market data."""

    equity: Equity
    pe_ratio: Optional[float] = Field(None, description="Price‑to‑earnings ratio")
    pb_ratio: Optional[float] = Field(None, description="Price‑to‑book ratio")
    ps_ratio: Optional[float] = Field(None, description="Price‑to‑sales ratio")
    ev_to_ebitda: Optional[float] = Field(None, description="Enterprise value to EBITDA")
    fcf_yield: Optional[float] = Field(None, description="Free cash flow yield")
    roe: Optional[float] = Field(None, description="Return on equity")
    roa: Optional[float] = Field(None, description="Return on assets")
    roic: Optional[float] = Field(None, description="Return on invested capital")
    leverage_ratio: Optional[float] = Field(None, description="Debt‑to‑equity ratio")
    quality: Optional[float] = Field(None, description="Quality metric (e.g., OCF/NI)")


class EquityValuation(BaseModel):
    """Valuation summary for an equity."""

    equity: Equity
    expected_pe: Optional[float] = Field(
        None, description="Expected P/E based on regression or industry multiples"
    )
    actual_pe: Optional[float] = Field(None, description="Actual P/E ratio from market data")
    valuation_difference: Optional[float] = Field(
        None, description="Difference between actual and expected P/E"
    )
    status: Optional[str] = Field(
        None, description="Valuation status (Undervalued/Fair/Overvalued)"
    )
