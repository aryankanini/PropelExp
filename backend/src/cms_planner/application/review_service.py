"""Read evidence-linked review projections from transient case state."""

from application.ports.case_repository import CaseRepository
from domain.case.aggregate import CaseAggregate
from domain.case.errors import CaseNotFoundError
from cms_planner.domain.review import EvidenceUnavailableError, ReviewField


def find_review_field(aggregate: CaseAggregate, field_id: str) -> ReviewField:
    """Return one review field or raise its stable identifier."""
    field = next(
        (item for item in aggregate.review_fields if item.field_id == field_id),
        None,
    )
    if field is None:
        raise KeyError(field_id)
    return field


class ReviewService:
    """Query complete, deterministically ordered review state."""

    def __init__(self, repository: CaseRepository) -> None:
        self._repository = repository

    def get_fields(self, session_id: str) -> tuple[ReviewField, ...]:
        aggregate = self._repository.get(session_id)
        if aggregate is None:
            raise CaseNotFoundError(session_id)
        for field in aggregate.review_fields:
            if field.current_revision.evidence is None:
                raise EvidenceUnavailableError(field.field_id)
        ordered_fields = (
            field.model_copy(update={"candidates": field.ordered_candidates})
            for field in aggregate.review_fields
        )
        return tuple(sorted(ordered_fields, key=lambda field: field.field_id))
