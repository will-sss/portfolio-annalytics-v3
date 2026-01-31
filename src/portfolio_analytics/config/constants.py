# SPDX-License-Identifier: MIT

"""Business constants shared across domains.

This module defines enumerations and threshold values used throughout the
portfolio analytics system.  These values can be referenced by domain
logic to maintain consistency across calculations.
"""

from typing import Dict, Tuple

# Market capitalisation buckets (in USD)
MARKET_CAP_BUCKETS: Dict[str, Tuple[float, float]] = {
    "Micro": (0.0, 300e6),  # <300M
    "Small": (300e6, 2e9),  # 300M–2B
    "Mid": (2e9, 10e9),    # 2B–10B
    "Large": (10e9, 50e9), # 10B–50B
    "Mega": (50e9, float("inf")),  # >50B
}

# Lifecycle classification thresholds.  Values are expressed as decimals
# representing annualised growth or margins.  These thresholds are
# indicative; adjust them via configuration if necessary.
LIFECYCLE_THRESHOLDS: Dict[str, float] = {
    "growth_rev_cagr": 0.15,   # revenue CAGR > 15% implies growth phase
    "mature_rev_cagr": 0.05,   # revenue CAGR > 5% implies mature phase
    "profit_margin": 0.10,     # net margin > 10% considered healthy
    "cfo_ni_ratio": 1.0,       # CFO / net income > 100% indicates quality earnings
}

# Sector classifications for high‑level grouping.  The value indicates
# whether a sector is generally growth‑oriented ("Growth"), mature ("Mature"),
# defensive ("Defensive"), or cyclic ("Cyclic").
SECTOR_CLASSIFICATIONS: Dict[str, str] = {
    "Technology": "Growth",
    "Consumer Discretionary": "Growth",
    "Healthcare": "Defensive",
    "Utilities": "Defensive",
    "Energy": "Cyclic",
    "Materials": "Cyclic",
    "Industrial": "Cyclic",
    "Consumer Staples": "Defensive",
    "Financial": "Mature",
    "Real Estate": "Mature",
    "Communication Services": "Growth",
}
