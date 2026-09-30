"""Application-owned port for session temporary workspaces."""

from dataclasses import dataclass
from typing import BinaryIO, Literal, Protocol


@dataclass(frozen=True)
class UploadHandle:
    """Identify an adapter-owned upload without exposing its path."""

    session_id: str
    upload_id: str


class Workspace(Protocol):
    """Define temporary upload and lifecycle operations."""

    @property
    def storage_kind(self) -> Literal["temporary"]: ...

    def begin_upload(self, session_id: str) -> UploadHandle: ...

    def write(self, handle: UploadHandle, chunk: bytes) -> None: ...

    def complete(self, handle: UploadHandle) -> int: ...

    def open_read(self, handle: UploadHandle) -> BinaryIO: ...

    def discard(self, handle: UploadHandle) -> None: ...

    def remove(self, session_id: str) -> None: ...

    def count_files(self, session_id: str) -> int: ...

    def exists(self, session_id: str) -> bool: ...

    def list_session_ids(self) -> tuple[str, ...]: ...