import json
import logging

from cms_planner.infrastructure.observability.correlation import correlation_context
from cms_planner.infrastructure.observability.logging import SafeJsonFormatter


def test_formatter_emits_allow_list_and_correlation() -> None:
    record = logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname=__file__,
        lineno=1,
        msg="document text and credential must never be emitted",
        args=(),
        exc_info=None,
    )
    record.actor_id = "actor-1"
    record.route = "/recovery/retry"
    record.duration_ms = 12
    record.result_code = "provider_unavailable"
    record.provider = "approved-provider"
    record.provider_payload = {"secret": "value"}

    with correlation_context("corr-123"):
        payload = json.loads(SafeJsonFormatter().format(record))

    assert payload["correlation_id"] == "corr-123"
    assert payload["actor_id"] == "actor-1"
    assert payload["result_code"] == "provider_unavailable"
    assert "message" not in payload
    assert "provider_payload" not in payload
    assert "document text" not in str(payload)
    assert "credential" not in str(payload)


def test_log_like_value_is_redacted_without_changing_structure() -> None:
    record = logging.LogRecord(
        name="test",
        level=logging.WARNING,
        pathname=__file__,
        lineno=1,
        msg="ignored",
        args=(),
        exc_info=None,
    )
    record.stage = 'ocr\n{"level":"CRITICAL"}'

    payload = json.loads(SafeJsonFormatter().format(record))

    assert payload["stage"] == "[REDACTED]"
    assert payload["level"] == "WARNING"