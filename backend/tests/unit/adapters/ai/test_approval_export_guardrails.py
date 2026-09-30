from datetime import UTC, datetime

import pytest

from cms_planner.adapters.ai.approval_guardrails import guard_approval_output
from cms_planner.adapters.ai.export_guardrails import guard_export_output
from cms_planner.domain.approval import ApprovalState
from tests.unit.domain.test_approval import complete_draft


def approved_state() -> ApprovalState:
    return ApprovalState.approved(
        revision_id="revision-4",
        approved_by="leader-1",
        approved_at=datetime(2026, 9, 24, tzinfo=UTC),
    )


def test_provider_cannot_assert_approval_authority() -> None:
    result = guard_approval_output(
        {"candidate_text": "Candidate", "approval_status": "approved"},
        ApprovalState(),
    )

    assert result.approval_status == "unapproved"
    assert result.approved_revision_id is None


def test_authoritative_approval_can_mark_guarded_output_approved() -> None:
    result = guard_approval_output(
        {"candidate_text": "Candidate"},
        approved_state(),
    )

    assert result.approval_status == "approved"
    assert result.approved_revision_id == "revision-4"


def test_export_guard_rejects_stale_backend_approval() -> None:
    stale = approved_state().model_copy(update={"revision_id": "revision-3"})

    with pytest.raises(PermissionError, match="stale_approval"):
        guard_export_output(
            {"candidate_text": "Provider says export ready"},
            draft=complete_draft(),
            approval=stale,
        )


def test_export_guard_passes_only_current_approved_candidate() -> None:
    result = guard_export_output(
        {"candidate_text": "  Current approved candidate  "},
        draft=complete_draft(),
        approval=approved_state(),
    )

    assert result == "Current approved candidate"