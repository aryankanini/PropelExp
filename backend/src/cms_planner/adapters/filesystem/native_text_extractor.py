"""Select classified native text without invoking an OCR provider."""

from collections.abc import Iterable

from pydantic import BaseModel, ConfigDict

from cms_planner.domain.page import PageClassification, PageRoute
from cms_planner.domain.text_span import ClassifiedPageText, TextSpan


class NativeTextExtraction(BaseModel):
    """Separate confirmed native spans from pages awaiting OCR."""

    model_config = ConfigDict(frozen=True, strict=True)

    native_spans: tuple[TextSpan, ...]
    ocr_required: tuple[PageClassification, ...]


def extract_native_text(
    pages: Iterable[ClassifiedPageText],
) -> NativeTextExtraction:
    """Return native spans and OCR routes while preserving source order."""
    native_spans: list[TextSpan] = []
    ocr_required: list[PageClassification] = []

    for page in pages:
        if page.classification.route is PageRoute.NATIVE_TEXT:
            native_spans.extend(page.spans)
        else:
            ocr_required.append(page.classification)

    return NativeTextExtraction(
        native_spans=tuple(native_spans),
        ocr_required=tuple(ocr_required),
    )