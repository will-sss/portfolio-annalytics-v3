# SPDX-License-Identifier: MIT

"""Caching wrapper for data source adapters."""

from __future__ import annotations

import time
from typing import Any, Dict, MutableMapping

from .base import BaseDataSource
from ...domain.equity.models import EquityFundamentals, EquityRatios, EquityValuation
from ...domain.fixed_income.models import Bond, YieldCurvePoint, DurationMetrics


class CachedDataSource(BaseDataSource):
    """Wraps another data source and caches its responses in memory.

    This simple caching layer stores responses in a dictionary with a
    time‑to‑live.  In production, you may want to replace this with a
    Redis‑based cache or similar.
    """

    def __init__(
        self,
        underlying: BaseDataSource,
        cache: MutableMapping[str, tuple[Any, float]] | None = None,
        ttl: int = 86_400,
    ) -> None:
        self.underlying = underlying
        self.cache: MutableMapping[str, tuple[Any, float]] = cache or {}
        self.ttl = ttl

    def _get_from_cache(self, key: str) -> Any | None:
        entry = self.cache.get(key)
        if entry is None:
            return None
        value, timestamp = entry
        if (time.time() - timestamp) > self.ttl:
            # expired
            del self.cache[key]
            return None
        return value

    def _set_cache(self, key: str, value: Any) -> None:
        self.cache[key] = (value, time.time())

    def get_equity_fundamentals(self, ticker: str) -> EquityFundamentals:
        key = f"eq_fundamentals:{ticker}"
        cached = self._get_from_cache(key)
        if cached is not None:
            return cached
        value = self.underlying.get_equity_fundamentals(ticker)
        self._set_cache(key, value)
        return value

    def get_equity_ratios(self, ticker: str) -> EquityRatios:
        key = f"eq_ratios:{ticker}"
        cached = self._get_from_cache(key)
        if cached is not None:
            return cached
        value = self.underlying.get_equity_ratios(ticker)
        self._set_cache(key, value)
        return value

    def get_equity_valuation(self, ticker: str) -> EquityValuation:
        key = f"eq_valuation:{ticker}"
        cached = self._get_from_cache(key)
        if cached is not None:
            return cached
        value = self.underlying.get_equity_valuation(ticker)
        self._set_cache(key, value)
        return value

    def get_bond(self, isin: str) -> Bond:
        key = f"bond:{isin}"
        cached = self._get_from_cache(key)
        if cached is not None:
            return cached
        value = self.underlying.get_bond(isin)
        self._set_cache(key, value)
        return value

    def get_yield_curve(self) -> list[YieldCurvePoint]:
        key = "yield_curve"
        cached = self._get_from_cache(key)
        if cached is not None:
            return cached
        value = self.underlying.get_yield_curve()
        self._set_cache(key, value)
        return value

    def get_duration_metrics(self, bond: Bond) -> DurationMetrics:
        key = f"duration:{bond.isin}"
        cached = self._get_from_cache(key)
        if cached is not None:
            return cached
        value = self.underlying.get_duration_metrics(bond)
        self._set_cache(key, value)
        return value
