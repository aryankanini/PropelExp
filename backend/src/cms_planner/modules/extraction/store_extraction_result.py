"""Atomically retain recognized layout and deficiency candidate state."""

from typing import Literal, Protocol, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from cms_planner.domain.cms_layout import CmsLayout, CmsLayoutStatus
from cms_planner.domain.deficiency_candidate import DeficiencyCandidate


class ExtractionResult(BaseModel):
    """Complete immutable extraction state for one active case."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    case_id: str = Field(min_length=1)
    layout: CmsLayout
    candidates: tuple[DeficiencyCandidate, ...]

    @model_validator(mode="after")
    def validate_result(self) -> Self:
        if self.layout.status is not CmsLayoutStatus.RECOGNIZED:
            raise ValueError("extraction result requires a recognized layout")
        if any(
            item.layout_pattern is not self.layout.pattern
            for item in self.candidates
        ):
            raise ValueError("all candidates must reference the retained layout")
        candidate_ids = [item.candidate_id for item in self.candidates]
        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("candidate identities must be unique")
        return self


class ExtractionResultStore(Protocol):
    """One-operation persistence boundary for transient extraction state."""

    @property
    def storage_kind(self) -> Literal["memory"]: ...

    def save(self, result: ExtractionResult) -> None: ...


def store_extraction_result(
    store: ExtractionResultStore,
    *,
    case_id: str,
    layout: CmsLayout,
    candidates: tuple[DeficiencyCandidate, ...],
) -> ExtractionResult:
    """Validate a complete result before invoking the atomic store operation."""
    result = ExtractionResult(
        case_id=case_id,
        layout=layout,
        candidates=candidates,
    )
    store.save(result)
    return result