# SPDX-License-Identifier: MIT

"""Modern Portfolio Theory optimisation functions."""

from __future__ import annotations

import numpy as np
from typing import List, Dict


def max_sharpe_ratio(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float = 0.0,
    bounds: tuple[float, float] = (0.0, 1.0),
) -> np.ndarray:
    """Compute the portfolio weights that maximise the Sharpe ratio.

    This function uses the closed‑form solution for the tangency portfolio
    under the assumption of no short selling and full investment (weights sum to 1).

    Parameters
    ----------
    expected_returns:
        Vector of expected returns for each asset.
    cov_matrix:
        Covariance matrix of asset returns.
    risk_free_rate:
        Risk‑free rate used to compute excess returns.
    bounds:
        Lower and upper bounds on weights (currently unused; no optimisation solver here).

    Returns
    -------
    numpy.ndarray
        Normalised weights that maximise the Sharpe ratio.
    """
    excess_returns = expected_returns - risk_free_rate
    inv_cov = np.linalg.pinv(cov_matrix)
    raw_weights = inv_cov @ excess_returns
    # Normalise to sum to 1
    weights = raw_weights / raw_weights.sum()
    # Clip negative weights to zero if no short selling is allowed
    weights = np.clip(weights, bounds[0], bounds[1])
    # Renormalise after clipping
    total = weights.sum()
    return weights / total if total != 0 else weights


def random_portfolios(
    expected_returns: np.ndarray,
    cov_matrix: np.ndarray,
    num_portfolios: int = 1000,
    seed: int | None = None,
) -> List[Dict[str, float]]:
    """Generate random portfolios for the efficient frontier.

    This function generates random weight vectors, computes their returns
    and volatilities and returns a list of portfolios.  The sum of
    weights is constrained to 1 and no short selling is allowed.
    """
    rng = np.random.default_rng(seed)
    n_assets = len(expected_returns)
    portfolios = []
    for _ in range(num_portfolios):
        weights = rng.random(n_assets)
        weights /= weights.sum()
        port_return = float(weights @ expected_returns)
        port_vol = float(np.sqrt(weights @ cov_matrix @ weights))
        portfolios.append({"return": port_return, "volatility": port_vol, "weights": weights})
    return portfolios
