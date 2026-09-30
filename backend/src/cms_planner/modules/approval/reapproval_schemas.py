"""HTTP contracts for POC reapproval transitions."""

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.approval import ApprovalState
from cms_planner.domain.poc import PocSectionName


class PocEditRequest(BaseModel):
    """One optimistic POC section-edit operation."""

    model_config = ConfigDict(extra="forbid")

    expected_revision_id: str = Field(min_length=1)
    revision_id: str = Field(min_length=1)
    section_updates: dict[PocSectionName, str | None] = Field(min_length=1)


class ReapprovalResponse(BaseModel):
    """Authoritative workflow and export state after a transition."""

    model_config = ConfigDict(extra="forbid", strict=True)

    approval: ApprovalState
    workflow_state: str
    export_enabled: bool