import pytest
from pydantic import ValidationError

from cms_planner.domain.cms_layout import CmsLayoutPattern
from cms_planner.domain.deficiency_candidate import (
    DeficiencyCandidate,
    DeficiencyCandidateEvidence,
)
from cms_planner.domain.deficiency_policy import (
    CandidateConfirmationError,
    confirm_deficiency_candidate,
)


def candidate(
    candidate_id: str = "candidate:0001",
    *,
    sod_text: str | None = "Complete SOD",
    uncertainty: bool = False,
) -> DeficiencyCandidate:
    return DeficiencyCandidate(
        candidate_id=candidate_id,
        boundary_id=candidate_id.replace("candidate", "cms-2567"),
        layout_pattern=CmsLayoutPattern.CMS_2567,
        f_tag="F0686",
        sod_text=sod_text,
        evidence=(
            DeficiencyCandidateEvidence(
                evidence_id=f"{candidate_id}:evidence:1",
                page_number=2,
                text="F 0686 evidence",
            ),
        ),
        confidence=0.8,
        uncertainty=uncertainty,
        confirmed=False,
    )


def test_confirms_complete_certain_candidate() -> None:
    confirmed = confirm_deficiency_candidate(candidate())

    assert confirmed.confirmed is True
    assert confirmed.candidate_id == "candidate:0001"


def test_incomplete_candidate_is_always_uncertain_and_unconfirmed() -> None:
    with pytest.raises(ValidationError, match="incomplete SOD"):
        candidate(sod_text=None, uncertainty=False)

    incomplete = candidate(sod_text=None, uncertainty=True)
    assert incomplete.confirmed is False
    with pytest.raises(CandidateConfirmationError, match="complete SOD"):
        confirm_deficiency_candidate(incomplete)


def test_uncertain_complete_candidate_cannot_be_confirmed() -> None:
    with pytest.raises(CandidateConfirmationError, match="uncertainty"):
        confirm_deficiency_candidate(candidate(uncertainty=True))


def test_repeated_f_tags_keep_independent_stable_identities() -> None:
    first = candidate("candidate:0001")
    second = candidate("candidate:0002")

    assert first.f_tag == second.f_tag
    assert first.candidate_id != second.candidate_id
    assert first.boundary_id != second.boundary_id