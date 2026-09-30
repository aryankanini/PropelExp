# Task - TASK_002

## Requirement Reference
- **User Story:** US_012
- **Story Location:** .propel/context/tasks/EP-001/us_012/us_012.md
- **Acceptance Criteria:**
  - AC-001: Valid structure marks the case extraction-ready.
  - AC-002: Invalid structure returns a reason and no extraction result.
- **Edge Cases:**
  - Mixed readability is rejected when identity cannot be established.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | FastAPI | 0.141.1 | UC-001 requires validation state through the case API. |

---

## Task Overview
Expose document validation state and safe rejection reasons in the case projection. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires CMS-2567 validation outcomes.
- US_011 TASK_004 - Requires the case API.

## Impacted Components
- New validation schemas and case projection assembler.

## Implementation Plan
- Map accepted results to extraction-ready case state.
- Map invalid results to stable reasons without extraction candidates.

## Current Project State
- The planned upload endpoint has no document validation projection.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/api/schemas/document_validation.py | Define safe validation states and reasons. |
| CREATE | backend/src/cms_planner/modules/intake/case_projection.py | Assemble intake validation state. |

## External References
- https://fastapi.tiangolo.com/tutorial/response-model/

## Build Commands
- `cd backend; python -m pytest tests/integration/api/test_document_validation.py`

## Implementation Validation Strategy
- [x] API checks prove valid readiness and invalid-result exclusion.

## Implementation Checklist
- [x] Expose extraction-ready state for valid documents for AC-001.
- [x] Expose a safe rejection reason for invalid documents for AC-002.
- [x] Exclude extraction results from rejected case projections for AC-002.
