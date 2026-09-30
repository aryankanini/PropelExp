import asyncio
from collections.abc import Mapping
from typing import Any

import pytest

from cms_planner.adapters.ai.http_adapter import AiHttpAdapter
from cms_planner.application.ports.providers import (
    ExtractionPage,
    ExtractionRequest,
    ExtractionResult,
    PocGenerationRequest,
    PocGenerationResult,
)
from cms_planner.application.providers.executor import (
    ProviderExecutor,
    TransientProviderTransportError,
)
from cms_planner.application.providers.results import (
    ExhaustedProviderRetries,
    InvalidProviderResponse,
)
from cms_planner.infrastructure.config.provider import ProviderSettings


class FakeTransport:
    def __init__(self, response: Mapping[str, Any] | Exception) -> None:
        self.response = response
        self.payloads: list[Mapping[str, Any]] = []

    async def post_json(
        self,
        *,
        endpoint: str,
        api_key: str,
        payload: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        self.payloads.append(payload)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


async def no_sleep(delay: float) -> None:
    return None


def extraction_request() -> ExtractionRequest:
    return ExtractionRequest(
        pages=(ExtractionPage(page_number=1, text="required page"),),
        fields=("provider_name", "f_tag", "sod"),
    )


def adapter(settings: ProviderSettings, transport: FakeTransport) -> AiHttpAdapter:
    return AiHttpAdapter(
        settings,
        transport,
        ProviderExecutor(sleep=no_sleep),
    )


def test_valid_extraction_returns_application_result(
    provider_settings: ProviderSettings,
    valid_extraction_response: dict[str, Any],
) -> None:
    transport = FakeTransport(valid_extraction_response)

    result = asyncio.run(adapter(provider_settings, transport).extract(extraction_request()))

    assert isinstance(result, ExtractionResult)
    assert set(transport.payloads[0]) == {"pages", "fields"}


def test_valid_five_part_poc_returns_application_result(
    provider_settings: ProviderSettings,
    valid_poc_response: dict[str, Any],
) -> None:
    result = asyncio.run(
        adapter(provider_settings, FakeTransport(valid_poc_response)).generate(
            PocGenerationRequest(
                deficiency_revision_id="revision-1",
                reviewed_fields=(),
                evidence=(),
            )
        )
    )

    assert isinstance(result, PocGenerationResult)
    assert result.content.monitoring == "Weekly audit"


@pytest.mark.parametrize("mutation", ("missing", "malformed", "unknown"))
def test_invalid_extraction_has_no_partial_payload(
    provider_settings: ProviderSettings,
    valid_extraction_response: dict[str, Any],
    mutation: str,
) -> None:
    response = dict(valid_extraction_response)
    if mutation == "missing":
        response.pop("sod")
    elif mutation == "malformed":
        response["f_tag"] = ""
    else:
        response["provider_metadata"] = "must not cross boundary"

    result = asyncio.run(adapter(provider_settings, FakeTransport(response)).extract(extraction_request()))

    assert result == InvalidProviderResponse()
    assert not hasattr(result, "provider_name")


def test_retry_exhaustion_returns_typed_failure(
    provider_settings: ProviderSettings,
) -> None:
    transport = FakeTransport(TransientProviderTransportError())

    result = asyncio.run(adapter(provider_settings, transport).extract(extraction_request()))

    assert result == ExhaustedProviderRetries(attempts=3)
    assert len(transport.payloads) == 3