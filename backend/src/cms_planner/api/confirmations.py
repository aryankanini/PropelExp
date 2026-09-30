"""Deficiency confirmation endpoint."""

from fastapi import APIRouter

from domain.case.errors import CaseNotFoundError
from cms_planner.api.errors import (
    ERROR_RESPONSES,
    ProblemDetail,
    raise_problem,
    raise_stale_problem,
)
from cms_planner.application.confirmation_service import ConfirmationService
from cms_planner.domain.confirmation import ConfirmationCommand, ConfirmationOutcome
from cms_planner.domain.review import StaleReviewRevisionError


def create_confirmations_router(service: ConfirmationService) -> APIRouter:
    router = APIRouter(prefix="/sessions/{session_id}", tags=["review"])

    @router.patch(
        "/deficiencies/{deficiency_id}/confirmation",
        response_model=ConfirmationOutcome,
        responses=ERROR_RESPONSES,
    )
    def confirm(
        session_id: str,
        deficiency_id: str,
        command: ConfirmationCommand,
    ) -> ConfirmationOutcome:
        if command.deficiency_id != deficiency_id:
            raise_problem(
                422,
                ProblemDetail(
                    code="deficiency-id-mismatch",
                    message="Path and body deficiency identifiers must match.",
                ),
            )
        try:
            return service.confirm(session_id, command)
        except CaseNotFoundError:
            raise_problem(
                404,
                ProblemDetail(code="case-not-found", message="Active case not found."),
            )
        except StaleReviewRevisionError as error:
            raise_stale_problem(error)

    return router
