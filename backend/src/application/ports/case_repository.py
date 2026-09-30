"""Application-owned port for transient case persistence."""

from collections.abc import Callable
from typing import Literal, Protocol, TypeVar

from domain.case.aggregate import CaseAggregate

UpdateResult = TypeVar("UpdateResult")


class CaseRepository(Protocol):
    """Define the sole persistence boundary for active case aggregates."""

    @property
    def storage_kind(self) -> Literal["memory"]: ...

    def add(self, aggregate: CaseAggregate) -> None: ...

    def get(self, session_id: str) -> CaseAggregate | None: ...

    def save(self, aggregate: CaseAggregate) -> None: ...

    def update(
        self,
        session_id: str,
        updater: Callable[[CaseAggregate], tuple[CaseAggregate, UpdateResult]],
    ) -> UpdateResult: ...

    def remove(self, session_id: str) -> bool: ...

    def contains(self, session_id: str) -> bool: ...

    def list_session_ids(self) -> tuple[str, ...]: ...