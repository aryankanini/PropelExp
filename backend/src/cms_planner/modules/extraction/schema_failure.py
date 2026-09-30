"""Content-free failure returned for invalid aggregate extraction responses."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class ExtractionSchemaFailure(BaseModel):
    """Identify schema rejection without retaining provider response content."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    code: Literal["invalid_extraction_response"] = "invalid_extraction_response"
