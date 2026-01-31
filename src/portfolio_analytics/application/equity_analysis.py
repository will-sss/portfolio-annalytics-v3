# SPDX-License-Identifier: MIT

"""Service orchestrating equity analysis workflows."""

from __future__ import annotations

import logging
from typing import Dict, Any, Optional

from ..config.settings import Settings, settings
from ..domain.equity.models import EquityFundamentals, EquityRatios, EquityValuation
from ..domain.common.models import Instrument
from ..infrastructure.data_sources.base import BaseDataSource
from ..utils.sanitization import to_serializable


logger = logging.getLogger(__name__)


class EquityAnalysisService:
    """Coordinate fetching and analysing equity data.

    This service retrieves fundamentals, ratios and valuation metrics from a
    data source and applies additional business rules, such as sector‑aware
    adjustments and projection haircuts.  It returns a serialisable
    dictionary containing all relevant results.
    """

    def __init__(self, data_source: BaseDataSource, cfg: Settings | None = None) -> None:
        self.data_source = data_source
        self.cfg = cfg or settings

    def analyse(self, ticker: str) -> Dict[str, Any]:
        """Run a full equity analysis pipeline for a single ticker.

        Parameters
        ----------
        ticker:
            The equity ticker symbol.

        Returns
        -------
        Dict[str, Any]
            A serialisable dictionary containing fundamentals, ratios and valuation.
        """
        logger.info("Starting analysis for %s", ticker)
        fundamentals: EquityFundamentals = self.data_source.get_equity_fundamentals(ticker)
        ratios: EquityRatios = self.data_source.get_equity_ratios(ticker)
        valuation: EquityValuation = self.data_source.get_equity_valuation(ticker)

        # Augment ratios with quality and leverage metrics from fundamentals
        ratios_copy = ratios.copy()
        if fundamentals.leverage_ratio is not None:
            ratios_copy.leverage_ratio = fundamentals.leverage_ratio
        if fundamentals.cfo_to_ni is not None:
            ratios_copy.quality = fundamentals.cfo_to_ni

        # TODO: apply sector‑aware adjustments and return haircuts (>50% annual growth)
        result = {
            "fundamentals": fundamentals.dict(),
            "ratios": ratios_copy.dict(),
            "valuation": valuation.dict(),
        }
        return to_serializable(result)
