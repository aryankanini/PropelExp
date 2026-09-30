from pathlib import Path

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from application.intake.commands import UploadCommand, UploadLimits
from application.intake.preflight import DocumentInspection
from application.intake.upload_guard import UploadGuard
from application.intake.upload_service import UploadService
from application.ports.workspace import UploadHandle


class StubInspector:
    def __init__(self, inspection: DocumentInspection) -> None:
        self.inspection = inspection

    def inspect(
        self,
        _handle: UploadHandle,
        _media_type: str,
        _max_pages: int,
    ) -> DocumentInspection:
        return self.inspection


def command() -> UploadCommand:
    return UploadCommand(
        session_id="session-1",
        client_filename="cms-2567.pdf",
        media_type="application/pdf",
    )


def test_valid_upload_creates_extraction_ready_case(tmp_path: Path) -> None:
    repository = InMemoryCaseRepository()
    workspace = TemporaryWorkspace(tmp_path)
    inspector = StubInspector(
        DocumentInspection(
            page_texts=(
                "CMS-2567 Statement of Deficiencies and Plan of Correction",
            )
        )
    )
    service = UploadService(
        repository,
        workspace,
        inspector,
        UploadGuard(),
        UploadLimits(max_bytes=10, max_pages=1),
    )

    result = service.execute(command(), [b"content"])

    assert result.status == "extraction_ready"
    assert repository.contains("session-1")
    assert workspace.count_files("session-1") == 1


def test_invalid_document_leaves_no_case_or_file(tmp_path: Path) -> None:
    repository = InMemoryCaseRepository()
    workspace = TemporaryWorkspace(tmp_path)
    service = UploadService(
        repository,
        workspace,
        StubInspector(DocumentInspection(page_texts=("Unrelated report",))),
        UploadGuard(),
    )

    result = service.execute(command(), [b"content"])

    assert result.status == "rejected"
    assert result.reason == "not_cms2567"
    assert not repository.contains("session-1")
    assert not workspace.exists("session-1")