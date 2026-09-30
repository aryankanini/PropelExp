"""Typed selective recovery commands and safe results."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.job_failure import JobFailure


class RecoveryOutcome(StrEnum):
    REVIEW_READY = "review-ready"
    REPLACEMENT_REQUIRED = "replacement-required"
    RETRY_LATER = "retry-later"


class RecoveryCommand(BaseModel):
    """Request a retry for exactly one recorded failed operation."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    case_id: str = Field(min_length=1)
    failure: JobFailure
    source_valid: bool = True


class RecoveryResult(BaseModel):
    """Safe recovery result with successful output left unconfirmed."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    outcome: RecoveryOutcome
    failure: JobFailure
    output: str | None = None
    confirmed: bool = False