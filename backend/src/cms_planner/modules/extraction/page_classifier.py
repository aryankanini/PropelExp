"""Classify page extraction routes before content extraction begins."""

from collections.abc import Iterable

from cms_planner.domain.page import (
    PageClassification,
    PageRoute,
    PageRouteReason,
    SourcePage,
)


def classify_pages(pages: Iterable[SourcePage]) -> tuple[PageClassification, ...]:
    """Classify every page in source order and retain the routing reason."""
    return tuple(_classify_page(page) for page in pages)


def _classify_page(page: SourcePage) -> PageClassification:
    if not any(character.isalnum() for character in page.native_text):
        route = PageRoute.OCR_REQUIRED
        reason = PageRouteReason.NO_SUBSTANTIVE_TEXT
    elif not page.native_text_complete:
        route = PageRoute.OCR_REQUIRED
        reason = PageRouteReason.INCOMPLETE_NATIVE_TEXT
    else:
        route = PageRoute.NATIVE_TEXT
        reason = PageRouteReason.COMPLETE_NATIVE_TEXT

    return PageClassification(
        page_number=page.page_number,
        route=route,
        reason=reason,
    )