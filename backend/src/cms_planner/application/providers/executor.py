"""Bound timeout and retry behavior for outbound provider calls."""

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

from cms_planner.application.providers.results import ExhaustedProviderRetries

MAX_ATTEMPT_TIMEOUT_SECONDS = 120.0
MAX_RETRIES = 2
DEFAULT_BACKOFF_SECONDS = (0.25, 0.5)

ResultT = TypeVar("ResultT")


class ProviderThrottledError(Exception):
    """Identify provider throttling that may succeed after bounded backoff."""


class ProviderRequestError(Exception):
    """Identify a provider rejection that must not be retried."""


class TransientProviderTransportError(Exception):
    """Identify a temporary transport failure safe to retry."""


class ProviderExecutor:
    """Execute idempotent provider calls with bounded transient retries."""

    def __init__(
        self,
        *,
        timeout_seconds: float = MAX_ATTEMPT_TIMEOUT_SECONDS,
        backoff_seconds: tuple[float, ...] = DEFAULT_BACKOFF_SECONDS,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> None:
        if not 0 < timeout_seconds <= MAX_ATTEMPT_TIMEOUT_SECONDS:
            raise ValueError("provider timeout must be between 0 and 120 seconds")
        if len(backoff_seconds) != MAX_RETRIES or any(
            delay < 0 or delay > MAX_ATTEMPT_TIMEOUT_SECONDS
            for delay in backoff_seconds
        ):
            raise ValueError("provider backoff must define two bounded delays")
        self._timeout_seconds = timeout_seconds
        self._backoff_seconds = backoff_seconds
        self._sleep = sleep

    async def execute(
        self,
        operation: Callable[[], Awaitable[ResultT]],
    ) -> ResultT | ExhaustedProviderRetries:
        """Return the first success or a typed result after three failures."""
        retryable_errors = (
            TimeoutError,
            ProviderThrottledError,
            TransientProviderTransportError,
        )
        for attempt in range(MAX_RETRIES + 1):
            try:
                return await asyncio.wait_for(
                    operation(),
                    timeout=self._timeout_seconds,
                )
            except retryable_errors:
                if attempt == MAX_RETRIES:
                    return ExhaustedProviderRetries(attempts=attempt + 1)
                await self._sleep(self._backoff_seconds[attempt])
        raise AssertionError("provider retry loop must return")