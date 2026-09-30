from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from cms_planner.domain.job_event import JobEvent, JobTerminalStatus
from cms_planner.domain.job_failure import JobStage
from cms_planner.modules.extraction.event_sequence import EventSequence


NOW = datetime(2026, 9, 24, 12, 0, tzinfo=UTC)


def event(**changes: object) -> JobEvent:
    values: dict[str, object] = {
        "job_id": "job-1",
        "event_id": 1,
        "stage": JobStage.EXTRACTION,
        "percent": 25,
        "timestamp": NOW,
        "terminal_status": None,
    }
    values.update(changes)
    return JobEvent.model_validate(values)


def test_event_is_strict_frozen_and_contains_no_document_text() -> None:
    progress = event()

    assert progress.model_dump() == {
        "job_id": "job-1",
        "event_id": 1,
        "stage": JobStage.EXTRACTION,
        "percent": 25,
        "timestamp": NOW,
        "terminal_status": None,
    }
    assert "document_text" not in JobEvent.model_fields

    with pytest.raises(ValidationError):
        event(document_text="must not cross the event boundary")
    with pytest.raises(ValidationError):
        progress.percent = 30


@pytest.mark.parametrize("percent", [-1, 101])
def test_event_rejects_percent_outside_closed_range(percent: int) -> None:
    with pytest.raises(ValidationError):
        event(percent=percent)


def test_event_requires_positive_id_and_timezone_aware_timestamp() -> None:
    with pytest.raises(ValidationError):
        event(event_id=0)
    with pytest.raises(ValidationError):
        event(timestamp=datetime(2026, 9, 24, 12, 0))


@pytest.mark.parametrize(
    "terminal_status",
    [JobTerminalStatus.COMPLETED, JobTerminalStatus.FAILED],
)
def test_event_accepts_terminal_status(terminal_status: JobTerminalStatus) -> None:
    assert event(terminal_status=terminal_status).terminal_status is terminal_status


def test_sequence_allocates_increasing_ids_independently_per_job() -> None:
    sequence = EventSequence()

    first = sequence.next_event(
        job_id="job-1",
        stage=JobStage.EXTRACTION,
        percent=10,
        timestamp=NOW,
    )
    other_job = sequence.next_event(
        job_id="job-2",
        stage=JobStage.OCR,
        percent=20,
        timestamp=NOW,
    )
    second = sequence.next_event(
        job_id="job-1",
        stage=JobStage.EXTRACTION,
        percent=100,
        timestamp=NOW,
        terminal_status=JobTerminalStatus.COMPLETED,
    )

    assert (first.event_id, second.event_id) == (1, 2)
    assert other_job.event_id == 1