import asyncio

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from cms_planner.api.routes.recovery import create_recovery_router
from cms_planner.application.recovery.commands import RecoveryCommand
from cms_planner.application.recovery.service import RecoveryService


def test_duplicate_endpoint_commands_make_one_provider_call() -> None:
    async def scenario() -> tuple[int, dict[str, object], dict[str, object]]:
        calls = 0
        entered = asyncio.Event()
        release = asyncio.Event()

        async def retry_operation(command: RecoveryCommand) -> str:
            nonlocal calls
            calls += 1
            entered.set()
            await release.wait()
            return "review-ready output"

        app = FastAPI()
        app.include_router(create_recovery_router(RecoveryService(retry_operation)))
        payload = {
            "case_id": "case-1",
            "failure": {
                "stage": "ocr",
                "code": "provider-failed",
                "page_number": 2,
                "retryable": True,
            },
            "confirmed_deficiency_ids": ["def-1"],
            "retained_poc_ids": ["poc-1"],
        }

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            first = asyncio.create_task(client.post("/recovery/retry", json=payload))
            second = asyncio.create_task(client.post("/recovery/retry", json=payload))
            await entered.wait()
            release.set()
            first_response, second_response = await asyncio.gather(first, second)
        return calls, first_response.json(), second_response.json()

    calls, first_payload, second_payload = asyncio.run(scenario())

    assert calls == 1
    assert first_payload == second_payload
    assert first_payload["confirmed_deficiency_ids"] == ["def-1"]
    assert first_payload["retained_poc_ids"] == ["poc-1"]