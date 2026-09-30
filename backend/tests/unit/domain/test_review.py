import pytest

from cms_planner.domain.review import (
    Evidence,
    HighlightCoordinates,
    Origin,
    ReviewCandidate,
    ReviewField,
    ReviewRevision,
    StaleReviewRevisionError,
)


def make_review_field() -> ReviewField:
    evidence = Evidence(
        page_number=24,
        full_snippet="The facility failed to maintain hand hygiene practices.",
        highlight=HighlightCoordinates(x=0.1, y=0.2, width=0.7, height=0.1),
        source="ocr",
    )
    candidates = (
        ReviewCandidate(
            candidate_id="candidate-2",
            value="F881",
            confidence=0.64,
            uncertainty="Conflicts with F880",
            origin=Origin.EXTRACTED,
            evidence=evidence.model_copy(update={"page_number": 25}),
        ),
        ReviewCandidate(
            candidate_id="candidate-1",
            value="F880",
            confidence=0.68,
            uncertainty="Conflicts with F881",
            origin=Origin.EXTRACTED,
            evidence=evidence,
        ),
    )
    original = ReviewRevision(
        revision_id="revision-1",
        revision_number=1,
        value="F880",
        origin=Origin.EXTRACTED,
        evidence=evidence,
    )
    return ReviewField(
        field_id="field-1",
        field_type="f_tag",
        candidates=candidates,
        revisions=(original,),
        current_revision_id=original.revision_id,
        unresolved=True,
    )


def test_review_projection_orders_candidates_and_preserves_complete_text() -> None:
    long_value = ("Complete SOD " * 2_000).strip()
    field = make_review_field().append_correction(
        expected_revision_id="revision-1",
        revision_id="revision-2",
        value=long_value,
    )

    assert [candidate.candidate_id for candidate in field.ordered_candidates] == [
        "candidate-1",
        "candidate-2",
    ]
    assert field.current_revision.value == long_value
    assert field.revisions[0].value == "F880"
    assert field.current_revision.origin is Origin.USER_EDITED


def test_supported_candidate_appends_resolved_revision() -> None:
    original = make_review_field()

    resolved = original.resolve_candidate(
        expected_revision_id="revision-1",
        candidate_id="candidate-2",
        revision_id="revision-2",
    )

    assert resolved.candidates == original.candidates
    assert resolved.current_revision.value == "F881"
    assert resolved.current_revision.evidence.page_number == 25
    assert resolved.unresolved is False


def test_stale_resolution_preserves_original_candidates() -> None:
    field = make_review_field()

    with pytest.raises(StaleReviewRevisionError) as error:
        field.resolve_candidate(
            expected_revision_id="stale-revision",
            candidate_id="candidate-1",
            revision_id="revision-2",
        )

    assert error.value.current_revision_id == "revision-1"
    assert len(field.candidates) == 2


def test_empty_correction_does_not_allocate_a_revision() -> None:
    field = make_review_field()

    with pytest.raises(ValueError, match="correction must not be empty"):
        field.append_correction(
            expected_revision_id="revision-1",
            revision_id="revision-2",
            value="   ",
        )

    assert len(field.revisions) == 1