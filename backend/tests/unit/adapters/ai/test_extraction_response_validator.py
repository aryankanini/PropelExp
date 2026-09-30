from copy import deepcopy

from cms_planner.adapters.ai.extraction_response_validator import (
    ValidatedExtractionResponse,
    validate_extraction_response,
)
from cms_planner.application.ports.deficiency_extraction import (
    DeficiencyExtractionRequest,
)
from cms_planner.domain.cms_layout import CmsLayout, CmsLayoutPattern, CmsLayoutStatus
from cms_planner.modules.extraction.deficiency_boundaries import (
    BoundaryEvidence,
    DeficiencyBoundary,
)
from cms_planner.modules.extraction.schema_failure import ExtractionSchemaFailure


def extraction_request() -> DeficiencyExtractionRequest:
    return DeficiencyExtractionRequest(
        layout=CmsLayout(
            status=CmsLayoutStatus.RECOGNIZED,
            pattern=CmsLayoutPattern.CMS_2567,
            marker_page_numbers=(1,),
        ),
        boundaries=(
            DeficiencyBoundary(
                boundary_id="cms-2567:0001",
                f_tag="F0686",
                sod_text="Complete SOD text",
                evidence=(BoundaryEvidence(page_number=2, text="F 0686 evidence"),),
                complete=True,
                uncertainty=False,
                confirmed=False,
            ),
        ),
    )


def valid_response() -> dict[str, object]:
    return {
        "provider_candidates": [
            {
                "provider": "North Clinic",
                "page_number": 1,
                "snippet": "North Clinic is the provider",
                "confidence": 0.91,
                "uncertainty": False,
            }
        ],
        "deficiency_candidates": [
            {
                "candidate_id": "candidate:0001",
                "boundary_id": "cms-2567:0001",
                "f_tag": "F0686",
                "sod_text": "Complete SOD text",
                "evidence": [
                    {
                        "evidence_id": "candidate:0001:evidence:1",
                        "page_number": 2,
                        "text": "F 0686 evidence",
                    }
                ],
                "confidence": 0.82,
                "uncertainty": False,
            }
        ],
    }


def test_validates_complete_response_as_unconfirmed_candidates() -> None:
    result = validate_extraction_response(extraction_request(), valid_response())

    assert isinstance(result, ValidatedExtractionResponse)
    assert result.provider_candidates[0].provider == "North Clinic"
    assert result.deficiency_candidates[0].confirmed is False


def test_returns_one_safe_failure_without_partial_candidates() -> None:
    response = deepcopy(valid_response())
    response["deficiency_candidates"][0]["confidence"] = 1.01  # type: ignore[index]

    result = validate_extraction_response(extraction_request(), response)

    assert result == ExtractionSchemaFailure()
    assert result.model_dump() == {"code": "invalid_extraction_response"}
