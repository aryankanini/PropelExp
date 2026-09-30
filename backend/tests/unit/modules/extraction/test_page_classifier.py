from cms_planner.domain.page import PageRoute, PageRouteReason, SourcePage
from cms_planner.modules.extraction.page_classifier import classify_pages


def test_complete_native_text_stays_on_native_route() -> None:
    page = SourcePage(page_number=1, native_text="Provider: North Clinic", native_text_complete=True)

    result = classify_pages((page,))

    assert result[0].route is PageRoute.NATIVE_TEXT
    assert result[0].reason is PageRouteReason.COMPLETE_NATIVE_TEXT


def test_incomplete_native_text_requires_ocr() -> None:
    page = SourcePage(page_number=2, native_text="Provider:", native_text_complete=False)

    result = classify_pages((page,))

    assert result[0].route is PageRoute.OCR_REQUIRED
    assert result[0].reason is PageRouteReason.INCOMPLETE_NATIVE_TEXT


def test_page_empty_after_artifact_removal_requires_ocr() -> None:
    page = SourcePage(page_number=3, native_text=" \n | -- | ", native_text_complete=True)

    result = classify_pages((page,))

    assert result[0].route is PageRoute.OCR_REQUIRED
    assert result[0].reason is PageRouteReason.NO_SUBSTANTIVE_TEXT


def test_mixed_pages_retain_source_order_and_identity() -> None:
    pages = (
        SourcePage(page_number=3, native_text="Complete", native_text_complete=True),
        SourcePage(page_number=7, native_text="Partial", native_text_complete=False),
    )

    result = classify_pages(pages)

    assert [item.page_number for item in result] == [3, 7]
    assert [item.route for item in result] == [
        PageRoute.NATIVE_TEXT,
        PageRoute.OCR_REQUIRED,
    ]