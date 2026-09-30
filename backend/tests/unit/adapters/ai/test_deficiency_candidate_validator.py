import pytest
from pydantic import ValidationError

from cms_planner.adapters.ai.deficiency_candidate_validator import (
    validate_deficiency_candidates,
)
from cms_planner.application.ports.deficiency_extraction import (
    DeficiencyExtractionRequest,
)
from cms_planner.domain.cms_layout import CmsLayout, CmsLayoutPattern, CmsLayoutStatus
from cms_planner.modules.extraction.deficiency_boundaries import (
    BoundaryEvidence,
    DeficiencyBoundary,
)


def request(*, complete: bool = True) -> DeficiencyExtractionRequest:
    layout = CmsLayout(
        status=CmsLayoutStatus.RECOGNIZED,
        pattern=CmsLayoutPattern.CMS_2567,
        marker_page_numbers=(1,),
    )
    boundary = DeficiencyBoundary(
        boundary_id="cms-2567:0001",
        f_tag="F0686",
        sod_text="Complete SOD" if complete else None,
        evidence=(BoundaryEvidence(page_number=2, text="F 0686 evidence"),),
        complete=complete,
        uncertainty=not complete,
        confirmed=False,
    )
    return DeficiencyExtractionRequest(layout=layout, boundaries=(boundary,))


def payload(*, page_number: int = 2, sod_text: str | None = "Complete SOD") -> dict[str, object]:
    complete = sod_text is not None
    return {
        "candidates": [
            {
                "candidate_id": "candidate:0001",
                "boundary_id": "cms-2567:0001",
                "f_tag": "F0686",
                "sod_text": sod_text,
                "evidence": [
                    {
                        "evidence_id": "candidate:0001:evidence:1",
                        "page_number": page_number,
                        "text": "F 0686 evidence",
                    }
                ],
                "confidence": 0.82,
                "uncertainty": not complete,
                "confirmed": False,
            }
        ]
    }


def test_accepts_complete_evidence_linked_candidate() -> None:
    candidates = validate_deficiency_candidates(request(), payload())

    assert candidates[0].candidate_id == "candidate:0001"
    assert candidates[0].boundary_id == "cms-2567:0001"


def test_accepts_incomplete_candidate_only_as_uncertain_unconfirmed() -> None:
    candidates = validate_deficiency_candidates(
        request(complete=False),
        payload(sod_text=None),
    )

    assert candidates[0].uncertainty is True
    assert candidates[0].confirmed is False


def test_rejects_candidate_evidence_outside_retained_boundary() -> None:
    with pytest.raises(ValidationError, match="retained boundary pages"):
        validate_deficiency_candidates(request(), payload(page_number=9))


def test_rejects_missing_or_unrelated_boundary_candidate() -> None:
    invalid = payload()
    invalid["candidates"][0]["boundary_id"] = "cms-2567:9999"  # type: ignore[index]

    with pytest.raises(ValidationError, match="exactly match retained boundaries"):
        validate_deficiency_candidates(request(), invalid)


def test_validates_zero_boundary_response_atomically() -> None:
    empty_request = DeficiencyExtractionRequest(layout=request().layout, boundaries=())
    assert validate_deficiency_candidates(empty_request, {"candidates": []}) == ()