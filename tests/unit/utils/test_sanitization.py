"""Unit tests for sanitisation utilities."""

import numpy as np
import pandas as pd

from portfolio_analytics.utils.sanitization import sanitize_number, sanitize_dataframe, to_serializable


def test_sanitize_number_with_nan_and_inf() -> None:
    assert sanitize_number(np.nan) is None
    assert sanitize_number(np.inf) is None
    assert sanitize_number(-np.inf) is None
    assert sanitize_number(123.45) == 123.45


def test_sanitize_dataframe_replaces_non_finite() -> None:
    df = pd.DataFrame({"a": [1.0, np.nan, np.inf, -np.inf]})
    cleaned = sanitize_dataframe(df)
    assert cleaned.iloc[1, 0] is None
    assert cleaned.iloc[2, 0] is None
    assert cleaned.iloc[3, 0] is None


def test_to_serializable_converts_nested_structures() -> None:
    data = {
        "numbers": [1, np.nan, 2],
        "dates": [pd.Timestamp("2022-01-01")],
        "nested": {"x": np.float64(1.23)},
    }
    serialised = to_serializable(data)
    assert serialised["numbers"][1] is None
    assert isinstance(serialised["dates"][0], str)
    assert serialised["nested"]["x"] == 1.23
