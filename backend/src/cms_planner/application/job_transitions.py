"""Truthful job transitions that retain independently validated work."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from cms_planner.domain.job_failure import JobFailure


class JobStatus(StrEnum):
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "completed"


class JobState(BaseModel):
    """Immutable processing state and retained confirmed work identifiers."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    status: JobStatus = JobStatus.PROCESSING
    failures: tuple[JobFailure, ...] = ()
    reviewed_page_numbers: tuple[int, ...] = ()
    confirmed_deficiency_ids: tuple[str, ...] = ()
    retained_poc_ids: tuple[str, ...] = ()


class InvalidJobTransitionError(Exception):
    """Report a terminal status that contradicts required failure state."""


def record_failure(state: JobState, failure: JobFailure) -> JobState:
    """Append a typed failure without altering retained confirmed work."""

    return state.model_copy(
        update={"status": JobStatus.FAILED, "failures": (*state.failures, failure)}
    )


def transition_to_completed(state: JobState) -> JobState:
    """Complete only when no required operation remains failed."""

    if any(failure.required for failure in state.failures):
        raise InvalidJobTransitionError(
            "required failed stages cannot transition to completed"
        )
    return state.model_copy(update={"status": JobStatus.COMPLETED})