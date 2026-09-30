"""Project current and historical revision provenance."""

from application.ports.case_repository import CaseRepository
from domain.case.errors import CaseNotFoundError
from cms_planner.application.review_service import find_review_field
from cms_planner.domain.provenance import ProvenanceProjection, RevisionProvenance


class ProvenanceService:
    """Expose exactly one current origin without historical label leakage."""

    def __init__(self, repository: CaseRepository) -> None:
        self._repository = repository

    def get(self, session_id: str, field_id: str) -> ProvenanceProjection:
        aggregate = self._repository.get(session_id)
        if aggregate is None:
            raise CaseNotFoundError(session_id)
        field = find_review_field(aggregate, field_id)
        revisions = tuple(
            RevisionProvenance(
                revision_id=revision.revision_id,
                revision_number=revision.revision_number,
                origin=revision.origin,
            )
            for revision in field.revisions
        )
        return ProvenanceProjection(
            field_id=field.field_id,
            current=revisions[-1],
            history=revisions,
            reapproval_required=field.reapproval_required,
        )