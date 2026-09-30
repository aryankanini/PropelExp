"""Coordinate-bearing page text retained as extraction evidence."""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from cms_planner.domain.page import PageClassification


class BoundingBox(BaseModel):
    """Rectangular source coordinates for an extracted text span."""

    model_config = ConfigDict(frozen=True, strict=True)

    x: float = Field(ge=0)
    y: float = Field(ge=0)
    width: float = Field(gt=0)
    height: float = Field(gt=0)


class TextSpan(BaseModel):
    """Raw text and its location on a source page."""

    model_config = ConfigDict(frozen=True, strict=True)

    page_number: int = Field(ge=1)
    text: str
    coordinates: BoundingBox


class ClassifiedPageText(BaseModel):
    """Associate raw native spans with a retained page classification."""

    model_config = ConfigDict(frozen=True, strict=True)

    classification: PageClassification
    spans: tuple[TextSpan, ...]

    @property
    def page_number(self) -> int:
        """Return the retained source page identity."""
        return self.classification.page_number

    @model_validator(mode="after")
    def validate_page_identity(self) -> Self:
        if any(
            span.page_number != self.classification.page_number
            for span in self.spans
        ):
            raise ValueError("all spans must match the classified page")
        return self