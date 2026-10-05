"""FastAPI routes for extraction job lifecycle and SSE progress streaming."""

import asyncio
import html as _html
import json
import re as _re
from typing import Annotated
from uuid import uuid4

import pymupdf
from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict, Field

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from application.ports.workspace import UploadHandle
from cms_planner.adapters.ocr.adapter import GuardedOcrAdapter
from cms_planner.domain.cms_layout import CmsLayoutPattern, CmsLayoutStatus
from cms_planner.domain.deficiency_candidate import (
    DeficiencyCandidate,
    DeficiencyCandidateEvidence,
)
from cms_planner.domain.job_failure import JobStage
from cms_planner.domain.page import PageRoute, SourcePage
from cms_planner.domain.review import (
    Evidence,
    HighlightCoordinates,
    Origin,
    ReviewCandidate,
    ReviewField,
    ReviewRevision,
)
from cms_planner.domain.text_span import BoundingBox, ClassifiedPageText, TextSpan
from cms_planner.infrastructure.config.provider import (
    ProviderConfigurationError,
    ProviderSettings,
)
from cms_planner.modules.extraction.cms_structure_detector import detect_cms_layout
from cms_planner.modules.extraction.deficiency_boundaries import (
    identify_deficiency_boundaries,
)
from cms_planner.modules.extraction.job_runner import ExtractionJobRunner
from cms_planner.modules.extraction.page_classifier import classify_pages
from cms_planner.modules.extraction.provider_metadata import (
    ProviderMetadata,
    extract_provider_metadata,
)
from cms_planner.modules.extraction.sod_llm_cleaner import (
    LlmCleanResult,
    PreprocessedSod,
    clean_sod_with_llm,
    preprocess_sod_text,
)
from cms_planner.modules.extraction.text_normalizer import normalize_extracted_page


class ExtractionJobAccepted(BaseModel):
    model_config = ConfigDict(frozen=True)

    job_id: str = Field(min_length=1)
    case_id: str = Field(min_length=1)
    status: str = "accepted"


