from cms_planner.domain.cms_layout import CmsLayout, CmsLayoutPattern, CmsLayoutStatus
from cms_planner.domain.page import PageClassification, PageRoute, PageRouteReason
from cms_planner.domain.text_span import BoundingBox, ClassifiedPageText, TextSpan
from cms_planner.modules.extraction.deficiency_boundaries import (
    identify_deficiency_boundaries,
)


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


def recognized_layout() -> CmsLayout:
    return CmsLayout(
        status=CmsLayoutStatus.RECOGNIZED,
        pattern=CmsLayoutPattern.CMS_2567,
        marker_page_numbers=(1,),
    )


def test_coalesces_repeated_tag_boundaries_without_losing_text() -> None:
    boundaries = identify_deficiency_boundaries(
        recognized_layout(),
        (
            page(1, "F 0686\nResidents did not receive required treatment."),
            page(2, "The failure affected three residents.\nF 0686\nA second event occurred."),
        ),
    )

    assert tuple(item.boundary_id for item in boundaries) == ("cms-2567:0001",)
    assert tuple(item.f_tag for item in boundaries) == ("F0686",)
    assert tuple(e.page_number for e in boundaries[0].evidence) == (1, 2)
    assert "three residents" in boundaries[0].sod_text
    assert "A second event occurred." in boundaries[0].sod_text
    assert all(item.complete for item in boundaries)


def test_merges_same_tag_continued_at_start_of_next_page() -> None:
    boundaries = identify_deficiency_boundaries(
        recognized_layout(),
        (
            page(1, "F 0686\nResidents did not receive required treatment."),
            page(
                2,
                "F 0686\nThe failure affected three residents.\n"
                "F 0880\nStaff did not follow infection-control practices.",
            ),
        ),
    )

    assert tuple(item.f_tag for item in boundaries) == ("F0686", "F0880")
    assert tuple(e.page_number for e in boundaries[0].evidence) == (1, 2)
    assert boundaries[0].sod_text == (
        "Residents did not receive required treatment.\n"
        "The failure affected three residents."
    )


def test_retains_initial_comments_as_zero_tag_boundary() -> None:
    boundaries = identify_deficiency_boundaries(
        recognized_layout(),
        (
            page(
                1,
                "L 000\nInitial Comments\nOne deficiency was cited.\n"
                "L 532\nThe facility lacked approved patient care policies.",
            ),
        ),
    )

    assert tuple(item.f_tag for item in boundaries) == ("L0000", "L0532")
    assert boundaries[0].sod_text == "Initial Comments\nOne deficiency was cited."


def test_retains_zero_tag_with_any_alphabetic_prefix() -> None:
    for raw_tag, normalized_tag in (
        ("A 000", "A0000"),
        ("K-0000", "K0000"),
        ("q.000", "Q0000"),
        ("Z0000", "Z0000"),
    ):
        boundaries = identify_deficiency_boundaries(
            recognized_layout(),
            (page(1, f"{raw_tag}\nInitial Comments\nNo deficiencies were cited."),),
        )

        assert tuple(item.f_tag for item in boundaries) == (normalized_tag,)
        assert boundaries[0].sod_text == (
            "Initial Comments\nNo deficiencies were cited."
        )


def test_retains_adjacent_zero_tags_with_different_prefixes() -> None:
    boundaries = identify_deficiency_boundaries(
        recognized_layout(),
        (
            page(
                1,
                "E0000\nEmergency preparedness initial comments.\n"
                "K0000\nLife safety code initial comments.\n"
                "K0222\nThe facility failed to maintain required exits.",
            ),
        ),
    )

    assert tuple(item.f_tag for item in boundaries) == (
        "E0000",
        "K0000",
        "K0222",
    )
    assert boundaries[0].sod_text == "Emergency preparedness initial comments."
    assert boundaries[1].sod_text == "Life safety code initial comments."
    assert boundaries[2].sod_text == "The facility failed to maintain required exits."


def test_separates_prefetched_emergency_and_life_safety_zero_tags() -> None:
    boundaries = identify_deficiency_boundaries(
        recognized_layout(),
        (
            page(
                1,
                "E0000\nK0000\n"
                "An Emergency Preparedness survey was conducted on 10/07/24.\n"
                "The facility was reviewed for emergency preparedness compliance.\n"
                "Bldg. 01 A Life Safety Code Recertification Survey was conducted.\n"
                "The facility was reviewed under NFPA 101.",
            ),
        ),
    )

    assert tuple(item.f_tag for item in boundaries) == ("E0000", "K0000")
    assert "Emergency Preparedness survey" in boundaries[0].sod_text
    assert "Life Safety Code" not in boundaries[0].sod_text
    assert "Life Safety Code Recertification" in boundaries[1].sod_text
    assert "Emergency Preparedness" not in boundaries[1].sod_text


