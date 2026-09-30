"""Application-owned provider-neutral OCR port."""

from typing import Protocol

from cms_planner.application.ports.ocr_types import OcrPageRequest, OcrResult


class OcrPort(Protocol):
    """Recognize one classified page through a replaceable adapter."""

    async def recognize(self, request: OcrPageRequest) -> OcrResult: ...