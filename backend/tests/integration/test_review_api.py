from fastapi import FastAPI
from fastapi.testclient import TestClient

from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from cms_planner.api.confirmations import create_confirmations_router
from cms_planner.api.corrections import create_corrections_router
from cms_planner.api.provenance import create_provenance_router
from cms_planner.api.resolutions import create_resolutions_router
from cms_planner.api.review import create_review_router
from cms_planner.application.confirmation_service import ConfirmationService
from cms_planner.application.correction_service import CorrectionService
from cms_planner.application.provenance_service import ProvenanceService
from cms_planner.application.resolution_service import ResolutionService
from cms_planner.application.review_service import ReviewService
from cms_planner.domain.review import (
    Evidence,
    HighlightCoordinates,
    Origin,
    ReviewCandidate,
    ReviewField,
    ReviewRevision,
)
from domain.case.aggregate import CaseAggregate


def make_field(field_id: str, field_type: str, value: str) -> ReviewField:
    evidence = Evidence(
        page_number=12,
        full_snippet=value,
        highlight=HighlightCoordinates(x=0.1, y=0.2, width=0.5, height=0.2),
        source="native-text",
    )
    revision = ReviewRevision(
        revision_id=f"{field_id}-revision-1",
        revision_number=1,
        value=value,
        origin=Origin.EXTRACTED,
        evidence=evidence,
    )
    candidate = ReviewCandidate(
        candidate_id=f"{field_id}-candidate-1",
        value=value,
        confidence=0.91,
        uncertainty=None,
        origin=Origin.EXTRACTED,
        evidence=evidence,
    )
    return ReviewField(
        field_id=field_id,
        label=field_id,
        deficiency_id="deficiency-1",
        field_type=field_type,
        candidates=(candidate,),
        revisions=(revision,),
        evidence_items=(evidence,),
        current_revision_id=revision.revision_id,
    )


def make_client(*fields: ReviewField) -> TestClient:
    aggregate = CaseAggregate(session_id="session-1", case_id="case-1")
    for field in fields:
        aggregate = aggregate.add_review_field(field)
    repository = InMemoryCaseRepository()
    repository.add(aggregate)
    app = FastAPI()
    app.include_router(create_review_router(ReviewService(repository)))
    app.include_router(create_resolutions_router(ResolutionService(repository)))
    app.include_router(create_corrections_router(CorrectionService(repository)))
    app.include_router(create_confirmations_router(ConfirmationService(repository)))
    app.include_router(create_provenance_router(ProvenanceService(repository)))
    return TestClient(app)


def test_review_response_retains_complete_sod_and_evidence() -> None:
    complete_sod = ("Complete statement of deficiency. " * 1_000).strip()
    field = make_field("field-sod", "sod", complete_sod)

    response = make_client(field).get("/sessions/session-1/review")

    assert response.status_code == 200
    body = response.json()[0]
    assert body["revisions"][0]["value"] == complete_sod
    assert body["revisions"][0]["evidence"]["full_snippet"] == complete_sod
    assert body["evidence_items"][0]["full_snippet"] == complete_sod
    assert body["candidates"][0]["confidence"] == 0.91
    assert body["candidates"][0]["origin"] == "Extracted"


def test_review_returns_typed_not_found_and_unavailable_evidence() -> None:
    field = make_field("field-sod", "sod", "Complete SOD")
    client = make_client(field)

    not_found = client.get("/sessions/missing-session/review")
    assert not_found.status_code == 404
    assert not_found.json()["detail"]["code"] == "case-not-found"

    unavailable = field.model_copy(
        update={
            "revisions": (
                field.current_revision.model_copy(update={"evidence": None}),
            )
        }
    )
    unavailable_client = make_client(unavailable)
    response = unavailable_client.get("/sessions/session-1/review")
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "evidence-unavailable"


def test_stale_resolution_returns_reload_details_without_losing_candidates() -> None:
    field = make_field("field-ftag", "f_tag", "F880")
    client = make_client(field)

    response = client.patch(
        "/sessions/session-1/review-fields/field-ftag/resolution",
        json={
            "kind": "select",
            "expected_revision_id": "stale-revision",
            "candidate_id": "field-ftag-candidate-1",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == {
        "code": "stale-review-revision",
        "message": "Reload the current values before retrying.",
        "current_revision_id": "field-ftag-revision-1",
        "reload_required": True,
    }
    retained = client.get("/sessions/session-1/review").json()[0]
    assert len(retained["candidates"]) == 1
    assert len(retained["revisions"]) == 1


def test_empty_correction_is_rejected_without_revision_increment() -> None:
    field = make_field("field-sod", "sod", "Original SOD")
    client = make_client(field)

    response = client.patch(
        "/sessions/session-1/review-fields/field-sod/correction",
        json={
            "expected_revision_id": "field-sod-revision-1",
            "value": " ",
        },
    )

    assert response.status_code == 422
    retained = client.get("/sessions/session-1/review").json()[0]
    assert len(retained["revisions"]) == 1


def test_incomplete_confirmation_lists_all_blockers_and_contract_errors() -> None:
    field = make_field("field-ftag", "f_tag", "F880").model_copy(
        update={"unresolved": True}
    )
    client = make_client(field)

    response = client.patch(
        "/sessions/session-1/deficiencies/deficiency-1/confirmation",
        json={
            "deficiency_id": "deficiency-1",
            "expected_revisions": [
                {
                    "field_id": "field-ftag",
                    "revision_id": "field-ftag-revision-1",
                }
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["poc_generation_eligible"] is False
    assert [blocker["code"] for blocker in response.json()["blockers"]] == [
        "unresolved",
        "missing-field",
    ]
    responses = client.get("/openapi.json").json()["paths"][
        "/sessions/{session_id}/review"
    ]["get"]["responses"]
    assert {"404", "503"}.issubset(responses)