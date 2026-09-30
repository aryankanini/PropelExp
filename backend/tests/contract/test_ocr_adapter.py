import asyncio

from cms_planner.adapters.ocr.adapter import GuardedOcrAdapter
from cms_planner.application.ports.ocr_types import OcrFailure, OcrPageRequest, OcrSuccess
from cms_planner.domain.page import PageClassification, PageRoute, PageRouteReason
from cms_planner.domain.text_span import BoundingBox, TextSpan


def request() -> OcrPageRequest:
    return OcrPageRequest(
        classification=PageClassification(
            page_number=4,
            route=PageRoute.OCR_REQUIRED,
            reason=PageRouteReason.INCOMPLETE_NATIVE_TEXT,
        ),
        page_bytes=b"minimum-page-payload",
    )


class FakeProvider:
    def __init__(self, result: OcrSuccess | Exception) -> None:
        self.result = result
        self.calls = 0

    async def recognize(self, page_request: OcrPageRequest) -> OcrSuccess:
        self.calls += 1
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


def test_unapproved_adapter_does_not_invoke_provider() -> None:
    provider = FakeProvider(RuntimeError("must not run"))
    result = asyncio.run(GuardedOcrAdapter(provider, approved=False).recognize(request()))

    assert isinstance(result, OcrFailure)
    assert result.code == "provider-not-approved"
    assert provider.calls == 0


def test_approved_adapter_preserves_raw_text_and_coordinates() -> None:
    provider = FakeProvider(
        OcrSuccess(
            page_number=4,
            spans=(
                TextSpan(
                    page_number=4,
                    text="Raw OCR text",
                    coordinates=BoundingBox(x=1, y=2, width=3, height=4),
                ),
            ),
        )
    )

    result = asyncio.run(GuardedOcrAdapter(provider, approved=True).recognize(request()))

    assert isinstance(result, OcrSuccess)
    assert result.spans[0].text == "Raw OCR text"
    assert result.spans[0].coordinates.x == 1


def test_provider_exception_maps_to_safe_failure() -> None:
    provider = FakeProvider(RuntimeError("secret provider detail"))

    result = asyncio.run(GuardedOcrAdapter(provider, approved=True).recognize(request()))

    assert result == OcrFailure(page_number=4, code="provider-failed")