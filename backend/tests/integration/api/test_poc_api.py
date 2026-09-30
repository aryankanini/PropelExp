from pathlib import Path

from fastapi.testclient import TestClient

from cms_planner.adapters.repositories.in_memory_poc_repository import InMemoryPocRepository
from cms_planner.app import create_app
from cms_planner.domain.deficiency import Deficiency, DeficiencyRevision
from cms_planner.domain.poc import PocSectionName
from cms_planner.domain.poc_generation import PocGenerationInput
from cms_planner.domain.review import (
    Evidence,
    HighlightCoordinates,
    Origin,
    ReviewCandidate,
    ReviewField,
    ReviewRevision,
)
from domain.case.aggregate import CaseAggregate


class StubProvider:
    def generate(self, request: PocGenerationInput) -> object:
        return {
            "sections": [
                {
                    "name": section.value,
                    "statements": [
                        {"kind": "generic_guidance", "text": f"Guidance for {section.value}."}
                    ],
                }
                for section in PocSectionName
            ]
        }


def confirmed_deficiency() -> Deficiency:
    revision = DeficiencyRevision(revision_id="def-rev-1", confirmed=True)
    return Deficiency(
        deficiency_id="deficiency-1",
        revisions=(revision,),
        current_revision_id=revision.revision_id,
    )


def test_generate_edit_and_stale_conflict_contract(tmp_path: Path) -> None:
    repository = InMemoryPocRepository()
    repository.add_deficiency(confirmed_deficiency())
    app = create_app(
        tmp_path,
        poc_repository=repository,
        poc_provider=StubProvider(),
    )

    with TestClient(app, raise_server_exceptions=False) as client:
        generated = client.post("/deficiencies/deficiency-1/poc")
        revision_id = generated.json()["current_revision_id"]
        edited = client.patch(
            "/deficiencies/deficiency-1/poc",
            json={
                "expected_revision_id": revision_id,
                "section_updates": {"monitoring": "Audit daily."},
            },
        )
        stale = client.patch(
            "/deficiencies/deficiency-1/poc",
            json={
                "expected_revision_id": revision_id,
                "section_updates": {"monitoring": "Overwrite."},
            },
        )

    assert generated.status_code == 200
    assert edited.status_code == 200
    assert edited.json()["revisions"][-1]["section_origins"]["monitoring"] == "user_edited"
    assert stale.status_code == 409
    assert stale.json()["code"] == "stale_revision"
    assert stale.json()["action"] == "reload"
    assert repository.get_draft("deficiency-1").current_revision_id == edited.json()[
        "current_revision_id"
    ]


def test_confirm_generate_and_attach_draft_for_approval(tmp_path: Path) -> None:
    app = create_app(tmp_path, poc_provider=StubProvider())
    evidence = Evidence(
        page_number=4,
        full_snippet="F0686 complete statement of deficiency",
        highlight=HighlightCoordinates(x=0, y=0, width=1, height=1),
        source="native-text",
    )
    revision = ReviewRevision(
        revision_id="review-revision-1",
        revision_number=1,
        value="Complete statement of deficiency",
        origin=Origin.EXTRACTED,
        evidence=evidence,
    )
    field = ReviewField(
        field_id="deficiency-1",
        label="F0686",
        deficiency_id="deficiency-1",
        field_type="sod",
        candidates=(
            ReviewCandidate(
                candidate_id="candidate-1",
                value=revision.value,
                confidence=0.95,
                origin=Origin.EXTRACTED,
                evidence=evidence,
            ),
        ),
        revisions=(revision,),
        evidence_items=(evidence,),
        current_revision_id=revision.revision_id,
    )
    app.state.repository.add(
        CaseAggregate(
            session_id="session-1",
            case_id="case-1",
            review_fields=(field,),
        )
    )

    with TestClient(app, raise_server_exceptions=False) as client:
        confirmed = client.patch(
            "/sessions/session-1/deficiencies/deficiency-1/confirmation",
            json={
                "deficiency_id": "deficiency-1",
                "expected_revisions": [
                    {
                        "field_id": field.field_id,
                        "revision_id": revision.revision_id,
                    }
                ],
            },
        )
        generated = client.post(
            "/deficiencies/deficiency-1/poc",
            headers={"X-Session-ID": "session-1"},
        )
        approved = client.post(
            "/api/v1/cases/case-1/approval",
            headers={
                "X-Session-ID": "session-1",
                "X-Actor-ID": "leader-1",
                "X-Actor-Role": "compliance_leader",
            },
            json={"revision_id": generated.json().get("current_revision_id", "missing")},
        )
        retained = app.state.repository.get("session-1")

    assert confirmed.status_code == 200
    assert confirmed.json()["poc_generation_eligible"] is True
    assert generated.status_code == 200
    assert retained is not None
    assert retained.poc_draft is not None
    assert retained.poc_draft.current_revision_id == generated.json()["current_revision_id"]
    assert approved.status_code == 200
    assert approved.json()["copy_enabled"] is True