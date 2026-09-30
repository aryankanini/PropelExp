"""Process-memory adapter for active case aggregates."""

from collections.abc import Callable
from threading import RLock
from typing import TypeVar

from application.ports.case_repository import CaseRepository
from domain.case.aggregate import CaseAggregate
from domain.case.errors import ActiveCaseExistsError, CaseNotFoundError

UpdateResult = TypeVar("UpdateResult")


class InMemoryCaseRepository(CaseRepository):
    """Store at most one active aggregate for each session."""

    storage_kind = "memory"

    def __init__(self) -> None:
        self._aggregates: dict[str, CaseAggregate] = {}
        self._lock = RLock()

    def add(self, aggregate: CaseAggregate) -> None:
        with self._lock:
            if aggregate.session_id in self._aggregates:
                raise ActiveCaseExistsError(aggregate.session_id)
            self._aggregates[aggregate.session_id] = aggregate

    def get(self, session_id: str) -> CaseAggregate | None:
        with self._lock:
            return self._aggregates.get(session_id)

    def save(self, aggregate: CaseAggregate) -> None:
        with self._lock:
            if aggregate.session_id not in self._aggregates:
                raise CaseNotFoundError(aggregate.session_id)
            self._aggregates[aggregate.session_id] = aggregate

    def update(
        self,
        session_id: str,
        updater: Callable[[CaseAggregate], tuple[CaseAggregate, UpdateResult]],
    ) -> UpdateResult:
        with self._lock:
            current = self._aggregates.get(session_id)
            if current is None:
                raise CaseNotFoundError(session_id)
            updated, result = updater(current)
            self._aggregates[session_id] = updated
            return result

    def remove(self, session_id: str) -> bool:
        with self._lock:
            return self._aggregates.pop(session_id, None) is not None

    def contains(self, session_id: str) -> bool:
        with self._lock:
            return session_id in self._aggregates

    def list_session_ids(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(self._aggregates)