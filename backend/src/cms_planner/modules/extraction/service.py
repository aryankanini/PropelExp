"""Project extraction output without failed unconfirmed page content."""

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.job_failure import JobFailure


class PageExtractionResult(BaseModel):
    """Content retained for review or already confirmed by a reviewer."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    page_number: int = Field(ge=1)
    content: str = Field(min_length=1)
    confirmed: bool = False


def project_extraction_results(
    results: tuple[PageExtractionResult, ...],
    failures: tuple[JobFailure, ...],
) -> tuple[PageExtractionResult, ...]:
    """Omit unconfirmed output for failed pages while retaining confirmed work."""

    failed_pages = {
        failure.page_number
        for failure in failures
        if failure.page_number is not None
    }
    return tuple(
        result
        for result in results
        if result.confirmed or result.page_number not in failed_pages
    )