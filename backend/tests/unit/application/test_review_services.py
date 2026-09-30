import pytest

from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from cms_planner.application.confirmation_service import ConfirmationService
from cms_planner.application.correction_service import CorrectionService
from cms_planner.application.provenance_service import ProvenanceService
from cms_planner.application.resolution_service import (
    ResolutionCommand,
    ResolutionKind,
    ResolutionService,
)
from cms_planner.application.review_service import ReviewService
from cms_planner.domain.confirmation import ConfirmationCommand, ExpectedRevision
from cms_planner.domain.review import (
    Evidence,
    HighlightCoordinates,
    Origin,
    ReviewCandidate,
    ReviewField,
    ReviewRevision,
    StaleReviewRevisionError,
)
from cms_planner.domain.revisions import CorrectionCommand
from domain.case.aggregate import CaseAggregate


def make_evidence(page_number: int = 1) -> Evidence:
    return Evidence(
        page_number=page_number,
        full_snippet="Complete supporting evidence",
        highlight=HighlightCoordinates(x=0.1, y=0.1, width=0.5, height=0.2),
        source="native-text",
    )


def make_field(
    field_id: str,
    field_type: str,
    *,
    unresolved: bool = False,
    evidence: Evidence | None = None,
) -> ReviewField:
    retained_evidence = evidence if evidence is not None else make_evidence()
    revision = ReviewRevision(
        revision_id=f"{field_id}-revision-1",
        revision_number=1,
        value=f"{field_type} value",
        origin=Origin.EXTRACTED,
        evidence=retained_evidence,
    )
    candidate = ReviewCandidate(
        candidate_id=f"{field_id}-candidate-1",
        value=f"resolved {field_type}",
        confidence=0.8,
        uncertainty="Competing extraction" if unresolved else None,
        origin=Origin.EXTRACTED,
        evidence=retained_evidence,
    )
    return ReviewField(
        field_id=field_id,
        deficiency_id="deficiency-1",
        field_type=field_type,
        candidates=(candidate,),
        revisions=(revision,),
        current_revision_id=revision.revision_id,
        unresolved=unresolved,
    )


def make_repository(*fields: ReviewField) -> InMemoryCaseRepository:
    aggregate = CaseAggregate(session_id="session-1", case_id="case-1")
    for field in fields:
        aggregate = aggregate.add_review_field(field)
    repository = InMemoryCaseRepository()
    repository.add(aggregate)
    return repository


def expected_revisions(*fields: ReviewField) -> tuple[ExpectedRevision, ...]:
    return tuple(
        ExpectedRevision(
            field_id=field.field_id,
            revision_id=field.current_revision_id,
        )
        for field in fields
    )


def test_review_query_is_stable_and_resolution_preserves_candidates() -> None:
    sod = make_field("field-sod", "sod")
    f_tag = make_field("field-ftag", "f_tag", unresolved=True)
    later_candidate = f_tag.candidates[0].model_copy(
        update={
            "candidate_id": "field-ftag-candidate-2",
            "evidence": make_evidence(page_number=2),
        }
    )
    f_tag = f_tag.model_copy(
        update={"candidates": (later_candidate, f_tag.candidates[0])}
    )
    repository = make_repository(sod, f_tag)

    fields = ReviewService(repository).get_fields("session-1")
    resolved = ResolutionService(repository).resolve(
        "session-1",
        "field-ftag",
        ResolutionCommand(
            kind=ResolutionKind.SELECT,
            expected_revision_id=f_tag.current_revision_id,
            candidate_id="field-ftag-candidate-1",
        ),
    )

    assert [field.field_id for field in fields] == ["field-ftag", "field-sod"]
    assert [candidate.candidate_id for candidate in fields[0].candidates] == [
        "field-ftag-candidate-1",
        "field-ftag-candidate-2",
    ]
    assert resolved.unresolved is False
    assert resolved.current_revision.value == "resolved f_tag"
    assert resolved.candidates == f_tag.candidates


