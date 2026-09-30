"""Map AI HTTP payloads to closed application-owned contracts."""

import json
from collections.abc import Mapping
from typing import Any, Protocol

from pydantic import ValidationError

from cms_planner.adapters.ai.schemas.requests import (
    ProviderExtractionPage,
    ProviderExtractionRequest,
    ProviderPocRequest,
)
from cms_planner.adapters.ai.schemas.responses import (
    ProviderExtractionResponse,
    ProviderPocResponse,
)
from cms_planner.application.ports.providers import (
    ExtractionRequest,
    ExtractionResult,
    PocGenerationRequest,
    PocGenerationResult,
)
from cms_planner.application.provider_approval import require_provider_approval
from cms_planner.application.providers.executor import ProviderExecutor
from cms_planner.application.providers.results import (
    ExhaustedProviderRetries,
    InvalidProviderResponse,
)
from cms_planner.infrastructure.config.provider import ProviderSettings


class JsonTransport(Protocol):
    async def post_json(
        self,
        *,
        endpoint: str,
        api_key: str,
        payload: Mapping[str, Any],
    ) -> Mapping[str, Any]: ...


class AiHttpAdapter:
    """Transmit validated minimum payloads and normalize provider responses."""

    def __init__(
        self,
        settings: ProviderSettings,
        transport: JsonTransport,
        executor: ProviderExecutor,
    ) -> None:
        self._settings = settings
        self._transport = transport
        self._executor = executor

    async def extract(
        self,
        request: ExtractionRequest,
    ) -> ExtractionResult | ExhaustedProviderRetries | InvalidProviderResponse:
        provider_request = ProviderExtractionRequest(
            pages=tuple(
                ProviderExtractionPage(
                    page_number=page.page_number,
                    text=page.text,
                )
                for page in request.pages
            ),
            fields=request.fields,
        )
        response = await self._send(provider_request.model_dump(mode="json"))
        if isinstance(response, ExhaustedProviderRetries):
            return response
        try:
            validated = ProviderExtractionResponse.model_validate_json(
                json.dumps(response)
            )
        except (TypeError, ValidationError):
            return InvalidProviderResponse()
        return ExtractionResult(**validated.model_dump())

    async def generate(
        self,
        request: PocGenerationRequest,
    ) -> PocGenerationResult | ExhaustedProviderRetries | InvalidProviderResponse:
        provider_request = ProviderPocRequest(**request.model_dump())
        response = await self._send(provider_request.model_dump(mode="json"))
        if isinstance(response, ExhaustedProviderRetries):
            return response
        try:
            validated = ProviderPocResponse.model_validate_json(json.dumps(response))
        except (TypeError, ValidationError):
            return InvalidProviderResponse()
        return PocGenerationResult(**validated.model_dump())

    async def _send(
        self,
        payload: Mapping[str, Any],
    ) -> Mapping[str, Any] | ExhaustedProviderRetries:
        require_provider_approval(self._settings.approval)

        async def invoke() -> Mapping[str, Any]:
            return await self._transport.post_json(
                endpoint=str(self._settings.endpoint),
                api_key=self._settings.api_key.get_secret_value(),
                payload=payload,
            )

        return await self._executor.execute(invoke)