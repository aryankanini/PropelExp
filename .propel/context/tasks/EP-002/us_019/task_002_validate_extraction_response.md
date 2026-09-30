# Task - TASK_002

## Requirement Reference
- **User Story:** US_019
- **Story Location:** .propel/context/tasks/EP-002/us_019/us_019.md
- **Acceptance Criteria:**
  - AC-001: Valid candidates enter case state as unconfirmed.
  - AC-002: Any invalid field rejects all candidates and records a safe typed failure.
- **Edge Cases:**
  - Confidence is never clamped and artifact-only text is empty.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-002 |
| **AI Pattern** | Hybrid |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | backend/src/cms_planner/adapters/ai/extraction_response_validator.py |
| **Model Provider** | N/A |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | JSON Schema and adapter contract | JSON Schema 2020-12; adapter contract v1 | AIR-002 requires all-or-nothing validation before case state. |

---

## Task Overview
Validate complete extraction responses atomically before repository writes. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires the aggregate closed schema.

## Impacted Components
- New aggregate adapter validator and typed validation failure.

## Implementation Plan
- Validate structural and semantic constraints before mapping candidates.
- Return all valid candidates as unconfirmed or one safe typed failure with no writes.

## Current Project State
- The closed schema is planned without aggregate validation orchestration.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/adapters/ai/extraction_response_validator.py | Validate responses atomically. |
| CREATE | backend/src/cms_planner/modules/extraction/schema_failure.py | Define safe typed extraction failure. |

## External References
- https://json-schema.org/draft/2020-12

## Build Commands
- `cd backend; python -m pytest tests/unit/adapters/ai/test_extraction_response_validator.py`

## Implementation Validation Strategy
- [x] Tests prove all-or-nothing storage and no confidence clamping.

## Implementation Checklist
- [x] Admit complete schema-valid candidates only as unconfirmed for AC-001.
- [x] Reject the entire response on any required or unknown field defect for AC-002.
- [x] Record a safe typed failure with no candidate writes for AC-002.
- [x] Reject range-invalid and normalization-empty values for AC-002.
