import json
from pathlib import Path


def test_aggregate_schema_is_closed_json_schema_2020_12() -> None:
    schema_path = (
        Path(__file__).parents[2]
        / "src/cms_planner/application/ports/extraction_response.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {
        "provider_candidates",
        "deficiency_candidates",
    }
    assert all(
        definition["additionalProperties"] is False
        for definition in schema["$defs"].values()
    )


def test_candidate_shapes_require_evidence_confidence_and_uncertainty() -> None:
    schema_path = (
        Path(__file__).parents[2]
        / "src/cms_planner/application/ports/extraction_response.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    provider_required = set(schema["$defs"]["providerCandidate"]["required"])
    deficiency_required = set(schema["$defs"]["deficiencyCandidate"]["required"])
    evidence_required = set(schema["$defs"]["evidence"]["required"])

    assert {"provider", "confidence", "uncertainty"} <= provider_required
    assert {"evidence", "confidence", "uncertainty"} <= deficiency_required
    assert {"page_number", "text"} <= evidence_required
