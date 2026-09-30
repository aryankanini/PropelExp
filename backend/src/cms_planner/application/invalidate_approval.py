"""Application commands for reapproval workflow transitions."""

from application.ports.case_repository import CaseRepository
from cms_planner.domain.poc import PocSectionName
from cms_planner.domain.reapproval import ReapprovalDecision
from domain.case.aggregate import CaseAggregate


class RequestChanges:
    """Return a reviewed POC to editing without export authority."""

    def __init__(self, repository: CaseRepository) -> None:
        self._repository = repository

    def execute(self, *, session_id: str) -> ReapprovalDecision:
        def request(aggregate: CaseAggregate) -> tuple[CaseAggregate, ReapprovalDecision]:
            return aggregate.request_poc_changes()

        return self._repository.update(session_id, request)


class SavePocEdit:
    """Save a revision and invalidate approval as one atomic update."""

    def __init__(self, repository: CaseRepository) -> None:
        self._repository = repository

    def execute(
        self,
        *,
        session_id: str,
        expected_revision_id: str,
        revision_id: str,
        section_updates: dict[PocSectionName, str | None],
    ) -> ReapprovalDecision:
        def save(aggregate: CaseAggregate) -> tuple[CaseAggregate, ReapprovalDecision]:
            return aggregate.save_poc_edit(
                expected_revision_id=expected_revision_id,
                revision_id=revision_id,
                section_updates=section_updates,
            )

        return self._repository.update(session_id, save)