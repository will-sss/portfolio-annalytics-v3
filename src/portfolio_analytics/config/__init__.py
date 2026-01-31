# SPDX-License-Identifier: MIT

"""Configuration package.

This package exposes the :class:`Settings` class used to configure the
application at runtime and a collection of constants used across domains.
"""

from .settings import Settings  # noqa: F401
from .constants import (
    MARKET_CAP_BUCKETS,
    LIFECYCLE_THRESHOLDS,
    SECTOR_CLASSIFICATIONS,
)

__all__ = [
    "Settings",
    "MARKET_CAP_BUCKETS",
    "LIFECYCLE_THRESHOLDS",
    "SECTOR_CLASSIFICATIONS",
]