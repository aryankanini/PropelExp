"""Locked process-memory storage for confirmed deficiencies and POC drafts."""

from collections.abc import Callable
from threading import RLock

from cms_planner.application.ports.poc_repository import PocRepository
from cms_planner.domain.deficiency import Deficiency
from cms_planner.domain.poc import PocDraft


class InMemoryPocRepository(PocRepository):
    """Apply draft creation and revision updates atomically in process memory."""

    storage_kind = "memory"

    def __init__(self) -> None:
        self._deficiencies: dict[str, Deficiency] = {}
        self._drafts: dict[str, PocDraft] = {}
        self._lock = RLock()

    def add_deficiency(self, deficiency: Deficiency) -> None:
        with self._lock:
            self._deficiencies[deficiency.deficiency_id] = deficiency

    def get_deficiency(self, deficiency_id: str) -> Deficiency | None:
        with self._lock:
            return self._deficiencies.get(deficiency_id)

    def get_draft(self, deficiency_id: str) -> PocDraft | None:
        with self._lock:
            return self._drafts.get(deficiency_id)

    def get_or_create_draft(
        self,
        deficiency_id: str,
        deficiency_revision_id: str,
        factory: Callable[[], PocDraft],
    ) -> PocDraft:
        with self._lock:
            current = self._drafts.get(deficiency_id)
            if (
                current is not None
                and current.current_revision.deficiency_revision_id
                == deficiency_revision_id
            ):
                return current
            created = factory()
            if created.current_revision.deficiency_revision_id != deficiency_revision_id:
                raise ValueError("draft revision does not match the idempotency boundary")
            self._drafts[deficiency_id] = created
            return created

    def update_draft(
        self,
        deficiency_id: str,
        updater: Callable[[PocDraft], PocDraft],
    ) -> PocDraft:
        with self._lock:
            current = self._drafts.get(deficiency_id)
            if current is None:
                raise KeyError(deficiency_id)
            updated = updater(current)
            self._drafts[deficiency_id] = updated
            return updated