import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from cms_planner.application.ports.provider_extraction import (
    ProviderCandidate,
    ProviderExtractionResponse,
)


def candidate(provider: str, *, page_number: int, uncertainty: bool) -> ProviderCandidate:
    return ProviderCandidate(
        provider=provider,
        page_number=page_number,
        snippet=f"Evidence for {provider}",
        confidence=0.75,
        uncertainty=uncertainty,
    )


def test_candidate_requires_closed_evidence_linked_shape() -> None:
    with pytest.raises(ValidationError):
        ProviderCandidate(
            provider="North Clinic",
            page_number=2,
            snippet="North Clinic is the provider",
            confidence=0.9,
            uncertainty=False,
            provider_sdk="not-permitted",
        )


def test_response_preserves_conflicting_candidates_as_uncertain() -> None:
    response = ProviderExtractionResponse(
        candidates=(
            candidate("North Clinic", page_number=2, uncertainty=True),
            candidate("North Clinical Group", page_number=5, uncertainty=True),
        )
    )

    assert tuple(item.provider for item in response.candidates) == (
        "North Clinic",
        "North Clinical Group",
    )


def test_response_rejects_conflict_not_marked_uncertain() -> None:
    with pytest.raises(ValidationError, match="must be uncertain"):
        ProviderExtractionResponse(
            candidates=(
                candidate("North Clinic", page_number=2, uncertainty=False),
                candidate("North Clinical Group", page_number=5, uncertainty=True),
            )
        )


def test_json_schema_is_closed_and_requires_evidence_fields() -> None:
    schema_path = (
        Path(__file__).parents[2]
        / "src/cms_planner/application/ports/extraction_schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    candidate_schema = schema["$defs"]["providerCandidate"]

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False
    assert candidate_schema["additionalProperties"] is False
    assert set(candidate_schema["required"]) == {
        "provider",
        "page_number",
        "snippet",
        "confidence",
        "uncertainty",
    }