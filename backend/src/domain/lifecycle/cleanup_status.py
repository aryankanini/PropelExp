"""Content-free result model for transient cleanup."""

from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

CleanupStoreName = Literal["case_memory", "workspace"]


class CleanupStatus(BaseModel):
    """Report cleanup truth without retaining case or document content."""

    model_config = ConfigDict(frozen=True, strict=True)

    outcome: Literal["completed", "failed"]
    remaining_files: int | None = Field(default=None, ge=0)
    failed_stores: tuple[CleanupStoreName, ...] = ()

    @model_validator(mode="after")
    def validate_completed_status(self) -> Self:
        if self.outcome == "completed" and (
            self.remaining_files != 0 or self.failed_stores
        ):
            raise ValueError("completed cleanup must have zero residue")
        return self