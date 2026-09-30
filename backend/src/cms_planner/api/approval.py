"""FastAPI adapter for current-revision approval."""

from typing import Annotated

from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse

from application.ports.case_repository import CaseRepository
from cms_planner.application.approve_revision import ApproveRevision
from cms_planner.modules.approval.schemas import ApprovalRequest, ApprovalResponse


def create_approval_router(repository: CaseRepository) -> APIRouter:
    """Create the server-authoritative approval route."""
    router = APIRouter(prefix="/api/v1/cases", tags=["approval"])
    command = ApproveRevision(repository)

    @router.post(
        "/{case_id}/approval",
        response_model=ApprovalResponse,
        responses={404: {"description": "Case not found"}, 409: {"model": ApprovalResponse}},
    )
    def approve_revision(
        case_id: str,
        request: ApprovalRequest,
        session_id: Annotated[str, Header(alias="X-Session-ID", min_length=1)],
        actor_id: Annotated[str, Header(alias="X-Actor-ID", min_length=1)],
        actor_role: Annotated[str, Header(alias="X-Actor-Role", min_length=1)],
    ) -> ApprovalResponse | JSONResponse:
        aggregate = repository.get(session_id)
        if aggregate is None or aggregate.case_id != case_id:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Case not found"})
        decision = command.execute(
            session_id=session_id,
            reviewed_revision_id=request.revision_id,
            actor_id=actor_id,
            actor_role=actor_role,
        )
        response = ApprovalResponse(
            approved=decision.approved,
            approval=decision.approval,
            blockers=decision.blockers,
            copy_enabled=decision.approval.export_enabled,
            download_enabled=decision.approval.export_enabled,
        )
        if decision.blockers:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=response.model_dump(mode="json"),
            )
        return response

    return router