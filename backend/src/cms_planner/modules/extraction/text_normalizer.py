"""Normalize extracted text while preserving evidence coordinates."""

import re
import unicodedata

from cms_planner.application.ports.ocr_types import OcrFailure
from cms_planner.domain.page import PageClassification, PageRoute, PageRouteReason
from cms_planner.domain.text_span import ClassifiedPageText, TextSpan

_ENCODING_ARTIFACTS = str.maketrans("", "", "\ufeff\u200b\ufffd")
_HORIZONTAL_WHITESPACE = re.compile(r"[^\S\n]+")
_SPACE_AROUND_LINE_BREAK = re.compile(r" *\n *")
_EXCESS_LINE_BREAKS = re.compile(r"\n{3,}")


def normalize_extracted_page(
    page: ClassifiedPageText | OcrFailure,
) -> ClassifiedPageText | OcrFailure:
    """Normalize successful spans and leave content-free OCR failures unchanged."""
    if isinstance(page, OcrFailure):
        return page

    normalized_spans = tuple(_normalize_span(span) for span in page.spans)
    if page.classification.route is PageRoute.NATIVE_TEXT and not _has_content(
        normalized_spans
    ):
        return ClassifiedPageText(
            classification=PageClassification(
                page_number=page.classification.page_number,
                route=PageRoute.OCR_REQUIRED,
                reason=PageRouteReason.NO_SUBSTANTIVE_TEXT,
            ),
            spans=(),
        )

    return ClassifiedPageText(
        classification=page.classification,
        spans=normalized_spans,
    )


def _normalize_span(span: TextSpan) -> TextSpan:
    text = unicodedata.normalize("NFC", span.text)
    text = text.translate(_ENCODING_ARTIFACTS)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _HORIZONTAL_WHITESPACE.sub(" ", text)
    text = _SPACE_AROUND_LINE_BREAK.sub("\n", text)
    text = _EXCESS_LINE_BREAKS.sub("\n\n", text).strip()
    return TextSpan(
        page_number=span.page_number,
        text=text,
        coordinates=span.coordinates,
    )


def _has_content(spans: tuple[TextSpan, ...]) -> bool:
    return any(character.isalnum() for span in spans for character in span.text)