from pathlib import Path

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from application.services.cleanup_case import CleanupCase
from application.services.stream_upload import StreamUpload
from domain.case.aggregate import CaseAggregate
from infrastructure.state.shutdown_cleanup import ShutdownCleanup


def test_shutdown_cleans_every_active_case_and_workspace(tmp_path: Path) -> None:
    repository = InMemoryCaseRepository()
    workspace = TemporaryWorkspace(tmp_path)
    for index in range(2):
        session_id = f"session-{index}"
        repository.add(CaseAggregate(session_id=session_id, case_id=f"case-{index}"))
        StreamUpload(workspace).execute(
            session_id=session_id,
            client_filename="case.pdf",
            chunks=[b"content"],
        )
    cleanup = CleanupCase(repository, workspace)

    results = ShutdownCleanup(repository, workspace, cleanup).execute()

    assert set(results) == {"session-0", "session-1"}
    assert all(status.outcome == "completed" for status in results.values())
    assert repository.list_session_ids() == ()
    assert workspace.list_session_ids() == ()