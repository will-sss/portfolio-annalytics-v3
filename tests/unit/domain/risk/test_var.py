"""Unit tests for VaR functions in the risk module."""

import numpy as np

from portfolio_analytics.domain.risk import (
    historical_var,
    parametric_var,
    monte_carlo_var,
)


def test_historical_var_non_negative() -> None:
    """Historical VaR should return a non‑negative value for any return series."""
    returns = [0.01, -0.02, 0.03, -0.01, 0.02]
    var95 = historical_var(returns, 0.95)
    assert var95 >= 0


def test_parametric_var_non_negative() -> None:
    """Parametric VaR should return a non‑negative value for any return series."""
    returns = np.array([0.01, -0.02, 0.03, -0.01, 0.02])
    var95 = parametric_var(returns, 0.95)
    assert var95 >= 0


def test_monte_carlo_var_non_negative() -> None:
    """Monte Carlo VaR should return a non‑negative value for any return series."""
    returns = [0.01, -0.02, 0.03, -0.01, 0.02]
    var95 = monte_carlo_var(returns, 0.95, num_simulations=5000)
    assert var95 >= 0