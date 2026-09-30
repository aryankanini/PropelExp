"""Provider-neutral contract for evidence-linked deficiency extraction."""

from typing import Protocol, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from cms_planner.domain.cms_layout import CmsLayout, CmsLayoutPattern, CmsLayoutStatus
from cms_planner.modules.extraction.deficiency_boundaries import DeficiencyBoundary


class DeficiencyEvidencePayload(BaseModel):
    """One stable source evidence item returned by an extraction adapter."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    evidence_id: str = Field(min_length=1)
    page_number: int = Field(ge=1)
    text: str = Field(min_length=1)


class DeficiencyCandidatePayload(BaseModel):
    """One provider-neutral deficiency candidate response value."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    candidate_id: str = Field(min_length=1)
    boundary_id: str = Field(min_length=1)
    f_tag: str = Field(pattern=r"^[A-Z]\d{4}$")
    sod_text: str | None
    evidence: tuple[DeficiencyEvidencePayload, ...] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    uncertainty: bool
    confirmed: bool

    @model_validator(mode="after")
    def validate_incomplete_sod(self) -> Self:
        if self.sod_text is None and (not self.uncertainty or self.confirmed):
            raise ValueError("incomplete SOD must be uncertain and unconfirmed")
        return self


class DeficiencyExtractionRequest(BaseModel):
    """Recognized layout and bounded evidence permitted at the adapter boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    layout: CmsLayout
    boundaries: tuple[DeficiencyBoundary, ...]

    @model_validator(mode="after")
    def validate_layout(self) -> Self:
        if (
            self.layout.status is not CmsLayoutStatus.RECOGNIZED
            or self.layout.pattern is not CmsLayoutPattern.CMS_2567
        ):
            raise ValueError("extraction requires a recognized CMS-2567 layout")
        return self


class DeficiencyExtractionResponse(BaseModel):
    """Complete adapter response validated as one closed unit."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    candidates: tuple[DeficiencyCandidatePayload, ...]

    @model_validator(mode="after")
    def validate_stable_identities(self) -> Self:
        candidate_ids = [item.candidate_id for item in self.candidates]
        evidence_ids = [
            evidence.evidence_id
            for item in self.candidates
            for evidence in item.evidence
        ]
        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("candidate identities must be unique")
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("evidence identities must be unique")
        return self


class DeficiencyExtractionPort(Protocol):
    """Extract structured deficiencies through any approved adapter."""

    async def extract(
        self,
        request: DeficiencyExtractionRequest,
    ) -> DeficiencyExtractionResponse: ...
