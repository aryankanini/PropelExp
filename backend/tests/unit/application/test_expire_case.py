from datetime import timedelta
from pathlib import Path

import pytest

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from application.expire_case import ExpireCase
from application.inactivity_policy import InactivityPolicy, SessionExpiredError
from application.services.cleanup_case import CleanupCase
from application.services.stream_upload import StreamUpload
from domain.case.aggregate import CaseAggregate


class Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def test_case_expires_at_exact_deadline_with_zero_residue(tmp_path: Path) -> None:
    clock = Clock()
    policy = InactivityPolicy(timedelta(seconds=60), clock)
    repository = InMemoryCaseRepository()
    workspace = TemporaryWorkspace(tmp_path)
    repository.add(CaseAggregate(session_id="session-1", case_id="case-1"))
    StreamUpload(workspace).execute(
        session_id="session-1", client_filename="case.pdf", chunks=[b"content"]
    )
    policy.start("session-1")

    clock.now = 60
    status = ExpireCase(policy, CleanupCase(repository, workspace)).execute(
        "session-1"
    )

    assert status is not None
    assert status.outcome == "completed"
    assert status.remaining_files == 0
    assert not repository.contains("session-1")
    assert not workspace.exists("session-1")


def test_activity_at_deadline_cannot_retain_a_write() -> None:
    clock = Clock()
    policy = InactivityPolicy(timedelta(seconds=60), clock)
    policy.start("session-1")
    clock.now = 60

    with pytest.raises(SessionExpiredError):
        with policy.activity("session-1"):
            raise AssertionError("expired activity body must not run")