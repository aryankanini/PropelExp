"""Provider-neutral structured generation contracts for POC drafts."""

from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from cms_planner.domain.deficiency import EvidenceSpan, ReviewedField
from cms_planner.domain.poc import (
    GroundedClaim,
    MissingInformationMarker,
    NonEmptyText,
    POC_SECTION_ORDER,
    PocContent,
    PocSectionName,
    SupportReference,
)


class PocGenerationInput(BaseModel):
    """The complete and deficiency-scoped provider input."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    deficiency_id: NonEmptyText
    deficiency_revision_id: NonEmptyText
    reviewed_fields: tuple[ReviewedField, ...]
    evidence_spans: tuple[EvidenceSpan, ...]


class FacilityClaim(BaseModel):
    """A facility assertion whose references require deterministic validation."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    kind: Literal["facility_claim"] = "facility_claim"
    text: NonEmptyText
    required_fact: NonEmptyText
    support_references: tuple[SupportReference, ...] = ()


class GeneratedGuidance(BaseModel):
    """Compliance guidance that does not assert a facility fact."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    kind: Literal["generic_guidance"] = "generic_guidance"
    text: NonEmptyText


GeneratedStatement = Annotated[
    FacilityClaim | GeneratedGuidance,
    Field(discriminator="kind"),
]


class GeneratedSection(BaseModel):
    """One named POC section containing at least one statement."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    name: PocSectionName
    statements: tuple[GeneratedStatement, ...] = Field(min_length=1)


class ProviderPocResponse(BaseModel):
    """Exactly five generated sections in the mandated order."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    sections: tuple[GeneratedSection, ...] = Field(min_length=5, max_length=5)

    @model_validator(mode="after")
    def validate_section_order(self) -> Self:
        if tuple(section.name for section in self.sections) != POC_SECTION_ORDER:
            raise ValueError("sections must contain the five POC sections in order")
        return self


class GuardedPocResult(BaseModel):
    """Validated content and provenance ready for draft retention."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    content: PocContent
    grounded_claims: tuple[GroundedClaim, ...]
    missing_information: tuple[MissingInformationMarker, ...]