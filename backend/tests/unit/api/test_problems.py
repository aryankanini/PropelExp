from pydantic import ValidationError
import pytest

from cms_planner.api.problems import ProblemDetails, map_failure
from cms_planner.application.failures import (
    AuthorizationFailure,
    CancellationFailure,
    FieldFailure,
    InternalFailure,
    ProviderFailure,
    ValidationFailure,
)


@pytest.mark.parametrize(
    ("failure", "expected_code", "expected_status", "expected_retryable"),
    (
        (ValidationFailure(), "validation_failed", 422, False),
        (AuthorizationFailure(), "authorization_failed", 403, False),
        (ProviderFailure(provider_payload={"secret": "value"}), "provider_unavailable", 503, True),
        (CancellationFailure(), "operation_cancelled", 409, False),
        (InternalFailure("traceback: credential=value"), "internal_error", 500, False),
    ),
)
def test_typed_failure_maps_to_stable_problem(
    failure: Exception,
    expected_code: str,
    expected_status: int,
    expected_retryable: bool,
) -> None:
    problem = map_failure(failure, "corr-123")

    assert problem.code == expected_code
    assert problem.status == expected_status
    assert problem.retryable is expected_retryable
    assert problem.correlation_id == "corr-123"


def test_validation_failure_maps_safe_field_errors() -> None:
    failure = ValidationFailure(
        (FieldFailure(field="request.provider_name", message="Invalid value."),)
    )

    problem = map_failure(failure, "corr-123")

    assert problem.field_errors[0].model_dump() == {
        "field": "request.provider_name",
        "message": "Invalid value.",
    }


def test_unknown_failure_retains_correlation_without_sensitive_detail() -> None:
    problem = map_failure(
        RuntimeError("provider payload: document text and credential"),
        "corr-unknown",
    )

    serialized = problem.model_dump_json()
    assert problem.code == "internal_error"
    assert problem.correlation_id == "corr-unknown"
    assert "provider payload" not in serialized
    assert "document text" not in serialized
    assert "credential" not in serialized


def test_problem_contract_rejects_unknown_serialized_fields() -> None:
    with pytest.raises(ValidationError):
        ProblemDetails(
            code="internal_error",
            message="Processing could not be completed.",
            correlation_id="corr-123",
            retryable=False,
            field_errors=(),
            provider_payload="secret",
        )