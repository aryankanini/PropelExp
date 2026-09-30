"""Stable HTTP problem responses for review operations."""

from typing import NoReturn

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.review import StaleReviewRevisionError


class ProblemDetail(BaseModel):
    """Machine-readable error details safe to return to clients."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    current_revision_id: str | None = None
    reload_required: bool = False


class ProblemResponse(BaseModel):
    """Match FastAPI's HTTPException response envelope."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    detail: ProblemDetail


ERROR_RESPONSES = {
    404: {"model": ProblemResponse, "description": "Review resource not found"},
    409: {"model": ProblemResponse, "description": "Displayed revision is stale"},
    503: {"model": ProblemResponse, "description": "Evidence is unavailable"},
}


def raise_problem(status_code: int, problem: ProblemDetail) -> NoReturn:
    raise HTTPException(
        status_code=status_code,
        detail=problem.model_dump(mode="json"),
    )


def raise_stale_problem(error: StaleReviewRevisionError) -> NoReturn:
    raise_problem(
        409,
        ProblemDetail(
            code="stale-review-revision",
            message="Reload the current values before retrying.",
            current_revision_id=error.current_revision_id,
            reload_required=True,
        ),
    )
