import pytest

from application.intake.commands import UploadLimits
from application.intake.errors import (
    ActiveUploadExistsError,
    PageLimitExceededError,
    UnsupportedMediaTypeError,
)
from application.intake.preflight import DocumentInspection, validate_preflight
from application.intake.upload_guard import UploadGuard


def test_supported_document_at_page_limit_is_accepted() -> None:
    inspection = DocumentInspection(page_texts=("page", "page"))

    validate_preflight(
        "application/pdf",
        inspection,
        UploadLimits(max_bytes=1, max_pages=2),
    )


def test_document_over_page_limit_is_rejected() -> None:
    inspection = DocumentInspection(page_texts=("page", "page", "page"))

    with pytest.raises(PageLimitExceededError):
        validate_preflight(
            "application/pdf",
            inspection,
            UploadLimits(max_bytes=1, max_pages=2),
        )


def test_unsupported_media_type_is_rejected() -> None:
    with pytest.raises(UnsupportedMediaTypeError):
        validate_preflight(
            "text/plain",
            DocumentInspection(page_texts=("page",)),
        )


def test_second_concurrent_upload_is_rejected() -> None:
    guard = UploadGuard()

    with guard.reserve("session-1"):
        with pytest.raises(ActiveUploadExistsError):
            with guard.reserve("session-1"):
                pass

    with guard.reserve("session-1"):
        pass