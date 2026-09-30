"""Authoritative query for transient session retention status."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from application.inactivity_policy import InactivityPolicy
from application.ports.case_repository import CaseRepository


class SessionStatus(BaseModel):
    """Expose session-only semantics and remaining inactivity time."""

    model_config = ConfigDict(frozen=True, strict=True)

    storage: Literal["session_only"] = "session_only"
    remaining_inactivity_seconds: int = Field(ge=0)
    active_case_id: str | None = None


class GetSessionStatus:
    """Read retention state without extending the inactivity deadline."""

    def __init__(self, policy: InactivityPolicy, repository: CaseRepository) -> None:
        self._policy = policy
        self._repository = repository

    def execute(self, session_id: str) -> SessionStatus:
        aggregate = self._repository.get(session_id)
        if aggregate is None:
            return SessionStatus(remaining_inactivity_seconds=0, active_case_id=None)

        try:
            remaining_seconds = self._policy.remaining_seconds(session_id)
        except KeyError:
            remaining_seconds = 0

        return SessionStatus(
            remaining_inactivity_seconds=remaining_seconds,
            active_case_id=aggregate.case_id,
        )