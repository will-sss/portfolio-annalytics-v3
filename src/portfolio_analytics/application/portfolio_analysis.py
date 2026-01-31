# SPDX-License-Identifier: MIT

"""Service orchestrating portfolio analysis workflows."""

from __future__ import annotations

import logging
from typing import Dict, Any

from ..config.settings import Settings, settings
from ..domain.portfolio.models import Portfolio
from ..infrastructure.data_sources.base import BaseDataSource
from ..utils.sanitization import to_serializable


logger = logging.getLogger(__name__)


class PortfolioAnalysisService:
    """Coordinate portfolio analytics and optimisation."""

    def __init__(self, data_source: BaseDataSource, cfg: Settings | None = None) -> None:
        self.data_source = data_source
        self.cfg = cfg or settings

    def analyse(self, portfolio: Portfolio) -> Dict[str, Any]:
        """Analyse a portfolio and compute optimisation and risk metrics.

        This basic implementation calculates portfolio weights based on the
        quantity of each holding, then generates synthetic return series to
        estimate simple risk metrics such as parametric VaR and maximum
        drawdown.  In future versions, this method will retrieve historical
        return data from data sources and perform mean‑variance optimisation,
        Monte Carlo simulations and more sophisticated risk analysis.
        """
        logger.info("Starting portfolio analysis")
        # Compute weights from quantities
        total_qty = float(sum(h.quantity for h in portfolio.holdings))
        if total_qty == 0:
            weights = [0.0 for _ in portfolio.holdings]
        else:
            weights = [float(h.quantity) / total_qty for h in portfolio.holdings]
        result: Dict[str, Any] = {
            "portfolio": portfolio.dict(),
            "total_value": portfolio.total_value,
            "weights": weights,
        }
        try:
            # Generate synthetic daily returns for each asset (mean=0.05% per day, sd=2%)
            import numpy as np
            from ..domain.risk import parametric_var, max_drawdown, correlation_matrix

            n_assets = len(portfolio.holdings)
            horizon = 252  # one trading year
            rng = np.random.default_rng()
            returns_matrix = rng.normal(loc=0.0005, scale=0.02, size=(horizon, n_assets))
            # Portfolio returns as weighted sum of asset returns
            weights_arr = np.array(weights, dtype=float)
            port_returns = returns_matrix @ weights_arr
            # Risk metrics
            var95 = parametric_var(port_returns, 0.95)
            max_dd, dd_start, dd_end, dd_recovery = max_drawdown(port_returns)
            corr = correlation_matrix(returns_matrix.T)
            result.update(
                {
                    "var95": var95,
                    "max_drawdown": max_dd,
                    "drawdown_start": dd_start,
                    "drawdown_end": dd_end,
                    "drawdown_recovery": dd_recovery,
                    "correlation_matrix": corr,
                }
            )
        except Exception as exc:
            # Risk analytics failed; log but continue
            logger.exception("Risk analytics failed")
            result["error"] = f"Risk analytics failed: {exc}"
        return to_serializable(result)
