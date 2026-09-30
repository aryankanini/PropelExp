"""Safe HTTP schemas for document intake."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class IntakeAccepted(BaseModel):
    """Expose an extraction-ready transient case."""

    model_config = ConfigDict(frozen=True, strict=True)

    status: Literal["extraction_ready"] = "extraction_ready"
    case_id: str = Field(min_length=1)
    upload_id: str = Field(min_length=1)
    size_bytes: int = Field(ge=0)
    page_count: int = Field(ge=1)


class IntakeProblem(BaseModel):
    """Expose a stable rejection code without protected content."""

    model_config = ConfigDict(frozen=True, strict=True)

    code: Literal[
        "active_upload_exists",
        "byte_limit_exceeded",
        "page_limit_exceeded",
        "unsupported_media_type",
        "unreadable",
        "not_cms2567",
    ]
    message: str = Field(min_length=1)