"""Content-free failure identity for page and stage processing."""

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class JobStage(StrEnum):
    EXTRACTION = "extraction"
    OCR = "ocr"
    GENERATION = "generation"


class JobFailure(BaseModel):
    """Identify the failed operation without retaining failed payload content."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    stage: JobStage
    code: str = Field(min_length=1)
    page_number: int | None = Field(default=None, ge=1)
    deficiency_id: str | None = Field(default=None, min_length=1)
    retryable: bool
    required: bool = True

    @model_validator(mode="after")
    def validate_affected_operation(self) -> Self:
        if self.stage in (JobStage.EXTRACTION, JobStage.OCR):
            if self.page_number is None or self.deficiency_id is not None:
                raise ValueError("page failures require only a page number")
        elif self.deficiency_id is None or self.page_number is not None:
            raise ValueError("generation failures require only a deficiency ID")
        return self