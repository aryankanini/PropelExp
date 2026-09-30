"""Page identity and retained extraction-routing decisions."""

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PageRoute(StrEnum):
    """Supported page extraction routes."""

    NATIVE_TEXT = "native-text"
    OCR_REQUIRED = "ocr-required"


class PageRouteReason(StrEnum):
    """Closed reasons for a page extraction route."""

    COMPLETE_NATIVE_TEXT = "complete-native-text"
    INCOMPLETE_NATIVE_TEXT = "incomplete-native-text"
    NO_SUBSTANTIVE_TEXT = "no-substantive-text"


class SourcePage(BaseModel):
    """Native page content available for pre-extraction classification."""

    model_config = ConfigDict(frozen=True, strict=True)

    page_number: int = Field(ge=1)
    native_text: str
    native_text_complete: bool


class PageClassification(BaseModel):
    """Retain the page route and its deterministic rationale."""

    model_config = ConfigDict(frozen=True, strict=True)

    page_number: int = Field(ge=1)
    route: PageRoute
    reason: PageRouteReason

    @model_validator(mode="after")
    def validate_route_reason(self) -> Self:
        if self.route is PageRoute.NATIVE_TEXT:
            if self.reason is not PageRouteReason.COMPLETE_NATIVE_TEXT:
                raise ValueError("native-text route requires complete native text")
        elif self.reason is PageRouteReason.COMPLETE_NATIVE_TEXT:
            raise ValueError("complete native text requires the native-text route")
        return self