"""Provider-neutral OCR request, success, and safe failure values."""

from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from cms_planner.domain.page import PageClassification, PageRoute
from cms_planner.domain.text_span import TextSpan


class OcrPageRequest(BaseModel):
    """Minimum page payload permitted at the OCR boundary."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    classification: PageClassification
    page_bytes: bytes = Field(min_length=1)

    @model_validator(mode="after")
    def validate_route(self) -> Self:
        if self.classification.route is not PageRoute.OCR_REQUIRED:
            raise ValueError("OCR requests require the ocr-required route")
        return self


class OcrSuccess(BaseModel):
    """Raw coordinate-bearing OCR output for one page."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    page_number: int = Field(ge=1)
    spans: tuple[TextSpan, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_page_identity(self) -> Self:
        if any(span.page_number != self.page_number for span in self.spans):
            raise ValueError("OCR spans must match the response page")
        return self


class OcrFailure(BaseModel):
    """Content-free OCR failure safe for case and stage state."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    page_number: int = Field(ge=1)
    stage: Literal["ocr"] = "ocr"
    code: Literal[
        "provider-not-approved",
        "provider-failed",
        "invalid-provider-response",
    ]


OcrResult = OcrSuccess | OcrFailure