"""Safe HTTP schemas for explicit session cleanup."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CleanupResponse(BaseModel):
    """Report verified cleanup without case content."""

    model_config = ConfigDict(frozen=True, strict=True)

    outcome: Literal["completed", "failed"]
    remaining_files: int | None = Field(default=None, ge=0)
    failed_stores: tuple[Literal["case_memory", "workspace"], ...] = ()