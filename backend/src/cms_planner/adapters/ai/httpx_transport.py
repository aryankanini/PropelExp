"""httpx-backed JSON transport for outbound provider calls."""

from collections.abc import Mapping
import logging
from typing import Any

import httpx

from cms_planner.application.providers.executor import (
    ProviderRequestError,
    ProviderThrottledError,
    TransientProviderTransportError,
)

logger = logging.getLogger(__name__)


class HttpxJsonTransport:
    """Send one JSON payload and return the parsed response body."""

    def __init__(self, timeout_seconds: float) -> None:
        self._timeout = timeout_seconds

    async def post_json(
        self,
        *,
        endpoint: str,
        api_key: str,
        payload: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                )
        except httpx.TimeoutException as exc:
            raise TimeoutError("provider request timed out") from exc
        except httpx.TransportError as exc:
            raise TransientProviderTransportError(str(exc)) from exc

        if response.status_code == 429:
            logger.warning("Provider request throttled: status=%s", response.status_code)
            raise ProviderThrottledError("provider rate limit exceeded")
        if response.status_code >= 500:
            logger.warning("Provider server failure: status=%s", response.status_code)
            raise TransientProviderTransportError(
                f"provider server error: {response.status_code}"
            )
        if response.status_code >= 400:
            logger.warning("Provider request rejected: status=%s", response.status_code)
            raise ProviderRequestError(
                f"provider rejected request: {response.status_code}"
            )
        try:
            return response.json()
        except ValueError as exc:
            raise ProviderRequestError("provider returned invalid JSON") from exc
