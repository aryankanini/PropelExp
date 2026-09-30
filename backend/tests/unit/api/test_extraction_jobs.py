from cms_planner.api.routes.extraction_jobs import _print_extracted_pages
from cms_planner.domain.page import PageClassification, PageRoute, PageRouteReason
from cms_planner.domain.text_span import BoundingBox, ClassifiedPageText, TextSpan


def _page(page_number: int, *texts: str) -> ClassifiedPageText:
    return ClassifiedPageText(
        classification=PageClassification(
            page_number=page_number,
            route=PageRoute.NATIVE_TEXT,
            reason=PageRouteReason.COMPLETE_NATIVE_TEXT,
        ),
        spans=tuple(
            TextSpan(
                page_number=page_number,
                text=text,
                coordinates=BoundingBox(x=0, y=0, width=1, height=1),
            )
            for text in texts
        ),
    )


def test_prints_final_extracted_text_by_page(capsys) -> None:
    _print_extracted_pages([_page(1, "Provider Name", "F-123"), _page(2)])

    assert capsys.readouterr().out == (
        "[EXTRACTION] Extracted PDF text\n"
        "[EXTRACTION] --- page 1 ---\n"
        "Provider Name\n"
        "F-123\n"
        "[EXTRACTION] --- page 2 ---\n"
        "[no text extracted]\n"
    )