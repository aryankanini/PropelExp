"""Immutable request and job correlation context."""

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
import re
from uuid import uuid4

_CORRELATION_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


@dataclass(frozen=True, slots=True)
class CorrelationContext:
    correlation_id: str


_CURRENT_CONTEXT: ContextVar[CorrelationContext | None] = ContextVar(
    "correlation_context", default=None
)


def resolve_correlation_id(candidate: str | None) -> str:
    """Accept a bounded safe identifier or generate a new opaque value."""

    if candidate is not None and _CORRELATION_PATTERN.fullmatch(candidate):
        return candidate
    return str(uuid4())


@contextmanager
def correlation_context(correlation_id: str) -> Iterator[CorrelationContext]:
    """Bind one immutable correlation value for a request or job scope."""

    context = CorrelationContext(correlation_id=correlation_id)
    token = _CURRENT_CONTEXT.set(context)
    try:
        yield context
    finally:
        _CURRENT_CONTEXT.reset(token)


def current_correlation_id() -> str | None:
    context = _CURRENT_CONTEXT.get()
    return None if context is None else context.correlation_id