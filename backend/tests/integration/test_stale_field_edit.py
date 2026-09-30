from concurrent.futures import ThreadPoolExecutor

from adapters.repositories.in_memory_case_repository import InMemoryCaseRepository
from application.commands.edit_extracted_field import EditExtractedField
from domain.case.aggregate import CaseAggregate
from domain.case.extracted_field import ExtractedField
from domain.case.field_revision import FieldRevision
from domain.case.revision_errors import StaleRevisionError


def test_concurrent_edits_accept_one_revision_and_reject_the_stale_edit() -> None:
    repository = InMemoryCaseRepository()
    original = FieldRevision(
        revision_id="revision-1",
        value="Original value",
        page_number=1,
        supporting_snippet="Evidence",
        confidence=0.9,
        origin="extracted",
        revision_number=1,
    )
    field = ExtractedField(
        field_id="field-1",
        revisions=(original,),
        current_revision_id=original.revision_id,
    )
    repository.add(
        CaseAggregate(session_id="session-1", case_id="case-1").add_extracted_field(field)
    )
    command = EditExtractedField(repository)

    def edit(value: str) -> ExtractedField | StaleRevisionError:
        try:
            return command.execute(
                session_id="session-1",
                field_id="field-1",
                expected_revision_id="revision-1",
                value=value,
            )
        except StaleRevisionError as error:
            return error

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(edit, ("First edit", "Second edit")))

    retained = repository.get("session-1")
    accepted = [result for result in results if isinstance(result, ExtractedField)]
    rejected = [result for result in results if isinstance(result, StaleRevisionError)]
    assert retained is not None
    assert len(accepted) == 1
    assert len(rejected) == 1
    assert retained.extracted_fields[0].current_revision_id == accepted[0].current_revision_id
    assert rejected[0].current_revision_id == accepted[0].current_revision_id