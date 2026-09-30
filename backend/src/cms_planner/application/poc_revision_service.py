"""Atomically append user-edited POC revisions."""

from collections.abc import Callable
from uuid import uuid4

from pydantic import ValidationError

from cms_planner.application.failures import (
    FieldFailure,
    ResourceNotFoundFailure,
    RetentionFailure,
    StaleStateFailure,
    ValidationFailure,
)
from cms_planner.application.ports.poc_repository import PocRepository, PocRetentionError
from cms_planner.domain.poc import PocDraft, PocSectionName
from domain.case.revision_errors import StaleRevisionError


class PocRevisionService:
    """Validate and retain edits without replacing the last good revision on failure."""

    def __init__(
        self,
        repository: PocRepository,
        revision_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._repository = repository
        self._revision_id_factory = revision_id_factory or (lambda: uuid4().hex)

    def save(
        self,
        *,
        deficiency_id: str,
        expected_revision_id: str,
        section_updates: dict[PocSectionName, str | None],
    ) -> PocDraft:
        if not section_updates:
            raise ValidationFailure(
                (FieldFailure(field="section_updates", message="Provide an edit."),)
            )

        def update(draft: PocDraft) -> PocDraft:
            return draft.append_edit(
                expected_revision_id=expected_revision_id,
                revision_id=self._revision_id_factory(),
                section_updates=section_updates,
            )

        try:
            return self._repository.update_draft(deficiency_id, update)
        except KeyError as error:
            raise ResourceNotFoundFailure() from error
        except StaleRevisionError as error:
            raise StaleStateFailure() from error
        except (ValidationError, ValueError) as error:
            raise ValidationFailure(
                (
                    FieldFailure(
                        field="section_updates",
                        message="Invalid POC section value.",
                    ),
                )
            ) from error
        except PocRetentionError as error:
            raise RetentionFailure() from error