import asyncio
from types import SimpleNamespace

import pytest
from pydantic import SecretStr

from cms_planner.adapters.ai.openai_poc_provider import (
    OpenAiPocProvider,
    _normalize_provider_response,
)
from cms_planner.application.failures import ProviderFailure
from cms_planner.application.providers.executor import (
    ProviderExecutor,
    ProviderRequestError,
)
from cms_planner.domain.poc import POC_SECTION_ORDER
from cms_planner.domain.poc_generation import PocGenerationInput


class _RejectedTransport:
    async def post_json(self, **kwargs):
        raise ProviderRequestError("provider rejected request: 401")


def test_normalizes_section_keyed_string_guidance() -> None:
    payload = {
        section.value: [f"Guidance for {section.value}."]
        for section in POC_SECTION_ORDER
    }

    normalized = _normalize_provider_response(payload)

    assert normalized == {
        "sections": [
            {
                "name": section.value,
                "statements": [
                    {
                        "kind": "generic_guidance",
                        "text": f"Guidance for {section.value}.",
                    }
                ],
            }
            for section in POC_SECTION_ORDER
        ]
    }


def test_normalizes_type_discriminator_without_accepting_extra_sections() -> None:
    payload = {
        section.value: [
            {
                "type": "generic_guidance",
                "text": f"Guidance for {section.value}.",
            }
        ]
        for section in POC_SECTION_ORDER
    }

    normalized = _normalize_provider_response(payload)

    assert normalized["sections"][0]["statements"][0]["kind"] == "generic_guidance"
    assert _normalize_provider_response({**payload, "unexpected": []}) != normalized


def test_provider_rejection_becomes_safe_application_failure() -> None:
    provider_settings = SimpleNamespace(
        endpoint="https://provider.example/v1/chat/completions",
        api_key=SecretStr("test-provider-key"),
        model="test-model",
    )
    provider = OpenAiPocProvider(
        provider_settings,
        _RejectedTransport(),
        ProviderExecutor(),
    )

    with pytest.raises(ProviderFailure):
        asyncio.run(provider._generate_async(PocGenerationInput(
            deficiency_id="deficiency-1",
            deficiency_revision_id="revision-1",
            reviewed_fields=(),
            evidence_spans=(),
        )))