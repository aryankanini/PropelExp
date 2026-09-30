"""Reviewer correction endpoint."""

from fastapi import APIRouter

from domain.case.errors import CaseNotFoundError
from cms_planner.api.errors import (
    ERROR_RESPONSES,
    ProblemDetail,
    raise_problem,
    raise_stale_problem,
)
from cms_planner.application.correction_service import CorrectionService
from cms_planner.domain.review import ReviewField, StaleReviewRevisionError
from cms_planner.domain.revisions import CorrectionCommand


def create_corrections_router(service: CorrectionService) -> APIRouter:
    router = APIRouter(prefix="/sessions/{session_id}", tags=["review"])

    @router.patch(
        "/review-fields/{field_id}/correction",
        response_model=ReviewField,
        responses=ERROR_RESPONSES,
    )
    def correct(
        session_id: str,
        field_id: str,
        command: CorrectionCommand,
    ) -> ReviewField:
        try:
            return service.correct(session_id, field_id, command)
        except (CaseNotFoundError, KeyError):
            raise_problem(
                404,
                ProblemDetail(
                    code="review-field-not-found",
                    message="Review field not found.",
                ),
            )
        except StaleReviewRevisionError as error:
            raise_stale_problem(error)
        except ValueError:
            raise_problem(
                422,
                ProblemDetail(
                    code="empty-correction",
                    message="Correction must not be empty.",
                ),
            )

    return router
