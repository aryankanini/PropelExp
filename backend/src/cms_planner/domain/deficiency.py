"""Confirmed deficiency state used as the POC generation boundary."""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ReviewedField(BaseModel):
    """A reviewed field value that may support generated POC claims."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    field_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    value: str = Field(min_length=1)


class EvidenceSpan(BaseModel):
    """A reviewed source span belonging to one deficiency."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    evidence_id: str = Field(min_length=1)
    page_number: int = Field(ge=1)
    text: str = Field(min_length=1)


class DeficiencyRevision(BaseModel):
    """One immutable reviewed revision of a deficiency."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    revision_id: str = Field(min_length=1)
    reviewed_fields: tuple[ReviewedField, ...] = ()
    evidence_spans: tuple[EvidenceSpan, ...] = ()
    confirmed: bool = False


class Deficiency(BaseModel):
    """Own immutable deficiency revisions and the current revision pointer."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    deficiency_id: str = Field(min_length=1)
    revisions: tuple[DeficiencyRevision, ...] = Field(min_length=1)
    current_revision_id: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_current_revision(self) -> Self:
        if self.revisions[-1].revision_id != self.current_revision_id:
            raise ValueError("current_revision_id must identify the latest revision")
        return self

    @property
    def current_revision(self) -> DeficiencyRevision:
        return self.revisions[-1]