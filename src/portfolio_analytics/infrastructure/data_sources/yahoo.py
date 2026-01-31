# SPDX-License-Identifier: MIT

"""Adapter for retrieving data from Yahoo Finance via yfinance."""

from __future__ import annotations

import logging
from typing import List

import yfinance as yf  # type: ignore[import]
import pandas as pd  # type: ignore[import]

from ...config.settings import Settings, settings
from ...domain.equity.models import Equity, EquityFundamentals, EquityRatios, EquityValuation
from ...domain.fixed_income.models import Bond, YieldCurvePoint, DurationMetrics
from .base import BaseDataSource
from .caching import CachedDataSource
from ..external.rate_limiter import RateLimiter


logger = logging.getLogger(__name__)


class YahooDataSource(BaseDataSource):
    """Data source for Yahoo Finance using the yfinance library.

    This adapter fetches company metadata, financial statements and
    market data from Yahoo Finance.  It uses a simple rate limiter to
    comply with unofficial rate limits and supports optional caching via
    :class:`CachedDataSource`.
    """

    def __init__(self, cfg: Settings | None = None, rate_limiter: RateLimiter | None = None):
        self.cfg = cfg or settings
        self.rate_limiter = rate_limiter or RateLimiter(max_calls=50, period_seconds=60)

    def _get_ticker(self, symbol: str) -> yf.Ticker:
        """Internal helper to instantiate a yfinance Ticker with rate limiting."""
        self.rate_limiter.acquire()
        return yf.Ticker(symbol)

    def get_equity_fundamentals(self, ticker: str) -> EquityFundamentals:
        """Fetch and compute fundamental metrics for a single equity.

        This implementation queries Yahoo Finance via yfinance to obtain income
        statements, balance sheets and cash flow statements.  It computes a
        revenue compound annual growth rate (CAGR), profit margins, cash‑flow
        quality and leverage.  Missing values are handled gracefully.
        """
        logger.debug("Fetching fundamentals for %s", ticker)
        yt = self._get_ticker(ticker)
        info = yt.info or {}
        equity = Equity(
            symbol=ticker,
            name=info.get("shortName"),
            sector=info.get("sector"),
            industry=info.get("industry"),
            country=info.get("country"),
            market_cap=info.get("marketCap"),
        )

        # Fetch financial statements (annual).  yfinance returns most recent
        # columns first; reverse order for chronological calculations.
        try:
            financials = yt.financials
        except Exception:
            financials = None
        try:
            balance_sheet = yt.balance_sheet
        except Exception:
            balance_sheet = None
        try:
            cashflow = yt.cashflow
        except Exception:
            cashflow = None

        revenue_cagr: float | None = None
        net_margin: float | None = None
        operating_margin: float | None = None
        cfo_to_ni: float | None = None
        leverage_ratio: float | None = None
        lifecycle: str | None = None

        if financials is not None and not financials.empty:
            try:
                revenue_series = financials.loc["Total Revenue"].dropna()
                revenue_series = revenue_series[::-1]  # chronological order oldest->newest
                if len(revenue_series) >= 2:
                    first = revenue_series.iloc[0]
                    last = revenue_series.iloc[-1]
                    years = len(revenue_series) - 1
                    if first and years > 0:
                        revenue_cagr = (last / first) ** (1 / years) - 1
            except Exception:
                revenue_cagr = None
            try:
                net_income_series = financials.loc["Net Income"].dropna()
                net_income_series = net_income_series[::-1]
                # Use the most recent period for margins
                if not revenue_series.empty and not net_income_series.empty:
                    net_margin = (
                        net_income_series.iloc[-1] / revenue_series.iloc[-1]
                        if revenue_series.iloc[-1] != 0
                        else None
                    )
                # Operating margin: Operating Income / Revenue
                op_income_series = financials.loc.get("Operating Income")
                if op_income_series is not None:
                    op_income_series = op_income_series.dropna()[::-1]
                    if not op_income_series.empty and not revenue_series.empty:
                        operating_margin = (
                            op_income_series.iloc[-1] / revenue_series.iloc[-1]
                            if revenue_series.iloc[-1] != 0
                            else None
                        )
            except Exception:
                net_margin = None
                operating_margin = None
        # Cash flow quality
        if cashflow is not None and not cashflow.empty:
            try:
                cfo_series = cashflow.loc["Total Cash From Operating Activities"].dropna()[::-1]
                if financials is not None and not financials.empty:
                    ni_series = financials.loc["Net Income"].dropna()[::-1]
                    if not cfo_series.empty and not ni_series.empty and ni_series.iloc[-1] != 0:
                        cfo_to_ni = cfo_series.iloc[-1] / ni_series.iloc[-1]
            except Exception:
                cfo_to_ni = None
        # Leverage ratio
        if balance_sheet is not None and not balance_sheet.empty:
            try:
                # total debt may be under "Total Debt" or sum of long + short term debt
                if "Total Debt" in balance_sheet.index:
                    debt_series = balance_sheet.loc["Total Debt"].dropna()[::-1]
                else:
                    long_term = balance_sheet.loc.get("Long Term Debt")
                    short_term = balance_sheet.loc.get("Short Term Debt")
                    if long_term is not None and short_term is not None:
                        debt_series = (long_term + short_term).dropna()[::-1]
                    else:
                        debt_series = None
                equity_series = balance_sheet.loc.get("Total Stockholder Equity")
                if equity_series is not None:
                    equity_series = equity_series.dropna()[::-1]
                if debt_series is not None and not debt_series.empty and equity_series is not None and not equity_series.empty:
                    if equity_series.iloc[-1] != 0:
                        leverage_ratio = debt_series.iloc[-1] / equity_series.iloc[-1]
            except Exception:
                leverage_ratio = None
        # Lifecycle classification
        from ...config.constants import LIFECYCLE_THRESHOLDS

        if revenue_cagr is not None:
            growth_thr = LIFECYCLE_THRESHOLDS.get("growth_rev_cagr", 0.15)
            mature_thr = LIFECYCLE_THRESHOLDS.get("mature_rev_cagr", 0.05)
            if revenue_cagr >= growth_thr:
                lifecycle = "Growth"
            elif revenue_cagr >= mature_thr:
                lifecycle = "Mature"
            else:
                lifecycle = "Defensive"

        return EquityFundamentals(
            equity=equity,
            revenue_cagr=revenue_cagr,
            net_margin=net_margin,
            operating_margin=operating_margin,
            cfo_to_ni=cfo_to_ni,
            leverage_ratio=leverage_ratio,
            lifecycle=lifecycle,
        )

    def get_equity_ratios(self, ticker: str) -> EquityRatios:
        """Fetch market‑based ratios for an equity.

        This method uses yfinance to obtain price and earnings information to
        compute valuation and return ratios.  Missing data is handled
        gracefully.
        """
        logger.debug("Fetching ratios for %s", ticker)
        yt = self._get_ticker(ticker)
        info = yt.info or {}
        equity = Equity(
            symbol=ticker,
            name=info.get("shortName"),
            sector=info.get("sector"),
            industry=info.get("industry"),
            country=info.get("country"),
            market_cap=info.get("marketCap"),
        )

        pe_ratio: float | None = None
        pb_ratio: float | None = None
        ps_ratio: float | None = None
        ev_to_ebitda: float | None = None
        fcf_yield: float | None = None
        roe: float | None = None
        roa: float | None = None
        roic: float | None = None
        leverage: float | None = None
        quality: float | None = None

        # Price and earnings
        try:
            # Price per share and earnings per share from info
            price = info.get("regularMarketPrice") or info.get("previousClose")
            eps = info.get("trailingEps")
            book = info.get("bookValue")
            revenue = info.get("totalRevenue")
            ebitda = info.get("ebitda")
            free_cash_flow = info.get("freeCashflow")
            total_assets = info.get("totalAssets")
            total_equity = info.get("totalStockholderEquity")
            # P/E ratio
            if price is not None and eps:
                if eps != 0:
                    pe_ratio = price / eps
            # P/B ratio
            if price is not None and book:
                if book != 0:
                    pb_ratio = price / book
            # P/S ratio
            if price is not None and revenue and equity.market_cap:
                # P/S = market cap / total revenue per share; approximate using market cap / revenue
                if revenue != 0:
                    ps_ratio = equity.market_cap / revenue
            # EV/EBITDA
            enterprise_value = info.get("enterpriseValue")
            if enterprise_value and ebitda:
                if ebitda != 0:
                    ev_to_ebitda = enterprise_value / ebitda
            # FCF yield
            if free_cash_flow and equity.market_cap:
                if equity.market_cap != 0:
                    fcf_yield = free_cash_flow / equity.market_cap
            # Returns
            net_income = info.get("netIncomeToCommon") or info.get("netIncome")
            if net_income and total_equity:
                if total_equity != 0:
                    roe = net_income / total_equity
            # ROA
            if net_income and total_assets:
                if total_assets != 0:
                    roa = net_income / total_assets
            # Leverage (Debt/Equity)
            total_debt = info.get("totalDebt") or info.get("longTermDebt")
            if total_debt and total_equity:
                if total_equity != 0:
                    leverage = total_debt / total_equity
            # Quality will be derived from fundamentals
        except Exception:
            # leave metrics as None
            pass

        return EquityRatios(
            equity=equity,
            pe_ratio=pe_ratio,
            pb_ratio=pb_ratio,
            ps_ratio=ps_ratio,
            ev_to_ebitda=ev_to_ebitda,
            fcf_yield=fcf_yield,
            roe=roe,
            roa=roa,
            roic=roic,
            leverage_ratio=leverage,
            quality=quality,
        )

    def get_equity_valuation(self, ticker: str) -> EquityValuation:
        """Compute a simple valuation comparison for an equity.

        The method retrieves fundamental and ratio data, then estimates an
        "expected" price‑to‑earnings ratio based on sector classification and
        revenue growth.  The difference between actual and expected P/E is
        used to classify the stock as Undervalued, Fair or Overvalued.
        """
        logger.debug("Computing valuation for %s", ticker)
        fundamentals = self.get_equity_fundamentals(ticker)
        ratios = self.get_equity_ratios(ticker)
        actual_pe = ratios.pe_ratio
        expected_pe: float | None = None
        valuation_difference: float | None = None
        status: str | None = None

        if actual_pe is not None:
            from ...config.constants import SECTOR_CLASSIFICATIONS
            # Determine base P/E by sector classification
            base_pe_map = {
                "Growth": 25.0,
                "Mature": 15.0,
                "Defensive": 12.0,
                "Cyclic": 10.0,
            }
            classification = None
            if fundamentals.equity.sector:
                classification = SECTOR_CLASSIFICATIONS.get(
                    fundamentals.equity.sector, None
                )
            base_pe = base_pe_map.get(classification or "Mature", 15.0)
            # Adjust expected P/E by revenue growth (CAGR).  More growth warrants higher multiples.
            growth_adj = 1.0
            if fundamentals.revenue_cagr is not None:
                growth_adj += fundamentals.revenue_cagr
            expected_pe = base_pe * growth_adj
            valuation_difference = actual_pe - expected_pe
            # Determine valuation status with a 10% band
            if expected_pe:
                lower = expected_pe * 0.9
                upper = expected_pe * 1.1
                if actual_pe < lower:
                    status = "Undervalued"
                elif actual_pe > upper:
                    status = "Overvalued"
                else:
                    status = "Fair"

        return EquityValuation(
            equity=fundamentals.equity,
            expected_pe=expected_pe,
            actual_pe=actual_pe,
            valuation_difference=valuation_difference,
            status=status,
        )

    def get_bond(self, isin: str) -> Bond:
        logger.debug("Fetching bond data for %s", isin)
        # Yahoo Finance does not provide bond data; stub implementation
        raise NotImplementedError("Bond data retrieval not implemented for YahooDataSource")

    def get_yield_curve(self) -> List[YieldCurvePoint]:
        logger.debug("Fetching yield curve data")
        raise NotImplementedError("Yield curve retrieval not implemented for YahooDataSource")

    def get_duration_metrics(self, bond: Bond) -> DurationMetrics:
        logger.debug("Calculating duration metrics for %s", bond.isin)
        raise NotImplementedError("Duration metrics calculation not implemented for YahooDataSource")
