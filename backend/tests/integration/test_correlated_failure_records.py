import json
import logging

from cms_planner.api.problems import map_failure, problem_payload
from cms_planner.application.failures import ProviderFailure
from cms_planner.application.job_transitions import JobState
from cms_planner.infrastructure.observability.correlation import correlation_context
from cms_planner.infrastructure.observability.logging import SafeJsonFormatter


def test_api_event_job_and_log_share_correlation_id() -> None:
    correlation_id = "corr-shared-1"
    problem = map_failure(ProviderFailure(), correlation_id)
    event = problem_payload(problem)
    job = JobState(correlation_id=correlation_id)
    record = logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname=__file__,
        lineno=1,
        msg="ignored",
        args=(),
        exc_info=None,
    )

    with correlation_context(correlation_id):
        log = json.loads(SafeJsonFormatter().format(record))

    assert event["correlation_id"] == correlation_id
    assert job.correlation_id == correlation_id
    assert log["correlation_id"] == correlation_id