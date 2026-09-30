"""Validate deficiency candidates against retained extraction boundaries."""

from collections.abc import Mapping
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

from cms_planner.application.ports.deficiency_extraction import (
    DeficiencyExtractionRequest,
    DeficiencyExtractionResponse,
)
from cms_planner.domain.deficiency_candidate import (
    DeficiencyCandidate,
    DeficiencyCandidateEvidence,
)


class _ValidationEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    request: DeficiencyExtractionRequest
    response: DeficiencyExtractionResponse

    @model_validator(mode="after")
    def validate_against_boundaries(self) -> Self:
        boundaries = {item.boundary_id: item for item in self.request.boundaries}
        candidate_ids = [item.boundary_id for item in self.response.candidates]
        if candidate_ids != list(boundaries):
            raise ValueError("candidate boundaries must exactly match retained boundaries")
        for candidate in self.response.candidates:
            boundary = boundaries[candidate.boundary_id]
            if candidate.f_tag != boundary.f_tag:
                raise ValueError("candidate F-tag must match its retained boundary")
            if not boundary.complete and candidate.sod_text is not None:
                raise ValueError("incomplete boundaries cannot acquire SOD text")
            retained_pages = {item.page_number for item in boundary.evidence}
            if any(
                item.page_number not in retained_pages for item in candidate.evidence
            ):
                raise ValueError("candidate evidence must use retained boundary pages")
        return self


def validate_deficiency_candidates(
    request: DeficiencyExtractionRequest,
    response: object,
) -> tuple[DeficiencyCandidate, ...]:
    """Return candidates only after the complete response matches its request."""
    normalized = _normalize_response(response)
    validated = _ValidationEnvelope(
        request=request,
        response=DeficiencyExtractionResponse.model_validate(normalized),
    )
    pattern = request.layout.pattern
    assert pattern is not None
    return tuple(
        DeficiencyCandidate(
            candidate_id=item.candidate_id,
            boundary_id=item.boundary_id,
            layout_pattern=pattern,
            f_tag=item.f_tag,
            sod_text=item.sod_text,
            evidence=tuple(
                DeficiencyCandidateEvidence(**evidence.model_dump())
                for evidence in item.evidence
            ),
            confidence=item.confidence,
            uncertainty=item.uncertainty,
            confirmed=item.confirmed,
        )
        for item in validated.response.candidates
    )


def _normalize_response(response: object) -> object:
    if not isinstance(response, Mapping) or not isinstance(
        response.get("candidates"), list
    ):
        return response
    candidates = []
    for candidate in response["candidates"]:
        if isinstance(candidate, Mapping) and isinstance(candidate.get("evidence"), list):
            candidate = {**candidate, "evidence": tuple(candidate["evidence"])}
        candidates.append(candidate)
    return {**response, "candidates": tuple(candidates)}