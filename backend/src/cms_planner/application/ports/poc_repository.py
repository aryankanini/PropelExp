"""Application-owned port for transient deficiency and POC state."""

from collections.abc import Callable
from typing import Literal, Protocol

from cms_planner.domain.deficiency import Deficiency
from cms_planner.domain.poc import PocDraft


class PocRepository(Protocol):
    """Atomically retain current process-memory POC drafts."""

    @property
    def storage_kind(self) -> Literal["memory"]: ...

    def add_deficiency(self, deficiency: Deficiency) -> None: ...

    def get_deficiency(self, deficiency_id: str) -> Deficiency | None: ...

    def get_draft(self, deficiency_id: str) -> PocDraft | None: ...

    def get_or_create_draft(
        self,
        deficiency_id: str,
        deficiency_revision_id: str,
        factory: Callable[[], PocDraft],
    ) -> PocDraft: ...

    def update_draft(
        self,
        deficiency_id: str,
        updater: Callable[[PocDraft], PocDraft],
    ) -> PocDraft: ...


class PocRetentionError(Exception):
    """Report that a repository could not retain an otherwise valid revision."""