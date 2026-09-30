"""Stable, allow-listed problem details for API responses and job events."""

from dataclasses import dataclass
from typing import Final, Literal
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from cms_planner.application.failures import (
    ApplicationFailure,
    AuthorizationFailure,
    CancellationFailure,
    FieldFailure,
    GenerationDeniedFailure,
    InternalFailure,
    ProviderFailure,
    ResourceNotFoundFailure,
    RetentionFailure,
    StaleStateFailure,
    ValidationFailure,
)

PROBLEM_MEDIA_TYPE: Final = "application/problem+json"


class ProblemFieldError(BaseModel):
    """Public validation detail for one request field."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    field: str
    message: str


class ProblemDetails(BaseModel):
    """Closed public error contract shared by HTTP and job events."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    code: str
    message: str
    correlation_id: str
    retryable: bool
    action: Literal["none", "retry", "reload"] = "none"
    field_errors: tuple[ProblemFieldError, ...] = ()
    status: int


@dataclass(frozen=True, slots=True)
class _ProblemDefinition:
    code: str
    message: str
    status: int
    retryable: bool
    action: Literal["none", "retry", "reload"] = "none"


_FAILURE_DEFINITIONS: Final = {
    ValidationFailure: _ProblemDefinition(
        "validation_failed", "Check the highlighted fields and try again.", 422, False
    ),
    AuthorizationFailure: _ProblemDefinition(
        "authorization_failed", "You cannot perform this action.", 403, False
    ),
    ProviderFailure: _ProblemDefinition(
        "provider_unavailable", "Processing is temporarily unavailable.", 503, True
    ),
    CancellationFailure: _ProblemDefinition(
        "operation_cancelled", "Processing was cancelled.", 409, False
    ),
    InternalFailure: _ProblemDefinition(
        "internal_error", "Processing could not be completed.", 500, False
    ),
    ResourceNotFoundFailure: _ProblemDefinition(
        "resource_not_found", "The requested item is no longer available.", 404, False
    ),
    GenerationDeniedFailure: _ProblemDefinition(
        "deficiency_not_confirmed",
        "Confirm the current deficiency revision before generating a draft.",
        409,
        False,
    ),
    StaleStateFailure: _ProblemDefinition(
        "stale_revision",
        "The draft changed before this edit could be saved.",
        409,
        False,
        "reload",
    ),
    RetentionFailure: _ProblemDefinition(
        "retention_failed",
        "The draft could not be saved. Retry without changing the current revision.",
        503,
        True,
        "retry",
    ),
}
_UNKNOWN_DEFINITION: Final = _FAILURE_DEFINITIONS[InternalFailure]


def map_failure(error: Exception, correlation_id: str) -> ProblemDetails:
    """Map an internal exception without serializing its message or attributes."""

    definition = _FAILURE_DEFINITIONS.get(type(error), _UNKNOWN_DEFINITION)
    field_errors = _map_field_errors(error)
    return ProblemDetails(
        code=definition.code,
        message=definition.message,
        correlation_id=correlation_id,
        retryable=definition.retryable,
        action=definition.action,
        field_errors=field_errors,
        status=definition.status,
    )


def problem_payload(problem: ProblemDetails) -> dict[str, object]:
    """Serialize the shared allow-listed API and job-event payload."""

    return problem.model_dump(mode="json")


def register_exception_handlers(app: FastAPI) -> None:
    """Register centralized handlers for request and application failures."""

    app.add_exception_handler(RequestValidationError, _request_validation_handler)
    app.add_exception_handler(ApplicationFailure, _application_failure_handler)
    app.add_exception_handler(Exception, _unknown_failure_handler)


async def _request_validation_handler(
    request: Request, error: RequestValidationError
) -> JSONResponse:
    fields = tuple(
        FieldFailure(
            field=".".join(str(part) for part in item["loc"]),
            message="Invalid value.",
        )
        for item in error.errors()
    )
    return _response(map_failure(ValidationFailure(fields), _correlation_id(request)))


async def _application_failure_handler(
    request: Request, error: ApplicationFailure
) -> JSONResponse:
    return _response(map_failure(error, _correlation_id(request)))


async def _unknown_failure_handler(
    request: Request, error: Exception
) -> JSONResponse:
    return _response(map_failure(error, _correlation_id(request)))


def _map_field_errors(error: Exception) -> tuple[ProblemFieldError, ...]:
    if not isinstance(error, ValidationFailure):
        return ()
    return tuple(
        ProblemFieldError(field=item.field, message=item.message)
        for item in error.field_errors
    )


def _correlation_id(request: Request) -> str:
    return getattr(request.state, "correlation_id", str(uuid4()))


def _response(problem: ProblemDetails) -> JSONResponse:
    return JSONResponse(
        status_code=problem.status,
        content=problem_payload(problem),
        media_type=PROBLEM_MEDIA_TYPE,
    )