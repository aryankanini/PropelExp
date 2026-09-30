"""Application-owned document media and page preflight."""

from dataclasses import dataclass

from application.intake.commands import UploadLimits
from application.intake.errors import (
    PageLimitExceededError,
    UnsupportedMediaTypeError,
)

SUPPORTED_MEDIA_TYPES = frozenset(
    {
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/tiff",
    }
)


@dataclass(frozen=True)
class DocumentInspection:
    """Describe locally inspected pages without retaining document bytes."""

    page_texts: tuple[str | None, ...]

    @property
    def page_count(self) -> int:
        return len(self.page_texts)


def validate_preflight(
    media_type: str,
    inspection: DocumentInspection,
    limits: UploadLimits = UploadLimits(),
) -> None:
    """Reject unsupported media and documents outside the page boundary."""
    validate_media_type(media_type)
    if inspection.page_count == 0:
        raise UnsupportedMediaTypeError(media_type)
    if inspection.page_count > limits.max_pages:
        raise PageLimitExceededError(limits.max_pages)


def validate_media_type(media_type: str) -> None:
    """Reject declared media outside the supported intake contract."""
    if media_type.lower() not in SUPPORTED_MEDIA_TYPES:
        raise UnsupportedMediaTypeError(media_type)