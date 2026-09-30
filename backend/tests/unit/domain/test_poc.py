import pytest
from pydantic import ValidationError

from cms_planner.domain.poc import (
    MissingInformationMarker,
    POC_SECTION_ORDER,
    PocContent,
    PocDraft,
    PocRevision,
    PocSectionName,
    SectionOrigin,
)
from domain.case.revision_errors import StaleRevisionError


def content(**changes: str) -> PocContent:
    values = {
        "affected_residents": "Assess every affected resident.",
        "others_at_risk": "Identify residents with the same risk.",
        "corrective_measures": "Complete corrective training.",
        "monitoring": "Audit compliance weekly.",
        "completion_date": "2026-10-15",
    }
    values.update(changes)
    return PocContent(**values)


def revision(revision_id: str, poc_content: PocContent | None = None) -> PocRevision:
    return PocRevision(
        revision_id=revision_id,
        deficiency_revision_id="def-rev-1",
        content=poc_content or content(),
        section_origins={section: SectionOrigin.AI_GENERATED for section in POC_SECTION_ORDER},
    )


def test_poc_content_rejects_empty_and_unknown_sections() -> None:
    with pytest.raises(ValidationError):
        content(monitoring="   ")

    with pytest.raises(ValidationError):
        PocContent(
            **content().model_dump(),
            unknown_section="not allowed",
        )


def test_draft_appends_an_unapproved_revision_immutably() -> None:
    initial = revision("poc-rev-1")
    draft = PocDraft(
        deficiency_id="deficiency-1",
        revisions=(initial,),
        current_revision_id=initial.revision_id,
    )
    edited = revision("poc-rev-2", content(monitoring="Audit compliance daily."))

    updated = draft.append_revision(
        expected_revision_id="poc-rev-1",
        revision=edited,
    )

    assert draft.current_revision_id == "poc-rev-1"
    assert updated.current_revision_id == "poc-rev-2"
    assert updated.current_revision.status == "unapproved"
    assert len(updated.revisions) == 2


def test_draft_rejects_a_stale_edit() -> None:
    initial = revision("poc-rev-1")
    draft = PocDraft(
        deficiency_id="deficiency-1",
        revisions=(initial,),
        current_revision_id=initial.revision_id,
    )

    with pytest.raises(StaleRevisionError):
        draft.append_revision(
            expected_revision_id="stale-revision",
            revision=revision("poc-rev-2"),
        )


def test_edit_replaces_and_removal_restores_a_missing_information_marker() -> None:
    marker = MissingInformationMarker(
        marker_id="marker-1",
        section=PocSectionName.MONITORING,
        required_fact="the monitoring frequency",
    )
    initial = revision("poc-rev-1").model_copy(
        update={"missing_information": (marker,)}
    )
    draft = PocDraft(
        deficiency_id="deficiency-1",
        revisions=(initial,),
        current_revision_id=initial.revision_id,
    )

    resolved = draft.append_edit(
        expected_revision_id="poc-rev-1",
        revision_id="poc-rev-2",
        section_updates={PocSectionName.MONITORING: "Audit compliance daily."},
    )

    assert resolved.current_revision.approval_ready
    assert resolved.current_revision.missing_information == ()
    assert (
        resolved.current_revision.section_origins[PocSectionName.MONITORING]
        is SectionOrigin.USER_EDITED
    )

    restored = resolved.append_edit(
        expected_revision_id="poc-rev-2",
        revision_id="poc-rev-3",
        section_updates={PocSectionName.MONITORING: None},
    )

    assert not restored.current_revision.approval_ready
    assert restored.current_revision.missing_information == (marker,)
    assert restored.current_revision.status == "unapproved"
    assert len(restored.revisions) == 3