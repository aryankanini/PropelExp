"""Uncertainty-resolution endpoint."""

from fastapi import APIRouter

from domain.case.errors import CaseNotFoundError
from cms_planner.api.errors import (
    ERROR_RESPONSES,
    ProblemDetail,
    raise_problem,
    raise_stale_problem,
)
from cms_planner.application.resolution_service import (
    ResolutionCommand,
    ResolutionService,
)
from cms_planner.domain.review import (
    CandidateNotFoundError,
    ReviewField,
    StaleReviewRevisionError,
)


def create_resolutions_router(service: ResolutionService) -> APIRouter:
    router = APIRouter(prefix="/sessions/{session_id}", tags=["review"])

    @router.patch(
        "/review-fields/{field_id}/resolution",
        response_model=ReviewField,
        responses=ERROR_RESPONSES,
    )
    def resolve(
        session_id: str,
        field_id: str,
        command: ResolutionCommand,
    ) -> ReviewField:
        try:
            return service.resolve(session_id, field_id, command)
        except (CaseNotFoundError, KeyError, CandidateNotFoundError):
            raise_problem(
                404,
                ProblemDetail(
                    code="review-field-not-found",
                    message="Review field or candidate not found.",
                ),
            )
        except StaleReviewRevisionError as error:
            raise_stale_problem(error)

    return router
