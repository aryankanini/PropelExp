"""Evidence-linked review state and append-only resolution behavior."""

from enum import StrEnum
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Origin(StrEnum):
    """Closed provenance labels exposed to reviewers."""

    EXTRACTED = "Extracted"
    AI_GENERATED = "AI-generated"
    USER_EDITED = "User-edited"
    APPROVED = "Approved"


class StaleReviewRevisionError(Exception):
    """Report the current revision when a write uses stale review state."""

    def __init__(self, expected_revision_id: str, current_revision_id: str) -> None:
        super().__init__("review revision is stale")
        self.expected_revision_id = expected_revision_id
        self.current_revision_id = current_revision_id


class CandidateNotFoundError(KeyError):
    """Report a candidate that does not belong to the reviewed field."""


class EvidenceUnavailableError(Exception):
    """Report review content whose evidence cannot be displayed."""


class HighlightCoordinates(BaseModel):
    """Normalized coordinates for one highlighted evidence region."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)
    width: float = Field(gt=0, le=1)
    height: float = Field(gt=0, le=1)

    @model_validator(mode="after")
    def validate_page_bounds(self) -> Self:
        if self.x + self.width > 1 or self.y + self.height > 1:
            raise ValueError("highlight coordinates must remain within the page")
        return self


class Evidence(BaseModel):
    """Complete source evidence for a candidate or revision."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    page_number: int = Field(ge=1)
    full_snippet: str = Field(min_length=1)
    highlight: HighlightCoordinates
    source: Literal["native-text", "ocr"]


class ReviewCandidate(BaseModel):
    """One extracted candidate with uncertainty and source evidence."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    candidate_id: str = Field(min_length=1)
    value: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    uncertainty: str | None = None
    origin: Origin
    evidence: Evidence


class ReviewRevision(BaseModel):
    """One immutable reviewed value revision."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    revision_id: str = Field(min_length=1)
    revision_number: int = Field(ge=1)
    value: str = Field(min_length=1)
    origin: Origin
    evidence: Evidence | None = None
    source_candidate_id: str | None = None


class ReviewField(BaseModel):
    """Own candidates, revisions, and review state for one extracted field."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    field_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    deficiency_id: str | None = None
    field_type: Literal["provider", "f_tag", "sod"]
    candidates: tuple[ReviewCandidate, ...] = ()
    revisions: tuple[ReviewRevision, ...] = Field(min_length=1)
    evidence_items: tuple[Evidence, ...] = ()
    current_revision_id: str = Field(min_length=1)
    unresolved: bool = False
    confirmed_revision_id: str | None = None
    poc_suggestion: str | None = None

    @model_validator(mode="after")
    def validate_revision_state(self) -> Self:
        if self.revisions[-1].revision_id != self.current_revision_id:
            raise ValueError("current_revision_id must identify the latest revision")
        if self.confirmed_revision_id is not None and not any(
            revision.revision_id == self.confirmed_revision_id
            for revision in self.revisions
        ):
            raise ValueError("confirmed_revision_id must identify a retained revision")
        return self

    @property
    def current_revision(self) -> ReviewRevision:
        return self.revisions[-1]

    @property
    def ordered_candidates(self) -> tuple[ReviewCandidate, ...]:
        return tuple(
            sorted(
                self.candidates,
                key=lambda candidate: (
                    candidate.evidence.page_number,
                    candidate.candidate_id,
                ),
            )
        )

    @property
    def reapproval_required(self) -> bool:
        return self.current_revision.origin is not Origin.APPROVED and any(
            revision.origin is Origin.APPROVED for revision in self.revisions
        )

    def resolve_candidate(
        self,
        *,
        expected_revision_id: str,
        candidate_id: str,
        revision_id: str,
    ) -> Self:
        """Append the selected evidence-supported candidate as current."""
        self._require_current(expected_revision_id)
        candidate = next(
            (
                item
                for item in self.candidates
                if item.candidate_id == candidate_id
            ),
            None,
        )
        if candidate is None:
            raise CandidateNotFoundError(candidate_id)
        revision = ReviewRevision(
            revision_id=revision_id,
            revision_number=self.current_revision.revision_number + 1,
            value=candidate.value,
            origin=candidate.origin,
            evidence=candidate.evidence,
            source_candidate_id=candidate.candidate_id,
        )
        return self._append_revision(revision, unresolved=False)

    def append_correction(
        self,
        *,
        expected_revision_id: str,
        revision_id: str,
        value: str,
    ) -> Self:
        """Append a reviewer correction without changing retained originals."""
        self._require_current(expected_revision_id)
        corrected_value = value.strip()
        if not corrected_value:
            raise ValueError("correction must not be empty")
        revision = ReviewRevision(
            revision_id=revision_id,
            revision_number=self.current_revision.revision_number + 1,
            value=corrected_value,
            origin=Origin.USER_EDITED,
            evidence=self.current_revision.evidence,
        )
        return self._append_revision(revision, unresolved=False)

    def leave_unresolved(self, *, expected_revision_id: str) -> Self:
        """Keep the field explicitly unresolved without allocating a revision."""
        self._require_current(expected_revision_id)
        return self.model_copy(update={"unresolved": True})

    def approve(self, *, expected_revision_id: str, revision_id: str) -> Self:
        """Append an approved projection of the current reviewed value."""
        self._require_current(expected_revision_id)
        if self.unresolved:
            raise ValueError("unresolved fields cannot be approved")
        current = self.current_revision
        revision = ReviewRevision(
            revision_id=revision_id,
            revision_number=current.revision_number + 1,
            value=current.value,
            origin=Origin.APPROVED,
            evidence=current.evidence,
            source_candidate_id=current.source_candidate_id,
        )
        return self._append_revision(
            revision,
            unresolved=False,
            confirmed_revision_id=revision.revision_id,
        )

    def _require_current(self, expected_revision_id: str) -> None:
        if expected_revision_id != self.current_revision_id:
            raise StaleReviewRevisionError(
                expected_revision_id,
                self.current_revision_id,
            )

    def _append_revision(
        self,
        revision: ReviewRevision,
        *,
        unresolved: bool,
        confirmed_revision_id: str | None = None,
    ) -> Self:
        return self.model_copy(
            update={
                "revisions": (*self.revisions, revision),
                "current_revision_id": revision.revision_id,
                "unresolved": unresolved,
                "confirmed_revision_id": confirmed_revision_id,
            }
        )