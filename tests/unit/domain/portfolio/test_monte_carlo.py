"""Unit tests for Monte Carlo simulation utilities."""

import numpy as np

from portfolio_analytics.domain.portfolio import simulate_portfolio_returns


def test_simulate_portfolio_returns_shape() -> None:
    """simulate_portfolio_returns should return an array of the correct shape."""
    weights = np.array([0.5, 0.5])
    expected_returns = np.array([0.001, 0.002])
    cov_matrix = np.array([[0.01, 0.005], [0.005, 0.02]])
    sims = simulate_portfolio_returns(weights, expected_returns, cov_matrix, horizon=10, num_simulations=100)
    assert sims.shape == (100,)