def create_extraction_jobs_router(
    repository: InMemoryCaseRepository,
    workspace: TemporaryWorkspace,
    ocr_adapter: GuardedOcrAdapter,
    job_runner: ExtractionJobRunner,
) -> APIRouter:
    router = APIRouter(prefix="/api/v1/cases", tags=["extraction"])

    @router.post(
        "/{case_id}/extraction-jobs",
        response_model=ExtractionJobAccepted,
        status_code=status.HTTP_202_ACCEPTED,
    )
    async def start_extraction(
        case_id: str,
        session_id: Annotated[str, Header(alias="X-Session-ID", min_length=1)],
    ) -> ExtractionJobAccepted:

        aggregate = repository.get(session_id)
        if aggregate is None or aggregate.case_id != case_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")

        job_id = job_runner.create_job()

        async def run_extraction() -> None:
            # --- read document ---
            upload_id = aggregate.documents[0] if aggregate.documents else None
            if upload_id is None:
                raise RuntimeError("No document attached to case")

            handle = UploadHandle(session_id=session_id, upload_id=upload_id)
            with workspace.open_read(handle) as f:
                content = f.read()

            # --- extract pages ---
            classified_pages = _extract_pages_from_bytes(content)
            job_runner.emit_progress(job_id, JobStage.EXTRACTION, 30)

            # --- OCR pass ---
            final_pages: list[ClassifiedPageText] = []
            for page in classified_pages:
                if page.classification.route == PageRoute.OCR_REQUIRED:
                    from cms_planner.application.ports.ocr_types import (
                        OcrPageRequest,
                        OcrSuccess,
                    )
                    page_bytes = _get_page_bytes(content, page.classification.page_number)
                    ocr_result = await ocr_adapter.recognize(
                        OcrPageRequest(classification=page.classification, page_bytes=page_bytes)
                    )
                    if isinstance(ocr_result, OcrSuccess):
                        final_pages.append(
                            ClassifiedPageText(classification=page.classification, spans=ocr_result.spans)
                        )
                    else:
                        final_pages.append(page)
                else:
                    final_pages.append(page)

            _print_extracted_pages(final_pages)
            job_runner.emit_progress(job_id, JobStage.EXTRACTION, 60)

            # --- boundary detection ---
            layout = detect_cms_layout(final_pages)
            boundaries = identify_deficiency_boundaries(layout, tuple(final_pages))
            if not boundaries:
                fallback_pages = _extract_pages_from_bytes(
                    content,
                    crop_cms_sod_column=False,
                )
                fallback_layout = detect_cms_layout(fallback_pages)
                fallback_boundaries = identify_deficiency_boundaries(
                    fallback_layout,
                    tuple(fallback_pages),
                )
                if fallback_boundaries:
                    final_pages = fallback_pages
                    layout = fallback_layout
                    boundaries = fallback_boundaries
            provider_metadata = extract_provider_metadata(tuple(final_pages))

            print(f"[EXTRACTION] layout={layout.status} boundaries={len(boundaries)} pages={len(final_pages)}")
            for b in boundaries:
                print(f"[EXTRACTION]   {b.f_tag} complete={b.complete} sod_chars={len(b.sod_text or '')}")

            if layout.status is not CmsLayoutStatus.RECOGNIZED or not boundaries:
                raise RuntimeError(
                    "No deficiency boundaries found after cropped and full-text extraction "
                    f"(layout={layout.status})"
                )

            candidates = tuple(
                DeficiencyCandidate(
                    candidate_id=boundary.boundary_id,
                    boundary_id=boundary.boundary_id,
                    layout_pattern=CmsLayoutPattern.CMS_2567,
                    f_tag=boundary.f_tag,
                    sod_text=boundary.sod_text,
                    evidence=tuple(
                        DeficiencyCandidateEvidence(
                            evidence_id=f"{boundary.boundary_id}:p{ev.page_number}",
                            page_number=ev.page_number,
                            text=ev.text,
                        )
                        for ev in boundary.evidence
                    ),
                    confidence=1.0 if boundary.complete else 0.5,
                    uncertainty=boundary.uncertainty,
                    confirmed=False,
                )
                for boundary in boundaries
            )

            job_runner.emit_progress(job_id, JobStage.EXTRACTION, 80)

            # --- LLM cleaning ---
            job_runner.emit_progress(job_id, JobStage.GENERATION, 85)
            _provider_settings: ProviderSettings | None = None
            try:
                _provider_settings = ProviderSettings.load()
                print(f"[LLM] Provider loaded: {_provider_settings.model} @ {_provider_settings.endpoint}")
            except ProviderConfigurationError as e:
                print(f"[LLM] Provider config error: {e}")

            review_fields = list(_provider_review_fields(provider_metadata))
            for c in candidates:
                llm_result: LlmCleanResult | None = None
                if _provider_settings is not None:
                    preprocessed = preprocess_sod_text(c.sod_text or c.f_tag, c.f_tag)
                    llm_result = await clean_sod_with_llm(
                        preprocessed=preprocessed,
                        f_tag=c.f_tag,
                        endpoint=str(_provider_settings.endpoint),
                        api_key=_provider_settings.api_key.get_secret_value(),
                        model=_provider_settings.model,
                        timeout_seconds=float(_provider_settings.timeout_seconds),
                    )
                review_fields.append(_candidate_to_review_field(c, llm_result))

            # --- persist ---
            def _apply(current, _fields=tuple(review_fields), _candidates=candidates):
                updated = current.set_deficiency_candidates(_candidates)
                return updated.set_review_fields(_fields), None

            repository.update(session_id, _apply)

        asyncio.create_task(job_runner.run(job_id, run_extraction()))

        return ExtractionJobAccepted(job_id=job_id, case_id=case_id)

    return router


