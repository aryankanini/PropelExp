"""Append supported, corrected, or unresolved review outcomes."""

from enum import StrEnum
from typing import Self
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

from application.ports.case_repository import CaseRepository
from domain.case.aggregate import CaseAggregate
from cms_planner.application.review_service import find_review_field
from cms_planner.domain.review import ReviewField


class ResolutionKind(StrEnum):
    SELECT = "select"
    CORRECT = "correct"
    UNRESOLVED = "unresolved"


class ResolutionCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: ResolutionKind
    expected_revision_id: str = Field(min_length=1)
    candidate_id: str | None = None
    value: str | None = None

    @model_validator(mode="after")
    def validate_resolution_path(self) -> Self:
        if self.kind is ResolutionKind.SELECT and not self.candidate_id:
            raise ValueError("candidate_id is required for selection")
        if self.kind is ResolutionKind.CORRECT and not self.value:
            raise ValueError("value is required for correction")
        if self.kind is ResolutionKind.UNRESOLVED and (
            self.candidate_id is not None or self.value is not None
        ):
            raise ValueError("unresolved resolution cannot include a value")
        return self


class ResolutionService:
    """Resolve one field inside the repository transaction."""

    def __init__(self, repository: CaseRepository) -> None:
        self._repository = repository

    def resolve(
        self,
        session_id: str,
        field_id: str,
        command: ResolutionCommand,
    ) -> ReviewField:
        def update(aggregate: CaseAggregate) -> tuple[CaseAggregate, ReviewField]:
            field = find_review_field(aggregate, field_id)
            if command.kind is ResolutionKind.SELECT:
                assert command.candidate_id is not None
                updated = field.resolve_candidate(
                    expected_revision_id=command.expected_revision_id,
                    candidate_id=command.candidate_id,
                    revision_id=uuid4().hex,
                )
            elif command.kind is ResolutionKind.CORRECT:
                assert command.value is not None
                updated = field.append_correction(
                    expected_revision_id=command.expected_revision_id,
                    revision_id=uuid4().hex,
                    value=command.value,
                )
            else:
                updated = field.leave_unresolved(
                    expected_revision_id=command.expected_revision_id
                )
            return aggregate.replace_review_field(updated), updated

        return self._repository.update(session_id, update)
