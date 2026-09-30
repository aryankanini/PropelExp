"""Revision-bound POC approval models and invariants."""

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from cms_planner.domain.poc import POC_SECTION_ORDER, PocRevision, PocSectionName


class ApprovalBlockerCode(StrEnum):
    """Stable reasons that prevent current-revision approval."""

    UNAUTHORIZED = "unauthorized"
    NO_CURRENT_REVISION = "no_current_revision"
    STALE_REVISION = "stale_revision"
    MISSING_EVIDENCE = "missing_evidence"
    INCOMPLETE_REVISION = "incomplete_revision"


class ApprovalBlocker(BaseModel):
    """A precise reason approval was denied."""

    model_config = ConfigDict(frozen=True, strict=True)

    code: ApprovalBlockerCode
    message: str = Field(min_length=1)
    section: PocSectionName | None = None


class ApprovalState(BaseModel):
    """The single approval state for a case's current POC."""

    model_config = ConfigDict(frozen=True, strict=True)

    status: Literal[
        "unapproved", "approved", "changes_requested", "reapproval_required"
    ] = "unapproved"
    revision_id: str | None = None
    approved_by: str | None = None
    approved_at: AwareDatetime | None = None

    @classmethod
    def approved(
        cls, *, revision_id: str, approved_by: str, approved_at: datetime
    ) -> "ApprovalState":
        return cls(
            status="approved",
            revision_id=revision_id,
            approved_by=approved_by,
            approved_at=approved_at,
        )

    @property
    def export_enabled(self) -> bool:
        return self.status == "approved" and self.revision_id is not None


class ApprovalDecision(BaseModel):
    """Approval outcome returned without hiding denial reasons."""

    model_config = ConfigDict(frozen=True, strict=True)

    approval: ApprovalState
    blockers: tuple[ApprovalBlocker, ...] = ()

    @property
    def approved(self) -> bool:
        return not self.blockers and self.approval.status == "approved"


def collect_approval_blockers(
    revision: PocRevision | None,
    *,
    reviewed_revision_id: str,
    actor_role: str,
    has_evidence: bool,
) -> tuple[ApprovalBlocker, ...]:
    """Return every blocker in stable review order."""
    blockers: list[ApprovalBlocker] = []
    if actor_role != "compliance_leader":
        blockers.append(
            ApprovalBlocker(
                code=ApprovalBlockerCode.UNAUTHORIZED,
                message="A designated compliance leader must approve this revision.",
            )
        )
    if revision is None:
        blockers.append(
            ApprovalBlocker(
                code=ApprovalBlockerCode.NO_CURRENT_REVISION,
                message="No current POC revision is available for approval.",
            )
        )
        return tuple(blockers)
    if revision.revision_id != reviewed_revision_id:
        blockers.append(
            ApprovalBlocker(
                code=ApprovalBlockerCode.STALE_REVISION,
                message=(
                    "The reviewed revision is stale; refresh the current revision "
                    "before approval."
                ),
            )
        )
    if not has_evidence:
        blockers.append(
            ApprovalBlocker(
                code=ApprovalBlockerCode.MISSING_EVIDENCE,
                message="Reviewed evidence is required before approval.",
            )
        )
    if not revision.approval_ready:
        blocked_sections = {marker.section for marker in revision.missing_information}
        for name in POC_SECTION_ORDER:
            if name in blocked_sections:
                blockers.append(
                    ApprovalBlocker(
                        code=ApprovalBlockerCode.INCOMPLETE_REVISION,
                        message=f"The {name.value} section has missing information.",
                        section=name,
                    )
                )
    return tuple(blockers)