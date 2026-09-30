# Task - TASK_003

## Requirement Reference
- **User Story:** US_018
- **Story Location:** .propel/context/tasks/EP-002/us_018/us_018.md
- **Acceptance Criteria:**
  - AC-001: CMS-2567 structural markers identify the document and retain its layout pattern; unrecognized documents stop extraction.
  - AC-002: Structured extraction returns separate F-tag and complete SOD records with evidence.
  - AC-003: Incomplete SOD records remain uncertain and unconfirmed.
- **Edge Cases:**
  - Repeated F-tag labels remain separate records.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-002 |
| **AI Pattern** | Hybrid |
| **Prompt Template Path** | Contract-only task; no prompt template is used |
| **Guardrails Config** | backend/src/cms_planner/application/ports/deficiency_schema.json |
| **Model Provider** | Provider-neutral contract; no provider is selected |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | JSON Schema and adapter contract | JSON Schema 2020-12; adapter contract v1 | AIR-002 requires a closed provider-neutral deficiency contract. |

---

## Task Overview
Define structured deficiency extraction requests and closed response schema. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_002 - Requires detected deficiency boundaries.

## Impacted Components
- New deficiency extraction port and JSON schema.

## Implementation Plan
- Define bounded evidence input for each detected deficiency region.
- Require F-tag, SOD, evidence, confidence, uncertainty, and separate identity.

## Current Project State
- No deficiency AI port or approved model provider exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/application/ports/deficiency_extraction.py | Define adapter contract v1 operations. |
| CREATE | backend/src/cms_planner/application/ports/deficiency_schema.json | Define closed JSON Schema 2020-12 output. |

## External References
- https://json-schema.org/draft/2020-12

## Build Commands
- `cd backend; python -m pytest tests/contract/test_deficiency_extraction_port.py`

## Implementation Validation Strategy
- [x] Contract tests require complete evidence-linked records and separate repeated tags.

## Implementation Checklist
- [x] Require a retained recognized CMS-2567 layout in extraction requests for AC-001.
- [x] Require separate F-tag, complete SOD, and evidence records for AC-002.
- [x] Preserve repeated F-tag identities for AC-002.
- [x] Represent incomplete SOD as uncertain and unconfirmed for AC-003.
