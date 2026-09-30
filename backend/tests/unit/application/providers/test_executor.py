import asyncio

import pytest

from cms_planner.application.providers.executor import (
    ProviderExecutor,
    TransientProviderTransportError,
)
from cms_planner.application.providers.results import ExhaustedProviderRetries


async def no_sleep(delay: float) -> None:
    return None


def test_executor_returns_success_without_retry() -> None:
    calls = 0

    async def operation() -> str:
        nonlocal calls
        calls += 1
        return "typed-result"

    result = asyncio.run(ProviderExecutor(sleep=no_sleep).execute(operation))

    assert result == "typed-result"
    assert calls == 1


def test_executor_returns_typed_exhaustion_after_two_retries() -> None:
    calls = 0

    async def operation() -> str:
        nonlocal calls
        calls += 1
        raise TransientProviderTransportError

    result = asyncio.run(ProviderExecutor(sleep=no_sleep).execute(operation))

    assert result == ExhaustedProviderRetries(attempts=3)
    assert calls == 3


def test_executor_does_not_retry_schema_error() -> None:
    calls = 0

    async def operation() -> str:
        nonlocal calls
        calls += 1
        raise ValueError("invalid provider schema")

    with pytest.raises(ValueError):
        asyncio.run(ProviderExecutor(sleep=no_sleep).execute(operation))

    assert calls == 1


def test_executor_retries_timed_out_attempt() -> None:
    calls = 0

    async def operation() -> str:
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.02)
        return "late"

    result = asyncio.run(
        ProviderExecutor(timeout_seconds=0.001, sleep=no_sleep).execute(operation)
    )

    assert isinstance(result, ExhaustedProviderRetries)
    assert calls == 3