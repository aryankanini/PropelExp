"""Extracted field entity and immutable revision history."""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from domain.case.field_revision import FieldRevision
from domain.case.revision_errors import StaleRevisionError


class ExtractedField(BaseModel):
    """Own revision history and the current revision pointer for one field."""

    model_config = ConfigDict(frozen=True, strict=True)

    field_id: str = Field(min_length=1)
    revisions: tuple[FieldRevision, ...] = Field(min_length=1)
    current_revision_id: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_current_revision(self) -> Self:
        if self.revisions[-1].revision_id != self.current_revision_id:
            raise ValueError("current_revision_id must identify the latest revision")
        return self

    @property
    def current_revision(self) -> FieldRevision:
        return self.revisions[-1]

    def append_edit(
        self,
        *,
        expected_revision_id: str,
        revision_id: str,
        value: str,
    ) -> Self:
        """Append an edit when the caller holds the current revision."""
        current = self.current_revision
        if expected_revision_id != current.revision_id:
            raise StaleRevisionError(expected_revision_id, current.revision_id)

        revision = FieldRevision(
            revision_id=revision_id,
            value=value,
            page_number=current.page_number,
            supporting_snippet=current.supporting_snippet,
            confidence=current.confidence,
            origin="user_edit",
            revision_number=current.revision_number + 1,
        )
        return self.model_copy(
            update={
                "revisions": (*self.revisions, revision),
                "current_revision_id": revision.revision_id,
            }
        )