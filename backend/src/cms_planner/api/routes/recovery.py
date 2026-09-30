"""HTTP route for selective failed-operation recovery."""

from fastapi import APIRouter

from cms_planner.application.recovery.commands import RecoveryCommand, RecoveryResult
from cms_planner.application.recovery.service import RecoveryService


def create_recovery_router(service: RecoveryService) -> APIRouter:
    router = APIRouter(prefix="/recovery", tags=["recovery"])

    @router.post("/retry", response_model=RecoveryResult)
    async def retry_failed_operation(command: RecoveryCommand) -> RecoveryResult:
        return await service.retry(command)

    return router