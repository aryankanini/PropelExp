"""Allocate monotonically increasing progress events within each job."""

from collections import defaultdict
from datetime import datetime

from cms_planner.domain.job_event import JobEvent, JobTerminalStatus
from cms_planner.domain.job_failure import JobStage


class EventSequence:
    def __init__(self) -> None:
        self._last_event_ids: dict[str, int] = defaultdict(int)

    def next_event(
        self,
        *,
        job_id: str,
        stage: JobStage,
        percent: int,
        timestamp: datetime,
        terminal_status: JobTerminalStatus | None = None,
        failure_code: str | None = None,
    ) -> JobEvent:
        event_id = self._last_event_ids[job_id] + 1
        event = JobEvent(
            job_id=job_id,
            event_id=event_id,
            stage=stage,
            percent=percent,
            timestamp=timestamp,
            terminal_status=terminal_status,
            failure_code=failure_code,
        )
        self._last_event_ids[job_id] = event_id
        return event