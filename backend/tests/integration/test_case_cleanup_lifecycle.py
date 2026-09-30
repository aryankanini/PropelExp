from datetime import timedelta
from pathlib import Path
from threading import Barrier, Thread

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


def test_exact_deadline_activity_cannot_race_with_retained_write(tmp_path: Path) -> None:
    clock = Clock()
    policy = InactivityPolicy(timedelta(seconds=60), clock)
    repository = InMemoryCaseRepository()
    workspace = TemporaryWorkspace(tmp_path)
    repository.add(CaseAggregate(session_id="session-1", case_id="case-1"))
    StreamUpload(workspace).execute(
        session_id="session-1", client_filename="case.pdf", chunks=[b"content"]
    )
    cleanup = ExpireCase(policy, CleanupCase(repository, workspace))
    policy.start("session-1")
    clock.now = 60
    barrier = Barrier(3)
    activity_body_ran = []

    def attempt_activity() -> None:
        barrier.wait()
        try:
            with policy.activity("session-1"):
                activity_body_ran.append(True)
        except SessionExpiredError:
            pass

    def expire() -> None:
        barrier.wait()
        cleanup.execute("session-1")

    activity_thread = Thread(target=attempt_activity)
    cleanup_thread = Thread(target=expire)
    activity_thread.start()
    cleanup_thread.start()
    barrier.wait()
    activity_thread.join()
    cleanup_thread.join()

    assert activity_body_ran == []
    assert not repository.contains("session-1")
    assert workspace.count_files("session-1") == 0