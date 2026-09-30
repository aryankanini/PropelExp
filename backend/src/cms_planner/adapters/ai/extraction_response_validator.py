"""Validate complete extraction responses before candidates enter case state."""

from collections.abc import Mapping
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from cms_planner.adapters.ai.deficiency_candidate_validator import (
    validate_deficiency_candidates,
)
from cms_planner.adapters.ai.provider_candidate_validator import (
    validate_provider_candidates,
)
from cms_planner.application.ports.deficiency_extraction import (
    DeficiencyCandidatePayload,
    DeficiencyExtractionRequest,
)
from cms_planner.application.ports.provider_extraction import ProviderCandidate
from cms_planner.domain.deficiency_candidate import DeficiencyCandidate
from cms_planner.modules.extraction.schema_failure import ExtractionSchemaFailure


class ValidatedExtractionResponse(BaseModel):
    """Complete candidate sets admitted by the aggregate response boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    provider_candidates: tuple[ProviderCandidate, ...]
    deficiency_candidates: tuple[DeficiencyCandidate, ...]


class _AggregateExtractionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    provider_candidates: tuple[ProviderCandidate, ...] = Field(min_length=1)
    deficiency_candidates: tuple[DeficiencyCandidatePayload, ...]

    @field_validator("provider_candidates", mode="before")
    @classmethod
    def normalize_provider_collection(cls, value: object) -> object:
        return tuple(value) if isinstance(value, list) else value

    @field_validator("deficiency_candidates", mode="before")
    @classmethod
    def normalize_deficiency_collection(cls, value: object) -> object:
        if not isinstance(value, list):
            return value
        return tuple(_normalize_deficiency(candidate) for candidate in value)

    @model_validator(mode="after")
    def validate_substantive_text(self) -> Self:
        text_values = (
            *(text for candidate in self.provider_candidates for text in (
                candidate.provider,
                candidate.snippet,
            )),
            *(text for candidate in self.deficiency_candidates for text in (
                candidate.f_tag,
                candidate.sod_text,
                *(evidence.text for evidence in candidate.evidence),
            ) if text is not None),
        )
        if not all(_has_substantive_text(text) for text in text_values):
            raise ValueError("candidate text must contain substantive content")
        return self


def validate_extraction_response(
    request: DeficiencyExtractionRequest,
    response: object,
) -> ValidatedExtractionResponse | ExtractionSchemaFailure:
    """Return both complete candidate sets or one content-free failure."""
    try:
        aggregate = _AggregateExtractionResponse.model_validate(response)
        provider_candidates = validate_provider_candidates(
            {"candidates": aggregate.provider_candidates}
        )
        deficiency_candidates = validate_deficiency_candidates(
            request,
            {"candidates": aggregate.deficiency_candidates},
        )
    except (TypeError, ValueError, ValidationError):
        return ExtractionSchemaFailure()
    return ValidatedExtractionResponse(
        provider_candidates=provider_candidates,
        deficiency_candidates=deficiency_candidates,
    )


def _normalize_deficiency(candidate: object) -> object:
    if not isinstance(candidate, Mapping):
        return candidate
    if "confirmed" in candidate:
        raise ValueError("provider responses cannot set confirmation state")
    evidence = candidate.get("evidence")
    return {
        **candidate,
        "evidence": tuple(evidence) if isinstance(evidence, list) else evidence,
        "confirmed": False,
    }


def _has_substantive_text(value: str) -> bool:
    return any(character.isalnum() for character in value)
