import pytest

from cms_planner.application.job_transitions import (
    InvalidJobTransitionError,
    JobState,
    JobStatus,
    record_failure,
    transition_to_completed,
)
from cms_planner.domain.job_failure import JobFailure, JobStage
from cms_planner.modules.extraction.service import (
    PageExtractionResult,
    project_extraction_results,
)


def test_failure_records_affected_page_and_retains_valid_state() -> None:
    state = JobState(
        reviewed_page_numbers=(1,),
        confirmed_deficiency_ids=("def-1",),
        retained_poc_ids=("poc-1",),
    )
    failure = JobFailure(
        stage=JobStage.OCR,
        code="provider-failed",
        page_number=2,
        retryable=True,
    )

    failed = record_failure(state, failure)

    assert failed.status is JobStatus.FAILED
    assert failed.reviewed_page_numbers == (1,)
    assert failed.confirmed_deficiency_ids == ("def-1",)
    assert failed.retained_poc_ids == ("poc-1",)


def test_failed_unconfirmed_content_is_not_projected() -> None:
    results = (
        PageExtractionResult(page_number=1, content="reviewed", confirmed=True),
        PageExtractionResult(page_number=2, content="unconfirmed"),
        PageExtractionResult(page_number=3, content="ready"),
    )
    failure = JobFailure(
        stage=JobStage.EXTRACTION,
        code="extraction-failed",
        page_number=2,
        retryable=True,
    )

    projected = project_extraction_results(results, (failure,))

    assert [result.page_number for result in projected] == [1, 3]


def test_required_failure_cannot_emit_completed_state() -> None:
    state = record_failure(
        JobState(),
        JobFailure(
            stage=JobStage.GENERATION,
            code="provider-failed",
            deficiency_id="def-1",
            retryable=True,
        ),
    )

    with pytest.raises(InvalidJobTransitionError):
        transition_to_completed(state)