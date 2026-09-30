"""Safe document validation projection schemas."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DocumentValidationState(BaseModel):
    """Represent readiness or a stable rejection reason."""

    model_config = ConfigDict(frozen=True, strict=True)

    status: Literal["extraction_ready", "rejected"]
    page_count: int | None = Field(default=None, ge=1)
    reason: Literal["unreadable", "not_cms2567"] | None = None