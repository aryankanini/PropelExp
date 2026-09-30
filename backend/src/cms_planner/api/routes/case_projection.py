"""FastAPI route for the full evidence-linked case projection."""

from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from adapters.repositories.in_memory_case_repository import (
    InMemoryCaseRepository,
)
from cms_planner.domain.deficiency_candidate import (
    DeficiencyCandidate,
)


class CandidateEvidenceOut(BaseModel):
    model_config = ConfigDict(frozen=True)

    evidence_id: str
    page_number: int
    text: str


class DeficiencyCandidateOut(BaseModel):
    model_config = ConfigDict(frozen=True)

    candidate_id: str
    boundary_id: str
    f_tag: str
    sod_text: str | None
    evidence: tuple[CandidateEvidenceOut, ...]
    confidence: float
    uncertainty: bool
    confirmed: bool


class CaseProjection(BaseModel):
    model_config = ConfigDict(frozen=True)

    case_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    status: str
    deficiency_candidates: tuple[
        DeficiencyCandidateOut,
        ...
    ]
    review_fields_count: int
    poc_draft_present: bool
    approval_status: str


def create_case_projection_router(
    repository: InMemoryCaseRepository,
) -> APIRouter:

    router = APIRouter(
        prefix="/api/v1/cases",
        tags=["cases"],
    )

    @router.get(
        "/{case_id}",
        response_model=CaseProjection,
    )
    def get_case(
        case_id: str,
        session_id: Annotated[
            str,
            Header(
                alias="X-Session-ID",
                min_length=1,
            ),
        ],
    ) -> CaseProjection:

        aggregate = repository.get(
            session_id
        )

        if (
            aggregate is None
            or aggregate.case_id != case_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Case not found",
            )

        if aggregate.poc_draft is not None:
            case_status = "poc_ready"
        elif aggregate.review_fields:
            case_status = "review_ready"
        elif aggregate.deficiency_candidates:
            case_status = "review_ready"
        else:
            case_status = "extraction_ready"

        candidates = tuple(
            _candidate_to_output(candidate)
            for candidate
            in aggregate.deficiency_candidates
        )

        return CaseProjection(
            case_id=aggregate.case_id,
            session_id=aggregate.session_id,
            status=case_status,
            deficiency_candidates=candidates,
            review_fields_count=len(
                aggregate.review_fields
            ),
            poc_draft_present=(
                aggregate.poc_draft is not None
            ),
            approval_status=aggregate.approval.status,
        )

    return router


def _candidate_to_output(
    candidate: DeficiencyCandidate,
) -> DeficiencyCandidateOut:

    return DeficiencyCandidateOut(
        candidate_id=candidate.candidate_id,
        boundary_id=candidate.boundary_id,
        f_tag=candidate.f_tag,
        sod_text=candidate.sod_text,
        evidence=tuple(
            CandidateEvidenceOut(
                evidence_id=evidence.evidence_id,
                page_number=evidence.page_number,
                text=evidence.text,
            )
            for evidence in candidate.evidence
        ),
        confidence=candidate.confidence,
        uncertainty=candidate.uncertainty,
        confirmed=candidate.confirmed,
    )