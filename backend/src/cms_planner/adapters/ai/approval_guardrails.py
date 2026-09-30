"""Provider-neutral guardrail for AI-produced approval claims."""

from collections.abc import Mapping
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.approval import ApprovalState


class GuardedApprovalOutput(BaseModel):
    """AI candidate content with backend-owned approval authority."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    candidate_text: str = Field(min_length=1)
    approval_status: Literal["unapproved", "approved"]
    approved_revision_id: str | None = None


def guard_approval_output(
    provider_output: Mapping[str, object], approval: ApprovalState
) -> GuardedApprovalOutput:
    """Ignore provider authority and expose only authoritative approval state."""
    candidate = provider_output.get("candidate_text")
    if not isinstance(candidate, str) or not candidate.strip():
        raise ValueError("provider output must contain candidate_text")
    approved = approval.status == "approved" and approval.revision_id is not None
    return GuardedApprovalOutput(
        candidate_text=candidate.strip(),
        approval_status="approved" if approved else "unapproved",
        approved_revision_id=approval.revision_id if approved else None,
    )