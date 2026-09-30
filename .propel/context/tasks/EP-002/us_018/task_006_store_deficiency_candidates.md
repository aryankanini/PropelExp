# Task - TASK_006

## Requirement Reference
- **User Story:** US_018
- **Story Location:** .propel/context/tasks/EP-002/us_018/us_018.md
- **Acceptance Criteria:**
  - AC-001: Detected layout state is retained.
  - AC-002: Separate complete deficiency records enter transient case state.
  - AC-003: Incomplete records enter as uncertain and unconfirmed.
- **Edge Cases:**
  - Header-only documents retain zero deficiencies without becoming unrecognized.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | DR-001 makes the backend sole writer of transient case state. |

---

## Task Overview
Store recognized layout and validated deficiency candidates atomically in the active case. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001, TASK_004, TASK_005 - Requires layout and validated candidate state.

## Impacted Components
- New extraction result application service.

## Implementation Plan
- Commit layout and all validated candidates in one repository operation.
- Preserve zero-deficiency and uncertain outcomes without false confirmation.

## Current Project State
- Extraction artifacts are planned without case-state orchestration.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/modules/extraction/store_extraction_result.py | Commit layout and candidate state atomically. |

## External References
- https://docs.python.org/3.14/library/typing.html

## Build Commands
- `cd backend; python -m pytest tests/unit/modules/extraction/test_store_extraction_result.py`

## Implementation Validation Strategy
- [x] Repository tests verify atomic complete, uncertain, zero-result, and rejected outcomes.

## Implementation Checklist
- [x] Retain recognized layout state for AC-001.
- [x] Store each complete F-tag and SOD record separately for AC-002.
- [x] Store incomplete records only as uncertain and unconfirmed for AC-003.
