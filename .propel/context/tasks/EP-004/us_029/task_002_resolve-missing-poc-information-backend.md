# Task - TASK_002

## Requirement Reference

- **User Story**: US_029 - Resolve missing POC information
- **Story Location**: .propel/context/tasks/EP-004/us_029/us_029.md
- **Acceptance Criteria**:
	- **AC-001: Display guarded draft**
		- **Given**: A grounded draft contains typed missing-information markers
		- **When**: The draft is displayed
		- **Then**: Each marker names the needed fact and keeps approval readiness blocked
	- **AC-002: Supply missing fact**
		- **Given**: A reviewer enters a supported missing fact
		- **When**: The draft is saved
		- **Then**: A user-edited revision replaces the marker and preserves its revision history
- **Edge Cases**:
	- Removing a required value restores the missing marker and incomplete state.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / compatible | TR-003 |

---

## Task Overview

Implement marker-resolution commands that append User-edited revisions, preserve history, and derive approval readiness from remaining required markers. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_028: Typed grounding results must be available.
- `task_001_resolve-missing-poc-information-frontend.md`: Uses marker-resolution outcomes.

---

## Impacted Components

- `backend/src/cms_planner/domain/poc.py` (CREATE)
- `backend/src/cms_planner/application/missing_information_service.py` (CREATE)
- `backend/src/cms_planner/api/poc.py` (CREATE)

---

## Implementation Plan

1. Validate supported replacement facts against the marker type and current revision.
2. Append a User-edited revision that replaces the marker while preserving history.
3. Re-derive markers and incomplete readiness when required content is removed.

---

## Current Project State

- Greenfield repository; marker-resolution commands do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `backend/src/cms_planner/domain/poc.py` | Define marker-resolution commands and outcomes. |
| CREATE | `backend/src/cms_planner/application/missing_information_service.py` | Append replacements and derive markers and readiness. |
| CREATE | `backend/src/cms_planner/api/poc.py` | Expose marker-resolution and restoration outcomes. |

---

## External References

- [Pydantic 2 validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [FastAPI error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)

---

## Build Commands

- Use the backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical backend lint, type, and startup checks.
- [ ] Verify integration tests cover supported replacement, preserved history, readiness blocking, removal, and marker restoration.

---

## Implementation Checklist

- [ ] Define marker-resolution command and response models. (AC-001, AC-002)
- [ ] Append User-edited replacement revisions with history intact. (AC-002)
- [ ] Derive readiness from all required markers. (AC-001)
- [ ] Restore typed markers after required-value removal. (AC-001, AC-002)
