"""Append reviewer-authored field corrections."""

from uuid import uuid4

from application.ports.case_repository import CaseRepository
from domain.case.aggregate import CaseAggregate
from cms_planner.application.review_service import find_review_field
from cms_planner.domain.review import ReviewField
from cms_planner.domain.revisions import CorrectionCommand


class CorrectionService:
    """Correct one field inside the repository transaction."""

    def __init__(self, repository: CaseRepository) -> None:
        self._repository = repository

    def correct(
        self,
        session_id: str,
        field_id: str,
        command: CorrectionCommand,
    ) -> ReviewField:
        def update(aggregate: CaseAggregate) -> tuple[CaseAggregate, ReviewField]:
            field = find_review_field(aggregate, field_id)
            corrected = field.append_correction(
                expected_revision_id=command.expected_revision_id,
                revision_id=uuid4().hex,
                value=command.value,
            )
            return aggregate.replace_review_field(corrected), corrected

        return self._repository.update(session_id, update)
