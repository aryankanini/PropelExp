import asyncio
from pathlib import Path

import pymupdf
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import SecretStr

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from cms_planner.adapters.ocr.adapter import GuardedOcrAdapter
from cms_planner.api.review import create_review_router
from cms_planner.api.routes.extraction_jobs import create_extraction_jobs_router
from cms_planner.api.routes.extraction_jobs import _extract_pages_from_bytes
from cms_planner.application.provider_approval import ProviderApproval
from cms_planner.application.review_service import ReviewService
from cms_planner.domain.job_event import JobTerminalStatus
from cms_planner.domain.review import Origin
from cms_planner.infrastructure.config.provider import ProviderSettings
from cms_planner.modules.extraction.job_runner import ExtractionJobRunner
from cms_planner.modules.extraction.sod_llm_cleaner import LlmCleanResult, LlmPointResult
from domain.case.aggregate import CaseAggregate


class NullOcrProvider:
    async def recognize(self, request: object) -> object:
        raise AssertionError("OCR should not be used for a text PDF")


def cms2567_pdf() -> bytes:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "FORM CMS-2567\nSTATEMENT OF DEFICIENCIES AND PLAN OF CORRECTION\n"
        "PROVIDER/SUPPLIER/CLIA IDENTIFICATION NUMBER: 12-3456\n"
        "NAME OF PROVIDER OR SUPPLIER: North Valley Care Center\n"
        "F 0686\n1. Repositioning was not documented.\n"
        "2. The care plan was not updated.",
    )
    page.insert_text(
        (330, 220),
        "FACILITY POC TEXT MUST NOT APPEAR IN THE SOD.",
    )
    page.insert_text(
        (72, 740),
        "FORM CMS-2567 Previous Versions Obsolete disclosure footer.",
    )
    content = document.tobytes()
    document.close()
    return content


def multi_page_cms2567_pdf() -> bytes:
    document = pymupdf.open()
    first_page = document.new_page()
    first_page.insert_text(
        (72, 72),
        "FORM CMS-2567\nSTATEMENT OF DEFICIENCIES AND PLAN OF CORRECTION\n"
        "K 0000\nA Life Safety Code survey found the facility",
    )
    second_page = document.new_page()
    second_page.insert_text(
        (72, 72),
        "DEPARTMENT OF HEALTH AND HUMAN SERVICES\n"
        "CENTERS FOR MEDICARE & MEDICAID SERVICES\n"
        "SUMMARY STATEMENT OF DEFICIENCIES",
    )
    second_page.insert_text(
        (72, 220),
        "K 0000 Continued From page 1\n"
        "not in compliance with Life Safety Code requirements.",
    )
    content = document.tobytes()
    document.close()
    return content


def alternate_geometry_cms2567_pdf() -> bytes:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "FORM CMS-2567\nSTATEMENT OF DEFICIENCIES AND PLAN OF CORRECTION",
    )
    page.insert_text(
        (310, 220),
        "F 0686\nResidents did not receive required treatment.",
    )
    content = document.tobytes()
    document.close()
    return content


def test_continuation_page_excludes_repeated_cms_header() -> None:
    pages = _extract_pages_from_bytes(multi_page_cms2567_pdf())

    assert "DEPARTMENT OF HEALTH" not in pages[1].spans[0].text
    assert "CENTERS FOR MEDICARE" not in pages[1].spans[0].text
    assert "not in compliance" in pages[1].spans[0].text


def test_full_text_fallback_recovers_tags_outside_standard_sod_crop() -> None:
    content = alternate_geometry_cms2567_pdf()

    cropped_pages = _extract_pages_from_bytes(content)
    full_pages = _extract_pages_from_bytes(content, crop_cms_sod_column=False)

    assert "F 0686" not in cropped_pages[0].spans[0].text
    assert "F 0686" in full_pages[0].spans[0].text


def test_preprocessed_llm_result_is_available_to_review_api(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repository = InMemoryCaseRepository()
    workspace = TemporaryWorkspace(tmp_path)
    handle = workspace.begin_upload("session-1")
    workspace.write(handle, cms2567_pdf())
    workspace.complete(handle)
    repository.add(
        CaseAggregate(
            session_id="session-1",
            case_id="case-1",
            documents=(handle.upload_id,),
        )
    )

    captured = {}

    async def clean_sod(preprocessed, f_tag, **kwargs):
        captured["preprocessed"] = preprocessed
        captured["f_tag"] = f_tag
        return LlmCleanResult(
            sod_text="1. Repositioning records were incomplete.",
            poc_suggestion="1. Audit repositioning records each shift.",
            points=[
                LlmPointResult(
                    label="1.",
                    text="Repositioning records were incomplete.",
                    poc="Audit repositioning records each shift.",
                )
            ],
        )

    settings = ProviderSettings.model_construct(
        endpoint="https://provider.example/v1",
        model="test-model",
        timeout_seconds=10,
        approval=ProviderApproval(baa=True, retention=True, training_use=True, risk=True),
    )
    settings._api_key = SecretStr("test-key")
    monkeypatch.setattr(
        "cms_planner.api.routes.extraction_jobs.ProviderSettings.load",
        lambda: settings,
    )
    monkeypatch.setattr(
        "cms_planner.api.routes.extraction_jobs.clean_sod_with_llm",
        clean_sod,
    )

    job_runner = ExtractionJobRunner()
    ocr_adapter = GuardedOcrAdapter(NullOcrProvider(), approval=settings.approval)
    app = FastAPI()
    app.include_router(
        create_extraction_jobs_router(repository, workspace, ocr_adapter, job_runner)
    )
    app.include_router(create_review_router(ReviewService(repository)))

    with TestClient(app) as client:
        accepted = client.post(
            "/api/v1/cases/case-1/extraction-jobs",
            headers={"X-Session-ID": "session-1"},
        )
        job_id = accepted.json()["job_id"]
        asyncio.run(_wait_for_job(job_runner, job_id))

        repeated = client.post(
            "/api/v1/cases/case-1/extraction-jobs",
            headers={"X-Session-ID": "session-1"},
        )
        repeated_job_id = repeated.json()["job_id"]
        asyncio.run(_wait_for_job(job_runner, repeated_job_id))
        review = client.get("/sessions/session-1/review")

    assert accepted.status_code == 202
    assert repeated.status_code == 202
    assert captured["f_tag"] == "F0686"
    assert "FORM CMS-2567" not in captured["preprocessed"].full_text
    assert captured["preprocessed"].points[0].text == "Repositioning was not documented."
    assert review.status_code == 200
    assert len(review.json()) == 3
    provider_fields = {
        field["label"]: field["revisions"][0]["value"]
        for field in review.json()
        if field["field_type"] == "provider"
    }
    assert provider_fields == {
        "Provider name": "North Valley Care Center",
        "Provider identification number": "12-3456",
    }
    field = next(item for item in review.json() if item["field_type"] == "sod")
    assert field["label"] == "F0686"
    assert field["revisions"][0]["value"] == (
        "1. Repositioning was not documented.\n"
        "2. The care plan was not updated."
    )
    assert "FACILITY POC" not in field["revisions"][0]["value"]
    assert "disclosure footer" not in field["revisions"][0]["value"]
    assert "Audit repositioning records each shift." in field["poc_suggestion"]


async def _wait_for_job(job_runner: ExtractionJobRunner, job_id: str) -> None:
    async for event in job_runner.stream_events(job_id):
        if event.terminal_status is not None:
            assert event.terminal_status is JobTerminalStatus.COMPLETED
            return
