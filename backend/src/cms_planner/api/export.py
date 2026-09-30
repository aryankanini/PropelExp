"""FastAPI adapter for authorized local POC export."""

from typing import Annotated, Literal

from fastapi import APIRouter, Header, Query, status
from fastapi.responses import JSONResponse

from application.ports.case_repository import CaseRepository
from cms_planner.application.export_approved_revision import (
    ExportApprovedRevision,
    ExportFormattingError,
)
from cms_planner.domain.export_policy import ExportBlocker
from cms_planner.modules.export.schemas import (
    ExportBlockedResponse,
    ExportFailureResponse,
    ExportResponse,
)


def create_export_router(repository: CaseRepository) -> APIRouter:
    """Create the current-approval export route."""
    router = APIRouter(prefix="/api/v1/cases", tags=["export"])
    service = ExportApprovedRevision(repository)

    @router.get(
        "/{case_id}/export",
        response_model=ExportResponse,
        responses={
            409: {"model": ExportBlockedResponse},
            503: {"model": ExportFailureResponse},
        },
    )
    def export_revision(
        case_id: str,
        export_format: Annotated[Literal["copy", "download"], Query(alias="format")],
        session_id: Annotated[str, Header(alias="X-Session-ID", min_length=1)],
    ) -> ExportResponse | JSONResponse:
        aggregate = repository.get(session_id)
        if aggregate is None or aggregate.case_id != case_id:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Case not found"})
        try:
            result = service.execute(
                session_id=session_id,
                export_format=export_format,
            )
        except ExportFormattingError:
            failure = ExportFailureResponse()
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content=failure.model_dump(mode="json"),
            )
        if isinstance(result, ExportBlocker):
            blocked = ExportBlockedResponse(blocker=result)
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=blocked.model_dump(mode="json"),
            )
        return ExportResponse(
            format=export_format,
            content=result.content,
            media_type=result.media_type,
            filename=result.filename,
        )

    return router