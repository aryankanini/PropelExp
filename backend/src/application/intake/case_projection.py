"""Assemble content-free document validation projections."""

from dataclasses import dataclass
from typing import Literal

from application.intake.validation_result import DocumentRejected, ExtractionReady


@dataclass(frozen=True)
class CaseValidationProjection:
    """Represent validation state without importing an HTTP schema."""

    status: Literal["extraction_ready", "rejected"]
    page_count: int | None = None
    reason: Literal["unreadable", "not_cms2567"] | None = None


def project_validation(
    result: ExtractionReady | DocumentRejected,
) -> CaseValidationProjection:
    """Map application validation outcomes without extraction candidates."""
    if isinstance(result, ExtractionReady):
        return CaseValidationProjection(
            status="extraction_ready",
            page_count=result.page_count,
        )
    return CaseValidationProjection(status="rejected", reason=result.reason)