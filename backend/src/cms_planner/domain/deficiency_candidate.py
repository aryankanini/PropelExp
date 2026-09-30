"""Evidence-linked deficiency candidate state retained for review."""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from cms_planner.domain.cms_layout import CmsLayoutPattern


class DeficiencyCandidateEvidence(BaseModel):
    """Stable source evidence retained with a deficiency candidate."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    evidence_id: str = Field(min_length=1)
    page_number: int = Field(ge=1)
    text: str = Field(min_length=1)


class DeficiencyCandidate(BaseModel):
    """One independently reviewable deficiency candidate."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    candidate_id: str = Field(min_length=1)
    boundary_id: str = Field(min_length=1)
    layout_pattern: CmsLayoutPattern
    f_tag: str = Field(pattern=r"^[A-Z]\d{4}$")
    sod_text: str | None
    evidence: tuple[DeficiencyCandidateEvidence, ...] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    uncertainty: bool
    confirmed: bool

    @model_validator(mode="after")
    def validate_candidate_state(self) -> Self:
        if self.sod_text is None and (not self.uncertainty or self.confirmed):
            raise ValueError("incomplete SOD must be uncertain and unconfirmed")
        evidence_ids = [item.evidence_id for item in self.evidence]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("candidate evidence identities must be unique")
        return self
