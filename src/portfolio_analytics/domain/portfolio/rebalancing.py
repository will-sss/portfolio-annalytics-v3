# SPDX-License-Identifier: MIT

"""Portfolio rebalancing utilities.

Rebalancing involves adjusting portfolio holdings back to target weights
after market movements cause drift.  This module provides simple helper
functions to determine the trades required to rebalance and to apply
those trades to compute new weights.  Transaction costs and taxes are
ignored in this minimal implementation.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np


def compute_rebalance_trades(
    current_weights: np.ndarray,
    target_weights: np.ndarray,
    threshold: float = 0.0,
) -> np.ndarray:
    """Compute the trades (buy/sell adjustments) needed to rebalance.

    Parameters
    ----------
    current_weights:
        Current portfolio weights.  Should sum to 1.
    target_weights:
        Desired portfolio weights.  Should sum to 1.
    threshold:
        Minimum absolute difference below which no trade is executed (e.g.,
        to avoid small turnover).  Differences with absolute value less
        than threshold are set to zero.

    Returns
    -------
    numpy.ndarray
        Vector of trades where positive values indicate a buy and negative
        values indicate a sell, expressed as weight fractions of the
        portfolio.
    """
    diffs = np.asarray(target_weights, dtype=float) - np.asarray(current_weights, dtype=float)
    # Zero out small differences
    trades = np.where(np.abs(diffs) >= threshold, diffs, 0.0)
    return trades


def apply_rebalance(
    current_weights: np.ndarray,
    trades: np.ndarray,
) -> np.ndarray:
    """Apply trades to obtain new weights.

    This function assumes that the total trade weights sum to zero (i.e.,
    fully invested portfolio remains fully invested).  It computes the
    updated weights after applying the trades.

    Parameters
    ----------
    current_weights:
        Current portfolio weights.
    trades:
        Trades computed by :func:`compute_rebalance_trades`.

    Returns
    -------
    numpy.ndarray
        New weights after rebalancing.
    """
    new_weights = np.asarray(current_weights, dtype=float) + np.asarray(trades, dtype=float)
    # Ensure no negative weights and renormalise to sum to 1
    new_weights = np.clip(new_weights, 0.0, None)
    total = new_weights.sum()
    return new_weights / total if total != 0 else new_weights
