"""Orchestrate ordered native and OCR page extraction."""

from collections.abc import Iterable

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.application.ports.ocr import OcrPort
from cms_planner.application.ports.ocr_types import (
    OcrFailure,
    OcrPageRequest,
    OcrSuccess,
)
from cms_planner.domain.page import PageClassification, PageRoute, SourcePage
from cms_planner.domain.text_span import ClassifiedPageText, TextSpan
from cms_planner.modules.extraction.page_classifier import classify_pages
from cms_planner.modules.extraction.text_normalizer import normalize_extracted_page


class PageExtractionInput(BaseModel):
    """Inputs required to route and extract one source page."""

    model_config = ConfigDict(frozen=True, strict=True)

    source_page: SourcePage
    native_spans: tuple[TextSpan, ...]
    page_bytes: bytes = Field(min_length=1)


class PageExtractionResult(BaseModel):
    """Ordered page outcomes and aggregate OCR stage state."""

    model_config = ConfigDict(frozen=True, strict=True)

    pages: tuple[ClassifiedPageText | OcrFailure, ...]
    ocr_stage_failed: bool


class PageExtractionService:
    """Coordinate classification, extraction, OCR fallback, and normalization."""

    def __init__(self, ocr: OcrPort) -> None:
        self._ocr = ocr

    async def extract(
        self,
        inputs: Iterable[PageExtractionInput],
    ) -> PageExtractionResult:
        ordered_inputs = tuple(inputs)
        classifications = classify_pages(
            item.source_page for item in ordered_inputs
        )
        outcomes = []

        for item, classification in zip(
            ordered_inputs,
            classifications,
            strict=True,
        ):
            outcome = await self._extract_page(item, classification)
            outcomes.append(outcome)

        return PageExtractionResult(
            pages=tuple(outcomes),
            ocr_stage_failed=any(
                isinstance(outcome, OcrFailure) for outcome in outcomes
            ),
        )

    async def _extract_page(
        self,
        item: PageExtractionInput,
        classification: PageClassification,
    ) -> ClassifiedPageText | OcrFailure:
        if classification.route is PageRoute.NATIVE_TEXT:
            native_page = ClassifiedPageText(
                classification=classification,
                spans=item.native_spans,
            )
            normalized = normalize_extracted_page(native_page)
            if normalized.classification.route is PageRoute.NATIVE_TEXT:
                return normalized
            classification = normalized.classification

        response = await self._ocr.recognize(
            OcrPageRequest(
                classification=classification,
                page_bytes=item.page_bytes,
            )
        )
        if isinstance(response, OcrFailure):
            return response
        return normalize_extracted_page(
            self._to_classified_page(classification, response)
        )

    @staticmethod
    def _to_classified_page(
        classification: PageClassification,
        response: OcrSuccess,
    ) -> ClassifiedPageText:
        return ClassifiedPageText(
            classification=classification,
            spans=response.spans,
        )