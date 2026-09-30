"""Randomized filesystem adapter for temporary session uploads."""

import secrets
import shutil
from dataclasses import dataclass
from pathlib import Path
from threading import RLock
from typing import BinaryIO
from uuid import uuid4

from application.ports.workspace import UploadHandle, Workspace


@dataclass
class _ActiveUpload:
    path: Path
    stream: BinaryIO


class TemporaryWorkspace(Workspace):
    """Own randomized workspace and file paths beneath a configured root."""

    storage_kind = "temporary"

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()
        self._root.mkdir(parents=True, exist_ok=True)
        self._purge_root()
        self._workspaces: dict[str, Path] = {}
        self._uploads: dict[UploadHandle, _ActiveUpload] = {}
        self._stored_uploads: dict[UploadHandle, Path] = {}
        self._lock = RLock()

    def begin_upload(self, session_id: str) -> UploadHandle:
        if not session_id:
            raise ValueError("session_id must not be empty")

        with self._lock:
            workspace = self._workspaces.get(session_id)
            if workspace is None:
                workspace = self._root / secrets.token_urlsafe(24)
                workspace.mkdir()
                self._workspaces[session_id] = workspace

            handle = UploadHandle(session_id=session_id, upload_id=uuid4().hex)
            path = workspace / f"{uuid4().hex}.upload"
            self._uploads[handle] = _ActiveUpload(path=path, stream=path.open("xb"))
            return handle

    def write(self, handle: UploadHandle, chunk: bytes) -> None:
        with self._lock:
            self._uploads[handle].stream.write(chunk)

    def complete(self, handle: UploadHandle) -> int:
        with self._lock:
            active = self._uploads[handle]
            active.stream.close()
            size_bytes = active.path.stat().st_size
            del self._uploads[handle]
            self._stored_uploads[handle] = active.path
            return size_bytes

    def open_read(self, handle: UploadHandle) -> BinaryIO:
        with self._lock:
            return self._stored_uploads[handle].open("rb")

    def discard(self, handle: UploadHandle) -> None:
        with self._lock:
            active = self._uploads.pop(handle, None)
            if active is not None:
                active.stream.close()
                active.path.unlink(missing_ok=True)
            stored_path = self._stored_uploads.pop(handle, None)
            if stored_path is not None:
                stored_path.unlink(missing_ok=True)
            self._remove_empty_workspace(handle.session_id)

    def remove(self, session_id: str) -> None:
        with self._lock:
            for handle in tuple(self._uploads):
                if handle.session_id == session_id:
                    active = self._uploads.pop(handle)
                    active.stream.close()
            for handle in tuple(self._stored_uploads):
                if handle.session_id == session_id:
                    del self._stored_uploads[handle]
            workspace = self._workspaces.pop(session_id, None)
            if workspace is not None:
                shutil.rmtree(workspace, ignore_errors=False)

    def count_files(self, session_id: str) -> int:
        with self._lock:
            workspace = self._workspaces.get(session_id)
            if workspace is None or not workspace.exists():
                return 0
            return sum(path.is_file() for path in workspace.rglob("*"))

    def exists(self, session_id: str) -> bool:
        with self._lock:
            workspace = self._workspaces.get(session_id)
            return workspace is not None and workspace.exists()

    def list_session_ids(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(self._workspaces)

    def _remove_empty_workspace(self, session_id: str) -> None:
        workspace = self._workspaces.get(session_id)
        if workspace is None or any(workspace.iterdir()):
            return
        workspace.rmdir()
        del self._workspaces[session_id]

    def _purge_root(self) -> None:
        for path in self._root.iterdir():
            if path.is_symlink() or path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path, ignore_errors=False)