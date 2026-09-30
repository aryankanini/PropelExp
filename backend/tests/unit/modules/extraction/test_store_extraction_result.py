import pytest
from pydantic import ValidationError

from cms_planner.domain.cms_layout import CmsLayout, CmsLayoutPattern, CmsLayoutStatus
from cms_planner.domain.deficiency_candidate import (
    DeficiencyCandidate,
    DeficiencyCandidateEvidence,
)
from cms_planner.modules.extraction.store_extraction_result import (
    ExtractionResult,
    store_extraction_result,
)


class RecordingStore:
    storage_kind = "memory"

    def __init__(self) -> None:
        self.saved: list[ExtractionResult] = []

    def save(self, result: ExtractionResult) -> None:
        self.saved.append(result)


def layout(*, recognized: bool = True) -> CmsLayout:
    if not recognized:
        return CmsLayout(status=CmsLayoutStatus.UNRECOGNIZED)
    return CmsLayout(
        status=CmsLayoutStatus.RECOGNIZED,
        pattern=CmsLayoutPattern.CMS_2567,
        marker_page_numbers=(1,),
    )


def candidate(*, complete: bool = True) -> DeficiencyCandidate:
    return DeficiencyCandidate(
        candidate_id="candidate:0001",
        boundary_id="cms-2567:0001",
        layout_pattern=CmsLayoutPattern.CMS_2567,
        f_tag="F0686",
        sod_text="Complete SOD" if complete else None,
        evidence=(
            DeficiencyCandidateEvidence(
                evidence_id="candidate:0001:evidence:1",
                page_number=2,
                text="F 0686 evidence",
            ),
        ),
        confidence=0.8,
        uncertainty=not complete,
        confirmed=False,
    )


@pytest.mark.parametrize("complete", [True, False])
def test_stores_layout_and_all_candidates_in_one_operation(complete: bool) -> None:
    store = RecordingStore()

    result = store_extraction_result(
        store,
        case_id="case-1",
        layout=layout(),
        candidates=(candidate(complete=complete),),
    )

    assert store.saved == [result]
    assert result.candidates[0].uncertainty is (not complete)
    assert result.candidates[0].confirmed is False


def test_stores_recognized_layout_with_zero_candidates() -> None:
    store = RecordingStore()

    result = store_extraction_result(
        store,
        case_id="case-1",
        layout=layout(),
        candidates=(),
    )

    assert store.saved == [result]
    assert result.candidates == ()


def test_rejection_causes_no_partial_write() -> None:
    store = RecordingStore()

    with pytest.raises(ValidationError, match="recognized layout"):
        store_extraction_result(
            store,
            case_id="case-1",
            layout=layout(recognized=False),
            candidates=(candidate(),),
        )

    assert store.saved == []