# SPDX-License-Identifier: MIT

"""API request and response schemas using Pydantic."""

from __future__ import annotations

from typing import List, Dict, Any

from pydantic import BaseModel, Field


class EquityAnalysisRequest(BaseModel):
    """Schema for equity analysis requests."""

    tickers: List[str] = Field(..., description="List of equity ticker symbols")


class EquityAnalysisResponse(BaseModel):
    """Schema for equity analysis responses."""

    results: List[Dict[str, Any]] = Field(..., description="List of analysis results per ticker")


class BondAnalysisRequest(BaseModel):
    """Schema for bond analysis requests."""

    isins: List[str] = Field(..., description="List of bond ISINs")


class BondAnalysisResponse(BaseModel):
    """Schema for bond analysis responses."""

    results: List[Dict[str, Any]] = Field(..., description="List of bond analysis results per ISIN")


class PortfolioAnalysisRequest(BaseModel):
    """Schema for portfolio analysis requests.

    A portfolio is defined by a list of holdings, where each holding
    specifies the instrument identifier and the quantity held.  Additional
    fields may be included to support constraints or preferences in future
    versions.
    """

    holdings: List[Dict[str, Any]] = Field(
        ..., description="List of holdings with instrument identifiers and quantities"
    )


class PortfolioAnalysisResponse(BaseModel):
    """Schema for portfolio analysis responses."""

    result: Dict[str, Any] = Field(..., description="Analysis results for the portfolio")
