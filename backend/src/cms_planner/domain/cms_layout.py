"""Retained CMS document layout recognition state."""

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator


class CmsLayoutStatus(StrEnum):
    """Closed CMS document recognition outcomes."""

    RECOGNIZED = "recognized"
    UNRECOGNIZED = "unrecognized"


class CmsLayoutPattern(StrEnum):
    """Supported CMS form layout patterns."""

    CMS_2567 = "cms-2567"


class CmsLayout(BaseModel):
    """Retain a supported layout or an explicit stopping outcome."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    status: CmsLayoutStatus
    pattern: CmsLayoutPattern | None = None
    marker_page_numbers: tuple[int, ...] = ()

    @model_validator(mode="after")
    def validate_recognition_state(self) -> Self:
        if self.status is CmsLayoutStatus.RECOGNIZED:
            if self.pattern is None or not self.marker_page_numbers:
                raise ValueError("recognized layouts require a pattern and marker pages")
        elif self.pattern is not None or self.marker_page_numbers:
            raise ValueError("unrecognized layouts cannot retain recognized markers")
        return self
