"""Closed provider payload schemas for minimum-necessary AI requests."""

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.application.ports.providers import ExtractedFieldName
from cms_planner.domain.deficiency import EvidenceSpan, ReviewedField


class ProviderExtractionPage(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    page_number: int = Field(ge=1)
    text: str = Field(min_length=1)


class ProviderExtractionRequest(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    pages: tuple[ProviderExtractionPage, ...] = Field(min_length=1)
    fields: tuple[ExtractedFieldName, ...] = Field(min_length=1)


class ProviderPocRequest(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    deficiency_revision_id: str = Field(min_length=1)
    reviewed_fields: tuple[ReviewedField, ...] = ()
    evidence: tuple[EvidenceSpan, ...] = ()