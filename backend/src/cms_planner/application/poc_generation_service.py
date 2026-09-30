"""Generate one guarded, unapproved POC draft per confirmed deficiency revision."""

from collections.abc import Callable
from uuid import uuid4

from cms_planner.application.failures import (
    GenerationDeniedFailure,
    ResourceNotFoundFailure,
)
from cms_planner.application.ports.poc_guardrails import PocGuardrails
from cms_planner.application.ports.poc_provider import PocProvider
from cms_planner.application.ports.poc_repository import PocRepository
from cms_planner.domain.poc import POC_SECTION_ORDER, PocDraft, PocRevision, SectionOrigin
from cms_planner.domain.poc_generation import PocGenerationInput


class PocGenerationService:
    """Enforce confirmation, scope, validation, grounding, and idempotency."""

    def __init__(
        self,
        repository: PocRepository,
        provider: PocProvider,
        guardrails: PocGuardrails,
        revision_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._repository = repository
        self._provider = provider
        self._guardrails = guardrails
        self._revision_id_factory = revision_id_factory or (lambda: uuid4().hex)

    def generate(self, deficiency_id: str) -> PocDraft:
        deficiency = self._repository.get_deficiency(deficiency_id)
        if deficiency is None:
            raise ResourceNotFoundFailure()
        deficiency_revision = deficiency.current_revision
        if not deficiency_revision.confirmed:
            raise GenerationDeniedFailure()

        def create() -> PocDraft:
            request = PocGenerationInput(
                deficiency_id=deficiency.deficiency_id,
                deficiency_revision_id=deficiency_revision.revision_id,
                reviewed_fields=deficiency_revision.reviewed_fields,
                evidence_spans=deficiency_revision.evidence_spans,
            )
            grounded = self._guardrails.apply(
                self._provider.generate(request),
                deficiency_revision,
            )
            revision = PocRevision(
                revision_id=self._revision_id_factory(),
                deficiency_revision_id=deficiency_revision.revision_id,
                content=grounded.content,
                section_origins={
                    section: SectionOrigin.AI_GENERATED
                    for section in POC_SECTION_ORDER
                },
                grounded_claims=grounded.grounded_claims,
                missing_information=grounded.missing_information,
            )
            return PocDraft(
                deficiency_id=deficiency.deficiency_id,
                revisions=(revision,),
                current_revision_id=revision.revision_id,
            )

        return self._repository.get_or_create_draft(
            deficiency.deficiency_id,
            deficiency_revision.revision_id,
            create,
        )