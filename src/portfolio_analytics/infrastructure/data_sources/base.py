# SPDX-License-Identifier: MIT

"""Abstract base class for data source adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from ...domain.equity.models import EquityFundamentals, EquityRatios, EquityValuation
from ...domain.fixed_income.models import Bond, YieldCurvePoint, DurationMetrics


class BaseDataSource(ABC):
    """Defines the interface for data source adapters.

    Implementations connect to external providers such as Yahoo Finance,
    SEC EDGAR, or Alpha Vantage to retrieve data needed by the domain.
    """

    @abstractmethod
    def get_equity_fundamentals(self, ticker: str) -> EquityFundamentals:
        """Retrieve fundamental data for an equity.

        Parameters
        ----------
        ticker:
            The ticker symbol of the equity.

        Returns
        -------
        EquityFundamentals
            A Pydantic model containing fundamental metrics.
        """

    @abstractmethod
    def get_equity_ratios(self, ticker: str) -> EquityRatios:
        """Retrieve financial ratios for an equity."""

    @abstractmethod
    def get_equity_valuation(self, ticker: str) -> EquityValuation:
        """Retrieve or compute valuation information for an equity."""

    @abstractmethod
    def get_bond(self, isin: str) -> Bond:
        """Retrieve bond details given an ISIN."""

    @abstractmethod
    def get_yield_curve(self) -> List[YieldCurvePoint]:
        """Retrieve the current yield curve as a list of points."""

    @abstractmethod
    def get_duration_metrics(self, bond: Bond) -> DurationMetrics:
        """Calculate duration and convexity metrics for a bond."""
