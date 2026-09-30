import pytest
from pydantic import ValidationError

from application.services.cleanup_errors import CleanupStore
from domain.lifecycle.cleanup_status import CleanupStatus


def test_completed_status_is_content_free_and_reports_zero_files() -> None:
    status = CleanupStatus(outcome="completed", remaining_files=0)

    assert status.model_dump(mode="json") == {
        "outcome": "completed",
        "remaining_files": 0,
        "failed_stores": [],
    }


def test_failed_status_contains_only_safe_store_diagnostics() -> None:
    status = CleanupStatus(
        outcome="failed",
        remaining_files=1,
        failed_stores=(CleanupStore.WORKSPACE,),
    )

    serialized = status.model_dump_json()
    assert "workspace" in serialized
    assert "document" not in serialized
    assert "content" not in serialized


def test_completed_status_rejects_nonzero_residue() -> None:
    with pytest.raises(ValidationError):
        CleanupStatus(outcome="completed", remaining_files=1)