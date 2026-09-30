"""Reapproval state returned after POC review transitions."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

from cms_planner.domain.approval import ApprovalState


class ReapprovalDecision(BaseModel):
    """Authoritative workflow state after an edit or change request."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    approval: ApprovalState
    workflow_state: Literal["editing", "reapproval_required"]
    export_enabled: Literal[False] = False