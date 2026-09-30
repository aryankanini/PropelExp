"""FastAPI adapter for request-changes and POC edit transitions."""

from typing import Annotated

from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse

from application.ports.case_repository import CaseRepository
from cms_planner.application.invalidate_approval import RequestChanges, SavePocEdit
from cms_planner.modules.approval.reapproval_schemas import (
    PocEditRequest,
    ReapprovalResponse,
)
from domain.case.revision_errors import StaleRevisionError


def create_reapproval_router(repository: CaseRepository) -> APIRouter:
    """Create review-disposition and atomic revision-save routes."""
    router = APIRouter(prefix="/api/v1/cases", tags=["reapproval"])
    request_changes = RequestChanges(repository)
    save_edit = SavePocEdit(repository)

    @router.post("/{case_id}/approval/request-changes", response_model=ReapprovalResponse)
    def request_poc_changes(
        case_id: str,
        session_id: Annotated[str, Header(alias="X-Session-ID", min_length=1)],
        actor_role: Annotated[str, Header(alias="X-Actor-Role", min_length=1)],
    ) -> ReapprovalResponse | JSONResponse:
        aggregate = repository.get(session_id)
        if aggregate is None or aggregate.case_id != case_id:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Case not found"})
        if actor_role != "compliance_leader":
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Compliance leader role required"})
        return ReapprovalResponse(**request_changes.execute(session_id=session_id).model_dump())

    @router.patch(
        "/{case_id}/poc",
        response_model=ReapprovalResponse,
        responses={409: {"description": "Stale revision"}},
    )
    def save_poc_edit(
        case_id: str,
        request: PocEditRequest,
        session_id: Annotated[str, Header(alias="X-Session-ID", min_length=1)],
    ) -> ReapprovalResponse | JSONResponse:
        aggregate = repository.get(session_id)
        if aggregate is None or aggregate.case_id != case_id:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Case not found"})
        try:
            decision = save_edit.execute(
                session_id=session_id,
                expected_revision_id=request.expected_revision_id,
                revision_id=request.revision_id,
                section_updates=request.section_updates,
            )
        except StaleRevisionError as error:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "code": "stale_revision",
                    "current_revision_id": error.current_revision_id,
                },
            )
        return ReapprovalResponse(**decision.model_dump())

    return router