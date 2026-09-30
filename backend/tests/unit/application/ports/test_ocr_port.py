import pytest
from pydantic import ValidationError

from cms_planner.application.ports.ocr_types import OcrFailure, OcrPageRequest, OcrSuccess
from cms_planner.domain.page import PageClassification, PageRoute, PageRouteReason
from cms_planner.domain.text_span import BoundingBox, TextSpan


def test_ocr_request_requires_ocr_classification() -> None:
    classification = PageClassification(
        page_number=1,
        route=PageRoute.NATIVE_TEXT,
        reason=PageRouteReason.COMPLETE_NATIVE_TEXT,
    )

    with pytest.raises(ValidationError):
        OcrPageRequest(classification=classification, page_bytes=b"page")


def test_ocr_success_requires_matching_coordinate_bearing_spans() -> None:
    result = OcrSuccess(
        page_number=2,
        spans=(
            TextSpan(
                page_number=2,
                text="Raw OCR text",
                coordinates=BoundingBox(x=1, y=2, width=3, height=4),
            ),
        ),
    )

    assert result.spans[0].text == "Raw OCR text"


def test_ocr_failure_cannot_contain_confirmed_content() -> None:
    with pytest.raises(ValidationError):
        OcrFailure(page_number=2, code="provider-failed", content="unsafe")