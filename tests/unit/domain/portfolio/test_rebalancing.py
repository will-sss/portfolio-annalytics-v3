"""Unit tests for portfolio rebalancing utilities."""

from portfolio_analytics.domain.portfolio import compute_rebalance_trades, apply_rebalance


def test_rebalancing_moves_weights_towards_target() -> None:
    """Rebalancing should adjust weights towards the target within tolerance."""
    current = [0.6, 0.4]
    target = [0.5, 0.5]
    trades = compute_rebalance_trades(current, target, threshold=0.0)
    new_weights = apply_rebalance(current, trades)
    assert abs(new_weights[0] - 0.5) < 1e-6
    assert abs(new_weights[1] - 0.5) < 1e-6