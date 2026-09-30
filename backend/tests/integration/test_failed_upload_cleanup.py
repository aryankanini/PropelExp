from collections.abc import Iterator
from pathlib import Path

import pytest

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from application.services.stream_upload import StreamUpload


def failing_chunks() -> Iterator[bytes]:
    yield b"partial"
    raise OSError("stream interrupted")


def test_stream_failure_removes_partial_file_and_workspace(tmp_path: Path) -> None:
    workspace = TemporaryWorkspace(tmp_path)
    service = StreamUpload(workspace)

    with pytest.raises(OSError):
        service.execute(
            session_id="session-1",
            client_filename="../../claim.pdf",
            chunks=failing_chunks(),
        )

    assert list(tmp_path.rglob("*")) == []
    assert not workspace.exists("session-1")


def test_validation_failure_removes_partial_file_and_workspace(tmp_path: Path) -> None:
    workspace = TemporaryWorkspace(tmp_path)
    service = StreamUpload(workspace)

    with pytest.raises(ValueError, match="validation failed"):
        service.execute(
            session_id="session-1",
            client_filename="claim.pdf",
            chunks=[b"invalid"],
            validator=lambda metadata: False,
        )

    assert list(tmp_path.rglob("*")) == []
    assert workspace.count_files("session-1") == 0