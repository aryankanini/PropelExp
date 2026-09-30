"""Provider-neutral contract for evidence-linked provider extraction."""

from typing import Protocol, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProviderExtractionPage(BaseModel):
    """One normalized source page permitted at the extraction boundary."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    page_number: int = Field(ge=1)
    text: str = Field(min_length=1)


class ProviderCandidate(BaseModel):
    """One provider value with the evidence required for review."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    provider: str = Field(min_length=1)
    page_number: int = Field(ge=1)
    snippet: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    uncertainty: bool


class ProviderExtractionRequest(BaseModel):
    """Minimum normalized page-text payload for provider extraction."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    pages: tuple[ProviderExtractionPage, ...] = Field(min_length=1)


class ProviderExtractionResponse(BaseModel):
    """Ordered provider candidates returned without conflict merging."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    candidates: tuple[ProviderCandidate, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_conflict_uncertainty(self) -> Self:
        distinct_providers = {candidate.provider for candidate in self.candidates}
        if len(distinct_providers) > 1 and any(
            not candidate.uncertainty for candidate in self.candidates
        ):
            raise ValueError("conflicting provider candidates must be uncertain")
        return self


class ProviderExtractionPort(Protocol):
    """Extract evidence-linked provider candidates through any adapter."""

    async def extract(
        self,
        request: ProviderExtractionRequest,
    ) -> ProviderExtractionResponse: ...