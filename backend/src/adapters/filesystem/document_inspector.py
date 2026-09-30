"""Local PDF and image inspection for bounded temporary uploads."""

import pymupdf

from application.intake.errors import (
    PageLimitExceededError,
    UnreadableDocumentError,
)
from application.intake.preflight import DocumentInspection
from application.ports.workspace import UploadHandle, Workspace


class FilesystemDocumentInspector:
    """Count pages before extracting local text or running local OCR."""

    def __init__(self, workspace: Workspace) -> None:
        self._workspace = workspace

    def inspect(
        self,
        handle: UploadHandle,
        media_type: str,
        max_pages: int,
    ) -> DocumentInspection:
        try:
            with self._workspace.open_read(handle) as stored:
                content = stored.read()
            if media_type.lower() == "application/pdf":
                return self._inspect_document(content, "pdf", max_pages)
            image_type = media_type.lower().removeprefix("image/")
            return self._inspect_document(content, image_type, max_pages)
        except (OSError, RuntimeError, ValueError) as error:
            raise UnreadableDocumentError() from error

    def _inspect_document(
        self,
        content: bytes,
        file_type: str,
        max_pages: int,
    ) -> DocumentInspection:
        with pymupdf.open(stream=content, filetype=file_type) as document:
            if document.page_count > max_pages:
                raise PageLimitExceededError(max_pages)
            page_texts = tuple(self._read_page(page) for page in document)
        return DocumentInspection(page_texts=page_texts)

    def _read_page(self, page: pymupdf.Page) -> str | None:
        native_text = page.get_text("text").strip()
        if native_text:
            return native_text
        text_page = page.get_textpage_ocr(dpi=150, full=True)
        return page.get_text("text", textpage=text_page).strip() or None