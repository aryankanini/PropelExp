import asyncio

from cms_planner.application.recovery.commands import (
    RecoveryCommand,
    RecoveryOutcome,
)
from cms_planner.application.recovery.service import (
    ProviderRetriesExhaustedError,
    RecoveryService,
)
from cms_planner.domain.job_failure import JobFailure, JobStage


def _command(*, source_valid: bool = True) -> RecoveryCommand:
    return RecoveryCommand(
        case_id="case-1",
        failure=JobFailure(
            stage=JobStage.OCR,
            code="provider-failed",
            page_number=2,
            retryable=True,
        ),
        source_valid=source_valid,
    )


def test_successful_retry_returns_unconfirmed_review_ready_output() -> None:
    async def retry_operation(command: RecoveryCommand) -> str:
        assert command.failure.page_number == 2
        return "recovered output"

    result = asyncio.run(RecoveryService(retry_operation).retry(_command()))

    assert result.outcome is RecoveryOutcome.REVIEW_READY
    assert result.output == "recovered output"
    assert result.confirmed is False


def test_invalid_source_requires_replacement_without_provider_call() -> None:
    calls = 0

    async def retry_operation(command: RecoveryCommand) -> str:
        nonlocal calls
        calls += 1
        return "unused"

    result = asyncio.run(
        RecoveryService(retry_operation).retry(_command(source_valid=False))
    )

    assert result.outcome is RecoveryOutcome.REPLACEMENT_REQUIRED
    assert calls == 0


def test_exhausted_provider_keeps_later_retry_available() -> None:
    async def retry_operation(command: RecoveryCommand) -> str:
        raise ProviderRetriesExhaustedError

    result = asyncio.run(RecoveryService(retry_operation).retry(_command()))

    assert result.outcome is RecoveryOutcome.RETRY_LATER
    assert result.failure.retryable is True


def test_duplicate_active_commands_share_one_provider_call() -> None:
    async def scenario() -> tuple[int, object, object]:
        calls = 0
        release = asyncio.Event()

        async def retry_operation(command: RecoveryCommand) -> str:
            nonlocal calls
            calls += 1
            await release.wait()
            return "recovered output"

        service = RecoveryService(retry_operation)
        first = asyncio.create_task(service.retry(_command()))
        second = asyncio.create_task(service.retry(_command()))
        await asyncio.sleep(0)
        release.set()
        first_result, second_result = await asyncio.gather(first, second)
        return calls, first_result, second_result

    calls, first_result, second_result = asyncio.run(scenario())

    assert calls == 1
    assert first_result == second_result