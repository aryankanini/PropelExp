"""Immutable evidence-linked field revision values."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class FieldRevision(BaseModel):
    """Capture one immutable value and its supporting evidence."""

    model_config = ConfigDict(frozen=True, strict=True)

    revision_id: str = Field(min_length=1)
    value: str
    page_number: int = Field(ge=1)
    supporting_snippet: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    origin: Literal["extracted", "user_edit"]
    revision_number: int = Field(ge=1)