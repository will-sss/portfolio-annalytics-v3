# SPDX-License-Identifier: MIT

"""Utilities for handling NaN, infinite and non‑serializable values.

These functions ensure that numerical values and data structures are safe for
JSON serialisation and downstream processing.  They centralise the logic
that was previously scattered across the V2 codebase.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Sequence

import numpy as np  # type: ignore[import]
import pandas as pd  # type: ignore[import]


def sanitize_number(value: Any) -> float | None:
    """Return a safe numeric value or ``None``.

    Accepts values that may be floats, numpy types or ``None``.  If the
    value is not finite (NaN or infinite), returns ``None``.  Otherwise
    returns the native Python float.

    Parameters
    ----------
    value:
        A number or value convertible to float.

    Returns
    -------
    float | None
        A finite float or ``None`` if the input is NaN/inf or not a number.
    """
    if value is None:
        return None
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(num) or math.isinf(num):
        return None
    return num


def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the DataFrame with non‑finite values replaced by ``None``.

    This function converts NaN and infinite values to ``None`` to
    facilitate JSON serialisation.  It does not modify the original
    DataFrame.

    Parameters
    ----------
    df:
        The input DataFrame.

    Returns
    -------
    pandas.DataFrame
        A sanitized copy of the input.
    """
    # Replace inf and -inf with NaN
    cleaned = df.replace([np.inf, -np.inf], np.nan)
    # Use where to replace NaNs with None (object dtype)
    return cleaned.where(pd.notna(cleaned), None)


def to_serializable(value: Any) -> Any:
    """Convert a value to a JSON‑serializable form.

    Recursively traverses lists, tuples and dictionaries, converting
    numpy scalar types and pandas objects to native Python types, and
    replacing NaN/inf with ``None``.
    """
    if isinstance(value, (list, tuple, set)):
        return [to_serializable(v) for v in value]
    if isinstance(value, dict):
        return {k: to_serializable(v) for k, v in value.items()}
    if isinstance(value, (np.generic,)):
        return sanitize_number(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return value
