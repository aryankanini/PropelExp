# Task - TASK_002

## Requirement Reference
- **User Story:** us_042
- **Story Location:** .propel/context/tasks/EP-007/us_042/us_042.md
- **Acceptance Criteria:** AC-001, AC-002, AC-003
- **Edge Cases:** Reject requests containing unrelated deficiency text.

---

## AI References [CONDITIONAL: AI Impact = Yes]
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-001 |
| **AI Pattern** | Hybrid structured generation with deterministic validation |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | backend/src/cms_planner/adapters/ai/schemas/ |
| **Model Provider** | Runtime-selected BAA-approved adapter |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI Gateway | Provider-neutral adapters, Pydantic, JSON Schema | Adapter contract v1; Pydantic 2.x; JSON Schema 2020-12 | AIR-001 requires replaceable adapters and bounded disclosure. |

---

## Task Overview
**Estimated Effort:** 6 hours

Define provider-neutral AI gateway contracts that reject excess request content and normalize provider responses.

## Dependent Tasks
- TASK_001 from US_042.

## Impacted Components
- AI adapter contracts, request schemas, and response normalization.

## Implementation Plan
- Define closed minimum-necessary request models.
- Map provider payloads at adapter boundaries.
- Reject unknown request fields before transmission.

## Current Project State
```text
backend/src/cms_planner/adapters/ai/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/adapters/ai/schemas/requests.py | Define closed request schemas. |
| CREATE | backend/src/cms_planner/adapters/ai/http_adapter.py | Normalize provider input and output at the boundary. |

## External References
- https://docs.pydantic.dev/2.12/concepts/models/#extra-data
- https://json-schema.org/draft/2020-12

## Build Commands
- [Backend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests reject unknown and unrelated request fields.
- [x] Contract tests prove adapters are replaceable behind AIR-001 contracts.

## Implementation Checklist
- [x] Consume only the validated environment-backed provider configuration. (AC-001)
- [x] Define closed request schemas for required pages, fields, and evidence. (AC-002)
- [x] Reject unrelated deficiency text and unknown fields before transmission. (AC-002, Edge Case)
- [x] Normalize provider responses to application-owned result types. (AC-003)
- [x] Keep provider-specific types inside adapter modules. (AC-003)
