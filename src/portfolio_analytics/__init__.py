# SPDX-License-Identifier: MIT

"""Top‑level package for the Portfolio Analytics Platform.

This package contains domain models, infrastructure adapters, application services
and presentation layers for the third version of the portfolio analytics platform.

The project is organised according to domain‑driven design principles.  Business
logic resides under the :mod:`portfolio_analytics.domain` package, while
connectors to external services live under :mod:`portfolio_analytics.infrastructure`.

Application services orchestrate workflows and live under
:mod:`portfolio_analytics.application`.  User interfaces are provided in
:mod:`portfolio_analytics.presentation`.
"""

from .config.settings import Settings  # noqa: F401 re-export for convenience