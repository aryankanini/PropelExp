"""FastAPI application composition root."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from tempfile import gettempdir

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from adapters.filesystem.document_inspector import FilesystemDocumentInspector
from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from cms_planner.adapters.ai.guardrails import DeterministicPocGuardrails
from cms_planner.adapters.ai.httpx_transport import HttpxJsonTransport
from cms_planner.adapters.ai.openai_poc_provider import OpenAiPocProvider
from cms_planner.adapters.ocr.adapter import GuardedOcrAdapter
from cms_planner.adapters.repositories.in_memory_poc_repository import (
    InMemoryPocRepository,
)
from cms_planner.api.approval import create_approval_router
from cms_planner.api.confirmations import create_confirmations_router
from cms_planner.api.corrections import create_corrections_router
from cms_planner.api.export import create_export_router
from cms_planner.api.poc import create_poc_router
from cms_planner.api.problems import register_exception_handlers
from cms_planner.api.provenance import create_provenance_router
from cms_planner.api.reapproval import create_reapproval_router
from cms_planner.api.resolutions import create_resolutions_router
from cms_planner.api.review import create_review_router
from cms_planner.api.routes.case_lifecycle import create_case_lifecycle_router
from cms_planner.api.routes.case_projection import create_case_projection_router
from cms_planner.api.routes.cases import create_cases_router
from cms_planner.api.routes.extraction_jobs import (
    create_extraction_jobs_router,
    create_job_events_router,
)
from cms_planner.api.routes.session_status import create_session_status_router
from cms_planner.application.confirmation_service import ConfirmationService
from cms_planner.application.correction_service import CorrectionService
from cms_planner.application.failures import ProviderFailure
from cms_planner.application.poc_generation_service import PocGenerationService
from cms_planner.application.poc_revision_service import PocRevisionService
from cms_planner.application.ports.ocr import OcrPort
from cms_planner.application.ports.poc_provider import PocProvider
from cms_planner.application.ports.poc_repository import PocRepository
from cms_planner.application.provenance_service import ProvenanceService
from cms_planner.application.provider_approval import require_provider_approval
from cms_planner.application.providers.executor import ProviderExecutor
from cms_planner.application.resolution_service import ResolutionService
from cms_planner.application.review_service import ReviewService
from cms_planner.domain.poc_generation import PocGenerationInput
from cms_planner.infrastructure.config.provider import (
    ProviderConfigurationError,
    ProviderSettings,
)
from cms_planner.infrastructure.observability.correlation import (
    correlation_context,
    resolve_correlation_id,
)
from cms_planner.modules.extraction.job_runner import ExtractionJobRunner
from application.inactivity_policy import InactivityPolicy
from application.intake.upload_guard import UploadGuard
from application.intake.upload_service import UploadService
from application.services.cleanup_case import CleanupCase
from application.session_status import GetSessionStatus
from infrastructure.state.shutdown_cleanup import ShutdownCleanup

CORRELATION_HEADER = "X-Correlation-ID"
LOCAL_FRONTEND_ORIGINS = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
)


class _UnavailablePocProvider:
    def generate(self, request: PocGenerationInput) -> object:
        raise ProviderFailure()


class _UnavailableOcrProvider:
    async def recognize(self, request: object) -> object:
        raise ProviderFailure()


@dataclass(frozen=True, slots=True)
class ProviderRegistry:
    """Approved outbound adapters available to application services."""

    ocr: GuardedOcrAdapter


def register_provider_adapters(
    settings: ProviderSettings,
    ocr_provider: OcrPort,
) -> ProviderRegistry:
    """Register adapters only after the centralized approval gate passes."""
    approval = require_provider_approval(settings.approval)
    return ProviderRegistry(
        ocr=GuardedOcrAdapter(ocr_provider, approval=approval),
    )


def create_configured_poc_provider() -> PocProvider:
    try:
        settings = ProviderSettings.load()
    except ProviderConfigurationError:
        return _UnavailablePocProvider()
    return OpenAiPocProvider(
        settings,
        HttpxJsonTransport(settings.timeout_seconds),
        ProviderExecutor(timeout_seconds=settings.timeout_seconds),
    )


def create_app(
    workspace_root: Path | None = None,
    *,
    poc_repository: PocRepository | None = None,
    poc_provider: PocProvider | None = None,
) -> FastAPI:
    root = workspace_root or Path(gettempdir()) / "cms-planner-workspaces"
    repository = InMemoryCaseRepository()
    active_poc_repository = poc_repository or InMemoryPocRepository()
    active_poc_provider = poc_provider or create_configured_poc_provider()
    workspace = TemporaryWorkspace(root)
    job_runner = ExtractionJobRunner()
    ocr_adapter = GuardedOcrAdapter(_UnavailableOcrProvider(), approved=False)
    inactivity_policy = InactivityPolicy()
    cleanup = CleanupCase(repository, workspace)
    shutdown_cleanup = ShutdownCleanup(repository, workspace, cleanup)
    upload_service = UploadService(
        repository,
        workspace,
        FilesystemDocumentInspector(workspace),
        UploadGuard(),
    )

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncGenerator[None]:
        yield
        application.state.shutdown_results = shutdown_cleanup.execute()

    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=LOCAL_FRONTEND_ORIGINS,
        allow_credentials=True,
        allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
        allow_headers=("*",),
    )
    register_exception_handlers(app)

    @app.middleware("http")
    async def propagate_correlation(request: Request, call_next):
        correlation_id = resolve_correlation_id(request.headers.get(CORRELATION_HEADER))
        request.state.correlation_id = correlation_id
        with correlation_context(correlation_id):
            response = await call_next(request)
        response.headers[CORRELATION_HEADER] = correlation_id
        return response

    app.include_router(create_cases_router(upload_service, inactivity_policy))
    app.include_router(
        create_extraction_jobs_router(
            repository,
            workspace,
            ocr_adapter,
            job_runner,
        )
    )
    app.include_router(create_job_events_router(job_runner))
    app.include_router(create_case_lifecycle_router(repository, cleanup))
    app.include_router(
        create_session_status_router(GetSessionStatus(inactivity_policy, repository))
    )
    app.include_router(
        create_poc_router(
            repository=active_poc_repository,
            generation_service=PocGenerationService(
                active_poc_repository,
                active_poc_provider,
                DeterministicPocGuardrails(),
            ),
            revision_service=PocRevisionService(active_poc_repository),
            case_repository=repository,
        )
    )
    app.include_router(create_approval_router(repository))
    app.include_router(create_reapproval_router(repository))
    app.include_router(create_export_router(repository))
    app.include_router(create_case_projection_router(repository))
    app.include_router(create_review_router(ReviewService(repository)))
    app.include_router(create_resolutions_router(ResolutionService(repository)))
    app.include_router(create_corrections_router(CorrectionService(repository)))
    app.include_router(
        create_confirmations_router(
            ConfirmationService(repository, active_poc_repository)
        )
    )
    app.include_router(create_provenance_router(ProvenanceService(repository)))
    app.state.repository = repository
    app.state.poc_repository = active_poc_repository
    app.state.workspace = workspace
    return app


app = create_app()