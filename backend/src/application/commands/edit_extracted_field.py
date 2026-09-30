"""Application command for optimistic extracted-field edits."""

from uuid import uuid4

from application.ports.case_repository import CaseRepository
from domain.case.aggregate import CaseAggregate
from domain.case.extracted_field import ExtractedField


class EditExtractedField:
    """Load, edit, and save one field through the case aggregate."""

    def __init__(self, repository: CaseRepository) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        session_id: str,
        field_id: str,
        expected_revision_id: str,
        value: str,
    ) -> ExtractedField:
        def apply_edit(aggregate: CaseAggregate) -> tuple[CaseAggregate, ExtractedField]:
            updated = aggregate.edit_extracted_field(
                field_id=field_id,
                expected_revision_id=expected_revision_id,
                revision_id=uuid4().hex,
                value=value,
            )
            field = next(
                item for item in updated.extracted_fields if item.field_id == field_id
            )
            return updated, field

        return self._repository.update(
            session_id,
            apply_edit,
        )