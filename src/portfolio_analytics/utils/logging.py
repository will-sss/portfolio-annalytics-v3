# SPDX-License-Identifier: MIT

"""Logging configuration for Portfolio Analytics Platform V3.

This module centralises logging setup.  Call :func:`configure_logging` at
application startup to configure the root logger according to settings.
"""

from __future__ import annotations

import logging
import json
from typing import Any, Dict

from ..config.settings import Settings, settings


class JsonFormatter(logging.Formatter):
    """Format log records as JSON strings.

    The default Python logging library outputs plain text.  This custom
    formatter serialises log records as JSON objects with standard fields.
    """

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        log_record: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def configure_logging(cfg: Settings | None = None) -> None:
    """Configure the root logger using the provided settings.

    Parameters
    ----------
    cfg:
        The configuration object.  If ``None``, the module‑level default
        settings instance is used.
    """
    cfg = cfg or settings
    level = getattr(logging, cfg.log_level.upper(), logging.INFO)
    root = logging.getLogger()
    root.setLevel(level)

    # Remove any existing handlers to avoid duplicate logs in case of reloads
    for handler in list(root.handlers):
        root.removeHandler(handler)

    handler = logging.StreamHandler()
    if cfg.log_format == "json":
        formatter: logging.Formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
    handler.setFormatter(formatter)
    root.addHandler(handler)
