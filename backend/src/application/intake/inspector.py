"""Application-owned contract for local document inspection."""

from typing import Protocol

from application.intake.preflight import DocumentInspection
from application.ports.workspace import UploadHandle


class DocumentInspector(Protocol):
    """Inspect bounded stored content without invoking remote providers."""

    def inspect(
        self,
        handle: UploadHandle,
        media_type: str,
        max_pages: int,
    ) -> DocumentInspection: ...