def test_assigns_prefetched_nfpa_heading_to_following_tag() -> None:
    boundaries = identify_deficiency_boundaries(
        recognized_layout(),
        (
            page(
                1,
                "K0000\nLife Safety Code survey summary.\n"
                "Quality Review completed on 10/08/24\n"
                "NFPA 101\nEgress Doors\nK0222\nSS=E\nBldg. 01\n"
                "The facility failed to maintain accessible exits.",
            ),
        ),
    )

    assert tuple(item.f_tag for item in boundaries) == ("K0000", "K0222")
    assert boundaries[0].sod_text == (
        "Life Safety Code survey summary.\n"
        "Quality Review completed on 10/08/24"
    )
    assert boundaries[1].sod_text.startswith("NFPA 101\nEgress Doors\nSS=E")


def test_separates_initial_comments_when_header_tags_are_emitted_first() -> None:
    boundaries = identify_deficiency_boundaries(
        recognized_layout(),
        (
            page(
                1,
                "L 000\nL 532\nInitial Comments\nInitial Comments\n"
                "A relicensure survey was completed on 4/10/24.\n"
                "One deficiency was cited.\n"
                "6.5.9 Patient Care\nThe facility lacked approved policies.",
            ),
        ),
    )

    assert tuple(item.f_tag for item in boundaries) == ("L0000", "L0532")
    assert "relicensure survey" in boundaries[0].sod_text
    assert "Patient Care" not in boundaries[0].sod_text
    assert boundaries[1].sod_text == (
        "6.5.9 Patient Care\nThe facility lacked approved policies."
    )
    assert "Initial Comments" not in boundaries[1].sod_text


def test_ignores_zero_tag_footer_without_closing_active_deficiency() -> None:
    boundaries = identify_deficiency_boundaries(
        recognized_layout(),
        (
            page(
                1,
                "L 000\nInitial Comments\nOne deficiency was cited.\n"
                "L 532\nThe facility lacked approved patient care policies.\n"
                "L 000\nL 532",
            ),
            page(
                2,
                "L 532 Continued From page 1\n"
                "Staff did not follow the patient care policy.",
            ),
        ),
    )

    assert tuple(item.f_tag for item in boundaries) == ("L0000", "L0532")
    assert tuple(e.page_number for e in boundaries[1].evidence) == (1, 2)
    assert "approved patient care policies" in boundaries[1].sod_text
    assert "Staff did not follow" in boundaries[1].sod_text


def test_does_not_treat_tag_ending_in_000_as_initial_comments() -> None:
    boundary = identify_deficiency_boundaries(
        recognized_layout(),
        (page(1, "F 1000\nThe facility failed to meet the requirement."),),
    )[0]

    assert boundary.f_tag == "F1000"


def test_normalizes_common_ocr_tag_variants() -> None:
    for tag_text in ("F.686", "F\u20110686", "f 0686"):
        boundary = identify_deficiency_boundaries(
            recognized_layout(),
            (page(1, f"{tag_text}\nResidents did not receive required treatment."),),
        )[0]

        assert boundary.f_tag == "F0686"


def test_merges_common_continuation_label_variants() -> None:
    for continuation_label in (
        "F 0686 Cont. from p. 1",
        "F 0686 Continued from pg 1",
    ):
        boundaries = identify_deficiency_boundaries(
            recognized_layout(),
            (
                page(
                    1,
                    "F 0686\nResidents did not receive required treatment.\n"
                    f"The failure affected three residents.\n{continuation_label}",
                ),
            ),
        )

        assert len(boundaries) == 1
        assert tuple(e.page_number for e in boundaries[0].evidence) == (1,)
        assert "three residents" in boundaries[0].sod_text


def test_marks_trailing_f_tag_without_sod_uncertain_and_unconfirmed() -> None:
    boundary = identify_deficiency_boundaries(
        recognized_layout(),
        (page(1, "F 0880\nSOD:"),),
    )[0]

    assert boundary.sod_text is None
    assert boundary.complete is False
    assert boundary.uncertainty is True
    assert boundary.confirmed is False
    assert boundary.evidence[0].page_number == 1


def test_unrecognized_layout_stops_boundary_creation() -> None:
    layout = CmsLayout(status=CmsLayoutStatus.UNRECOGNIZED)

    assert identify_deficiency_boundaries(layout, (page(1, "F 0686\nText"),)) == ()