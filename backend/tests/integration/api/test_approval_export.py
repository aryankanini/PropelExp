from datetime import UTC, datetime

from fastapi.testclient import TestClient

from cms_planner.app import create_app
from cms_planner.domain.approval import ApprovalState
from cms_planner.domain.export_label import DRAFT_EXPORT_PREFIX
from cms_planner.domain.poc import (
    POC_SECTION_ORDER,
    PocContent,
    PocDraft,
    PocRevision,
    SectionOrigin,
)
from domain.case.aggregate import CaseAggregate


def draft(revision_id: str = "revision-4") -> PocDraft:
    revision = PocRevision(
        revision_id=revision_id,
        deficiency_revision_id="deficiency-revision-1",
        content=PocContent(
            affected_residents="Affected residents",
            others_at_risk="Other residents at risk",
            corrective_measures="Corrective measures",
            monitoring="Monitoring",
            completion_date="2026-10-01",
        ),
        section_origins={name: SectionOrigin.USER_EDITED for name in POC_SECTION_ORDER},
    )
    return PocDraft(
        deficiency_id="F689",
        revisions=(revision,),
        current_revision_id=revision_id,
    )


def seed_case(app, approval: ApprovalState | None = None) -> None:
    app.state.repository.add(
        CaseAggregate(
            session_id="session-1",
            case_id="case-1",
            poc_draft=draft(),
            approval_evidence=("page-3",),
            approval=approval or ApprovalState(),
        )
    )


def leader_headers() -> dict[str, str]:
    return {
        "X-Session-ID": "session-1",
        "X-Actor-ID": "leader-1",
        "X-Actor-Role": "compliance_leader",
    }


def test_approval_enables_labeled_copy_and_download() -> None:
    app = create_app()
    seed_case(app)
    client = TestClient(app)

    approved = client.post(
        "/api/v1/cases/case-1/approval",
        headers=leader_headers(),
        json={"revision_id": "revision-4"},
    )
    copied = client.get(
        "/api/v1/cases/case-1/export?format=copy",
        headers={"X-Session-ID": "session-1"},
    )
    downloaded = client.get(
        "/api/v1/cases/case-1/export?format=download",
        headers={"X-Session-ID": "session-1"},
    )

    assert approved.status_code == 200
    assert approved.json()["copy_enabled"] is True
    assert copied.status_code == 200
    assert copied.json()["content"].startswith(DRAFT_EXPORT_PREFIX)
    assert "Affected Residents\n" not in copied.json()["content"]
    assert "Corrective Measures\n" not in copied.json()["content"]
    assert "Affected residents\n\nOther residents at risk" in copied.json()["content"]
    assert downloaded.status_code == 200
    assert downloaded.json()["filename"] == "approved-poc-draft.txt"


def test_stale_approval_request_returns_blocker_without_mutation() -> None:
    existing = ApprovalState.approved(
        revision_id="revision-4",
        approved_by="leader-1",
        approved_at=datetime(2026, 9, 24, tzinfo=UTC),
    )
    app = create_app()
    seed_case(app, existing)
    client = TestClient(app)

    response = client.post(
        "/api/v1/cases/case-1/approval",
        headers=leader_headers(),
        json={"revision_id": "revision-3"},
    )

    retained = app.state.repository.get("session-1")
    assert response.status_code == 409
    assert response.json()["blockers"][0]["code"] == "stale_revision"
    assert retained is not None
    assert retained.approval == existing


def test_saved_edit_revokes_approval_and_blocks_export() -> None:
    existing = ApprovalState.approved(
        revision_id="revision-4",
        approved_by="leader-1",
        approved_at=datetime(2026, 9, 24, tzinfo=UTC),
    )
    app = create_app()
    seed_case(app, existing)
    client = TestClient(app)

    edited = client.patch(
        "/api/v1/cases/case-1/poc",
        headers={"X-Session-ID": "session-1"},
        json={
            "expected_revision_id": "revision-4",
            "revision_id": "revision-5",
            "section_updates": {"monitoring": "Audit daily."},
        },
    )
    exported = client.get(
        "/api/v1/cases/case-1/export?format=copy",
        headers={"X-Session-ID": "session-1"},
    )

    assert edited.status_code == 200
    assert edited.json()["workflow_state"] == "reapproval_required"
    assert exported.status_code == 409
    assert exported.json()["blocker"]["code"] == "approval_required"


def test_reviewer_cannot_approve() -> None:
    app = create_app()
    seed_case(app)
    client = TestClient(app)
    headers = leader_headers() | {"X-Actor-Role": "compliance_reviewer"}

    response = client.post(
        "/api/v1/cases/case-1/approval",
        headers=headers,
        json={"revision_id": "revision-4"},
    )

    assert response.status_code == 409
    assert response.json()["blockers"][0]["code"] == "unauthorized"
    assert response.json()["copy_enabled"] is False