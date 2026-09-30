# Task - TASK_001

## Requirement Reference
- **User Story:** US_019
- **Story Location:** .propel/context/tasks/EP-002/us_019/us_019.md
- **Acceptance Criteria:**
  - AC-001: Closed responses require provider, deficiency, evidence, confidence, and uncertainty fields with no unknown fields.
  - AC-002: Missing or unknown fields reject the entire response.
- **Edge Cases:**
  - Out-of-range confidence and normalization-empty text are rejected.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-002 |
| **AI Pattern** | Hybrid |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | backend/src/cms_planner/application/ports/extraction_response.schema.json |
| **Model Provider** | N/A |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | JSON Schema | 2020-12 | AIR-002 requires one closed extraction response schema. |

---

## Task Overview
Define the complete closed extraction response schema and semantic constraints. Estimated effort: 8 hours.

## Dependent Tasks
- US_017 TASK_001, US_018 TASK_003 - Requires provider and deficiency candidate shapes.

## Impacted Components
- New aggregate extraction response schema.

## Implementation Plan
- Compose required candidate and evidence shapes with unknown fields prohibited.
- Constrain confidence range and substantive text content.

## Current Project State
- Separate candidate contracts are planned without one aggregate response schema.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/application/ports/extraction_response.schema.json | Define closed JSON Schema 2020-12 extraction output. |

## External References
- https://json-schema.org/draft/2020-12

## Build Commands
- `cd backend; python -m pytest tests/contract/test_extraction_schema.py`

## Implementation Validation Strategy
- [x] Schema fixtures cover required, unknown, range, and empty-content cases.

## Implementation Checklist
- [x] Require all provider, deficiency, evidence, confidence, and uncertainty fields for AC-001.
- [x] Prohibit unknown fields for AC-001.
- [x] Reject missing or additional fields for AC-002.
- [x] Reject out-of-range confidence and empty normalized text for AC-002.
