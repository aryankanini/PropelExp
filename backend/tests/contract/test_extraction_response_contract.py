from copy import deepcopy
from typing import Any

import pytest

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


def request() -> DeficiencyExtractionRequest:
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


def test_accepts_closed_response_only_as_unconfirmed_candidates() -> None:
    result = validate_extraction_response(request(), response())

    assert isinstance(result, ValidatedExtractionResponse)
    assert all(not item.confirmed for item in result.deficiency_candidates)


@pytest.mark.parametrize(
    ("collection", "missing_field"),
    [
        ("provider_candidates", "uncertainty"),
        ("deficiency_candidates", "evidence"),
    ],
)
def test_rejects_entire_response_with_missing_field(
    collection: str,
    missing_field: str,
) -> None:
    invalid = response()
    del invalid[collection][0][missing_field]

    assert validate_extraction_response(request(), invalid) == ExtractionSchemaFailure()


@pytest.mark.parametrize(
    ("collection", "unknown_field"),
    [
        ("provider_candidates", "provider_sdk"),
        ("deficiency_candidates", "confirmed"),
    ],
)
def test_rejects_entire_response_with_unknown_field(
    collection: str,
    unknown_field: str,
) -> None:
    invalid = response()
    invalid[collection][0][unknown_field] = "forbidden"

    assert validate_extraction_response(request(), invalid) == ExtractionSchemaFailure()


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_rejects_out_of_range_confidence_without_clamping(
    confidence: float,
) -> None:
    invalid = response()
    invalid["deficiency_candidates"][0]["confidence"] = confidence

    assert validate_extraction_response(request(), invalid) == ExtractionSchemaFailure()
    assert invalid["deficiency_candidates"][0]["confidence"] == confidence


@pytest.mark.parametrize(
    ("path", "artifact"),
    [
        (("provider_candidates", 0, "provider"), " \u200b\ufeff "),
        (("provider_candidates", 0, "snippet"), "\ufffd"),
        (("deficiency_candidates", 0, "sod_text"), " \u200b "),
        (("deficiency_candidates", 0, "evidence", 0, "text"), "\ufeff"),
    ],
)
def test_rejects_normalization_artifact_only_text(
    path: tuple[str | int, ...],
    artifact: str,
) -> None:
    invalid = deepcopy(response())
    target: Any = invalid
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = artifact

    assert validate_extraction_response(request(), invalid) == ExtractionSchemaFailure()
