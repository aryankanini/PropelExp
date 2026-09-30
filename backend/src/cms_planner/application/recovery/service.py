"""Coordinate one active retry for each typed failed operation."""

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeAlias

from cms_planner.application.recovery.commands import (
    RecoveryCommand,
    RecoveryOutcome,
    RecoveryResult,
)
from cms_planner.domain.job_failure import JobStage

RetryOperation: TypeAlias = Callable[[RecoveryCommand], Awaitable[str]]
OperationKey: TypeAlias = tuple[str, JobStage, int | str]


class ProviderRetriesExhaustedError(Exception):
    """Report exhaustion while keeping the operation eligible for a later retry."""


class RecoveryService:
    """Dispatch only the failed operation and coalesce concurrent duplicates."""

    def __init__(self, retry_operation: RetryOperation) -> None:
        self._retry_operation = retry_operation
        self._active: dict[OperationKey, asyncio.Task[RecoveryResult]] = {}
        self._active_lock = asyncio.Lock()

    async def retry(self, command: RecoveryCommand) -> RecoveryResult:
        if not command.source_valid and command.failure.stage in (
            JobStage.EXTRACTION,
            JobStage.OCR,
        ):
            return RecoveryResult(
                outcome=RecoveryOutcome.REPLACEMENT_REQUIRED,
                failure=command.failure,
            )

        key = _operation_key(command)
        async with self._active_lock:
            task = self._active.get(key)
            if task is None:
                task = asyncio.create_task(self._run_retry(command))
                self._active[key] = task

        try:
            return await asyncio.shield(task)
        finally:
            async with self._active_lock:
                if self._active.get(key) is task and task.done():
                    del self._active[key]

    async def _run_retry(self, command: RecoveryCommand) -> RecoveryResult:
        try:
            output = await self._retry_operation(command)
        except ProviderRetriesExhaustedError:
            return RecoveryResult(
                outcome=RecoveryOutcome.RETRY_LATER,
                failure=command.failure,
            )
        return RecoveryResult(
            outcome=RecoveryOutcome.REVIEW_READY,
            failure=command.failure,
            output=output,
        )


def _operation_key(command: RecoveryCommand) -> OperationKey:
    operation_id: int | str
    if command.failure.page_number is not None:
        operation_id = command.failure.page_number
    else:
        operation_id = command.failure.deficiency_id or ""
    return (command.case_id, command.failure.stage, operation_id)