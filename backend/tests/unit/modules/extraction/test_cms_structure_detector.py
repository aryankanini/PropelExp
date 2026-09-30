from cms_planner.domain.cms_layout import CmsLayoutPattern, CmsLayoutStatus
from cms_planner.domain.page import PageClassification, PageRoute, PageRouteReason
from cms_planner.domain.text_span import BoundingBox, ClassifiedPageText, TextSpan
from cms_planner.modules.extraction.cms_structure_detector import detect_cms_layout


def page(page_number: int, text: str) -> ClassifiedPageText:
    return ClassifiedPageText(
        classification=PageClassification(
            page_number=page_number,
            route=PageRoute.NATIVE_TEXT,
            reason=PageRouteReason.COMPLETE_NATIVE_TEXT,
        ),
        spans=(
            TextSpan(
                page_number=page_number,
                text=text,
                coordinates=BoundingBox(x=0.0, y=0.0, width=100.0, height=20.0),
            ),
        ),
    )


def test_recognizes_and_retains_cms_2567_layout() -> None:
    layout = detect_cms_layout(
        (
            page(
                1,
                "FORM CMS-2567\nSTATEMENT OF DEFICIENCIES AND PLAN OF CORRECTION\n"
                "(X4) ID PREFIX TAG\nF 0686",
            ),
        )
    )

    assert layout.status is CmsLayoutStatus.RECOGNIZED
    assert layout.pattern is CmsLayoutPattern.CMS_2567
    assert layout.marker_page_numbers == (1,)


def test_recognizes_spaced_form_identifier() -> None:
    layout = detect_cms_layout(
        (page(1, "FORM CMS 2567\nF.686\nStatement of deficiency"),)
    )

    assert layout.status is CmsLayoutStatus.RECOGNIZED
    assert layout.pattern is CmsLayoutPattern.CMS_2567


def test_unrecognized_document_returns_stopping_layout() -> None:
    layout = detect_cms_layout((page(1, "Unrelated clinical correspondence"),))

    assert layout.status is CmsLayoutStatus.UNRECOGNIZED
    assert layout.pattern is None
    assert layout.marker_page_numbers == ()


def test_recognizable_header_without_f_tags_remains_recognized() -> None:
    layout = detect_cms_layout(
        (
            page(
                1,
                "STATEMENT OF DEFICIENCIES AND PLAN OF CORRECTION\n"
                "(X1) PROVIDER/SUPPLIER/CLIA IDENTIFICATION NUMBER\n"
                "(X4) ID PREFIX TAG",
            ),
        )
    )

    assert layout.status is CmsLayoutStatus.RECOGNIZED
    assert layout.pattern is CmsLayoutPattern.CMS_2567


def test_recognizes_cms_header_with_interrupted_provider_label() -> None:
    layout = detect_cms_layout(
        (
            page(
                1,
                "(X1) PROVIDER/SUPPLIER/CLIA\n"
                "DEPARTMENT OF HEALTH AND HUMAN SERVICES\n"
                "CENTERS FOR MEDICARE & MEDICAID SERVICES\n"
                "STATEMENT OF DEFICIENCIES\nAND PLAN OF CORRECTION\n"
                "IDENTIFICATION NUMBER\n(X4) ID\nPREFIX\nTAG\nE 0000",
            ),
        )
    )

    assert layout.status is CmsLayoutStatus.RECOGNIZED
    assert layout.pattern is CmsLayoutPattern.CMS_2567