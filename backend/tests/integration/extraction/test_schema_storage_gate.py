from typing import Any

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
from cms_planner.modules.extraction.store_extraction_result import (
    ExtractionResult,
    store_extraction_result,
)


class RecordingStore:
    storage_kind = "memory"

    def __init__(self) -> None:
        self.saved: list[ExtractionResult] = []

    def save(self, result: ExtractionResult) -> None:
        self.saved.append(result)


def request() -> DeficiencyExtractionRequest:
    layout = CmsLayout(
        status=CmsLayoutStatus.RECOGNIZED,
        pattern=CmsLayoutPattern.CMS_2567,
        marker_page_numbers=(1,),
    )
    return DeficiencyExtractionRequest(
        layout=layout,
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


def response() -> dict[str, Any]:
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


def test_valid_response_is_stored_atomically_as_unconfirmed() -> None:
    extraction_request = request()
    outcome = validate_extraction_response(extraction_request, response())
    store = RecordingStore()

    assert isinstance(outcome, ValidatedExtractionResponse)
    stored = store_extraction_result(
        store,
        case_id="case-1",
        layout=extraction_request.layout,
        candidates=outcome.deficiency_candidates,
    )

    assert store.saved == [stored]
    assert all(not candidate.confirmed for candidate in stored.candidates)


def test_invalid_response_returns_one_failure_and_causes_zero_writes() -> None:
    invalid = response()
    del invalid["provider_candidates"][0]["uncertainty"]
    store = RecordingStore()

    outcome = validate_extraction_response(request(), invalid)

    assert outcome == ExtractionSchemaFailure()
    assert store.saved == []
