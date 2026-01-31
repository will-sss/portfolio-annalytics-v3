# SPDX-License-Identifier: MIT

"""Monte Carlo simulation utilities for portfolio analysis.

This module provides functions to simulate the distribution of future
portfolio returns using geometric Brownian motion assumptions.  Monte Carlo
simulations are widely used to estimate the distribution of outcomes for
portfolios and to compute metrics such as expected returns, volatility and
Value at Risk.

The functions here are intentionally simple and should be expanded to
incorporate more sophisticated dynamics, non-normal distributions and
serial correlation where required.
"""

from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np


def simulate_portfolio_returns(
    weights: np.ndarray,
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    horizon: int = 252,
    num_simulations: int = 10000,
) -> np.ndarray:
    """Simulate portfolio returns over a time horizon using multivariate normal draws.

    The simulation assumes that asset returns follow a multivariate normal
    distribution with constant mean and covariance.  It generates random
    returns for each asset at each step, aggregates them into portfolio
    returns and returns the distribution of cumulative portfolio returns.

    Parameters
    ----------
    weights:
        Array of portfolio weights summing to 1.  Length must equal the
        dimension of expected_returns and cov_matrix.
    expected_returns:
        Expected periodic returns for each asset (e.g., daily returns).
    cov_matrix:
        Covariance matrix of asset returns per period.
    horizon:
        Number of periods to simulate (e.g., 252 for one trading year).
    num_simulations:
        Number of Monte Carlo paths to simulate.

    Returns
    -------
    numpy.ndarray
        Array of simulated cumulative portfolio returns of length num_simulations.
    """
    n_assets = len(weights)
    # Cholesky decomposition for sampling correlated returns
    chol = np.linalg.cholesky(cov_matrix)
    # Precompute drift component for each asset
    dt_returns = np.asarray(expected_returns, dtype=float)
    # Container for final portfolio returns
    final_returns = np.empty(num_simulations, dtype=float)
    rng = np.random.default_rng()
    for i in range(num_simulations):
        # Simulate asset returns path
        # Generate random normal innovations for each period and asset
        z = rng.standard_normal((horizon, n_assets))
        # Compute correlated returns per period: mu + L * z
        paths = dt_returns + z @ chol.T
        # Aggregate into portfolio returns per period
        port_ret_series = paths @ weights
        # Compute cumulative portfolio return (compound)
        cumulative = np.prod(1.0 + port_ret_series) - 1.0
        final_returns[i] = cumulative
    return final_returns


def simulate_asset_paths(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    horizon: int = 252,
    num_simulations: int = 10000,
) -> np.ndarray:
    """Simulate future paths for multiple assets using multivariate normal draws.

    This function returns a three‑dimensional array of shape
    (num_simulations, horizon, n_assets) containing simulated return paths.
    It can be used for scenario analysis, stress testing or as input to
    derivative pricing models.
    """
    n_assets = len(expected_returns)
    chol = np.linalg.cholesky(cov_matrix)
    rng = np.random.default_rng()
    paths = rng.standard_normal((num_simulations, horizon, n_assets))
    # Broadcast addition of expected returns and multiplication by Cholesky factor
    correlated = expected_returns + np.matmul(paths, chol.T)
    return correlated
