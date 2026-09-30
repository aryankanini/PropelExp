# Task - TASK_001

## Requirement Reference
- **User Story:** US_015
- **Story Location:** .propel/context/tasks/EP-001/us_015/us_015.md
- **Acceptance Criteria:**
  - AC-001: Confirmed end session cleans memory and workspace before returning empty intake.
  - AC-002: Cleanup failure retains the case and does not claim it was cleared.
- **Edge Cases:**
  - Retrying after failure is idempotent and cannot reuse the workspace prematurely.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | FastAPI | 0.141.1 | FR-020 and UC-009 require an explicit case lifecycle endpoint. |

---

## Task Overview
Expose confirmed case termination with truthful cleanup results. Estimated effort: 8 hours.

## Dependent Tasks
- US_009 - Requires verified lifecycle cleanup.

## Impacted Components
- New case deletion route and cleanup response schema.

## Implementation Plan
- Authorize and invoke idempotent cleanup for the active case.
- Return success only after memory and workspace verification; preserve state on failure.

## Current Project State
- No explicit case termination route exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/api/routes/case_lifecycle.py | Expose `DELETE /api/v1/cases/{caseId}`. |
| CREATE | backend/src/cms_planner/api/schemas/cleanup.py | Define completed and failed cleanup outcomes. |

## External References
- https://fastapi.tiangolo.com/tutorial/handling-errors/

## Build Commands
- `cd backend; python -m pytest tests/integration/api/test_end_case.py`

## Implementation Validation Strategy
- [x] API tests verify success only after cleanup and retained state on failure.

## Implementation Checklist
- [x] Complete memory and workspace cleanup before success for AC-001.
- [x] Return a truthful failed outcome while retaining the case for AC-002.
- [x] Make repeated cleanup safe and prevent premature workspace reuse for AC-002.
