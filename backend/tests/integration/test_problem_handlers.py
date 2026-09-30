from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from cms_planner.api.problems import register_exception_handlers


class _RequestBody(BaseModel):
    count: int


def _test_app() -> FastAPI:
    app = FastAPI()
    register_exception_handlers(app)

    @app.post("/validate")
    async def validate(body: _RequestBody) -> _RequestBody:
        return body

    @app.get("/fail")
    async def fail() -> None:
        raise RuntimeError("provider payload with document-secret")

    return app


def test_validation_response_uses_safe_problem_contract() -> None:
    client = TestClient(_test_app(), raise_server_exceptions=False)

    response = client.post(
        "/validate",
        headers={"X-Correlation-ID": "corr-validation"},
        json={"count": "document-secret"},
    )

    assert response.status_code == 422
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["code"] == "validation_failed"
    assert response.json()["field_errors"] == [
        {"field": "body.count", "message": "Invalid value."}
    ]
    assert "document-secret" not in response.text


def test_unknown_exception_returns_safe_correlated_problem() -> None:
    app = _test_app()

    @app.middleware("http")
    async def set_correlation_id(request, call_next):
        request.state.correlation_id = request.headers["X-Correlation-ID"]
        return await call_next(request)

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get(
        "/fail", headers={"X-Correlation-ID": "corr-unknown"}
    )

    assert response.status_code == 500
    assert response.json()["correlation_id"] == "corr-unknown"
    assert response.json()["code"] == "internal_error"
    assert "provider payload" not in response.text
    assert "document-secret" not in response.text