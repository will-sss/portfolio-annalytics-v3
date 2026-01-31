# SPDX-License-Identifier: MIT

"""Repository abstractions for persistence."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import json

from ...utils.sanitization import to_serializable


class BaseRepository(ABC):
    """Abstract base class for storing and retrieving analysis results."""

    @abstractmethod
    def save(self, key: str, data: Any) -> None:
        """Persist the provided data under the given key."""

    @abstractmethod
    def load(self, key: str) -> Optional[Any]:
        """Retrieve previously saved data for the given key, if present."""


class FileRepository(BaseRepository):
    """Persist analysis results as JSON files on disk."""

    def __init__(self, base_dir: str | Path = "./data") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path_for(self, key: str) -> Path:
        safe_key = key.replace("/", "_")
        return self.base_dir / f"{safe_key}.json"

    def save(self, key: str, data: Any) -> None:
        path = self._path_for(key)
        with path.open("w", encoding="utf-8") as f:
            json.dump(to_serializable(data), f)

    def load(self, key: str) -> Optional[Any]:
        path = self._path_for(key)
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
