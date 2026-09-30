import asyncio

from cms_planner.application.ports.ocr_types import OcrFailure, OcrPageRequest, OcrSuccess
from cms_planner.domain.page import SourcePage
from cms_planner.domain.text_span import BoundingBox, ClassifiedPageText, TextSpan
from cms_planner.modules.extraction.page_extraction_service import (
    PageExtractionInput,
    PageExtractionService,
)


def span(page_number: int, text: str) -> TextSpan:
    return TextSpan(
        page_number=page_number,
        text=text,
        coordinates=BoundingBox(x=1, y=2, width=3, height=4),
    )


class FakeOcr:
    def __init__(self, failures: set[int] | None = None) -> None:
        self.failures = failures or set()
        self.requested_pages: list[int] = []

    async def recognize(self, request: OcrPageRequest) -> OcrSuccess | OcrFailure:
        page_number = request.classification.page_number
        self.requested_pages.append(page_number)
        if page_number in self.failures:
            return OcrFailure(page_number=page_number, code="provider-failed")
        return OcrSuccess(page_number=page_number, spans=(span(page_number, " OCR  text "),))


def test_mixed_pipeline_preserves_order_and_only_ocrs_required_pages() -> None:
    ocr = FakeOcr()
    service = PageExtractionService(ocr)
    inputs = (
        PageExtractionInput(
            source_page=SourcePage(page_number=1, native_text="Native", native_text_complete=True),
            native_spans=(span(1, "Native  text"),),
            page_bytes=b"one",
        ),
        PageExtractionInput(
            source_page=SourcePage(page_number=2, native_text="Partial", native_text_complete=False),
            native_spans=(span(2, "Partial"),),
            page_bytes=b"two",
        ),
    )

    result = asyncio.run(service.extract(inputs))

    assert [page.page_number for page in result.pages] == [1, 2]
    assert ocr.requested_pages == [2]
    assert isinstance(result.pages[0], ClassifiedPageText)
    assert result.pages[0].spans[0].text == "Native text"
    assert isinstance(result.pages[1], ClassifiedPageText)
    assert result.pages[1].spans[0].text == "OCR text"
    assert result.ocr_stage_failed is False


def test_normalization_empty_native_page_reroutes_once() -> None:
    ocr = FakeOcr()
    service = PageExtractionService(ocr)
    inputs = (
        PageExtractionInput(
            source_page=SourcePage(page_number=3, native_text="Content", native_text_complete=True),
            native_spans=(span(3, "\ufeff | -- |"),),
            page_bytes=b"three",
        ),
    )

    result = asyncio.run(service.extract(inputs))

    assert ocr.requested_pages == [3]
    assert isinstance(result.pages[0], ClassifiedPageText)


def test_ocr_failure_retains_successful_pages_and_marks_stage_failed() -> None:
    service = PageExtractionService(FakeOcr(failures={2}))
    inputs = (
        PageExtractionInput(
            source_page=SourcePage(page_number=1, native_text="Native", native_text_complete=True),
            native_spans=(span(1, "Native"),),
            page_bytes=b"one",
        ),
        PageExtractionInput(
            source_page=SourcePage(page_number=2, native_text="", native_text_complete=False),
            native_spans=(),
            page_bytes=b"two",
        ),
    )

    result = asyncio.run(service.extract(inputs))

    assert isinstance(result.pages[0], ClassifiedPageText)
    assert result.pages[1] == OcrFailure(page_number=2, code="provider-failed")
    assert result.ocr_stage_failed is True