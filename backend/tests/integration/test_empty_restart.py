from pathlib import Path

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from application.services.stream_upload import StreamUpload
from domain.case.aggregate import CaseAggregate


def test_restart_recovers_no_case_memory_or_workspace_files(tmp_path: Path) -> None:
    repository = InMemoryCaseRepository()
    workspace = TemporaryWorkspace(tmp_path)
    repository.add(CaseAggregate(session_id="session-1", case_id="case-1"))
    StreamUpload(workspace).execute(
        session_id="session-1",
        client_filename="claim.pdf",
        chunks=[b"content"],
    )

    restarted_repository = InMemoryCaseRepository()
    restarted_workspace = TemporaryWorkspace(tmp_path)

    assert restarted_repository.get("session-1") is None
    assert not restarted_workspace.exists("session-1")
    assert list(tmp_path.rglob("*")) == []