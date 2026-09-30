from datetime import timedelta

from application.inactivity_policy import InactivityPolicy
from application.session_status import GetSessionStatus
from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from domain.case.aggregate import CaseAggregate


class Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def test_status_is_session_only_and_does_not_extend_deadline() -> None:
    clock = Clock()
    policy = InactivityPolicy(timedelta(seconds=60), clock)
    policy.start("session-1")
    repository = InMemoryCaseRepository()
    repository.add(CaseAggregate(session_id="session-1", case_id="case-1"))
    status = GetSessionStatus(policy, repository)

    clock.now = 10
    first = status.execute("session-1")
    clock.now = 20
    reconnected = status.execute("session-1")

    assert first.storage == "session_only"
    assert first.active_case_id == "case-1"
    assert first.remaining_inactivity_seconds == 50
    assert reconnected.remaining_inactivity_seconds == 40


def test_status_reports_no_active_case_without_a_repository_record() -> None:
    status = GetSessionStatus(InactivityPolicy(), InMemoryCaseRepository())

    result = status.execute("session-1")

    assert result.active_case_id is None
    assert result.remaining_inactivity_seconds == 0