def _print_extracted_pages(pages: list[ClassifiedPageText]) -> None:
    print("[EXTRACTION] Extracted PDF text")
    for page in pages:
        text = "\n".join(span.text for span in page.spans) or "[no text extracted]"
        print(f"[EXTRACTION] --- page {page.page_number} ---")
        print(text)


def create_job_events_router(job_runner: ExtractionJobRunner) -> APIRouter:
    router = APIRouter(prefix="/api/v1/jobs", tags=["extraction"])

    @router.get("/{job_id}/events")
    async def stream_job_events(job_id: str, last_event_id: int = 0) -> StreamingResponse:
        async def generate():
            async for event in job_runner.stream_events(job_id, last_event_id):
                data = json.dumps(event.model_dump(mode="json"))
                yield f"id: {event.event_id}\ndata: {data}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    return router


def _extract_pages_from_bytes(
    content: bytes,
    *,
    crop_cms_sod_column: bool = True,
) -> list[ClassifiedPageText]:
    pages: list[ClassifiedPageText] = []
    with pymupdf.open(stream=content, filetype="pdf") as doc:
        full_page_texts = tuple(page.get_text("text").strip() for page in doc)
        is_cms_document = _looks_like_cms_document("\n".join(full_page_texts))

        for page_index, page in enumerate(doc):
            page_number = page_index + 1
            full_text = full_page_texts[page_index]
            native_text = _extract_native_reading_text(
                page,
                full_text,
                is_cms_document=is_cms_document and crop_cms_sod_column,
                include_header=page_index == 0,
            )
            source = SourcePage(
                page_number=page_number,
                native_text=native_text,
                native_text_complete=bool(native_text),
            )
            classification = classify_pages([source])[0]
            spans = (
                (TextSpan(page_number=page_number, text=native_text, coordinates=BoundingBox(x=0, y=0, width=1, height=1)),)
                if native_text
                else ()
            )
            pages.append(normalize_extracted_page(ClassifiedPageText(classification=classification, spans=spans)))
    return pages


def _extract_native_reading_text(
    page: pymupdf.Page,
    full_text: str,
    *,
    is_cms_document: bool,
    include_header: bool,
) -> str:
    if not is_cms_document:
        return full_text

    width = page.rect.width
    height = page.rect.height
    header = ""
    if include_header:
        header = page.get_text(
            "text",
            clip=pymupdf.Rect(0, 0, width, height * 0.21),
        ).strip()
    sod_body = page.get_text(
        "text",
        clip=pymupdf.Rect(0, height * 0.20, width * 0.48, height * 0.82),
    ).strip()
    return "\n".join(part for part in (header, sod_body) if part)


def _looks_like_cms_document(text: str) -> bool:
    normalized = " ".join(text.upper().split())
    return (
        "FORM CMS-2567" in normalized
        or "STATEMENT OF DEFICIENCIES AND PLAN OF CORRECTION" in normalized
    )


def _get_page_bytes(content: bytes, page_number: int) -> bytes:
    with pymupdf.open(stream=content, filetype="pdf") as doc:
        page = doc[page_number - 1]
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
        return pix.tobytes("png")


_BOILERPLATE_LINE = _re.compile(
    r"^("
    r"Colorado\s+De?[a-z]*\s+(?:of|Department|De).*|"
    r"[A-Z][A-Z ]+DIALYSIS\s+CENTER.*|"
    r"[A-Z][A-Z ]+CROSSING.*|"
    r"DEFICIENCY\)|"
    r"\(EACH\s+(?:DEFICIENCY|CORRECTIVE).*|"
    r"REGULATORY\s+OR\s+LSC.*|"
    r"CROSS.REFERENCED.*|"
    r"CORRECTIVE\s+ACTION\s+SHOULD.*|"
    r"PRINTED:.*|"
    r"FORM\s+APPROVED.*|"
    r"STATE\s+FORM.*|"
    r"If\s+continuation\s+sheet.*|"
    r"Health\s+Facilities.*|"
    r"LABORATORY\s+DIRECTOR.*|"
    r"[A-Z]\d{5,}|"
    r"\d{4,5}X?|"
    r"A\.\s*BUILDING.*|"
    r"B\.?\s*WING.*|"
    r"CONSTRUCTION\s*|"
    r"COMPLETED\s*|"
    r"\d{2}/\d{2}/\d{4}|"
    r"PREFIX\s*TAG?\s*|"
    r"\d{3,5}\s+[A-Z]\s+\w+.*|"
    r"[A-Z ,\.]+,\s*[A-Z]{2}\s+\d+.*|"
    r"BLVD\s*|"
    r"\d+\s*"
    r")$",
    _re.IGNORECASE,
)


