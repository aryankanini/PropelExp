# Task - TASK_002

## Requirement Reference

- **User Story**: US_030 - Save edited POC revisions
- **Story Location**: .propel/context/tasks/EP-004/us_030/us_030.md
- **Acceptance Criteria**:
	- **AC-001: Save edit**
		- **Given**: A current POC draft exists
		- **When**: The reviewer edits one or more sections and saves
		- **Then**: A user-edited unapproved revision is appended and each changed section shows its origin
	- **AC-002: Save failure**
		- **Given**: An edit cannot be retained
		- **When**: Save fails
		- **Then**: The last retained revision remains current and the user receives a safe retry action
- **Edge Cases**:
	- A stale revision conflict does not overwrite the newer draft.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / compatible | TR-003 |

---

## Task Overview

Implement atomic append-only POC saves with section-level origin tracking, unapproved status, optimistic concurrency, and failure preservation. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_027: The five stable POC sections must be available.
- `task_001_save-edited-poc-revisions-frontend.md`: Uses save and conflict outcomes.

---

## Impacted Components

- `backend/src/cms_planner/domain/poc.py` (CREATE)
- `backend/src/cms_planner/application/poc_revision_service.py` (CREATE)
- `backend/src/cms_planner/api/poc.py` (CREATE)

---

## Implementation Plan

1. Validate edits against the five-section model and expected current revision.
2. Atomically append one unapproved User-edited revision with changed-section origins.
3. On retention failure or stale conflict, leave the last retained revision current and return safe retry or reload details.

---

## Current Project State

- Greenfield repository; POC revision save commands do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `backend/src/cms_planner/domain/poc.py` | Define POC edit, revision, origin, and save-outcome models. |
| CREATE | `backend/src/cms_planner/application/poc_revision_service.py` | Atomically append unapproved revisions and preserve retained state on failure. |
| CREATE | `backend/src/cms_planner/api/poc.py` | Expose save, retry, and stale-conflict outcomes. |

---

## External References

- [FastAPI handling errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Pydantic 2 models](https://docs.pydantic.dev/latest/concepts/models/)

---

## Build Commands

- Use the backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical backend lint, type, and startup checks.
- [ ] Verify integration tests cover single and multi-section edits, origins, unapproved status, retention failure, safe retry, and stale conflict preservation.

---

## Implementation Checklist

- [ ] Define POC edit and save-outcome models. (AC-001, AC-002)
- [ ] Append unapproved User-edited revisions atomically. (AC-001)
- [ ] Track origin for every changed section. (AC-001)
- [ ] Preserve the last retained revision on failure or stale conflict. (AC-002)