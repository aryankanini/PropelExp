"""HTTP contracts for current-revision approval."""

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.approval import ApprovalBlocker, ApprovalState


class ApprovalRequest(BaseModel):
    """The exact displayed revision submitted for approval."""

    model_config = ConfigDict(extra="forbid", strict=True)

    revision_id: str = Field(min_length=1)


class ApprovalResponse(BaseModel):
    """Current approval state and any exact denial blockers."""

    model_config = ConfigDict(extra="forbid", strict=True)

    approved: bool
    approval: ApprovalState
    blockers: tuple[ApprovalBlocker, ...] = ()
    copy_enabled: bool
    download_enabled: bool