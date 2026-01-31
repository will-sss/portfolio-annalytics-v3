# SPDX-License-Identifier: MIT

"""API package providing a Flask application factory."""

from .app import create_app

__all__ = ["create_app"]