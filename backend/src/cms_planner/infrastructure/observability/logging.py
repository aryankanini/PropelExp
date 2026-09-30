"""Allow-listed structured diagnostics with no content-bearing fields."""

from datetime import UTC, datetime
import json
import logging
from typing import Final

from cms_planner.infrastructure.observability.correlation import current_correlation_id

_OPTIONAL_FIELDS: Final = (
    "actor_id",
    "route",
    "stage",
    "duration_ms",
    "result_code",
    "provider",
)
_REDACTED: Final = "[REDACTED]"


class SafeJsonFormatter(logging.Formatter):
    """Serialize only the diagnostic schema approved for persisted logs."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "correlation_id": current_correlation_id(),
        }
        for field_name in _OPTIONAL_FIELDS:
            value = getattr(record, field_name, None)
            if value is not None:
                payload[field_name] = _safe_scalar(value)
        return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def configure_structured_logging(logger: logging.Logger) -> None:
    """Replace logger handlers with one safe structured stream handler."""

    handler = logging.StreamHandler()
    handler.setFormatter(SafeJsonFormatter())
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def _safe_scalar(value: object) -> str | int | float | bool:
    if isinstance(value, bool | int | float):
        return value
    text = str(value)
    if any(character in text for character in ("\r", "\n", "{", "}")):
        return _REDACTED
    return text[:128]