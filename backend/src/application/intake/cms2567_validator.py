"""Deterministic CMS-2567 identity validation from inspected page text."""

from application.intake.preflight import DocumentInspection
from application.intake.validation_result import DocumentRejected, ExtractionReady

CMS2567_MARKERS = (
    "statement of deficiencies",
    "plan of correction",
)


class Cms2567Validator:
    """Classify readable inspected content without invoking a provider."""

    def validate(
        self, inspection: DocumentInspection
    ) -> ExtractionReady | DocumentRejected:
        if any(not text or not text.strip() for text in inspection.page_texts):
            return DocumentRejected(reason="unreadable")

        normalized_text = " ".join(inspection.page_texts).casefold()
        if not all(marker in normalized_text for marker in CMS2567_MARKERS):
            return DocumentRejected(reason="not_cms2567")
        return ExtractionReady(page_count=inspection.page_count)