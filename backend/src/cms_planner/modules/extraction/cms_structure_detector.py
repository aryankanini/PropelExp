"""Deterministically recognize supported CMS-2567 document structure."""

import re
from collections.abc import Iterable

from cms_planner.domain.cms_layout import (
    CmsLayout,
    CmsLayoutPattern,
    CmsLayoutStatus,
)
from cms_planner.domain.text_span import ClassifiedPageText

_WHITESPACE = re.compile(r"\s+")
_FORM_MARKER = re.compile(r"\bFORM\s+CMS[\s\-\u2010-\u2015]*2567\b")
_TITLE_MARKER = "STATEMENT OF DEFICIENCIES AND PLAN OF CORRECTION"
_PROVIDER_MARKER = "PROVIDER/SUPPLIER/CLIA IDENTIFICATION NUMBER"
_TAG_COLUMN_MARKER = "ID PREFIX TAG"
_CMS_AGENCY_MARKER = "CENTERS FOR MEDICARE & MEDICAID SERVICES"


def detect_cms_layout(pages: Iterable[ClassifiedPageText]) -> CmsLayout:
    """Return retained CMS-2567 layout state for ordered normalized pages."""
    ordered_pages = tuple(pages)
    texts = tuple(_page_text(page) for page in ordered_pages)
    document_text = "\n".join(texts)
    recognized = _FORM_MARKER.search(document_text) is not None or (
        _TITLE_MARKER in document_text
        and _TAG_COLUMN_MARKER in document_text
        and (
            _PROVIDER_MARKER in document_text
            or _CMS_AGENCY_MARKER in document_text
        )
    )
    if not recognized:
        return CmsLayout(status=CmsLayoutStatus.UNRECOGNIZED)

    marker_pages = tuple(
        page.page_number
        for page, text in zip(ordered_pages, texts, strict=True)
        if _FORM_MARKER.search(text) is not None
        or any(marker in text for marker in _structural_markers())
    )
    return CmsLayout(
        status=CmsLayoutStatus.RECOGNIZED,
        pattern=CmsLayoutPattern.CMS_2567,
        marker_page_numbers=marker_pages,
    )


def _page_text(page: ClassifiedPageText) -> str:
    combined = "\n".join(span.text for span in page.spans)
    return _WHITESPACE.sub(" ", combined).upper()


def _structural_markers() -> tuple[str, ...]:
    return (
        _TITLE_MARKER,
        _PROVIDER_MARKER,
        _TAG_COLUMN_MARKER,
        _CMS_AGENCY_MARKER,
    )