def _clean_sod_text(text: str) -> str:
    lines = text.splitlines()
    cleaned = [line for line in lines if line.strip() and not _BOILERPLATE_LINE.match(line.strip())]
    return "\n".join(cleaned).strip()


def _candidate_to_review_field(
    candidate: DeficiencyCandidate,
    llm_result: LlmCleanResult | None = None,
) -> ReviewField:
    evidence_items = tuple(
        Evidence(
            page_number=item.page_number,
            full_snippet=item.text,
            highlight=HighlightCoordinates(x=0, y=0, width=1, height=1),
            source="native-text",
        )
        for item in candidate.evidence
    )
    evidence = evidence_items[0]

    value = _html.unescape(_clean_sod_text(candidate.sod_text or candidate.f_tag))

    if llm_result is not None:
        if llm_result.points:
            poc_suggestion = json.dumps(
                [{"label": p.label, "text": p.text, "poc": p.poc} for p in llm_result.points]
            )
        else:
            poc_suggestion = llm_result.poc_suggestion or None
    else:
        poc_suggestion = None

    revision_id = uuid4().hex
    return ReviewField(
        field_id=candidate.candidate_id,
        label=candidate.f_tag,
        deficiency_id=candidate.candidate_id,
        field_type="sod",
        candidates=(
            ReviewCandidate(
                candidate_id=candidate.candidate_id,
                value=value,
                confidence=candidate.confidence,
                uncertainty="Incomplete SOD text" if candidate.uncertainty else None,
                origin=Origin.EXTRACTED,
                evidence=evidence,
            ),
        ),
        revisions=(
            ReviewRevision(
                revision_id=revision_id,
                revision_number=1,
                value=value,
                origin=Origin.EXTRACTED,
                evidence=evidence,
                source_candidate_id=candidate.candidate_id,
            ),
        ),
        evidence_items=evidence_items,
        current_revision_id=revision_id,
        unresolved=candidate.uncertainty,
        poc_suggestion=poc_suggestion,
    )


def _provider_review_fields(
    metadata: ProviderMetadata | None,
) -> tuple[ReviewField, ...]:
    if metadata is None:
        return ()

    evidence = Evidence(
        page_number=metadata.page_number,
        full_snippet=metadata.evidence_text,
        highlight=HighlightCoordinates(x=0, y=0, width=1, height=1),
        source="native-text",
    )
    values = (
        ("provider:name", "Provider name", metadata.provider_name),
        (
            "provider:identification-number",
            "Provider identification number",
            metadata.provider_number,
        ),
    )

    fields: list[ReviewField] = []
    for field_id, label, value in values:
        revision_id = uuid4().hex
        fields.append(
            ReviewField(
                field_id=field_id,
                label=label,
                field_type="provider",
                candidates=(
                    ReviewCandidate(
                        candidate_id=field_id,
                        value=value,
                        confidence=1.0,
                        origin=Origin.EXTRACTED,
                        evidence=evidence,
                    ),
                ),
                revisions=(
                    ReviewRevision(
                        revision_id=revision_id,
                        revision_number=1,
                        value=value,
                        origin=Origin.EXTRACTED,
                        evidence=evidence,
                        source_candidate_id=field_id,
                    ),
                ),
                evidence_items=(evidence,),
                current_revision_id=revision_id,
            )
        )

    return tuple(fields)
