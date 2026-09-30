import pytest

from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from domain.case.aggregate import CaseAggregate
from domain.case.errors import ActiveCaseExistsError


def test_second_active_case_is_rejected_without_replacement() -> None:
    repository = InMemoryCaseRepository()
    current = CaseAggregate(session_id="session-1", case_id="case-1")
    repository.add(current)

    with pytest.raises(ActiveCaseExistsError):
        repository.add(CaseAggregate(session_id="session-1", case_id="case-2"))

    assert repository.get("session-1") == current


def test_active_cases_are_isolated_by_session() -> None:
    repository = InMemoryCaseRepository()
    first = CaseAggregate(session_id="session-1", case_id="case-1")
    second = CaseAggregate(session_id="session-2", case_id="case-2")

    repository.add(first)
    repository.add(second)

    assert repository.get("session-1") == first
    assert repository.get("session-2") == second