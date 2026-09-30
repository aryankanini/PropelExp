"""Application command for current-revision approval."""

from collections.abc import Callable
from datetime import UTC, datetime

from application.ports.case_repository import CaseRepository
from cms_planner.domain.approval import ApprovalDecision
from domain.case.aggregate import CaseAggregate


class ApproveRevision:
    """Atomically validate and approve one case's current POC revision."""

    def __init__(
        self,
        repository: CaseRepository,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._repository = repository
        self._clock = clock or (lambda: datetime.now(UTC))

    def execute(
        self,
        *,
        session_id: str,
        reviewed_revision_id: str,
        actor_id: str,
        actor_role: str,
    ) -> ApprovalDecision:
        def approve(aggregate: CaseAggregate) -> tuple[CaseAggregate, ApprovalDecision]:
            return aggregate.approve_poc(
                reviewed_revision_id=reviewed_revision_id,
                actor_id=actor_id,
                actor_role=actor_role,
                approved_at=self._clock(),
            )

        return self._repository.update(session_id, approve)