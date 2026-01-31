# SPDX-License-Identifier: MIT

"""Application settings using Pydantic.

This module defines a :class:`Settings` class based on Pydantic's
``BaseSettings`` that reads configuration from environment variables or
a ``.env`` file.  It centralises all configurable parameters, making the
application environment‑aware and easier to test.
"""

from pathlib import Path
from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration values for Portfolio Analytics Platform V3.

    Values are loaded from environment variables with names matching the
    field names (case insensitive) and can be overridden by a ``.env`` file.
    Use :mod:`python_dotenv` or a similar tool to load `.env` in development.
    """

    # Application environment
    app_env: Literal["development", "testing", "production"] = Field(
        default="development", env="APP_ENV"
    )

    # Data source API keys
    alphavantage_api_key: Optional[str] = Field(
        default=None, env="ALPHAVANTAGE_API_KEY"
    )
    edgar_api_key: Optional[str] = Field(default=None, env="EDGAR_API_KEY")

    # Cache configuration
    cache_dir: Path = Field(default=Path("./cache"), env="CACHE_DIR")
    cache_ttl: int = Field(default=86_400, env="CACHE_TTL")  # one day default

    # Risk and valuation parameters
    risk_free_rate: float = Field(default=0.03, env="RISK_FREE_RATE")
    max_expected_return: float = Field(default=0.50, env="MAX_EXPECTED_RETURN")
    ridge_alpha: float = Field(default=1.0, env="RIDGE_ALPHA")

    # Logging configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: Literal["json", "plain"] = Field(
        default="json", env="LOG_FORMAT"
    )

    # API server configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    enable_cors: bool = Field(default=True, env="ENABLE_CORS")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()  # instantiate default settings at import time