def test_correction_preserves_original_and_rejects_empty_value() -> None:
    field = make_field("field-sod", "sod")
    repository = make_repository(field)
    service = CorrectionService(repository)

    corrected = service.correct(
        "session-1",
        field.field_id,
        CorrectionCommand(
            expected_revision_id=field.current_revision_id,
            value="Complete corrected SOD",
        ),
    )

    assert corrected.revisions[0] == field.revisions[0]
    assert corrected.current_revision.origin is Origin.USER_EDITED
    with pytest.raises(ValueError, match="correction must not be empty"):
        service.correct(
            "session-1",
            field.field_id,
            CorrectionCommand(
                expected_revision_id=corrected.current_revision_id,
                value=" ",
            ),
        )
    retained = repository.get("session-1")
    assert retained is not None
    assert len(retained.review_fields[0].revisions) == 2


def test_confirmation_returns_every_blocker_without_mutating_state() -> None:
    f_tag = make_field("field-ftag", "f_tag", unresolved=True)
    repository = make_repository(f_tag)

    outcome = ConfirmationService(repository).confirm(
        "session-1",
        ConfirmationCommand(
            deficiency_id="deficiency-1",
            expected_revisions=expected_revisions(f_tag),
        ),
    )

    assert outcome.confirmed is False
    assert [(blocker.field_type, blocker.code) for blocker in outcome.blockers] == [
        ("f_tag", "unresolved"),
        ("sod", "missing-field"),
    ]
    retained = repository.get("session-1")
    assert retained is not None
    assert len(retained.review_fields[0].revisions) == 1


def test_confirmation_is_atomic_and_edit_requires_reapproval() -> None:
    f_tag = make_field("field-ftag", "f_tag")
    sod = make_field("field-sod", "sod")
    repository = make_repository(f_tag, sod)

    outcome = ConfirmationService(repository).confirm(
        "session-1",
        ConfirmationCommand(
            deficiency_id="deficiency-1",
            expected_revisions=expected_revisions(f_tag, sod),
        ),
    )

    assert outcome.confirmed is True
    assert outcome.poc_generation_eligible is True
    confirmed = repository.get("session-1")
    assert confirmed is not None
    approved_f_tag = next(
        field for field in confirmed.review_fields if field.field_id == "field-ftag"
    )
    CorrectionService(repository).correct(
        "session-1",
        approved_f_tag.field_id,
        CorrectionCommand(
            expected_revision_id=approved_f_tag.current_revision_id,
            value="Corrected after approval",
        ),
    )
    provenance = ProvenanceService(repository).get("session-1", "field-ftag")
    assert provenance.current.origin is Origin.USER_EDITED
    assert provenance.reapproval_required is True
    assert Origin.APPROVED in [revision.origin for revision in provenance.history]


def test_stale_confirmation_reports_current_revision() -> None:
    f_tag = make_field("field-ftag", "f_tag")
    sod = make_field("field-sod", "sod")
    repository = make_repository(f_tag, sod)

    with pytest.raises(StaleReviewRevisionError) as error:
        ConfirmationService(repository).confirm(
            "session-1",
            ConfirmationCommand(
                deficiency_id="deficiency-1",
                expected_revisions=(
                    ExpectedRevision(
                        field_id=f_tag.field_id,
                        revision_id="stale-revision",
                    ),
                    ExpectedRevision(
                        field_id=sod.field_id,
                        revision_id=sod.current_revision_id,
                    ),
                ),
            ),
        )

    assert error.value.current_revision_id == f_tag.current_revision_id


@pytest.mark.parametrize("origin", tuple(Origin))
def test_provenance_projects_each_closed_origin(origin: Origin) -> None:
    field = make_field("field-1", "provider")
    revision = field.current_revision.model_copy(update={"origin": origin})
    field = field.model_copy(update={"revisions": (revision,)})

    projection = ProvenanceService(make_repository(field)).get(
        "session-1",
        field.field_id,
    )

    assert projection.current.origin is origin
    assert len(projection.history) == 1


def test_provenance_rejects_origin_outside_closed_set() -> None:
    with pytest.raises(ValueError):
        Origin("Imported")