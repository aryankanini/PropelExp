"""Application-owned provider boundary for structured POC generation."""

from typing import Protocol

from cms_planner.domain.poc_generation import PocGenerationInput


class PocProvider(Protocol):
    """Generate provider-neutral structured output from one deficiency revision."""

    def generate(self, request: PocGenerationInput) -> object: ...