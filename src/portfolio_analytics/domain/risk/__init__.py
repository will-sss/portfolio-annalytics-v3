# SPDX-License-Identifier: MIT

"""Risk analytics domain models and analytics."""

"""Risk analytics exports.

This package exposes both the data models (VaRResult, DrawdownStats,
CorrelationMatrix) and a suite of analytic functions for computing risk
metrics such as Value at Risk, maximum drawdown and correlation matrices.
"""

from .models import VaRResult, DrawdownStats, CorrelationMatrix
from .var import historical_var, parametric_var, monte_carlo_var
from .drawdown import max_drawdown
from .correlation import correlation_matrix

__all__ = [
    "VaRResult",
    "DrawdownStats",
    "CorrelationMatrix",
    "historical_var",
    "parametric_var",
    "monte_carlo_var",
    "max_drawdown",
    "correlation_matrix",
]