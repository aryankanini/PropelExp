import pytest

from cms_planner.adapters.ai.guardrails import ground_response, validate_provider_response
from cms_planner.application.failures import ValidationFailure
from cms_planner.domain.deficiency import DeficiencyRevision, EvidenceSpan, ReviewedField
from cms_planner.domain.poc import PocSectionName


SECTION_NAMES = tuple(section.value for section in PocSectionName)


def provider_payload() -> dict[str, object]:
    return {
        "sections": [
            {
                "name": name,
                "statements": [
                    {"kind": "generic_guidance", "text": f"Guidance for {name}."}
                ],
            }
            for name in SECTION_NAMES
        ]
    }


@pytest.mark.parametrize("invalid_kind", ("missing", "reordered", "empty", "extra"))
def test_guardrail_rejects_invalid_five_part_output(invalid_kind: str) -> None:
    payload = provider_payload()
    sections = payload["sections"]
    assert isinstance(sections, list)
    if invalid_kind == "missing":
        sections.pop()
    elif invalid_kind == "reordered":
        sections[0], sections[1] = sections[1], sections[0]
    elif invalid_kind == "empty":
        sections[0]["statements"] = []
    else:
        sections[0]["unexpected"] = "rejected"

    with pytest.raises(ValidationFailure):
        validate_provider_response(payload)


def test_grounding_filters_references_and_replaces_unsupported_claims() -> None:
    payload = provider_payload()
    first_section = payload["sections"][0]
    first_section["statements"] = [
        {
            "kind": "facility_claim",
            "text": "The facility identified an affected resident.",
            "required_fact": "the affected resident",
            "support_references": [
                {"kind": "reviewed_field", "reference_id": "field-1"},
                {"kind": "evidence_span", "reference_id": "other-deficiency"},
            ],
        },
        {
            "kind": "facility_claim",
            "text": "The facility completed retraining.",
            "required_fact": "completion of retraining",
            "support_references": [],
        },
        {"kind": "generic_guidance", "text": "Monitor corrective action."},
    ]
    revision = DeficiencyRevision(
        revision_id="def-rev-1",
        reviewed_fields=(ReviewedField(field_id="field-1", name="SOD", value="value"),),
        evidence_spans=(
            EvidenceSpan(evidence_id="evidence-1", page_number=1, text="source"),
        ),
        confirmed=True,
    )

    result = ground_response(validate_provider_response(payload), revision)

    assert result.grounded_claims[0].support_references[0].reference_id == "field-1"
    assert len(result.grounded_claims[0].support_references) == 1
    assert result.missing_information[0].required_fact == "completion of retraining"
    assert "The facility completed retraining." not in result.content.affected_residents
    assert "[Missing information: completion of retraining]" in result.content.affected_residents
    assert "Monitor corrective action." in result.content.affected_residents