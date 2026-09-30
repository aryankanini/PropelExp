from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.main import app, create_app


def test_backend_composition_root_creates_independent_app() -> None:
    created_app = create_app()

    assert isinstance(created_app, FastAPI)
    assert created_app is not app
    assert created_app.routes
    assert "/api/v1/cases" in created_app.openapi()["paths"]
    assert "/api/v1/cases/{case_id}/extraction-jobs" in (
        created_app.openapi()["paths"]
    )
    assert "/api/v1/jobs/{job_id}/events" in created_app.openapi()["paths"]


def test_local_frontend_preflight_is_allowed() -> None:
    with TestClient(create_app()) as client:
        response = client.options(
            "/api/v1/session/status",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == (
        "http://localhost:5173"
    )


def test_untrusted_frontend_preflight_is_rejected() -> None:
    with TestClient(create_app()) as client:
        response = client.options(
            "/api/v1/session/status",
            headers={
                "Origin": "https://untrusted.example",
                "Access-Control-Request-Method": "GET",
            },
        )

    assert response.status_code == 400