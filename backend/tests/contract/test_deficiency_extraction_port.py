import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from cms_planner.application.ports.deficiency_extraction import (
    DeficiencyCandidatePayload,
    DeficiencyEvidencePayload,
    DeficiencyExtractionRequest,
    DeficiencyExtractionResponse,
)
from cms_planner.domain.cms_layout import CmsLayout, CmsLayoutPattern, CmsLayoutStatus
from cms_planner.modules.extraction.deficiency_boundaries import (
    BoundaryEvidence,
    DeficiencyBoundary,
)


def layout() -> CmsLayout:
    return CmsLayout(
        status=CmsLayoutStatus.RECOGNIZED,
        pattern=CmsLayoutPattern.CMS_2567,
        marker_page_numbers=(1,),
    )


def boundary(boundary_id: str = "cms-2567:0001") -> DeficiencyBoundary:
    return DeficiencyBoundary(
        boundary_id=boundary_id,
        f_tag="F0686",
        sod_text="Residents did not receive required care.",
        evidence=(BoundaryEvidence(page_number=2, text="F 0686\nResidents did not receive required care."),),
        complete=True,
        uncertainty=False,
        confirmed=False,
    )


def candidate(candidate_id: str, *, sod_text: str | None = "Complete SOD") -> DeficiencyCandidatePayload:
    complete = sod_text is not None
    return DeficiencyCandidatePayload(
        candidate_id=candidate_id,
        boundary_id=candidate_id.replace("candidate", "cms-2567"),
        f_tag="F0686",
        sod_text=sod_text,
        evidence=(
            DeficiencyEvidencePayload(
                evidence_id=f"{candidate_id}:evidence:1",
                page_number=2,
                text="F 0686 evidence",
            ),
        ),
        confidence=0.9,
        uncertainty=not complete,
        confirmed=False,
    )


def test_request_requires_recognized_layout_and_boundaries() -> None:
    request = DeficiencyExtractionRequest(layout=layout(), boundaries=(boundary(),))
    assert request.boundaries[0].boundary_id == "cms-2567:0001"

    with pytest.raises(ValidationError, match="recognized CMS-2567"):
        DeficiencyExtractionRequest(
            layout=CmsLayout(status=CmsLayoutStatus.UNRECOGNIZED),
            boundaries=(),
        )


def test_response_is_closed_and_preserves_repeated_tag_identities() -> None:
    response = DeficiencyExtractionResponse(
        candidates=(candidate("candidate:0001"), candidate("candidate:0002")),
    )

    assert tuple(item.f_tag for item in response.candidates) == ("F0686", "F0686")
    assert response.candidates[0].candidate_id != response.candidates[1].candidate_id
    with pytest.raises(ValidationError):
        DeficiencyCandidatePayload(**candidate("candidate:0003").model_dump(), extra="forbidden")


def test_zero_candidates_is_a_valid_recognized_result() -> None:
    assert DeficiencyExtractionResponse(candidates=()).candidates == ()


def test_incomplete_sod_must_be_uncertain_and_unconfirmed() -> None:
    incomplete = candidate("candidate:0001", sod_text=None)
    assert incomplete.uncertainty is True
    assert incomplete.confirmed is False

    with pytest.raises(ValidationError, match="incomplete SOD"):
        DeficiencyCandidatePayload(
            **{
                **incomplete.model_dump(),
                "uncertainty": False,
            }
        )


def test_json_schema_is_closed_and_requires_evidence_confidence_and_uncertainty() -> None:
    schema_path = Path(__file__).parents[2] / "src/cms_planner/application/ports/deficiency_schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    candidate_schema = schema["$defs"]["deficiencyCandidate"]

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False
    assert candidate_schema["additionalProperties"] is False
    assert {"candidate_id", "boundary_id", "f_tag", "sod_text", "evidence", "confidence", "uncertainty", "confirmed"} == set(candidate_schema["required"])