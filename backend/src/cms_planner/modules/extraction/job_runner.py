"""In-process bounded extraction job runner with SSE event buffering."""

import asyncio
import logging
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from uuid import uuid4

from cms_planner.domain.job_event import JobEvent, JobTerminalStatus
from cms_planner.domain.job_failure import JobStage
from cms_planner.modules.extraction.event_sequence import EventSequence

logger = logging.getLogger(__name__)


class ExtractionJobRunner:
    """Run at most one extraction job and buffer events for SSE reconnect."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._active_job_id: str | None = None
        self._events: dict[str, list[JobEvent]] = {}
        self._waiters: dict[str, list[asyncio.Event]] = {}
        self._sequence = EventSequence()

    def create_job(self) -> str:
        job_id = uuid4().hex
        self._events[job_id] = []
        self._waiters[job_id] = []
        return job_id

    async def run(
        self,
        job_id: str,
        work: "asyncio.coroutines.Coroutine[None, None, None]",
    ) -> None:
        async with self._lock:
            if self._active_job_id is not None:
                raise RuntimeError("A job is already running")
            self._active_job_id = job_id

        self._emit(job_id, JobStage.EXTRACTION, 0)
        try:
            await work
            self._emit(job_id, JobStage.EXTRACTION, 100, terminal=JobTerminalStatus.COMPLETED)
        except Exception:
            logger.exception("Extraction job failed", extra={"job_id": job_id})
            current_stage = self._events[job_id][-1].stage
            self._emit(
                job_id,
                current_stage,
                0,
                terminal=JobTerminalStatus.FAILED,
                failure_code=f"{current_stage.value}_failed",
            )
        finally:
            async with self._lock:
                self._active_job_id = None

    def _emit(
        self,
        job_id: str,
        stage: JobStage,
        percent: int,
        terminal: JobTerminalStatus | None = None,
        failure_code: str | None = None,
    ) -> None:
        event = self._sequence.next_event(
            job_id=job_id,
            stage=stage,
            percent=percent,
            timestamp=datetime.now(UTC),
            terminal_status=terminal,
            failure_code=failure_code,
        )
        self._events.setdefault(job_id, []).append(event)
        for waiter in self._waiters.get(job_id, []):
            waiter.set()

    def emit_progress(self, job_id: str, stage: JobStage, percent: int) -> None:
        self._emit(job_id, stage, percent)

    def emit_failure(self, job_id: str, stage: JobStage) -> None:
        self._emit(job_id, stage, 0, terminal=JobTerminalStatus.FAILED)

    async def stream_events(
        self,
        job_id: str,
        last_event_id: int = 0,
    ) -> AsyncGenerator[JobEvent, None]:
        """Yield buffered and future events after the caller's last seen ID."""
        buffered = self._events.get(job_id, [])
        for event in buffered:
            if event.event_id > last_event_id:
                yield event
                if event.terminal_status is not None:
                    return

        while True:
            events = self._events.get(job_id, [])
            last_seen = events[-1] if events else None
            if last_seen and last_seen.terminal_status is not None:
                return

            waiter = asyncio.Event()
            self._waiters.setdefault(job_id, []).append(waiter)
            try:
                await asyncio.wait_for(waiter.wait(), timeout=30.0)
            except TimeoutError:
                yield self._sequence.next_event(
                    job_id=job_id,
                    stage=JobStage.EXTRACTION,
                    percent=0,
                    timestamp=datetime.now(UTC),
                )
                continue
            finally:
                waiters = self._waiters.get(job_id, [])
                if waiter in waiters:
                    waiters.remove(waiter)

            for event in self._events.get(job_id, []):
                if event.event_id > last_event_id:
                    last_event_id = event.event_id
                    yield event
                    if event.terminal_status is not None:
                        return


_runner = ExtractionJobRunner()


def get_job_runner() -> ExtractionJobRunner:
    return _runner
