from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime

from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from cms_planner.application.approve_revision import ApproveRevision
from cms_planner.domain.approval import (
    ApprovalBlockerCode,
)
from cms_planner.domain.poc import (
    POC_SECTION_ORDER,
    MissingInformationMarker,
    PocContent,
    PocDraft,
    PocRevision,
    PocSectionName,
    SectionOrigin,
)
from domain.case.aggregate import CaseAggregate


NOW = datetime(2026, 9, 24, tzinfo=UTC)


def complete_draft(revision_id: str = "revision-4") -> PocDraft:
    revision = PocRevision(
        revision_id=revision_id,
        deficiency_revision_id="deficiency-revision-1",
        content=PocContent(
            affected_residents="Affected residents",
            others_at_risk="Other residents at risk",
            corrective_measures="Corrective measures",
            monitoring="Monitoring",
            completion_date="2026-10-01",
        ),
        section_origins={name: SectionOrigin.USER_EDITED for name in POC_SECTION_ORDER},
    )
    return PocDraft(
        deficiency_id="F689",
        revisions=(revision,),
        current_revision_id=revision_id,
    )


def test_complete_current_revision_is_approved() -> None:
    repository = InMemoryCaseRepository()
    repository.add(
        CaseAggregate(
            session_id="session-1",
            case_id="case-1",
            poc_draft=complete_draft(),
            approval_evidence=("page-3: fall prevention policy",),
        )
    )

    decision = ApproveRevision(repository, clock=lambda: NOW).execute(
        session_id="session-1",
        reviewed_revision_id="revision-4",
        actor_id="leader-1",
        actor_role="compliance_leader",
    )

    assert decision.approved is True
    assert decision.approval.revision_id == "revision-4"
    assert decision.approval.export_enabled is True


def test_incomplete_revision_returns_exact_blockers_without_mutation() -> None:
    repository = InMemoryCaseRepository()
    original = CaseAggregate(
        session_id="session-1",
        case_id="case-1",
        poc_draft=complete_draft().model_copy(
            update={
                "revisions": (
                    complete_draft().current_revision.model_copy(
                        update={
                            "missing_information": (
                                MissingInformationMarker(
                                    marker_id="missing-1",
                                    section=PocSectionName.MONITORING,
                                    required_fact="monitoring frequency",
                                ),
                            )
                        }
                    ),
                )
            }
        ),
    )
    repository.add(original)

    decision = ApproveRevision(repository, clock=lambda: NOW).execute(
        session_id="session-1",
        reviewed_revision_id="revision-4",
        actor_id="leader-1",
        actor_role="compliance_leader",
    )

    assert [blocker.code for blocker in decision.blockers] == [
        ApprovalBlockerCode.MISSING_EVIDENCE,
        ApprovalBlockerCode.INCOMPLETE_REVISION,
    ]
    assert repository.get("session-1") == original


def test_stale_revision_is_denied_without_mutation() -> None:
    repository = InMemoryCaseRepository()
    original = CaseAggregate(
        session_id="session-1",
        case_id="case-1",
        poc_draft=complete_draft(),
        approval_evidence=("page-3: fall prevention policy",),
    )
    repository.add(original)

    decision = ApproveRevision(repository, clock=lambda: NOW).execute(
        session_id="session-1",
        reviewed_revision_id="revision-3",
        actor_id="leader-1",
        actor_role="compliance_leader",
    )

    assert [blocker.code for blocker in decision.blockers] == [
        ApprovalBlockerCode.STALE_REVISION
    ]
    assert repository.get("session-1") == original


def test_concurrent_approval_retains_one_current_state() -> None:
    repository = InMemoryCaseRepository()
    repository.add(
        CaseAggregate(
            session_id="session-1",
            case_id="case-1",
            poc_draft=complete_draft(),
            approval_evidence=("page-3: fall prevention policy",),
        )
    )
    command = ApproveRevision(repository, clock=lambda: NOW)

    def approve(actor_id: str):
        return command.execute(
            session_id="session-1",
            reviewed_revision_id="revision-4",
            actor_id=actor_id,
            actor_role="compliance_leader",
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        decisions = list(executor.map(approve, ("leader-1", "leader-2")))

    retained = repository.get("session-1")
    assert retained is not None
    assert all(decision.approval == retained.approval for decision in decisions)
    assert retained.approval.revision_id == "revision-4"