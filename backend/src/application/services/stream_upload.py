"""Application service for safe streamed uploads."""

from collections.abc import Callable, Iterable

from application.intake.commands import UploadLimits
from application.intake.errors import ByteLimitExceededError
from application.ports.workspace import Workspace
from domain.documents.upload_metadata import UploadMetadata

UploadValidator = Callable[[UploadMetadata], bool]


class StreamUpload:
    """Stream bytes to an adapter-owned path and clean every failed upload."""

    def __init__(
        self,
        workspace: Workspace,
        limits: UploadLimits = UploadLimits(),
    ) -> None:
        self._workspace = workspace
        self._limits = limits

    def execute(
        self,
        *,
        session_id: str,
        client_filename: str,
        chunks: Iterable[bytes],
        validator: UploadValidator | None = None,
    ) -> UploadMetadata:
        handle = self._workspace.begin_upload(session_id)
        size_bytes = 0
        try:
            for chunk in chunks:
                if not isinstance(chunk, bytes):
                    raise TypeError("upload chunks must be bytes")
                size_bytes += len(chunk)
                if size_bytes > self._limits.max_bytes:
                    raise ByteLimitExceededError(self._limits.max_bytes)
                self._workspace.write(handle, chunk)

            metadata = UploadMetadata(
                client_filename=client_filename,
                upload_id=handle.upload_id,
                size_bytes=size_bytes,
            )
            if validator is not None and not validator(metadata):
                raise ValueError("upload validation failed")
            stored_size = self._workspace.complete(handle)
            return metadata.model_copy(update={"size_bytes": stored_size})
        except Exception:
            self._workspace.discard(handle)
            raise