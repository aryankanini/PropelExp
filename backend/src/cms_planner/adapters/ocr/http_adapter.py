"""TLS-configured OCR adapter using the shared bounded executor."""

from collections.abc import Mapping
from typing import Any

from pydantic import ValidationError

from cms_planner.adapters.ai.http_adapter import JsonTransport
from cms_planner.application.ports.ocr_types import OcrFailure, OcrPageRequest, OcrResult, OcrSuccess
from cms_planner.application.provider_approval import require_provider_approval
from cms_planner.application.providers.executor import ProviderExecutor
from cms_planner.application.providers.results import ExhaustedProviderRetries
from cms_planner.infrastructure.config.provider import ProviderSettings


class HttpOcrAdapter:
    """Transmit one classified page and normalize its OCR response."""

    def __init__(
        self,
        settings: ProviderSettings,
        transport: JsonTransport,
        executor: ProviderExecutor,
    ) -> None:
        self._settings = settings
        self._transport = transport
        self._executor = executor

    async def recognize(self, request: OcrPageRequest) -> OcrResult:
        require_provider_approval(self._settings.approval)
        page_number = request.classification.page_number
        payload: Mapping[str, Any] = {
            "page_number": page_number,
            "page_bytes": request.page_bytes.hex(),
        }

        async def invoke() -> Mapping[str, Any]:
            return await self._transport.post_json(
                endpoint=str(self._settings.endpoint),
                api_key=self._settings.api_key.get_secret_value(),
                payload=payload,
            )

        response = await self._executor.execute(invoke)
        if isinstance(response, ExhaustedProviderRetries):
            return OcrFailure(page_number=page_number, code="provider-failed")
        try:
            return OcrSuccess.model_validate(response)
        except ValidationError:
            return OcrFailure(page_number=page_number, code="invalid-provider-response")