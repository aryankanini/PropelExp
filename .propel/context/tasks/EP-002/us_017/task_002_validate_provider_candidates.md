# Task - TASK_002

## Requirement Reference
- **User Story:** US_017
- **Story Location:** .propel/context/tasks/EP-002/us_017/us_017.md
- **Acceptance Criteria:**
  - AC-001: Valid provider candidates retain evidence, confidence, and uncertainty.
  - AC-002: Candidates missing a page or snippet are rejected before case state.
- **Edge Cases:**
  - Conflicting provider names remain separate uncertain candidates.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-002 |
| **AI Pattern** | Hybrid |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | backend/src/cms_planner/adapters/ai/provider_candidate_validator.py |
| **Model Provider** | N/A |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | JSON Schema and adapter contract | JSON Schema 2020-12; adapter contract v1 | AIR-002 requires validation before candidates enter state. |

---

## Task Overview
Validate provider extraction responses and preserve valid conflicts as uncertain. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires the provider extraction schema.

## Impacted Components
- New provider candidate adapter validator.

## Implementation Plan
- Validate closed shape, evidence references, confidence, and uncertainty.
- Reject invalid candidates before repository operations.

## Current Project State
- A provider extraction contract is planned without runtime response validation.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/adapters/ai/provider_candidate_validator.py | Validate provider candidate responses. |

## External References
- https://json-schema.org/draft/2020-12

## Build Commands
- `cd backend; python -m pytest tests/unit/adapters/ai/test_provider_candidate_validator.py`

## Implementation Validation Strategy
- [x] Validation tests cover missing evidence, confidence bounds, and conflicts.

## Implementation Checklist
- [x] Accept complete evidence-linked provider candidates for AC-001.
- [x] Preserve conflicts as separate uncertain candidates for AC-001.
- [x] Reject missing page or snippet before case state for AC-002.
