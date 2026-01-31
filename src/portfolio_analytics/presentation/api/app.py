# SPDX-License-Identifier: MIT

"""Flask application factory for the Portfolio Analytics API."""

from __future__ import annotations

import logging
from typing import Optional

from flask import Flask, jsonify
from flask_cors import CORS

from typing import Any, Dict, List  # noqa: F401

from ...config.settings import Settings, settings
from ...utils.logging import configure_logging

from .schemas import (
    EquityAnalysisRequest,
    EquityAnalysisResponse,
    BondAnalysisRequest,
    BondAnalysisResponse,
    PortfolioAnalysisRequest,
    PortfolioAnalysisResponse,
)
from ...application.equity_analysis import EquityAnalysisService
from ...application.bond_analysis import BondAnalysisService
from ...application.portfolio_analysis import PortfolioAnalysisService
from ...infrastructure.data_sources.yahoo import YahooDataSource


def create_app(cfg: Optional[Settings] = None) -> Flask:
    """Create and configure a Flask application instance.

    Parameters
    ----------
    cfg:
        Optional settings object.  If ``None``, the default
        application settings will be used.

    Returns
    -------
    Flask
        The configured Flask application.
    """
    cfg = cfg or settings
    configure_logging(cfg)
    app = Flask(__name__)
    if cfg.enable_cors:
        CORS(app)

    logger = logging.getLogger(__name__)
    logger.info("Initializing API in %s mode", cfg.app_env)

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health() -> tuple[dict[str, str], int]:
        return {"status": "ok"}, 200

    # Instantiate data source and services
    data_source = YahooDataSource(cfg)
    equity_service = EquityAnalysisService(data_source, cfg)
    bond_service = BondAnalysisService(data_source, cfg)
    portfolio_service = PortfolioAnalysisService(data_source, cfg)

    # Equity analysis endpoint
    @app.route("/api/equity/analyse", methods=["POST"])
    def analyse_equity() -> tuple[dict[str, Any], int]:  # type: ignore[override]
        """Analyse a list of equity tickers.

        Expects a JSON body matching :class:`EquityAnalysisRequest`.  Returns
        a list of results, one per ticker.  Errors for individual tickers
        are captured in the result list rather than aborting the whole
        request.
        """
        from flask import request

        payload = request.get_json(force=True)
        try:
            req = EquityAnalysisRequest(**payload)
        except Exception as exc:
            return {"error": str(exc)}, 400
        results: list[dict[str, Any]] = []
        for ticker in req.tickers:
            try:
                result = equity_service.analyse(ticker)
                results.append(result)
            except Exception as exc:
                logger.exception("Error analysing %s", ticker)
                results.append({"ticker": ticker, "error": str(exc)})
        resp = EquityAnalysisResponse(results=results)
        return resp.dict(), 200

    # Bond analysis endpoint
    @app.route("/api/bond/analyse", methods=["POST"])
    def analyse_bond() -> tuple[dict[str, Any], int]:  # type: ignore[override]
        """Analyse a list of bond ISINs.

        Expects a JSON body matching :class:`BondAnalysisRequest`.  Because
        bond data retrieval is not implemented in the default Yahoo data
        source, the response will contain error messages for each ISIN.
        """
        from flask import request

        payload = request.get_json(force=True)
        try:
            req = BondAnalysisRequest(**payload)
        except Exception as exc:
            return {"error": str(exc)}, 400
        results: list[dict[str, Any]] = []
        for isin in req.isins:
            try:
                result = bond_service.analyse(isin)
                results.append(result)
            except Exception as exc:
                logger.exception("Error analysing bond %s", isin)
                results.append({"isin": isin, "error": str(exc)})
        resp = BondAnalysisResponse(results=results)
        return resp.dict(), 200

    # Portfolio analysis endpoint
    @app.route("/api/portfolio/analyse", methods=["POST"])
    def analyse_portfolio() -> tuple[dict[str, Any], int]:  # type: ignore[override]
        """Analyse a portfolio of holdings.

        This endpoint accepts a JSON body matching :class:`PortfolioAnalysisRequest`.
        The portfolio analysis service will compute metrics such as total
        value, and (in future versions) optimisation and risk analytics.
        """
        from flask import request

        payload = request.get_json(force=True)
        try:
            req = PortfolioAnalysisRequest(**payload)
        except Exception as exc:
            return {"error": str(exc)}, 400
        # Build Portfolio model from holdings; here we use simple dicts
        from ...domain.common.models import Instrument
        from ...domain.portfolio.models import Holding, Portfolio

        holdings = []
        for item in req.holdings:
            try:
                instrument_data = item.get("instrument")
                if isinstance(instrument_data, dict):
                    instrument = Instrument(**instrument_data)
                else:
                    instrument = Instrument(symbol=instrument_data)  # type: ignore[call-arg]
                quantity = float(item.get("quantity", 0))
                holdings.append(Holding(instrument=instrument, quantity=quantity))
            except Exception as exc:
                logger.exception("Invalid holding: %s", item)
                return {"error": f"Invalid holding format: {item}: {exc}"}, 400
        portfolio = Portfolio(holdings=holdings)
        try:
            result = portfolio_service.analyse(portfolio)
        except Exception as exc:
            logger.exception("Error analysing portfolio")
            return {"error": str(exc)}, 500
        resp = PortfolioAnalysisResponse(result=result)
        return resp.dict(), 200

    return app
