"""HTTP contracts for approved current-revision export."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

from cms_planner.domain.export_policy import ExportBlocker


class ExportResponse(BaseModel):
    """Labeled content for local copy or download."""

    model_config = ConfigDict(extra="forbid", strict=True)

    format: Literal["copy", "download"]
    content: str
    media_type: str
    filename: str | None = None


class ExportBlockedResponse(BaseModel):
    """Approval-required response for a blocked export."""

    model_config = ConfigDict(extra="forbid", strict=True)

    blocker: ExportBlocker
    retry_available: Literal[False] = False
    copy_available: Literal[False] = False


class ExportFailureResponse(BaseModel):
    """Non-destructive download-formatting recovery metadata."""

    model_config = ConfigDict(extra="forbid", strict=True)

    code: Literal["formatting_failed"] = "formatting_failed"
    message: Literal["Download formatting failed; approval remains unchanged."] = (
        "Download formatting failed; approval remains unchanged."
    )
    retry_available: Literal[True] = True
    copy_available: Literal[True] = True