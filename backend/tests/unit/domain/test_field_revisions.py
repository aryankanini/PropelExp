import pytest

from domain.case.extracted_field import ExtractedField
from domain.case.field_revision import FieldRevision
from domain.case.revision_errors import StaleRevisionError


def make_extracted_field() -> ExtractedField:
    original = FieldRevision(
        revision_id="revision-1",
        value="Original value",
        page_number=3,
        supporting_snippet="Supporting text",
        confidence=0.82,
        origin="extracted",
        revision_number=1,
    )
    return ExtractedField(
        field_id="field-1",
        revisions=(original,),
        current_revision_id=original.revision_id,
    )


def test_edit_appends_revision_without_changing_original_evidence() -> None:
    field = make_extracted_field()
    original = field.current_revision

    updated = field.append_edit(
        expected_revision_id="revision-1",
        revision_id="revision-2",
        value="Corrected value",
    )

    assert updated.revisions[0] == original
    assert updated.current_revision.value == "Corrected value"
    assert updated.current_revision.page_number == original.page_number
    assert updated.current_revision.supporting_snippet == original.supporting_snippet
    assert updated.current_revision.origin == "user_edit"
    assert updated.current_revision_id == "revision-2"


def test_stale_edit_reports_current_revision_identifier() -> None:
    field = make_extracted_field()

    with pytest.raises(StaleRevisionError) as error:
        field.append_edit(
            expected_revision_id="stale-revision",
            revision_id="revision-2",
            value="Corrected value",
        )

    assert error.value.current_revision_id == "revision-1"