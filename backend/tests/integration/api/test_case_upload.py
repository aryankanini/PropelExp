from pathlib import Path

import pymupdf
from fastapi import FastAPI
from fastapi.testclient import TestClient

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from application.inactivity_policy import InactivityPolicy
from application.intake.commands import UploadLimits
from application.intake.preflight import DocumentInspection
from application.intake.upload_guard import UploadGuard
from application.intake.upload_service import UploadService
from application.ports.workspace import UploadHandle
from cms_planner.app import create_app
from cms_planner.api.routes.cases import create_cases_router


def cms2567_pdf() -> bytes:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "CMS-2567 Statement of Deficiencies and Plan of Correction",
    )
    content = document.tobytes()
    document.close()
    return content


class StubInspector:
    def __init__(self, page_texts: tuple[str | None, ...]) -> None:
        self._inspection = DocumentInspection(page_texts=page_texts)

    def inspect(
        self,
        _handle: UploadHandle,
        _media_type: str,
        _max_pages: int,
    ) -> DocumentInspection:
        return self._inspection


def bounded_app(
    tmp_path: Path,
    *,
    page_texts: tuple[str | None, ...],
    max_bytes: int = 10,
    max_pages: int = 2,
) -> FastAPI:
    repository = InMemoryCaseRepository()
    workspace = TemporaryWorkspace(tmp_path)
    service = UploadService(
        repository,
        workspace,
        StubInspector(page_texts),
        UploadGuard(),
        UploadLimits(max_bytes=max_bytes, max_pages=max_pages),
    )
    app = FastAPI()
    app.include_router(create_cases_router(service, InactivityPolicy()))
    app.state.repository = repository
    app.state.workspace = workspace
    return app


def test_upload_status_and_explicit_cleanup(tmp_path: Path) -> None:
    app = create_app(tmp_path)
    headers = {"X-Session-ID": "session-1"}

    with TestClient(app) as client:
        uploaded = client.post(
            "/api/v1/cases",
            headers=headers,
            files={"file": ("cms-2567.pdf", cms2567_pdf(), "application/pdf")},
        )
        case_id = uploaded.json()["case_id"]
        retention = client.get("/api/v1/session/status", headers=headers)
        cleaned = client.delete(f"/api/v1/cases/{case_id}", headers=headers)

    assert uploaded.status_code == 201
    assert uploaded.json()["status"] == "extraction_ready"
    assert retention.status_code == 200
    assert retention.json()["storage"] == "session_only"
    assert cleaned.status_code == 200
    assert cleaned.json()["remaining_files"] == 0


def test_non_cms_document_is_rejected_without_residue(tmp_path: Path) -> None:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "Unrelated readable report")
    content = document.tobytes()
    document.close()
    app = create_app(tmp_path)

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/cases",
            headers={"X-Session-ID": "session-1"},
            files={"file": ("report.pdf", content, "application/pdf")},
        )

    assert response.status_code == 422
    assert response.json()["code"] == "not_cms2567"
    assert app.state.repository.list_session_ids() == ()
    assert app.state.workspace.list_session_ids() == ()


def test_oversized_upload_returns_safe_problem_without_residue(tmp_path: Path) -> None:
    app = bounded_app(
        tmp_path,
        page_texts=("CMS-2567 Statement of Deficiencies and Plan of Correction",),
        max_bytes=4,
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/cases",
            headers={"X-Session-ID": "session-1"},
            files={"file": ("case.pdf", b"12345", "application/pdf")},
        )

    assert response.status_code == 413
    assert response.json()["code"] == "byte_limit_exceeded"
    assert app.state.workspace.list_session_ids() == ()


def test_over_page_upload_returns_safe_problem_without_residue(tmp_path: Path) -> None:
    app = bounded_app(
        tmp_path,
        page_texts=("page", "page", "page"),
        max_pages=2,
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/cases",
            headers={"X-Session-ID": "session-1"},
            files={"file": ("case.pdf", b"content", "application/pdf")},
        )

    assert response.status_code == 422
    assert response.json()["code"] == "page_limit_exceeded"
    assert app.state.workspace.list_session_ids() == ()


def test_second_upload_preserves_first_active_case(tmp_path: Path) -> None:
    app = bounded_app(
        tmp_path,
        page_texts=("CMS-2567 Statement of Deficiencies and Plan of Correction",),
    )
    headers = {"X-Session-ID": "session-1"}

    with TestClient(app) as client:
        accepted = client.post(
            "/api/v1/cases",
            headers=headers,
            files={"file": ("first.pdf", b"first", "application/pdf")},
        )
        original = app.state.repository.get("session-1")
        rejected = client.post(
            "/api/v1/cases",
            headers=headers,
            files={"file": ("second.pdf", b"second", "application/pdf")},
        )

    assert accepted.status_code == 201
    assert rejected.status_code == 409
    assert rejected.json()["code"] == "active_upload_exists"
    assert app.state.repository.get("session-1") == original
    assert app.state.workspace.count_files("session-1") == 1