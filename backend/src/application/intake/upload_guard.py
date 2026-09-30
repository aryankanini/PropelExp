"""Atomic one-active-upload policy for each session."""

from contextlib import contextmanager
from threading import Lock
from collections.abc import Generator

from application.intake.errors import ActiveUploadExistsError


class UploadGuard:
    """Reserve one upload slot per session until intake completes."""

    def __init__(self) -> None:
        self._active_sessions: set[str] = set()
        self._lock = Lock()

    @contextmanager
    def reserve(self, session_id: str) -> Generator[None]:
        with self._lock:
            if session_id in self._active_sessions:
                raise ActiveUploadExistsError(session_id)
            self._active_sessions.add(session_id)
        try:
            yield
        finally:
            with self._lock:
                self._active_sessions.remove(session_id)