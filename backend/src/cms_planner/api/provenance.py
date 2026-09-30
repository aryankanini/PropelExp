"""Current and historical provenance endpoint."""

from fastapi import APIRouter

from domain.case.errors import CaseNotFoundError
from cms_planner.api.errors import ERROR_RESPONSES, ProblemDetail, raise_problem
from cms_planner.application.provenance_service import ProvenanceService
from cms_planner.domain.provenance import ProvenanceProjection


def create_provenance_router(service: ProvenanceService) -> APIRouter:
    router = APIRouter(prefix="/sessions/{session_id}", tags=["review"])

    @router.get(
        "/review-fields/{field_id}/provenance",
        response_model=ProvenanceProjection,
        responses=ERROR_RESPONSES,
    )
    def get_provenance(session_id: str, field_id: str) -> ProvenanceProjection:
        try:
            return service.get(session_id, field_id)
        except (CaseNotFoundError, KeyError):
            raise_problem(
                404,
                ProblemDetail(
                    code="review-field-not-found",
                    message="Review field not found.",
                ),
            )

    return router