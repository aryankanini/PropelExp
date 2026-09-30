"""Evidence-review query endpoint."""

from fastapi import APIRouter

from domain.case.errors import CaseNotFoundError
from cms_planner.api.errors import ERROR_RESPONSES, ProblemDetail, raise_problem
from cms_planner.application.review_service import ReviewService
from cms_planner.domain.review import EvidenceUnavailableError, ReviewField


def create_review_router(service: ReviewService) -> APIRouter:
    router = APIRouter(prefix="/sessions/{session_id}", tags=["review"])

    @router.get(
        "/review",
        response_model=list[ReviewField],
        responses=ERROR_RESPONSES,
    )
    def get_review(session_id: str) -> tuple[ReviewField, ...]:
        try:
            return service.get_fields(session_id)
        except CaseNotFoundError:
            raise_problem(
                404,
                ProblemDetail(code="case-not-found", message="Active case not found."),
            )
        except EvidenceUnavailableError:
            raise_problem(
                503,
                ProblemDetail(
                    code="evidence-unavailable",
                    message="Supporting evidence is unavailable.",
                ),
            )

    return router
