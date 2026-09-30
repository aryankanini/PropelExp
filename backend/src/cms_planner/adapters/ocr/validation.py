"""Validate provider OCR output against the requested page identity."""

from cms_planner.application.ports.ocr_types import OcrPageRequest, OcrSuccess


def validate_ocr_success(
    request: OcrPageRequest,
    response: OcrSuccess,
) -> OcrSuccess:
    """Reject a structurally valid response for the wrong page."""
    if response.page_number != request.classification.page_number:
        raise ValueError("OCR response page does not match the request")
    return response