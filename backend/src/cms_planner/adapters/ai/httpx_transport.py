"""httpx-backed JSON transport for outbound provider calls."""

from collections.abc import Mapping
from typing import Any

import httpx

from cms_planner.application.providers.executor import (
    ProviderThrottledError,
    TransientProviderTransportError,
)


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
            raise ProviderThrottledError("provider rate limit exceeded")
        if response.status_code >= 500:
            raise TransientProviderTransportError(
                f"provider server error: {response.status_code}"
            )
        response.raise_for_status()
        return response.json()
