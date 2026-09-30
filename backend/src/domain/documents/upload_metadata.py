"""Content-free metadata for a stored upload."""

from pydantic import BaseModel, ConfigDict, Field


class UploadMetadata(BaseModel):
    """Retain the client filename as inert metadata only."""

    model_config = ConfigDict(frozen=True, strict=True)

    client_filename: str
    upload_id: str = Field(min_length=1)
    size_bytes: int = Field(ge=0)