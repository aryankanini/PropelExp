"""Atomically confirm complete current deficiency revisions."""

from uuid import uuid4

from application.ports.case_repository import CaseRepository
from domain.case.aggregate import CaseAggregate
from cms_planner.domain.confirmation import (
    BlockerCode,
    ConfirmationBlocker,
    ConfirmationCommand,
    ConfirmationOutcome,
)
from cms_planner.application.ports.poc_repository import PocRepository
from cms_planner.domain.deficiency import (
    Deficiency,
    DeficiencyRevision,
    EvidenceSpan,
    ReviewedField,
)
from cms_planner.domain.review import ReviewField, StaleReviewRevisionError

REQUIRED_DEFICIENCY_FIELDS = ("sod",)


class ConfirmationService:
    """Evaluate all blockers and confirm eligible fields as one transaction."""

    def __init__(
        self,
        repository: CaseRepository,
        poc_repository: PocRepository | None = None,
    ) -> None:
        self._repository = repository
        self._poc_repository = poc_repository

    def confirm(
        self,
        session_id: str,
        command: ConfirmationCommand,
    ) -> ConfirmationOutcome:
        def update(aggregate: CaseAggregate) -> tuple[CaseAggregate, ConfirmationOutcome]:
            fields = tuple(
                field
                for field in aggregate.review_fields
                if field.deficiency_id == command.deficiency_id
            )
            expected = {
                item.field_id: item.revision_id for item in command.expected_revisions
            }
            for field in fields:
                if expected.get(field.field_id) != field.current_revision_id:
                    raise StaleReviewRevisionError(
                        expected.get(field.field_id, ""),
                        field.current_revision_id,
                    )

            blockers = self._find_blockers(fields)
            if blockers:
                outcome = ConfirmationOutcome(
                    deficiency_id=command.deficiency_id,
                    confirmed=False,
                    poc_generation_eligible=False,
                    blockers=blockers,
                )
                return aggregate, outcome

            updated_aggregate = aggregate
            approved_ids: list[str] = []
            for field in fields:
                approved = field.approve(
                    expected_revision_id=field.current_revision_id,
                    revision_id=uuid4().hex,
                )
                approved_ids.append(approved.current_revision_id)
                updated_aggregate = updated_aggregate.replace_review_field(approved)
            outcome = ConfirmationOutcome(
                deficiency_id=command.deficiency_id,
                confirmed=True,
                poc_generation_eligible=True,
                confirmed_revision_ids=tuple(approved_ids),
            )
            return updated_aggregate, outcome

        outcome = self._repository.update(session_id, update)
        if outcome.confirmed and self._poc_repository is not None:
            aggregate = self._repository.get(session_id)
            if aggregate is not None:
                self._register_confirmed_deficiency(
                    command.deficiency_id,
                    tuple(
                        field
                        for field in aggregate.review_fields
                        if field.deficiency_id == command.deficiency_id
                    ),
                )
        return outcome

    def _register_confirmed_deficiency(
        self,
        deficiency_id: str,
        fields: tuple[ReviewField, ...],
    ) -> None:
        revision_id = uuid4().hex
        reviewed_fields = tuple(
            ReviewedField(
                field_id=field.field_id,
                name=field.field_type,
                value=field.current_revision.value,
            )
            for field in fields
        )
        evidence_by_id = {
            f"{field.field_id}:p{evidence.page_number}": EvidenceSpan(
                evidence_id=f"{field.field_id}:p{evidence.page_number}",
                page_number=evidence.page_number,
                text=evidence.full_snippet,
            )
            for field in fields
            for evidence in field.evidence_items
        }
        revision = DeficiencyRevision(
            revision_id=revision_id,
            reviewed_fields=reviewed_fields,
            evidence_spans=tuple(evidence_by_id.values()),
            confirmed=True,
        )
        self._poc_repository.add_deficiency(
            Deficiency(
                deficiency_id=deficiency_id,
                revisions=(revision,),
                current_revision_id=revision_id,
            )
        )

    @staticmethod
    def _find_blockers(
        fields: tuple[ReviewField, ...],
    ) -> tuple[ConfirmationBlocker, ...]:
        blockers: list[ConfirmationBlocker] = []
        for field_type in REQUIRED_DEFICIENCY_FIELDS:
            matching = [field for field in fields if field.field_type == field_type]
            if not matching:
                blockers.append(
                    ConfirmationBlocker(
                        field_type=field_type,
                        code=BlockerCode.MISSING_FIELD,
                    )
                )
                continue
            for field in matching:
                if field.unresolved:
                    blockers.append(
                        ConfirmationBlocker(
                            field_type=field_type,
                            field_id=field.field_id,
                            code=BlockerCode.UNRESOLVED,
                        )
                    )
                if field.current_revision.evidence is None:
                    blockers.append(
                        ConfirmationBlocker(
                            field_type=field_type,
                            field_id=field.field_id,
                            code=BlockerCode.MISSING_EVIDENCE,
                        )
                    )
        return tuple(blockers)
