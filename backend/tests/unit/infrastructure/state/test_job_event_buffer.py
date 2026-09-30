from datetime import UTC, datetime

import pytest

from cms_planner.domain.job_event import JobEvent, JobTerminalStatus
from cms_planner.domain.job_failure import JobStage
from cms_planner.infrastructure.state.job_event_buffer import (
    EventCursorNotFoundError,
    EventOrderError,
    EventStreamClosedError,
    JobEventBuffer,
    StaleEventCursorError,
)
from cms_planner.modules.extraction.active_job_guard import (
    ActiveExtractionError,
    ActiveJobGuard,
)


NOW = datetime(2026, 9, 24, 12, 0, tzinfo=UTC)


def event(
    event_id: int,
    *,
    job_id: str = "job-1",
    terminal_status: JobTerminalStatus | None = None,
) -> JobEvent:
    return JobEvent(
        job_id=job_id,
        event_id=event_id,
        stage=JobStage.EXTRACTION,
        percent=100 if terminal_status else event_id * 10,
        timestamp=NOW,
        terminal_status=terminal_status,
    )


def test_buffer_requires_explicit_positive_capacity() -> None:
    with pytest.raises(TypeError):
        JobEventBuffer()  # type: ignore[call-arg]
    with pytest.raises(ValueError, match="capacity"):
        JobEventBuffer(capacity=0)


def test_append_preserves_order_and_resume_is_strictly_after_cursor() -> None:
    buffer = JobEventBuffer(capacity=3)
    for event_id in range(1, 4):
        buffer.append(event(event_id))

    assert [item.event_id for item in buffer.events_after("job-1", 1)] == [2, 3]
    assert buffer.events_after("job-1", 3) == ()


def test_buffer_is_bounded_per_job() -> None:
    buffer = JobEventBuffer(capacity=2)
    buffer.append(event(1, job_id="job-1"))
    buffer.append(event(1, job_id="job-2"))
    buffer.append(event(2, job_id="job-1"))
    buffer.append(event(3, job_id="job-1"))

    assert [item.event_id for item in buffer.events_after("job-1")] == [2, 3]
    assert [item.event_id for item in buffer.events_after("job-2")] == [1]


def test_stale_cursor_raises_typed_error_instead_of_partial_replay() -> None:
    buffer = JobEventBuffer(capacity=2)
    for event_id in range(1, 4):
        buffer.append(event(event_id))

    with pytest.raises(StaleEventCursorError) as raised:
        buffer.events_after("job-1", 1)

    assert raised.value.job_id == "job-1"
    assert raised.value.event_id == 1
    assert raised.value.oldest_retained_event_id == 2


def test_unknown_cursor_and_out_of_order_append_are_rejected() -> None:
    buffer = JobEventBuffer(capacity=3)
    buffer.append(event(1))

    with pytest.raises(EventCursorNotFoundError):
        buffer.events_after("job-1", 2)
    with pytest.raises(EventOrderError):
        buffer.append(event(3))


def test_terminal_event_is_retained_and_closes_job_stream() -> None:
    buffer = JobEventBuffer(capacity=2)
    buffer.append(event(1))
    terminal = event(2, terminal_status=JobTerminalStatus.COMPLETED)
    buffer.append(terminal)

    assert buffer.terminal_event("job-1") == terminal
    with pytest.raises(EventStreamClosedError):
        buffer.append(event(3))


def test_second_active_job_is_rejected_without_disrupting_original_stream() -> None:
    guard = ActiveJobGuard()
    buffer = JobEventBuffer(capacity=2)
    guard.start("job-1")
    buffer.append(event(1))

    with pytest.raises(ActiveExtractionError) as raised:
        guard.start("job-2")

    assert raised.value.active_job_id == "job-1"
    assert guard.active_job_id == "job-1"
    assert buffer.events_after("job-1") == (event(1),)


def test_new_job_can_start_after_terminal_completion() -> None:
    guard = ActiveJobGuard()
    guard.start("job-1")
    guard.finish("job-1", JobTerminalStatus.COMPLETED)

    guard.start("job-2")

    assert guard.active_job_id == "job-2"