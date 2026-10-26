"""Generate and edit one case-level SOD/POC document."""

from collections.abc import Callable
from uuid import uuid4

from application.ports.case_repository import CaseRepository
from cms_planner.application.failures import (
    GenerationDeniedFailure,
    ResourceNotFoundFailure,
    ValidationFailure,
)
from cms_planner.application.ports.poc_guardrails import PocGuardrails
from cms_planner.application.ports.poc_provider import PocProvider
from cms_planner.domain.deficiency import DeficiencyRevision, EvidenceSpan, ReviewedField
from cms_planner.domain.poc import (
    POC_SECTION_ORDER,
    PocDocumentEntry,
    PocDraft,
    PocRevision,
    PocSectionName,
    SectionOrigin,
    combine_document_content,
)
from cms_planner.domain.poc_generation import PocGenerationInput
from cms_planner.domain.review import ReviewField
from domain.case.errors import CaseNotFoundError
from domain.case.revision_errors import StaleRevisionError


class CasePocDocumentService:
    """Own the single provider call and revision history for a complete case."""

    def __init__(
        self,
        repository: CaseRepository,
        provider: PocProvider,
        guardrails: PocGuardrails,
        revision_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._repository = repository
        self._provider = provider
        self._guardrails = guardrails
        self._revision_id_factory = revision_id_factory or (lambda: uuid4().hex)

    def generate(self, session_id: str) -> PocDraft:
        aggregate = self._repository.get(session_id)
        if aggregate is None:
            raise CaseNotFoundError(session_id)
        fields = tuple(
            field for field in aggregate.review_fields if field.field_type == "sod"
        )
        if not fields or any(
            field.confirmed_revision_id != field.current_revision_id for field in fields
        ):
            raise GenerationDeniedFailure()

        boundary = "|".join(field.current_revision_id for field in fields)
        current = aggregate.poc_draft
        if (
            current is not None
            and current.current_revision.deficiency_revision_id == boundary
        ):
            return current

        revisions = tuple(_deficiency_revision(field) for field in fields)
        requests = tuple(
            PocGenerationInput(
                deficiency_id=field.deficiency_id or field.field_id,
                deficiency_revision_id=revision.revision_id,
                reviewed_fields=revision.reviewed_fields,
                evidence_spans=revision.evidence_spans,
            )
            for field, revision in zip(fields, revisions, strict=True)
        )
        raw = self._provider.generate_case(requests)
        payload_by_id = _case_entries(raw)
        if set(payload_by_id) != {request.deficiency_id for request in requests}:
            raise ValidationFailure(())
        entries: list[PocDocumentEntry] = []
        for field, revision in zip(fields, revisions, strict=True):
            deficiency_id = field.deficiency_id or field.field_id
            generated = self._guardrails.apply(
                _provider_entry(payload_by_id[deficiency_id]),
                revision,
            )
            entries.append(
                PocDocumentEntry(
                    deficiency_id=deficiency_id,
                    label=field.label,
                    sod_text=field.current_revision.value,
                    content=generated.content,
                    section_origins={
                        section: SectionOrigin.AI_GENERATED
                        for section in POC_SECTION_ORDER
                    },
                    grounded_claims=generated.grounded_claims,
                    missing_information=generated.missing_information,
                )
            )

        document_entries = tuple(entries)
        revision = PocRevision(
            revision_id=self._revision_id_factory(),
            deficiency_revision_id=boundary,
            content=combine_document_content(document_entries),
            section_origins={
                section: SectionOrigin.AI_GENERATED for section in POC_SECTION_ORDER
            },
            missing_information=tuple(
                marker
                for entry in document_entries
                for marker in entry.missing_information
            ),
            document_entries=document_entries,
        )
        draft = PocDraft(
            deficiency_id=f"case:{aggregate.case_id}",
            revisions=(revision,),
            current_revision_id=revision.revision_id,
        )
        self._repository.update(
            session_id,
            lambda case: (case.attach_poc_draft(draft), None),
        )
        return draft

    def get(self, session_id: str) -> PocDraft:
        aggregate = self._repository.get(session_id)
        if aggregate is None:
            raise CaseNotFoundError(session_id)
        if aggregate.poc_draft is None:
            raise ResourceNotFoundFailure()
        return aggregate.poc_draft

    def edit(
        self,
        *,
        session_id: str,
        expected_revision_id: str,
        deficiency_id: str,
        section_updates: dict[PocSectionName, str],
    ) -> PocDraft:
        if not section_updates or any(not value.strip() for value in section_updates.values()):
            raise ValidationFailure(())

        def update(case):
            if case.poc_draft is None:
                raise ResourceNotFoundFailure()
            draft = case.poc_draft.append_document_edit(
                expected_revision_id=expected_revision_id,
                revision_id=self._revision_id_factory(),
                deficiency_id=deficiency_id,
                section_updates=section_updates,
            )
            return case.attach_poc_draft(draft), draft

        try:
            return self._repository.update(session_id, update)
        except KeyError as error:
            raise ResourceNotFoundFailure() from error
        except StaleRevisionError:
            raise


def _deficiency_revision(field: ReviewField) -> DeficiencyRevision:
    evidence = {
        f"{field.field_id}:p{item.page_number}": EvidenceSpan(
            evidence_id=f"{field.field_id}:p{item.page_number}",
            page_number=item.page_number,
            text=item.full_snippet,
        )
        for item in field.evidence_items
    }
    return DeficiencyRevision(
        revision_id=field.current_revision_id,
        reviewed_fields=(
            ReviewedField(
                field_id=field.field_id,
                name=field.field_type,
                value=field.current_revision.value,
            ),
        ),
        evidence_spans=tuple(evidence.values()),
        confirmed=True,
    )


def _case_entries(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict) or not isinstance(payload.get("entries"), list):
        raise ValidationFailure(())
    entries: dict[str, object] = {}
    for entry in payload["entries"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("deficiency_id"), str):
            raise ValidationFailure(())
        deficiency_id = entry["deficiency_id"]
        if deficiency_id in entries:
            raise ValidationFailure(())
        entries[deficiency_id] = entry
    return entries


def _provider_entry(entry: object) -> object:
    if not isinstance(entry, dict):
        raise ValidationFailure(())
    return {
        "sections": [
            {
                "name": section.value,
                "statements": [
                    {"kind": "generic_guidance", "text": statement}
                    for statement in entry.get(section.value, [])
                ],
            }
            for section in POC_SECTION_ORDER
        ]
    }
