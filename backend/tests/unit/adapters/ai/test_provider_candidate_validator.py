import pytest
from pydantic import ValidationError

from cms_planner.adapters.ai.provider_candidate_validator import (
    validate_provider_candidates,
)


def candidate(
    provider: str,
    *,
    page_number: int = 3,
    snippet: str = "Provider evidence",
    confidence: float = 0.8,
    uncertainty: bool = False,
) -> dict[str, object]:
    return {
        "provider": provider,
        "page_number": page_number,
        "snippet": snippet,
        "confidence": confidence,
        "uncertainty": uncertainty,
    }


def test_accepts_complete_evidence_linked_candidate() -> None:
    candidates = validate_provider_candidates(
        {"candidates": [candidate("North Clinic")]}
    )

    assert candidates[0].provider == "North Clinic"
    assert candidates[0].page_number == 3
    assert candidates[0].snippet == "Provider evidence"
    assert candidates[0].confidence == 0.8
    assert candidates[0].uncertainty is False


@pytest.mark.parametrize("missing_field", ["page_number", "snippet"])
def test_rejects_candidate_missing_evidence(missing_field: str) -> None:
    invalid_candidate = candidate("North Clinic")
    del invalid_candidate[missing_field]

    with pytest.raises(ValidationError):
        validate_provider_candidates({"candidates": [invalid_candidate]})


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_rejects_confidence_outside_unit_interval(confidence: float) -> None:
    with pytest.raises(ValidationError):
        validate_provider_candidates(
            {"candidates": [candidate("North Clinic", confidence=confidence)]}
        )


def test_preserves_conflicting_provider_names_as_separate_candidates() -> None:
    candidates = validate_provider_candidates(
        {
            "candidates": [
                candidate("North Clinic", uncertainty=True),
                candidate(
                    "North Clinical Group",
                    page_number=7,
                    uncertainty=True,
                ),
            ]
        }
    )

    assert tuple(item.provider for item in candidates) == (
        "North Clinic",
        "North Clinical Group",
    )
    assert all(item.uncertainty for item in candidates)


def test_rejects_complete_response_when_any_candidate_lacks_evidence() -> None:
    invalid_candidate = candidate("North Clinical Group", uncertainty=True)
    del invalid_candidate["snippet"]

    with pytest.raises(ValidationError):
        validate_provider_candidates(
            {
                "candidates": [
                    candidate("North Clinic", uncertainty=True),
                    invalid_candidate,
                ]
            }
        )