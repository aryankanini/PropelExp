import pytest
from pydantic import ValidationError

from domain.case.aggregate import CaseAggregate


def test_aggregate_records_every_case_state_category_immutably() -> None:
    original = CaseAggregate(session_id="session-1", case_id="case-1")

    updated = original
    for category in (
        "documents",
        "jobs",
        "providers",
        "deficiencies",
        "poc_drafts",
        "approvals",
        "provenance",
    ):
        updated = updated.append_state(category, f"{category}-1")

    assert original.documents == ()
    assert updated.documents == ("documents-1",)
    assert updated.jobs == ("jobs-1",)
    assert updated.providers == ("providers-1",)
    assert updated.deficiencies == ("deficiencies-1",)
    assert updated.poc_drafts == ("poc_drafts-1",)
    assert updated.approvals == ("approvals-1",)
    assert updated.provenance == ("provenance-1",)


def test_aggregate_rejects_empty_identity() -> None:
    with pytest.raises(ValidationError):
        CaseAggregate(session_id="", case_id="case-1")