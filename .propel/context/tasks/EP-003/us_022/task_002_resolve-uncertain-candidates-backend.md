# Task - TASK_002

## Requirement Reference

- **User Story**: US_022 - Resolve uncertain candidates
- **Story Location**: .propel/context/tasks/EP-003/us_022/us_022.md
- **Acceptance Criteria**:
	- **AC-001: Select supported candidate**
		- **Given**: Competing candidates and evidence are displayed
		- **When**: The reviewer selects an evidence-supported candidate
		- **Then**: A resolved revision is appended and the uncertainty block is removed
	- **AC-002: Enter correction**
		- **Given**: No candidate is correct
		- **When**: The reviewer enters a correction
		- **Then**: Originals remain and the new revision is labeled user-edited
	- **AC-003: Leave unresolved**
		- **Given**: Evidence is insufficient
		- **When**: The reviewer leaves the value unresolved
		- **Then**: Confirmation and drafting remain blocked for that deficiency
- **Edge Cases**:
	- Concurrent resolution against a stale revision is rejected without losing either original candidate.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / compatible | TR-003 |

---

## Task Overview

Implement append-only uncertainty resolution with supported selection, user correction, explicit unresolved state, and optimistic revision checks. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_021: Evidence-linked review data must be available.
- `task_001_resolve-uncertain-candidates-frontend.md`: Uses the resolution contract.

---

## Impacted Components

- `backend/src/cms_planner/domain/review.py` (CREATE)
- `backend/src/cms_planner/application/resolution_service.py` (CREATE)
- `backend/src/cms_planner/api/resolutions.py` (CREATE)

---

## Implementation Plan

1. Model selection, correction, and unresolved commands with expected revision identifiers.
2. Append a resolved revision for supported selections or user-edited corrections while preserving originals.
3. Keep unresolved deficiencies blocked and reject stale revisions with current-state conflict details.

---

## Current Project State

- Greenfield repository; no resolution command path exists.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `backend/src/cms_planner/domain/review.py` | Model selection, correction, unresolved commands, and outcomes. |
| CREATE | `backend/src/cms_planner/application/resolution_service.py` | Append immutable resolutions and enforce revision checks and blocks. |
| CREATE | `backend/src/cms_planner/api/resolutions.py` | Expose resolution operations and recoverable conflict details. |

---

## External References

- [FastAPI 0.141.1 body models](https://fastapi.tiangolo.com/tutorial/body/)
- [Pydantic 2 validators](https://docs.pydantic.dev/latest/concepts/validators/)

---

## Build Commands

- Use the backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical backend lint, type, and startup checks.
- [x] Verify integration tests cover selection, correction, unresolved blocking, immutable originals, and stale revision rejection.

---

## Implementation Checklist

- [x] Define typed resolution commands and outcomes. (AC-001, AC-002, AC-003)
- [x] Append selection and correction revisions without mutating originals. (AC-001, AC-002)
- [x] Enforce unresolved confirmation and drafting blocks. (AC-003)
- [x] Reject stale revisions with recoverable conflict details. (AC-001, AC-002)
