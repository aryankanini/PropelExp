# Task - TASK_004

## Requirement Reference
- **User Story:** US_018
- **Story Location:** .propel/context/tasks/EP-002/us_018/us_018.md
- **Acceptance Criteria:**
  - AC-001: CMS-2567 structural markers identify the document and retain its layout pattern; unrecognized documents stop extraction.
  - AC-002: Each F-tag record contains complete SOD and source evidence.
  - AC-003: Incomplete SOD remains uncertain and unconfirmed.
- **Edge Cases:**
  - Repeated F-tag labels with distinct sections remain separate.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-002 |
| **AI Pattern** | Hybrid |
| **Prompt Template Path** | Validation-only task; no prompt template is used |
| **Guardrails Config** | backend/src/cms_planner/adapters/ai/deficiency_candidate_validator.py |
| **Model Provider** | Provider-neutral validation; no provider is selected |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | JSON Schema and adapter contract | JSON Schema 2020-12; adapter contract v1 | AIR-002 requires deterministic candidate validation. |

---

## Task Overview
Validate evidence-linked deficiency candidates and complete SOD boundaries. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_003 - Requires the closed deficiency schema.

## Impacted Components
- New deficiency candidate validator.

## Implementation Plan
- Enforce closed fields, evidence references, complete text, and identity uniqueness.
- Retain incomplete but structurally valid candidates only as uncertain.

## Current Project State
- The deficiency contract is planned without runtime response guardrails.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/adapters/ai/deficiency_candidate_validator.py | Validate structured deficiency output. |

## External References
- https://json-schema.org/draft/2020-12

## Build Commands
- `cd backend; python -m pytest tests/unit/adapters/ai/test_deficiency_candidate_validator.py`

## Implementation Validation Strategy
- [x] Tests cover complete, incomplete, repeated-tag, and evidence-invalid candidates.

## Implementation Checklist
- [x] Reject candidates that do not reference a retained recognized CMS-2567 layout for AC-001.
- [x] Accept separate complete evidence-linked deficiency records for AC-002.
- [x] Preserve repeated labels as distinct records for AC-002.
- [x] Mark incomplete SOD candidates uncertain and unconfirmed for AC-003.
