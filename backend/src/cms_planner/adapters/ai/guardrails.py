"""Deterministic schema and grounding guardrails for generated POC output."""

import json

from pydantic import ValidationError

from cms_planner.application.failures import FieldFailure, ValidationFailure
from cms_planner.domain.deficiency import DeficiencyRevision
from cms_planner.domain.poc import (
    GroundedClaim,
    MissingInformationMarker,
    PocContent,
    SupportReference,
)
from cms_planner.domain.poc_generation import (
    FacilityClaim,
    GeneratedGuidance,
    GuardedPocResult,
    ProviderPocResponse,
)


class DeterministicPocGuardrails:
    """Apply closed-schema validation and same-deficiency grounding."""

    def apply(
        self,
        payload: object,
        deficiency_revision: DeficiencyRevision,
    ) -> GuardedPocResult:
        response = validate_provider_response(payload)
        return ground_response(response, deficiency_revision)


def validate_provider_response(payload: object) -> ProviderPocResponse:
    """Reject malformed or incomplete provider output with typed public fields."""
    try:
        if isinstance(payload, ProviderPocResponse):
            return payload
        serialized = json.dumps(payload, allow_nan=False)
        return ProviderPocResponse.model_validate_json(serialized)
    except ValidationError as error:
        field_errors = tuple(
            FieldFailure(
                field="provider_output."
                + ".".join(str(part) for part in item["loc"]),
                message="Invalid generated section.",
            )
            for item in error.errors()
        )
        raise ValidationFailure(field_errors) from error
    except (TypeError, ValueError) as error:
        raise ValidationFailure(
            (
                FieldFailure(
                    field="provider_output",
                    message="Invalid generated output.",
                ),
            )
        ) from error


def ground_response(
    response: ProviderPocResponse,
    deficiency_revision: DeficiencyRevision,
) -> GuardedPocResult:
    """Retain only same-deficiency support and replace unsupported assertions."""
    valid_fields = {field.field_id for field in deficiency_revision.reviewed_fields}
    valid_evidence = {
        evidence.evidence_id for evidence in deficiency_revision.evidence_spans
    }
    content: dict[str, str] = {}
    grounded_claims: list[GroundedClaim] = []
    markers: list[MissingInformationMarker] = []

    for section in response.sections:
        rendered: list[str] = []
        for index, statement in enumerate(section.statements):
            if isinstance(statement, GeneratedGuidance):
                rendered.append(statement.text)
                continue

            references = _valid_references(
                statement,
                valid_fields=valid_fields,
                valid_evidence=valid_evidence,
            )
            if references:
                rendered.append(statement.text)
                grounded_claims.append(
                    GroundedClaim(
                        section=section.name,
                        text=statement.text,
                        support_references=references,
                    )
                )
                continue

            marker = MissingInformationMarker(
                marker_id=(
                    f"{deficiency_revision.revision_id}:{section.name.value}:{index}"
                ),
                section=section.name,
                required_fact=statement.required_fact,
            )
            markers.append(marker)
            rendered.append(f"[Missing information: {marker.required_fact}]")
        content[section.name.value] = "\n\n".join(rendered)

    return GuardedPocResult(
        content=PocContent(**content),
        grounded_claims=tuple(grounded_claims),
        missing_information=tuple(markers),
    )


def _valid_references(
    claim: FacilityClaim,
    *,
    valid_fields: set[str],
    valid_evidence: set[str],
) -> tuple[SupportReference, ...]:
    return tuple(
        reference
        for reference in claim.support_references
        if (
            reference.kind == "reviewed_field"
            and reference.reference_id in valid_fields
        )
        or (
            reference.kind == "evidence_span"
            and reference.reference_id in valid_evidence
        )
    )