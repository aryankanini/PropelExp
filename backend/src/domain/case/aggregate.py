"""Session-scoped aggregate for transient case state."""

from datetime import datetime
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.approval import (
    ApprovalDecision,
    ApprovalState,
    collect_approval_blockers,
)
from cms_planner.domain.deficiency_candidate import DeficiencyCandidate
from cms_planner.domain.poc import PocDraft, PocSectionName
from cms_planner.domain.reapproval import ReapprovalDecision
from cms_planner.domain.review import ReviewField
from domain.case.extracted_field import ExtractedField


CaseStateCategory = Literal[
    "documents",
    "jobs",
    "providers",
    "deficiencies",
    "poc_drafts",
    "approvals",
    "provenance",
]


class CaseAggregate(BaseModel):
    """Own all transient state for one active session case."""

    model_config = ConfigDict(frozen=True, strict=True)

    session_id: str = Field(min_length=1)
    case_id: str = Field(min_length=1)

    documents: tuple[str, ...] = ()
    jobs: tuple[str, ...] = ()
    providers: tuple[str, ...] = ()
    deficiencies: tuple[str, ...] = ()
    poc_drafts: tuple[str, ...] = ()
    approvals: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()

    extracted_fields: tuple[ExtractedField, ...] = ()
    review_fields: tuple[ReviewField, ...] = ()

    # Deficiency candidates produced by the CMS-2567 extraction pipeline.
    deficiency_candidates: tuple[DeficiencyCandidate, ...] = ()

    poc_draft: PocDraft | None = None
    approval_evidence: tuple[str, ...] = ()
    approval: ApprovalState = ApprovalState()

    def append_state(
        self,
        category: CaseStateCategory,
        state_id: str,
    ) -> Self:
        """Return a new aggregate with one state identifier appended."""

        if not state_id:
            raise ValueError("state_id must not be empty")

        current = getattr(self, category)

        return self.model_copy(
            update={
                category: (*current, state_id),
            }
        )

    def add_extracted_field(
        self,
        field: ExtractedField,
    ) -> Self:
        """Return a new aggregate containing an extracted field."""

        return self.model_copy(
            update={
                "extracted_fields": (
                    *self.extracted_fields,
                    field,
                )
            }
        )

    def add_review_field(
        self,
        field: ReviewField,
    ) -> Self:
        """Return a new aggregate containing an evidence-linked review field."""

        if any(
            item.field_id == field.field_id
            for item in self.review_fields
        ):
            raise ValueError(
                f"review field already exists: {field.field_id}"
            )

        return self.model_copy(
            update={
                "review_fields": (
                    *self.review_fields,
                    field,
                )
            }
        )

    def set_review_fields(
        self,
        fields: tuple[ReviewField, ...],
    ) -> Self:
        """Return a new aggregate containing the complete review field set."""

        field_ids = [field.field_id for field in fields]
        if len(field_ids) != len(set(field_ids)):
            raise ValueError("review field identities must be unique")

        return self.model_copy(update={"review_fields": fields})

    def replace_review_field(
        self,
        field: ReviewField,
    ) -> Self:
        """Return a new aggregate with one review field replaced."""

        fields = list(self.review_fields)

        for index, current in enumerate(fields):
            if current.field_id == field.field_id:
                fields[index] = field

                return self.model_copy(
                    update={
                        "review_fields": tuple(fields),
                    }
                )

        raise KeyError(field.field_id)

    def set_deficiency_candidates(
        self,
        candidates: tuple[DeficiencyCandidate, ...],
    ) -> Self:
        """Return a new aggregate containing extracted deficiency candidates."""

        candidate_ids = [
            candidate.candidate_id
            for candidate in candidates
        ]

        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError(
                "deficiency candidate identities must be unique"
            )

        return self.model_copy(
            update={
                "deficiency_candidates": candidates,
            }
        )

    def approve_poc(
        self,
        *,
        reviewed_revision_id: str,
        actor_id: str,
        actor_role: str,
        approved_at: datetime,
    ) -> tuple[Self, ApprovalDecision]:
        """Approve the complete current POC revision or preserve existing state."""

        revision = (
            self.poc_draft.current_revision
            if self.poc_draft
            else None
        )

        blockers = collect_approval_blockers(
            revision,
            reviewed_revision_id=reviewed_revision_id,
            actor_role=actor_role,
            has_evidence=bool(self.approval_evidence),
        )

        if blockers:
            return self, ApprovalDecision(
                approval=self.approval,
                blockers=blockers,
            )

        assert revision is not None

        if (
            self.approval.status == "approved"
            and self.approval.revision_id == revision.revision_id
        ):
            return self, ApprovalDecision(
                approval=self.approval,
            )

        approval = ApprovalState.approved(
            revision_id=revision.revision_id,
            approved_by=actor_id,
            approved_at=approved_at,
        )

        updated = self.model_copy(
            update={
                "approval": approval,
            }
        )

        return updated, ApprovalDecision(
            approval=approval,
        )

    def attach_poc_draft(self, draft: PocDraft) -> Self:
        """Make a generated POC draft and its reviewed evidence approval-ready."""
        evidence_ids = tuple(
            f"{field.field_id}:p{evidence.page_number}"
            for field in self.review_fields
            if field.deficiency_id == draft.deficiency_id
            for evidence in field.evidence_items
        )
        return self.model_copy(
            update={
                "poc_draft": draft,
                "poc_drafts": (*self.poc_drafts, draft.current_revision_id),
                "approval_evidence": tuple(dict.fromkeys(evidence_ids)),
                "approval": ApprovalState(),
            }
        )

    def request_poc_changes(
        self,
    ) -> tuple[Self, ReapprovalDecision]:
        """Return the current POC to editing with export disabled."""

        approval = ApprovalState(
            status="changes_requested"
        )

        updated = self.model_copy(
            update={
                "approval": approval,
            }
        )

        return updated, ReapprovalDecision(
            approval=approval,
            workflow_state="editing",
        )

    def save_poc_edit(
        self,
        *,
        expected_revision_id: str,
        revision_id: str,
        section_updates: dict[
            PocSectionName,
            str | None,
        ],
    ) -> tuple[Self, ReapprovalDecision]:
        """Append an edit and invalidate approval in the same aggregate update."""

        if self.poc_draft is None:
            raise ValueError(
                "a POC draft is required before editing"
            )

        draft = self.poc_draft.append_edit(
            expected_revision_id=expected_revision_id,
            revision_id=revision_id,
            section_updates=section_updates,
        )

        status = (
            "reapproval_required"
            if self.approval.status == "approved"
            else "unapproved"
        )

        approval = ApprovalState(
            status=status
        )

        updated = self.model_copy(
            update={
                "poc_draft": draft,
                "approval": approval,
            }
        )

        workflow_state = (
            "reapproval_required"
            if status == "reapproval_required"
            else "editing"
        )

        return updated, ReapprovalDecision(
            approval=approval,
            workflow_state=workflow_state,
        )

    def edit_extracted_field(
        self,
        *,
        field_id: str,
        expected_revision_id: str,
        revision_id: str,
        value: str,
    ) -> Self:
        """Return a new aggregate with one field edit appended."""

        for index, field in enumerate(self.extracted_fields):
            if field.field_id == field_id:
                updated = field.append_edit(
                    expected_revision_id=expected_revision_id,
                    revision_id=revision_id,
                    value=value,
                )

                fields = list(
                    self.extracted_fields
                )

                fields[index] = updated

                return self.model_copy(
                    update={
                        "extracted_fields": tuple(fields),
                    }
                )

        raise KeyError(field_id)