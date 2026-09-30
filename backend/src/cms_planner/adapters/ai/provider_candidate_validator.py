"""Validate provider candidates before application state mapping."""

from collections.abc import Mapping

from cms_planner.application.ports.provider_extraction import (
    ProviderCandidate,
    ProviderExtractionResponse,
)


def validate_provider_candidates(
    response: object,
) -> tuple[ProviderCandidate, ...]:
    """Return candidates only after the complete provider response is valid."""
    if isinstance(response, Mapping) and isinstance(
        response.get("candidates"),
        list,
    ):
        response = {**response, "candidates": tuple(response["candidates"])}
    return ProviderExtractionResponse.model_validate(response).candidates