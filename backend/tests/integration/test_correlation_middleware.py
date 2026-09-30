from fastapi.testclient import TestClient

from cms_planner.app import create_app


def test_request_correlation_is_returned_on_response() -> None:
    app = create_app()

    @app.get("/ok")
    async def ok() -> dict[str, bool]:
        return {"ok": True}

    response = TestClient(app).get(
        "/ok", headers={"X-Correlation-ID": "corr-request-1"}
    )

    assert response.headers["X-Correlation-ID"] == "corr-request-1"


def test_invalid_correlation_value_is_replaced() -> None:
    app = create_app()

    @app.get("/ok")
    async def ok() -> dict[str, bool]:
        return {"ok": True}

    response = TestClient(app).get(
        "/ok", headers={"X-Correlation-ID": "bad value"}
    )

    assert response.headers["X-Correlation-ID"] != "bad value"