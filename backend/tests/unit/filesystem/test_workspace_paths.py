from pathlib import Path

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from application.services.stream_upload import StreamUpload


def test_client_filename_never_controls_workspace_or_file_path(tmp_path: Path) -> None:
    workspace = TemporaryWorkspace(tmp_path)
    service = StreamUpload(workspace)
    client_filename = "../../outside/claim.pdf"

    metadata = service.execute(
        session_id="session-1",
        client_filename=client_filename,
        chunks=[b"claim"],
    )

    stored_files = [path for path in tmp_path.rglob("*") if path.is_file()]
    assert metadata.client_filename == client_filename
    assert len(stored_files) == 1
    assert all("claim.pdf" not in str(path) for path in stored_files)
    assert stored_files[0].parent.parent == tmp_path


def test_sessions_receive_distinct_randomized_workspaces(tmp_path: Path) -> None:
    workspace = TemporaryWorkspace(tmp_path)
    service = StreamUpload(workspace)

    service.execute(session_id="session-1", client_filename="a.pdf", chunks=[b"a"])
    service.execute(session_id="session-2", client_filename="a.pdf", chunks=[b"b"])

    directories = [path for path in tmp_path.iterdir() if path.is_dir()]
    assert len(directories) == 2
    assert directories[0].name != directories[1].name