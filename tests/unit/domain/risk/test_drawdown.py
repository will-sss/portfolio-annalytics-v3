"""Unit tests for drawdown calculations."""

from portfolio_analytics.domain.risk import max_drawdown


def test_max_drawdown_returns_negative_value() -> None:
    """The maximum drawdown should be non‑positive for any return series."""
    returns = [0.1, -0.05, -0.1, 0.02, 0.05]
    mdd, start, end, recovery = max_drawdown(returns)
    assert mdd <= 0
    # Start, end, recovery should be either None or strings
    assert start is None or isinstance(start, str)
    assert end is None or isinstance(end, str)
    assert recovery is None or isinstance(recovery, str)