"""Unit tests for correlation matrix computation."""

from portfolio_analytics.domain.risk import correlation_matrix


def test_correlation_matrix_dimensions() -> None:
    """Correlation matrix should be square with size equal to number of series."""
    data = [
        [0.1, 0.2, -0.1],
        [0.05, 0.03, 0.04],
    ]
    corr = correlation_matrix(data)
    assert len(corr) == 2
    assert all(len(row) == 2 for row in corr)
    # Diagonal elements should be approximately one
    assert abs(corr[0][0] - 1.0) < 1e-8
    assert abs(corr[1][1] - 1.0) < 1e-8