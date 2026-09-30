"""Correction commands and append-only revision projections."""

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.review import ReviewRevision


class CorrectionCommand(BaseModel):
    """Request one correction against the displayed revision."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    expected_revision_id: str = Field(min_length=1)
    value: str = Field(min_length=1)


class RevisionHistory(BaseModel):
    """Expose the current revision with every retained predecessor."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    current_revision_id: str = Field(min_length=1)
    revisions: tuple[ReviewRevision, ...] = Field(min_length=1)
