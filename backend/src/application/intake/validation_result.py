"""Content-free outcomes from CMS-2567 structure validation."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ExtractionReady(BaseModel):
    """Identify a validated document that may proceed to extraction."""

    model_config = ConfigDict(frozen=True, strict=True)

    status: Literal["extraction_ready"] = "extraction_ready"
    page_count: int = Field(ge=1)


class DocumentRejected(BaseModel):
    """Identify a safe reason for rejecting a document."""

    model_config = ConfigDict(frozen=True, strict=True)

    status: Literal["rejected"] = "rejected"
    reason: Literal["unreadable", "not_cms2567"]


ValidationResult = ExtractionReady | DocumentRejected