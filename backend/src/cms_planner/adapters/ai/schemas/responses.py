"""Closed provider response schemas retained inside the AI adapter boundary."""

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.application.ports.providers import ExtractedFieldName
from cms_planner.domain.poc import GroundedClaim, MissingInformationMarker, PocContent


class ProviderExtractionResponse(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    provider_name: str = Field(min_length=1)
    f_tag: str = Field(min_length=1)
    sod: str = Field(min_length=1)
    uncertain_fields: tuple[ExtractedFieldName, ...] = ()


class ProviderPocResponse(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    content: PocContent
    claims: tuple[GroundedClaim, ...] = ()
    missing_information: tuple[MissingInformationMarker, ...] = ()