"""Application contracts for bounded document intake."""

from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field


@dataclass(frozen=True)
class UploadLimits:
    """Define the accepted upload byte and page boundaries."""

    max_bytes: int = 50 * 1024 * 1024
    max_pages: int = 200

    def __post_init__(self) -> None:
        if self.max_bytes <= 0 or self.max_pages <= 0:
            raise ValueError("upload limits must be positive")


@dataclass(frozen=True)
class UploadCommand:
    """Carry one streamed upload without transport or provider details."""

    session_id: str
    client_filename: str
    media_type: str


class AcceptedUpload(BaseModel):
    """Report a transient case whose document is extraction-ready."""

    model_config = ConfigDict(frozen=True, strict=True)

    status: str = "extraction_ready"
    case_id: str = Field(min_length=1)
    upload_id: str = Field(min_length=1)
    size_bytes: int = Field(ge=0)
    page_count: int = Field(ge=1)