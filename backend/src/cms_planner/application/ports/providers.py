"""Application-owned contracts for minimum-necessary provider operations."""

from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.deficiency import EvidenceSpan, ReviewedField
from cms_planner.domain.poc import GroundedClaim, MissingInformationMarker, PocContent

ExtractedFieldName = Literal["provider_name", "f_tag", "sod"]


class ExtractionPage(BaseModel):
    """One required page and its bounded extracted text."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    page_number: int = Field(ge=1)
    text: str = Field(min_length=1)


class ExtractionRequest(BaseModel):
    """Closed extraction payload containing only requested pages and fields."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    pages: tuple[ExtractionPage, ...] = Field(min_length=1)
    fields: tuple[ExtractedFieldName, ...] = Field(min_length=1)


class ExtractionResult(BaseModel):
    """Provider-neutral extraction values with explicit uncertainty."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    provider_name: str = Field(min_length=1)
    f_tag: str = Field(min_length=1)
    sod: str = Field(min_length=1)
    uncertain_fields: tuple[ExtractedFieldName, ...] = ()


class PocGenerationRequest(BaseModel):
    """Reviewed fields and evidence permitted for one POC generation call."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    deficiency_revision_id: str = Field(min_length=1)
    reviewed_fields: tuple[ReviewedField, ...] = ()
    evidence: tuple[EvidenceSpan, ...] = ()


class PocGenerationResult(BaseModel):
    """Closed five-part POC result with deterministic grounding metadata."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    content: PocContent
    claims: tuple[GroundedClaim, ...] = ()
    missing_information: tuple[MissingInformationMarker, ...] = ()


class ExtractionPort(Protocol):
    async def extract(self, request: ExtractionRequest) -> ExtractionResult: ...


class PocGenerationPort(Protocol):
    async def generate(
        self,
        request: PocGenerationRequest,
    ) -> PocGenerationResult: ...