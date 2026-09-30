"""Plan-of-correction draft models and revision invariants."""

from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

from domain.case.revision_errors import StaleRevisionError

NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class PocSectionName(StrEnum):
    AFFECTED_RESIDENTS = "affected_residents"
    OTHERS_AT_RISK = "others_at_risk"
    CORRECTIVE_MEASURES = "corrective_measures"
    MONITORING = "monitoring"
    COMPLETION_DATE = "completion_date"


POC_SECTION_ORDER = tuple(PocSectionName)


class PocContent(BaseModel):
    """The closed five-part POC content contract."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    affected_residents: NonEmptyText
    others_at_risk: NonEmptyText
    corrective_measures: NonEmptyText
    monitoring: NonEmptyText
    completion_date: NonEmptyText


class SupportReference(BaseModel):
    """A reviewed field or evidence span supporting one facility claim."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    kind: Literal["reviewed_field", "evidence_span"]
    reference_id: NonEmptyText


class GroundedClaim(BaseModel):
    """A supported claim retained in a guarded draft."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    kind: Literal["supported_claim"] = "supported_claim"
    section: PocSectionName
    text: NonEmptyText
    support_references: tuple[SupportReference, ...] = Field(min_length=1)


class GenericGuidance(BaseModel):
    """Compliance guidance that does not assert a facility-specific fact."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    kind: Literal["generic_guidance"] = "generic_guidance"
    text: NonEmptyText


class MissingInformationMarker(BaseModel):
    """A deterministic replacement for an unsupported required fact."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    kind: Literal["missing_information"] = "missing_information"
    marker_id: str = Field(min_length=1)
    section: PocSectionName
    required_fact: NonEmptyText


class SectionOrigin(StrEnum):
    AI_GENERATED = "ai_generated"
    USER_EDITED = "user_edited"


class PocRevision(BaseModel):
    """One immutable, unapproved POC revision."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    revision_id: str = Field(min_length=1)
    deficiency_revision_id: str = Field(min_length=1)
    content: PocContent
    section_origins: dict[PocSectionName, SectionOrigin]
    grounded_claims: tuple[GroundedClaim, ...] = ()
    missing_information: tuple[MissingInformationMarker, ...] = ()
    status: Literal["unapproved"] = "unapproved"

    @model_validator(mode="after")
    def validate_section_origins(self) -> Self:
        if set(self.section_origins) != set(POC_SECTION_ORDER):
            raise ValueError("section_origins must identify every POC section")
        return self

    @property
    def approval_ready(self) -> bool:
        return not self.missing_information


class PocDraft(BaseModel):
    """Own append-only POC history for one deficiency revision."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    deficiency_id: str = Field(min_length=1)
    revisions: tuple[PocRevision, ...] = Field(min_length=1)
    current_revision_id: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_current_revision(self) -> Self:
        if self.revisions[-1].revision_id != self.current_revision_id:
            raise ValueError("current_revision_id must identify the latest revision")
        return self

    @property
    def current_revision(self) -> PocRevision:
        return self.revisions[-1]

    def append_revision(
        self,
        *,
        expected_revision_id: str,
        revision: PocRevision,
    ) -> Self:
        if expected_revision_id != self.current_revision_id:
            raise StaleRevisionError(expected_revision_id, self.current_revision_id)
        if revision.deficiency_revision_id != self.current_revision.deficiency_revision_id:
            raise ValueError("an edit cannot change the deficiency revision boundary")
        return self.model_copy(
            update={
                "revisions": (*self.revisions, revision),
                "current_revision_id": revision.revision_id,
            }
        )

    def append_edit(
        self,
        *,
        expected_revision_id: str,
        revision_id: str,
        section_updates: dict[PocSectionName, str | None],
    ) -> Self:
        if expected_revision_id != self.current_revision_id:
            raise StaleRevisionError(expected_revision_id, self.current_revision_id)

        content_values = self.current_revision.content.model_dump()
        section_origins = dict(self.current_revision.section_origins)
        missing_information = list(self.current_revision.missing_information)

        for section, value in section_updates.items():
            section_origins[section] = SectionOrigin.USER_EDITED
            missing_information = [
                marker for marker in missing_information if marker.section != section
            ]
            if value is not None:
                content_values[section.value] = value
                continue

            marker = self._latest_marker_for(section)
            if marker is None:
                raise ValueError("a section without a marker cannot be removed")
            content_values[section.value] = (
                f"[Missing information: {marker.required_fact}]"
            )
            missing_information.append(marker)

        revision = PocRevision(
            revision_id=revision_id,
            deficiency_revision_id=self.current_revision.deficiency_revision_id,
            content=PocContent(**content_values),
            section_origins=section_origins,
            missing_information=tuple(missing_information),
        )
        return self.append_revision(
            expected_revision_id=expected_revision_id,
            revision=revision,
        )

    def _latest_marker_for(
        self, section: PocSectionName
    ) -> MissingInformationMarker | None:
        for revision in reversed(self.revisions):
            for marker in revision.missing_information:
                if marker.section == section:
                    return marker
        return None