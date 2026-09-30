from pathlib import Path

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from application.services.cleanup_case import CleanupCase
from application.services.cleanup_errors import CleanupStore
from application.services.stream_upload import StreamUpload
from domain.case.aggregate import CaseAggregate


def test_repeated_cleanup_converges_on_completed_zero_residue(tmp_path: Path) -> None:
    repository = InMemoryCaseRepository()
    workspace = TemporaryWorkspace(tmp_path)
    repository.add(CaseAggregate(session_id="session-1", case_id="case-1"))
    StreamUpload(workspace).execute(
        session_id="session-1",
        client_filename="claim.pdf",
        chunks=[b"content"],
    )
    cleanup = CleanupCase(repository, workspace)

    first = cleanup.execute("session-1")
    repeated = cleanup.execute("session-1")

    assert first.outcome == "completed"
    assert repeated.outcome == "completed"
    assert repeated.remaining_files == 0
    assert not repository.contains("session-1")
    assert not workspace.exists("session-1")


def test_cleanup_converges_after_aggregate_was_already_removed(tmp_path: Path) -> None:
    repository = InMemoryCaseRepository()
    workspace = TemporaryWorkspace(tmp_path)
    StreamUpload(workspace).execute(
        session_id="session-1",
        client_filename="claim.pdf",
        chunks=[b"content"],
    )

    status = CleanupCase(repository, workspace).execute("session-1")

    assert status.outcome == "completed"
    assert status.remaining_files == 0


class FailingRepository(InMemoryCaseRepository):
    def remove(self, session_id: str) -> bool:
        raise OSError("sensitive repository detail")


def test_store_failure_reports_failed_after_attempting_workspace_cleanup(
    tmp_path: Path,
) -> None:
    repository = FailingRepository()
    workspace = TemporaryWorkspace(tmp_path)
    repository.add(CaseAggregate(session_id="session-1", case_id="case-1"))
    StreamUpload(workspace).execute(
        session_id="session-1",
        client_filename="secret-document.pdf",
        chunks=[b"secret content"],
    )

    status = CleanupCase(repository, workspace).execute("session-1")

    assert status.outcome == "failed"
    assert status.remaining_files == 0
    assert status.failed_stores == (CleanupStore.CASE_MEMORY,)
    assert not workspace.exists("session-1")
    assert "sensitive" not in status.model_dump_json()
    assert "secret" not in status.model_dump_json()