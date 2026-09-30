"""Inactivity-triggered orchestration for verified case cleanup."""

from application.inactivity_policy import InactivityPolicy
from application.services.cleanup_case import CleanupCase
from domain.lifecycle.cleanup_status import CleanupStatus


class ExpireCase:
    """Run shared cleanup only when the server-owned deadline is due."""

    def __init__(self, policy: InactivityPolicy, cleanup: CleanupCase) -> None:
        self._policy = policy
        self._cleanup = cleanup

    def execute(self, session_id: str) -> CleanupStatus | None:
        return self._policy.expire_if_due(
            session_id,
            lambda: self._cleanup.execute(session_id),
        )