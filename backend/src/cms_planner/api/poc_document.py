"""Case-level combined SOD/POC document routes."""

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from cms_planner.application.case_poc_document_service import CasePocDocumentService
from cms_planner.application.failures import StaleStateFailure
from cms_planner.domain.poc import PocDraft, PocSectionName
from domain.case.revision_errors import StaleRevisionError


class PocDocumentEditRequest(BaseModel):
    """Optimistic edit for one deficiency inside the combined document."""

    model_config = ConfigDict(extra="forbid")

    expected_revision_id: str = Field(min_length=1)
    deficiency_id: str = Field(min_length=1)
    section_updates: dict[PocSectionName, str] = Field(min_length=1)


def create_poc_document_router(service: CasePocDocumentService) -> APIRouter:
    router = APIRouter(prefix="/sessions/{session_id}/poc-document", tags=["poc"])

    @router.post("", response_model=PocDraft)
    def generate_document(session_id: str) -> PocDraft:
        return service.generate(session_id)

    @router.get("", response_model=PocDraft)
    def get_document(session_id: str) -> PocDraft:
        return service.get(session_id)

    @router.patch("", response_model=PocDraft)
    def edit_document(
        session_id: str,
        request: PocDocumentEditRequest,
    ) -> PocDraft:
        try:
            return service.edit(
                session_id=session_id,
                expected_revision_id=request.expected_revision_id,
                deficiency_id=request.deficiency_id,
                section_updates=request.section_updates,
            )
        except StaleRevisionError as error:
            raise StaleStateFailure() from error

    return router
