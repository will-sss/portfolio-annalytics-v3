# SPDX-License-Identifier: MIT

"""Persistence layer for storing analysis results."""

from .repositories import BaseRepository
from .file_storage import FileRepository

__all__ = ["BaseRepository", "FileRepository"]