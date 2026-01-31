# SPDX-License-Identifier: MIT

"""Simple rate limiter for API calls."""

from __future__ import annotations

import threading
import time


class RateLimiter:
    """Token-bucket rate limiter.

    Allows up to ``max_calls`` per ``period_seconds``.  Excess calls will block
    until a token becomes available.  This class is thread‑safe.
    """

    def __init__(self, max_calls: int, period_seconds: float) -> None:
        self.max_calls = max_calls
        self.period = period_seconds
        self.tokens = max_calls
        self.lock = threading.Lock()
        self.updated_at = time.monotonic()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.updated_at
        # Add tokens proportional to elapsed time
        new_tokens = (elapsed / self.period) * self.max_calls
        if new_tokens >= 1:
            self.tokens = min(self.max_calls, self.tokens + int(new_tokens))
            self.updated_at = now

    def acquire(self) -> None:
        """Acquire a token, blocking until one is available."""
        while True:
            with self.lock:
                self._refill()
                if self.tokens > 0:
                    self.tokens -= 1
                    return
            time.sleep(0.05)
