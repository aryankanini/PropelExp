from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from application.services.cleanup_case import CleanupCase
from application.services.stream_upload import StreamUpload
from cms_planner.api.routes.case_lifecycle import create_case_lifecycle_router
from domain.case.aggregate import CaseAggregate


class FailingWorkspace(TemporaryWorkspace):
    def remove(self, session_id: str) -> None:
        raise OSError("protected file detail")


def test_cleanup_failure_retains_case_and_allows_retry(tmp_path: Path) -> None:
    repository = InMemoryCaseRepository()
    workspace = FailingWorkspace(tmp_path)
    aggregate = CaseAggregate(session_id="session-1", case_id="case-1")
    repository.add(aggregate)
    StreamUpload(workspace).execute(
        session_id="session-1",
        client_filename="secret.pdf",
        chunks=[b"protected content"],
    )
    app = FastAPI()
    app.include_router(
        create_case_lifecycle_router(repository, CleanupCase(repository, workspace))
    )
    client = TestClient(app)

    first = client.delete(
        "/api/v1/cases/case-1",
        headers={"X-Session-ID": "session-1"},
    )
    retried = client.delete(
        "/api/v1/cases/case-1",
        headers={"X-Session-ID": "session-1"},
    )

    assert first.status_code == 503
    assert retried.status_code == 503
    assert repository.get("session-1") == aggregate
    assert workspace.count_files("session-1") == 1
    assert "protected" not in first.text
    assert "secret" not in first.text