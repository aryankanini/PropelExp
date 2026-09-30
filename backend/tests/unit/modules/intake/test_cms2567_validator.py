from application.intake.cms2567_validator import Cms2567Validator
from application.intake.preflight import DocumentInspection


VALID_TEXT = (
    "CMS-2567 Statement of Deficiencies and Plan of Correction",
    "Continuation page",
)


def test_valid_document_is_extraction_ready() -> None:
    result = Cms2567Validator().validate(DocumentInspection(page_texts=VALID_TEXT))

    assert result.status == "extraction_ready"
    assert result.page_count == 2

def test_cms2567_without_literal_form_number_is_accepted() -> None:
    result = Cms2567Validator().validate(
        DocumentInspection(
            page_texts=(
                "STATEMENT OF DEFICIENCIES",
                "AND PLAN OF CORRECTION",
            )
        )
    )
    assert result.status == "extraction_ready"

def test_unreadable_document_is_rejected() -> None:
    result = Cms2567Validator().validate(DocumentInspection(page_texts=(None,)))

    assert result.status == "rejected"
    assert result.reason == "unreadable"


def test_non_cms_document_is_rejected() -> None:
    result = Cms2567Validator().validate(
        DocumentInspection(page_texts=("Unrelated readable report",))
    )

    assert result.status == "rejected"
    assert result.reason == "not_cms2567"


def test_mixed_readability_is_rejected() -> None:
    result = Cms2567Validator().validate(
        DocumentInspection(page_texts=(VALID_TEXT[0], None))
    )

    assert result.status == "rejected"
    assert result.reason == "unreadable"