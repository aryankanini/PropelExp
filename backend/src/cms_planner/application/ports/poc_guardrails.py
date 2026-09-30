"""Application-owned boundary for deterministic generated-output guardrails."""

from typing import Protocol

from cms_planner.domain.deficiency import DeficiencyRevision
from cms_planner.domain.poc_generation import GuardedPocResult


class PocGuardrails(Protocol):
    """Validate and ground provider output against one deficiency revision."""

    def apply(
        self,
        payload: object,
        deficiency_revision: DeficiencyRevision,
    ) -> GuardedPocResult: ...