"""Lifecycle service for convergent transient case cleanup."""

from application.ports.case_repository import CaseRepository
from application.ports.workspace import Workspace
from application.services.cleanup_errors import CleanupStore
from domain.lifecycle.cleanup_status import CleanupStatus


class CleanupCase:
    """Remove case memory and files, then report their verified state."""

    def __init__(self, repository: CaseRepository, workspace: Workspace) -> None:
        self._repository = repository
        self._workspace = workspace

    def execute(self, session_id: str) -> CleanupStatus:
        failures: list[CleanupStore] = []

        try:
            self._workspace.remove(session_id)
        except Exception:
            failures.append(CleanupStore.WORKSPACE)

        workspace_absent = self._workspace_is_absent(session_id, failures)
        remaining_files = self._count_remaining_files(session_id, failures)
        if workspace_absent and remaining_files == 0:
            try:
                self._repository.remove(session_id)
            except Exception:
                failures.append(CleanupStore.CASE_MEMORY)

        aggregate_absent = self._aggregate_is_absent(session_id, failures)
        unique_failures = tuple(dict.fromkeys(failures))

        if (
            not unique_failures
            and aggregate_absent
            and workspace_absent
            and remaining_files == 0
        ):
            return CleanupStatus(outcome="completed", remaining_files=0)
        return CleanupStatus(
            outcome="failed",
            remaining_files=remaining_files,
            failed_stores=tuple(store.value for store in unique_failures),
        )

    def _aggregate_is_absent(
        self, session_id: str, failures: list[CleanupStore]
    ) -> bool:
        try:
            return not self._repository.contains(session_id)
        except Exception:
            failures.append(CleanupStore.CASE_MEMORY)
            return False

    def _workspace_is_absent(
        self, session_id: str, failures: list[CleanupStore]
    ) -> bool:
        try:
            return not self._workspace.exists(session_id)
        except Exception:
            failures.append(CleanupStore.WORKSPACE)
            return False

    def _count_remaining_files(
        self, session_id: str, failures: list[CleanupStore]
    ) -> int | None:
        try:
            return self._workspace.count_files(session_id)
        except Exception:
            failures.append(CleanupStore.WORKSPACE)
            return None