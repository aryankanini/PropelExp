"""Typed, content-free outcomes for bounded provider execution."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class ExhaustedProviderRetries:
    """Report that all permitted transient attempts failed."""

    code: Literal["provider_retries_exhausted"] = "provider_retries_exhausted"
    attempts: int = 3


@dataclass(frozen=True, slots=True)
class InvalidProviderResponse:
    """Report a terminal schema failure without retaining partial content."""

    code: Literal["invalid_provider_response"] = "invalid_provider_response"