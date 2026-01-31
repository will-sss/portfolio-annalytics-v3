# SPDX-License-Identifier: MIT

"""Adapter for retrieving filings and financial data from the SEC EDGAR API."""

from __future__ import annotations

import logging
from typing import List

from ...config.settings import Settings, settings
from ...domain.equity.models import EquityFundamentals, EquityRatios, EquityValuation
from ...domain.fixed_income.models import Bond, YieldCurvePoint, DurationMetrics
from .base import BaseDataSource
from ..external.rate_limiter import RateLimiter


logger = logging.getLogger(__name__)


class EdgarDataSource(BaseDataSource):
    """SEC EDGAR data source.

    This adapter is currently a stub.  In the future, it will connect to
    the SEC EDGAR API to retrieve corporate filings and extract financial
    statements not available via Yahoo Finance.
    """

    def __init__(self, cfg: Settings | None = None, rate_limiter: RateLimiter | None = None):
        self.cfg = cfg or settings
        self.rate_limiter = rate_limiter or RateLimiter(max_calls=10, period_seconds=1)

    def get_equity_fundamentals(self, ticker: str) -> EquityFundamentals:
        raise NotImplementedError("EDGAR fundamentals retrieval not yet implemented")

    def get_equity_ratios(self, ticker: str) -> EquityRatios:
        raise NotImplementedError("EDGAR ratios retrieval not yet implemented")

    def get_equity_valuation(self, ticker: str) -> EquityValuation:
        raise NotImplementedError("EDGAR valuation retrieval not yet implemented")

    def get_bond(self, isin: str) -> Bond:
        raise NotImplementedError("EDGAR bond retrieval not yet implemented")

    def get_yield_curve(self) -> List[YieldCurvePoint]:
        raise NotImplementedError("EDGAR yield curve retrieval not yet implemented")

    def get_duration_metrics(self, bond: Bond) -> DurationMetrics:
        raise NotImplementedError("EDGAR duration metrics not yet implemented")
