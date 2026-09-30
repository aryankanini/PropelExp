from pathlib import Path

import pytest

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from application.intake.commands import UploadLimits
from application.intake.errors import ByteLimitExceededError
from application.ports.workspace import UploadHandle
from application.services.stream_upload import StreamUpload


def test_upload_at_byte_limit_is_retained(tmp_path: Path) -> None:
    workspace = TemporaryWorkspace(tmp_path)
    service = StreamUpload(workspace, UploadLimits(max_bytes=4, max_pages=1))

    metadata = service.execute(
        session_id="session-1",
        client_filename="cms-2567.pdf",
        chunks=[b"12", b"34"],
    )

    assert metadata.size_bytes == 4
    assert workspace.count_files("session-1") == 1


def test_upload_over_byte_limit_removes_partial_file(tmp_path: Path) -> None:
    workspace = TemporaryWorkspace(tmp_path)
    service = StreamUpload(workspace, UploadLimits(max_bytes=4, max_pages=1))

    with pytest.raises(ByteLimitExceededError):
        service.execute(
            session_id="session-1",
            client_filename="cms-2567.pdf",
            chunks=[b"1234", b"5"],
        )

    assert workspace.count_files("session-1") == 0
    assert not workspace.exists("session-1")


def test_completed_upload_can_be_read_and_discarded(tmp_path: Path) -> None:
    workspace = TemporaryWorkspace(tmp_path)
    metadata = StreamUpload(workspace).execute(
        session_id="session-1",
        client_filename="cms-2567.pdf",
        chunks=[b"content"],
    )
    handle = UploadHandle("session-1", metadata.upload_id)

    with workspace.open_read(handle) as stored:
        assert stored.read() == b"content"
    workspace.discard(handle)

    assert not workspace.exists("session-1")