"""HTTP routes for deficiency-scoped POC generation and revision edits."""

from typing import Annotated

from fastapi import APIRouter, Header
from pydantic import BaseModel, ConfigDict, Field

from cms_planner.application.failures import ResourceNotFoundFailure
from cms_planner.application.poc_generation_service import PocGenerationService
from cms_planner.application.poc_revision_service import PocRevisionService
from cms_planner.application.ports.poc_repository import PocRepository
from cms_planner.domain.poc import PocDraft, PocSectionName
from application.ports.case_repository import CaseRepository


class PocEditRequest(BaseModel):
    """Optimistic edit command for one or more POC sections."""

    model_config = ConfigDict(extra="forbid")

    expected_revision_id: str = Field(min_length=1)
    section_updates: dict[PocSectionName, str | None] = Field(min_length=1)


def create_poc_router(
    *,
    repository: PocRepository,
    generation_service: PocGenerationService,
    revision_service: PocRevisionService,
    case_repository: CaseRepository | None = None,
) -> APIRouter:
    router = APIRouter(prefix="/deficiencies", tags=["poc"])

    @router.post("/{deficiency_id}/poc", response_model=PocDraft)
    def generate_poc(
        deficiency_id: str,
        session_id: Annotated[str | None, Header(alias="X-Session-ID")] = None,
    ) -> PocDraft:
        draft = generation_service.generate(deficiency_id)
        _sync_case_draft(case_repository, session_id, draft)
        return draft

    @router.get("/{deficiency_id}/poc", response_model=PocDraft)
    def get_poc(deficiency_id: str) -> PocDraft:
        draft = repository.get_draft(deficiency_id)
        if draft is None:
            raise ResourceNotFoundFailure()
        return draft

    @router.patch("/{deficiency_id}/poc", response_model=PocDraft)
    def edit_poc(
        deficiency_id: str,
        request: PocEditRequest,
        session_id: Annotated[str | None, Header(alias="X-Session-ID")] = None,
    ) -> PocDraft:
        draft = revision_service.save(
            deficiency_id=deficiency_id,
            expected_revision_id=request.expected_revision_id,
            section_updates=request.section_updates,
        )
        _sync_case_draft(case_repository, session_id, draft)
        return draft

    return router


def _sync_case_draft(
    repository: CaseRepository | None,
    session_id: str | None,
    draft: PocDraft,
) -> None:
    if repository is None or session_id is None:
        return
    repository.update(
        session_id,
        lambda aggregate: (aggregate.attach_poc_draft(draft), None),
    )