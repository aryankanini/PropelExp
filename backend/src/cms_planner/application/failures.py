"""Typed application failures that may cross process boundaries safely."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FieldFailure:
    """Identify one invalid field using public, non-sensitive text."""

    field: str
    message: str


class ApplicationFailure(Exception):
    """Base class for failures with a stable public mapping."""


class ValidationFailure(ApplicationFailure):
    """Report one or more invalid public input fields."""

    def __init__(self, field_errors: tuple[FieldFailure, ...] = ()) -> None:
        super().__init__()
        self.field_errors = field_errors


class AuthorizationFailure(ApplicationFailure):
    """Report that the actor cannot perform the requested operation."""


class ProviderFailure(ApplicationFailure):
    """Retain provider diagnostics internally while exposing a safe category."""

    def __init__(self, *, provider_payload: object | None = None) -> None:
        super().__init__()
        self.provider_payload = provider_payload


class CancellationFailure(ApplicationFailure):
    """Report that processing was cancelled before completion."""


class InternalFailure(ApplicationFailure):
    """Report an internal failure whose original detail must remain private."""


class ResourceNotFoundFailure(ApplicationFailure):
    """Report that a requested transient resource is unavailable."""


class GenerationDeniedFailure(ApplicationFailure):
    """Report that generation is blocked by the current deficiency state."""


class StaleStateFailure(ApplicationFailure):
    """Report an optimistic concurrency conflict requiring a reload."""


class RetentionFailure(ApplicationFailure):
    """Report that valid transient state could not be retained."""
