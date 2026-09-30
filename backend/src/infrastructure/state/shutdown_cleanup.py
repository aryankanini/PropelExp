"""Graceful-shutdown cleanup for every active transient session."""

from application.ports.case_repository import CaseRepository
from application.ports.workspace import Workspace
from application.services.cleanup_case import CleanupCase
from domain.lifecycle.cleanup_status import CleanupStatus


class ShutdownCleanup:
    """Run the shared idempotent cleanup across all known session IDs."""

    def __init__(
        self,
        repository: CaseRepository,
        workspace: Workspace,
        cleanup: CleanupCase,
    ) -> None:
        self._repository = repository
        self._workspace = workspace
        self._cleanup = cleanup

    def execute(self) -> dict[str, CleanupStatus]:
        session_ids = set(self._repository.list_session_ids())
        session_ids.update(self._workspace.list_session_ids())
        return {
            session_id: self._cleanup.execute(session_id)
            for session_id in sorted(session_ids)
        }