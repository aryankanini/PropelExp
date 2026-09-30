from cms_planner.application.ports.ocr_types import OcrFailure
from cms_planner.domain.page import PageClassification, PageRoute, PageRouteReason
from cms_planner.domain.text_span import BoundingBox, ClassifiedPageText, TextSpan
from cms_planner.modules.extraction.text_normalizer import normalize_extracted_page


def page(text: str) -> ClassifiedPageText:
    return ClassifiedPageText(
        classification=PageClassification(
            page_number=1,
            route=PageRoute.NATIVE_TEXT,
            reason=PageRouteReason.COMPLETE_NATIVE_TEXT,
        ),
        spans=(
            TextSpan(
                page_number=1,
                text=text,
                coordinates=BoundingBox(x=1, y=2, width=3, height=4),
            ),
        ),
    )


def test_normalizes_artifacts_without_changing_substantive_content() -> None:
    result = normalize_extracted_page(page("\ufeffCMS\t2567\r\nProvider:  North Clinic\u200b"))

    assert isinstance(result, ClassifiedPageText)
    assert result.spans[0].text == "CMS 2567\nProvider: North Clinic"
    assert result.spans[0].coordinates == BoundingBox(x=1, y=2, width=3, height=4)


def test_preserves_substantive_punctuation_and_values() -> None:
    result = normalize_extracted_page(page("F-123: 10%"))

    assert isinstance(result, ClassifiedPageText)
    assert result.spans[0].text == "F-123: 10%"


def test_normalization_empty_native_page_is_routed_to_ocr() -> None:
    result = normalize_extracted_page(page("\ufeff \u200b | -- |"))

    assert isinstance(result, ClassifiedPageText)
    assert result.classification.route is PageRoute.OCR_REQUIRED
    assert result.classification.reason is PageRouteReason.NO_SUBSTANTIVE_TEXT
    assert result.spans == ()


def test_ocr_failure_is_returned_without_confirmed_content() -> None:
    failure = OcrFailure(page_number=1, code="provider-failed")

    assert normalize_extracted_page(failure) is failure