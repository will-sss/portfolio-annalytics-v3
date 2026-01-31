# SPDX-License-Identifier: MIT

"""Service orchestrating fixed income analysis workflows."""

from __future__ import annotations

import logging
from typing import Dict, Any

from ..config.settings import Settings, settings
from ..domain.fixed_income.models import Bond, DurationMetrics
from ..infrastructure.data_sources.base import BaseDataSource
from ..utils.sanitization import to_serializable


logger = logging.getLogger(__name__)


class BondAnalysisService:
    """Coordinate fetching and analysing bond data."""

    def __init__(self, data_source: BaseDataSource, cfg: Settings | None = None) -> None:
        self.data_source = data_source
        self.cfg = cfg or settings

    def analyse(self, isin: str) -> Dict[str, Any]:
        """Run a full bond analysis pipeline for a single ISIN."""
        logger.info("Starting bond analysis for %s", isin)
        bond: Bond = self.data_source.get_bond(isin)
        duration: DurationMetrics = self.data_source.get_duration_metrics(bond)
        # Placeholder for yield curve retrieval and price sensitivity
        result = {
            "bond": bond.dict(),
            "duration": duration.dict(),
        }
        return to_serializable(result)
