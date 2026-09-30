"""Content-free progress events for resumable processing streams."""

from enum import StrEnum

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from cms_planner.domain.job_failure import JobStage


class JobTerminalStatus(StrEnum):
    FAILED = "failed"
    COMPLETED = "completed"


class JobEvent(BaseModel):
    """Immutable progress metadata that never carries document content."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    job_id: str = Field(min_length=1)
    event_id: int = Field(ge=1)
    stage: JobStage
    percent: int = Field(ge=0, le=100)
    timestamp: AwareDatetime
    terminal_status: JobTerminalStatus | None
    failure_code: str | None = Field(default=None, exclude_if=lambda value: value is None)