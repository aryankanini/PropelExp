"""Deterministic local-only export formatting."""

from pydantic import BaseModel, ConfigDict

from cms_planner.domain.export_label import prefix_export_content


class LabeledExport(BaseModel):
    """A labeled payload returned directly to the requesting user."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    content: str
    media_type: str
    filename: str | None = None


def format_labeled_export(content: str, *, download: bool) -> LabeledExport:
    """Create a copy or plain-text download without external submission."""
    labeled = prefix_export_content(content)
    return LabeledExport(
        content=labeled,
        media_type="text/plain; charset=utf-8",
        filename="approved-poc-draft.txt" if download else None,
    )