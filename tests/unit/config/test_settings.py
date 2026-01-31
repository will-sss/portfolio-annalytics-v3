"""Unit tests for the settings module."""

from portfolio_analytics.config.settings import Settings


def test_default_settings_values() -> None:
    cfg = Settings(_env_file=None)  # ignore .env
    assert cfg.app_env == "development"
    assert cfg.cache_ttl == 86_400
    assert cfg.risk_free_rate == 0.03
    assert cfg.max_expected_return == 0.50
