"""Deficiency readiness and confirmation outcomes."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class BlockerCode(StrEnum):
    """Closed reasons a deficiency cannot be confirmed."""

    MISSING_FIELD = "missing-field"
    UNRESOLVED = "unresolved"
    MISSING_EVIDENCE = "missing-evidence"


class ConfirmationBlocker(BaseModel):
    """Identify one field preventing confirmation."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    field_type: str = Field(min_length=1)
    field_id: str | None = None
    code: BlockerCode


class ExpectedRevision(BaseModel):
    """Bind confirmation to one displayed field revision."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    field_id: str = Field(min_length=1)
    revision_id: str = Field(min_length=1)


class ConfirmationCommand(BaseModel):
    """Request atomic confirmation for a deficiency."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    deficiency_id: str = Field(min_length=1)
    expected_revisions: tuple[ExpectedRevision, ...] = Field(min_length=1)


class ConfirmationOutcome(BaseModel):
    """Return eligibility and every field blocking it."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    deficiency_id: str = Field(min_length=1)
    confirmed: bool
    poc_generation_eligible: bool
    blockers: tuple[ConfirmationBlocker, ...] = ()
    confirmed_revision_ids: tuple[str, ...] = ()
