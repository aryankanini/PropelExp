# Task - TASK_002

## Requirement Reference

- **User Story**: US_024 - Confirm complete reviewed deficiencies
- **Story Location**: .propel/context/tasks/EP-003/us_024/us_024.md
- **Acceptance Criteria**:
	- **AC-001: Confirm complete deficiency**
		- **Given**: The F-tag, complete SOD, and supporting evidence are resolved
		- **When**: The reviewer confirms the deficiency
		- **Then**: The current revision is confirmed and POC generation becomes available
	- **AC-002: Deny incomplete deficiency**
		- **Given**: Any required value or evidence is unresolved
		- **When**: Confirmation is requested
		- **Then**: Confirmation is denied and every blocking field is identified
- **Edge Cases**:
	- A confirmation based on a stale revision is denied until the reviewer reloads the current values.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / compatible | TR-003 |

---

## Task Overview

Implement atomic confirmation validation for resolved F-tag, complete SOD, supporting evidence, and current revision eligibility. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_022: Uncertainty resolution must be available.
- `task_001_confirm-complete-reviewed-deficiencies-frontend.md`: Uses confirmation outcomes.

---

## Impacted Components

- `backend/src/cms_planner/domain/confirmation.py` (CREATE)
- `backend/src/cms_planner/application/confirmation_service.py` (CREATE)
- `backend/src/cms_planner/api/confirmations.py` (CREATE)

---

## Implementation Plan

1. Evaluate all required fields and evidence, returning a complete blocker list.
2. Confirm only the current revision and mark it eligible for POC generation atomically.
3. Reject stale expected revisions with reload-required conflict details.

---

## Current Project State

- Greenfield repository; confirmation policy and endpoint do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `backend/src/cms_planner/domain/confirmation.py` | Define readiness, blocker, and confirmation outcome models. |
| CREATE | `backend/src/cms_planner/application/confirmation_service.py` | Validate and atomically confirm eligible current revisions. |
| CREATE | `backend/src/cms_planner/api/confirmations.py` | Expose confirmation outcomes, blockers, and stale conflicts. |

---

## External References

- [FastAPI error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Pydantic 2 models](https://docs.pydantic.dev/latest/concepts/models/)

---

## Build Commands

- Use the backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical backend lint, type, and startup checks.
- [x] Verify integration tests cover complete confirmation, exhaustive blockers, generation eligibility, and stale revision denial.

---

## Implementation Checklist

- [x] Define confirmation readiness and blocker models. (AC-001, AC-002)
- [x] Implement atomic current-revision confirmation. (AC-001)
- [x] Return every blocker for incomplete deficiencies. (AC-002)
- [x] Reject stale confirmation requests. (AC-001, AC-002)
