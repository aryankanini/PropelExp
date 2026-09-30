import pytest
from pydantic import ValidationError

from cms_planner.adapters.filesystem.native_text_extractor import extract_native_text
from cms_planner.domain.page import PageClassification, PageRoute, PageRouteReason
from cms_planner.domain.text_span import BoundingBox, ClassifiedPageText, TextSpan


def classification(page_number: int, route: PageRoute) -> PageClassification:
    reason = (
        PageRouteReason.COMPLETE_NATIVE_TEXT
        if route is PageRoute.NATIVE_TEXT
        else PageRouteReason.INCOMPLETE_NATIVE_TEXT
    )
    return PageClassification(page_number=page_number, route=route, reason=reason)


def span(page_number: int, text: str) -> TextSpan:
    return TextSpan(
        page_number=page_number,
        text=text,
        coordinates=BoundingBox(x=10, y=20, width=30, height=40),
    )


def test_extracts_only_native_pages_with_coordinates_in_source_order() -> None:
    pages = (
        ClassifiedPageText(
            classification=classification(2, PageRoute.NATIVE_TEXT),
            spans=(span(2, "First"), span(2, "Second")),
        ),
        ClassifiedPageText(
            classification=classification(3, PageRoute.OCR_REQUIRED),
            spans=(span(3, "Unconfirmed"),),
        ),
        ClassifiedPageText(
            classification=classification(5, PageRoute.NATIVE_TEXT),
            spans=(span(5, "Third"),),
        ),
    )

    result = extract_native_text(pages)

    assert [item.text for item in result.native_spans] == ["First", "Second", "Third"]
    assert result.native_spans[0].coordinates == BoundingBox(
        x=10,
        y=20,
        width=30,
        height=40,
    )
    assert [item.page_number for item in result.ocr_required] == [3]


def test_rejects_spans_that_do_not_match_the_classified_page() -> None:
    with pytest.raises(ValidationError):
        ClassifiedPageText(
            classification=classification(1, PageRoute.NATIVE_TEXT),
            spans=(span(2, "Wrong page"),),
        )