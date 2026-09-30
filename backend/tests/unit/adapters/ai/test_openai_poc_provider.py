from cms_planner.adapters.ai.openai_poc_provider import _normalize_provider_response
from cms_planner.domain.poc import POC_SECTION_ORDER


def test_normalizes_section_keyed_string_guidance() -> None:
    payload = {
        section.value: [f"Guidance for {section.value}."]
        for section in POC_SECTION_ORDER
    }

    normalized = _normalize_provider_response(payload)

    assert normalized == {
        "sections": [
            {
                "name": section.value,
                "statements": [
                    {
                        "kind": "generic_guidance",
                        "text": f"Guidance for {section.value}.",
                    }
                ],
            }
            for section in POC_SECTION_ORDER
        ]
    }


def test_normalizes_type_discriminator_without_accepting_extra_sections() -> None:
    payload = {
        section.value: [
            {
                "type": "generic_guidance",
                "text": f"Guidance for {section.value}.",
            }
        ]
        for section in POC_SECTION_ORDER
    }

    normalized = _normalize_provider_response(payload)

    assert normalized["sections"][0]["statements"][0]["kind"] == "generic_guidance"
    assert _normalize_provider_response({**payload, "unexpected": []}) != normalized