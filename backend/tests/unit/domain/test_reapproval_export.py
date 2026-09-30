from datetime import UTC, datetime

import pytest

from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from cms_planner.application.export_approved_revision import (
    ExportApprovedRevision,
    ExportFormattingError,
)
from cms_planner.application.invalidate_approval import RequestChanges, SavePocEdit
from cms_planner.domain.approval import ApprovalState
from cms_planner.domain.export_label import DRAFT_EXPORT_PREFIX, EmptyExportContentError
from cms_planner.domain.export_label import prefix_export_content
from cms_planner.domain.export_policy import ExportBlocker, ExportBlockerCode
from cms_planner.domain.poc import PocSectionName
from domain.case.aggregate import CaseAggregate
from domain.case.revision_errors import StaleRevisionError
from tests.unit.domain.test_approval import complete_draft


APPROVAL = ApprovalState.approved(
    revision_id="revision-4",
    approved_by="leader-1",
    approved_at=datetime(2026, 9, 24, tzinfo=UTC),
)


def approved_case() -> CaseAggregate:
    return CaseAggregate(
        session_id="session-1",
        case_id="case-1",
        poc_draft=complete_draft(),
        approval_evidence=("page-3",),
        approval=APPROVAL,
    )


def test_successful_edit_requires_reapproval_atomically() -> None:
    repository = InMemoryCaseRepository()
    repository.add(approved_case())

    decision = SavePocEdit(repository).execute(
        session_id="session-1",
        expected_revision_id="revision-4",
        revision_id="revision-5",
        section_updates={PocSectionName.MONITORING: "Audit daily."},
    )

    retained = repository.get("session-1")
    assert retained is not None
    assert retained.poc_draft is not None
    assert retained.poc_draft.current_revision_id == "revision-5"
    assert decision.workflow_state == "reapproval_required"
    assert retained.approval.status == "reapproval_required"
    assert retained.approval.export_enabled is False


def test_failed_edit_preserves_approved_revision() -> None:
    repository = InMemoryCaseRepository()
    original = approved_case()
    repository.add(original)

    with pytest.raises(StaleRevisionError):
        SavePocEdit(repository).execute(
            session_id="session-1",
            expected_revision_id="stale",
            revision_id="revision-5",
            section_updates={PocSectionName.MONITORING: "Audit daily."},
        )

    assert repository.get("session-1") == original


def test_request_changes_returns_to_editing() -> None:
    repository = InMemoryCaseRepository()
    repository.add(approved_case())

    decision = RequestChanges(repository).execute(session_id="session-1")

    assert decision.workflow_state == "editing"
    assert decision.approval.status == "changes_requested"
    assert decision.export_enabled is False


def test_export_rechecks_approval_and_prefixes_content() -> None:
    repository = InMemoryCaseRepository()
    repository.add(approved_case())

    result = ExportApprovedRevision(repository).execute(
        session_id="session-1", export_format="copy"
    )

    assert not isinstance(result, ExportBlocker)
    assert result.content.startswith(f"{DRAFT_EXPORT_PREFIX}\n\n")
    assert result.content == (
        f"{DRAFT_EXPORT_PREFIX}\n\n"
        "Affected residents\n\n"
        "Other residents at risk\n\n"
        "Corrective measures\n\n"
        "Monitoring\n\n"
        "2026-10-01"
    )
    assert "Affected Residents\n" not in result.content
    assert "Corrective Measures\n" not in result.content


def test_stale_approval_blocks_export() -> None:
    repository = InMemoryCaseRepository()
    repository.add(
        approved_case().model_copy(
            update={"approval": APPROVAL.model_copy(update={"revision_id": "revision-3"})}
        )
    )

    result = ExportApprovedRevision(repository).execute(
        session_id="session-1", export_format="download"
    )

    assert isinstance(result, ExportBlocker)
    assert result.code is ExportBlockerCode.STALE_APPROVAL


def test_absent_approval_blocks_export() -> None:
    repository = InMemoryCaseRepository()
    repository.add(approved_case().model_copy(update={"approval": ApprovalState()}))

    result = ExportApprovedRevision(repository).execute(
        session_id="session-1", export_format="copy"
    )

    assert isinstance(result, ExportBlocker)
    assert result.code is ExportBlockerCode.APPROVAL_REQUIRED


def test_empty_content_cannot_produce_label_only_export() -> None:
    with pytest.raises(EmptyExportContentError):
        prefix_export_content("   ")


def test_formatting_failure_preserves_approval() -> None:
    repository = InMemoryCaseRepository()
    original = approved_case()
    repository.add(original)

    def fail_formatter(content: str, *, download: bool):
        raise EmptyExportContentError("failed")

    with pytest.raises(ExportFormattingError):
        ExportApprovedRevision(repository, formatter=fail_formatter).execute(
            session_id="session-1", export_format="download"
        )

    assert repository.get("session-1") == original