"""Server-owned inactivity deadlines serialized with case activity."""

from collections.abc import Callable, Generator
from contextlib import contextmanager
from datetime import timedelta
from threading import RLock
from time import monotonic
from typing import TypeVar

DEFAULT_INACTIVITY_TIMEOUT = timedelta(minutes=60)
PolicyResult = TypeVar("PolicyResult")


class SessionExpiredError(Exception):
    """Report activity attempted at or after the inactivity deadline."""


class InactivityPolicy:
    """Own monotonic deadlines and serialize activity against expiration."""

    def __init__(
        self,
        timeout: timedelta = DEFAULT_INACTIVITY_TIMEOUT,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        if timeout.total_seconds() <= 0:
            raise ValueError("inactivity timeout must be positive")
        self._timeout_seconds = timeout.total_seconds()
        self._clock = clock
        self._deadlines: dict[str, float] = {}
        self._lock = RLock()

    def start(self, session_id: str) -> None:
        with self._lock:
            self._deadlines[session_id] = self._clock() + self._timeout_seconds

    @contextmanager
    def activity(self, session_id: str) -> Generator[None]:
        with self._lock:
            now = self._clock()
            deadline = self._deadlines.get(session_id)
            if deadline is None or now >= deadline:
                raise SessionExpiredError(session_id)
            yield
            self._deadlines[session_id] = self._clock() + self._timeout_seconds

    def remaining_seconds(self, session_id: str) -> int:
        with self._lock:
            deadline = self._deadlines.get(session_id)
            if deadline is None:
                raise KeyError(session_id)
            return max(0, int(deadline - self._clock()))

    def expire_if_due(
        self,
        session_id: str,
        cleanup: Callable[[], PolicyResult],
    ) -> PolicyResult | None:
        with self._lock:
            deadline = self._deadlines.get(session_id)
            if deadline is None or self._clock() < deadline:
                return None
            result = cleanup()
            if getattr(result, "outcome", None) == "completed":
                del self._deadlines[session_id]
            return result