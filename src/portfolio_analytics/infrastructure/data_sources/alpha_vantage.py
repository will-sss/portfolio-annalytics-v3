# SPDX-License-Identifier: MIT

"""Adapter for retrieving data from the Alpha Vantage API."""

from __future__ import annotations

import logging
from typing import List

import requests

from ...config.settings import Settings, settings
from ...domain.equity.models import EquityFundamentals, EquityRatios, EquityValuation
from ...domain.fixed_income.models import Bond, YieldCurvePoint, DurationMetrics
from .base import BaseDataSource
from ..external.rate_limiter import RateLimiter


logger = logging.getLogger(__name__)


class AlphaVantageDataSource(BaseDataSource):
    """Alpha Vantage data source.

    Only free tier endpoints are used.  The adapter currently provides
    placeholders; actual implementations should respect rate limits
    (5 API requests per minute, 500 per day on the free tier) and
    parse responses into domain models.
    """

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, cfg: Settings | None = None, rate_limiter: RateLimiter | None = None):
        self.cfg = cfg or settings
        self.api_key = self.cfg.alphavantage_api_key
        self.rate_limiter = rate_limiter or RateLimiter(max_calls=5, period_seconds=60)

    def _get(self, params: dict[str, str]) -> dict:
        if not self.api_key:
            raise ValueError("Alpha Vantage API key not configured")
        params_with_key = {**params, "apikey": self.api_key}
        self.rate_limiter.acquire()
        response = requests.get(self.BASE_URL, params=params_with_key, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_equity_fundamentals(self, ticker: str) -> EquityFundamentals:
        raise NotImplementedError("Alpha Vantage fundamentals retrieval not yet implemented")

    def get_equity_ratios(self, ticker: str) -> EquityRatios:
        raise NotImplementedError("Alpha Vantage ratios retrieval not yet implemented")

    def get_equity_valuation(self, ticker: str) -> EquityValuation:
        raise NotImplementedError("Alpha Vantage valuation retrieval not yet implemented")

    def get_bond(self, isin: str) -> Bond:
        raise NotImplementedError("Alpha Vantage bond retrieval not yet implemented")

    def get_yield_curve(self) -> List[YieldCurvePoint]:
        raise NotImplementedError("Alpha Vantage yield curve retrieval not yet implemented")

    def get_duration_metrics(self, bond: Bond) -> DurationMetrics:
        raise NotImplementedError("Alpha Vantage duration metrics not yet implemented")
