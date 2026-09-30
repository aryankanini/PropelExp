from cms_planner.domain.page import PageClassification, PageRoute, PageRouteReason
from cms_planner.domain.text_span import BoundingBox, ClassifiedPageText, TextSpan
from cms_planner.modules.extraction.provider_metadata import extract_provider_metadata


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
                coordinates=BoundingBox(x=0.0, y=0.0, width=100.0, height=20.0),
            ),
        ),
    )


def test_extracts_provider_values_from_split_cms_header() -> None:
    metadata = extract_provider_metadata(
        (
            page(
                "(X1) PROVIDER/SUPPLIER/CLIA\nIDENTIFICATION NUMBER:\n12044X\n"
                "(X2) MULTIPLE CONSTRUCTION\nNAME OF PROVIDER OR SUPPLIER\n"
                "STREET ADDRESS, CITY, STATE, ZIP CODE\n1057 S WADSWORTH BLVD\n"
                "LAKEWOOD CROSSING DIALYSIS CENTER\nLAKEWOOD, CO 80226\n"
                "(X4) ID PREFIX TAG"
            ),
        )
    )

    assert metadata is not None
    assert metadata.provider_name == "LAKEWOOD CROSSING DIALYSIS CENTER"
    assert metadata.provider_number == "12044X"
    assert metadata.page_number == 1


def test_extracts_provider_values_when_appended_to_labels() -> None:
    metadata = extract_provider_metadata(
        (
            page(
                "PROVIDER/SUPPLIER/CLIA IDENTIFICATION NUMBER: 12-3456\n"
                "NAME OF PROVIDER OR SUPPLIER: North Valley Care Center\n"
                "STREET ADDRESS, CITY, STATE, ZIP CODE"
            ),
        )
    )

    assert metadata is not None
    assert metadata.provider_name == "North Valley Care Center"
    assert metadata.provider_number == "12-3456"