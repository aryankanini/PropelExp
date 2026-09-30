"""Application service for authorized current-revision export."""

from collections.abc import Callable
from typing import Literal

from application.ports.case_repository import CaseRepository
from cms_planner.application.format_labeled_export import (
    LabeledExport,
    format_labeled_export,
)
from cms_planner.domain.export_policy import (
    ExportBlocker,
    ExportBlockerCode,
    authorize_export,
)
from cms_planner.domain.poc import POC_SECTION_ORDER, PocRevision


class ExportFormattingError(RuntimeError):
    """A retryable formatter failure that cannot alter approval state."""


class ExportApprovedRevision:
    """Recheck approval and format the current revision for local delivery."""

    def __init__(
        self,
        repository: CaseRepository,
        formatter: Callable[..., LabeledExport] = format_labeled_export,
    ) -> None:
        self._repository = repository
        self._formatter = formatter

    def execute(
        self, *, session_id: str, export_format: Literal["copy", "download"]
    ) -> LabeledExport | ExportBlocker:
        aggregate = self._repository.get(session_id)
        if aggregate is None:
            return ExportBlocker(
                code=ExportBlockerCode.NO_CURRENT_REVISION,
                message="No current POC revision is available for export.",
            )
        blocker = authorize_export(aggregate.poc_draft, aggregate.approval)
        if blocker is not None:
            return blocker
        assert aggregate.poc_draft is not None
        content = _revision_text(aggregate.poc_draft.current_revision)
        try:
            return self._formatter(content, download=export_format == "download")
        except Exception as error:
            raise ExportFormattingError("export formatting failed") from error


def _revision_text(revision: PocRevision) -> str:
    values = revision.content.model_dump()
    return "\n\n".join(
        values[section.value]
        for section in POC_SECTION_ORDER
    )