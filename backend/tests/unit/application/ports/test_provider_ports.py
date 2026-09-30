import pytest
from pydantic import ValidationError

from cms_planner.application.ports.providers import ExtractionPage, ExtractionRequest


def test_extraction_request_rejects_unrelated_deficiency_text() -> None:
    with pytest.raises(ValidationError):
        ExtractionRequest(
            pages=(ExtractionPage(page_number=1, text="required page"),),
            fields=("provider_name",),
            deficiency_text="unrelated deficiency",
        )


def test_extraction_request_contains_only_required_contract_fields() -> None:
    request = ExtractionRequest(
        pages=(ExtractionPage(page_number=1, text="required page"),),
        fields=("provider_name", "f_tag", "sod"),
    )

    assert set(request.model_dump()) == {"pages", "fields"}