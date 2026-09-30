"""Server-authoritative current-revision export policy."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.approval import ApprovalState
from cms_planner.domain.poc import PocDraft


class ExportBlockerCode(StrEnum):
    """Stable reasons an export cannot be authorized."""

    NO_CURRENT_REVISION = "no_current_revision"
    APPROVAL_REQUIRED = "approval_required"
    STALE_APPROVAL = "stale_approval"


class ExportBlocker(BaseModel):
    """A precise reason export authorization failed."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    code: ExportBlockerCode
    message: str = Field(min_length=1)


def authorize_export(
    draft: PocDraft | None, approval: ApprovalState
) -> ExportBlocker | None:
    """Require approval of the current retained POC revision."""
    if draft is None:
        return ExportBlocker(
            code=ExportBlockerCode.NO_CURRENT_REVISION,
            message="No current POC revision is available for export.",
        )
    if approval.status != "approved" or approval.revision_id is None:
        return ExportBlocker(
            code=ExportBlockerCode.APPROVAL_REQUIRED,
            message="Compliance-leader approval is required before export.",
        )
    if approval.revision_id != draft.current_revision_id:
        return ExportBlocker(
            code=ExportBlockerCode.STALE_APPROVAL,
            message="Approval does not match the current revision.",
        )
    return None