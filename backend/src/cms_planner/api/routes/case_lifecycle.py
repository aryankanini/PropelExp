"""FastAPI adapter for explicit transient case termination."""

from typing import Annotated

from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse

from application.ports.case_repository import CaseRepository
from application.services.cleanup_case import CleanupCase
from cms_planner.api.schemas.cleanup import CleanupResponse


def create_case_lifecycle_router(
    repository: CaseRepository,
    cleanup: CleanupCase,
) -> APIRouter:
    """Create the session-owned case deletion route."""
    router = APIRouter(prefix="/api/v1/cases", tags=["case-lifecycle"])

    @router.delete(
        "/{case_id}",
        response_model=CleanupResponse,
        responses={404: {"description": "Case not found"}, 503: {"model": CleanupResponse}},
    )
    def end_case(
        case_id: str,
        session_id: Annotated[str, Header(alias="X-Session-ID", min_length=1)],
    ) -> CleanupResponse | JSONResponse:
        aggregate = repository.get(session_id)
        if aggregate is None or aggregate.case_id != case_id:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "Case not found"},
            )

        result = cleanup.execute(session_id)
        response = CleanupResponse(**result.model_dump())
        if result.outcome == "failed":
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content=response.model_dump(mode="json"),
            )
        return response

    return router