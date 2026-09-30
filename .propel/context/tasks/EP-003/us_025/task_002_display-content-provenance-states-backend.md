# Task - TASK_002

## Requirement Reference

- **User Story**: US_025 - Display content provenance states
- **Story Location**: .propel/context/tasks/EP-003/us_025/us_025.md
- **Acceptance Criteria**:
	- **AC-001: Closed provenance labels**
		- **Given**: A value or draft section is displayed
		- **When**: Its current revision loads
		- **Then**: It shows exactly one origin from Extracted, AI-generated, User-edited, or Approved and displays its revision
	- **AC-002: Stale approval**
		- **Given**: Approved content receives an edit
		- **When**: The new revision is displayed
		- **Then**: It shows User-edited and Reapproval required rather than Approved
- **Edge Cases**:
	- Historical approval remains in revision history but never labels the edited current revision.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / compatible | TR-003 |

---

## Task Overview

Define closed provenance and approval-state projections for current and historical revisions, invalidating current approval when approved content is edited. Estimated effort: 6 hours.

---

## Dependent Tasks

- US_007: Immutable origin and revision data must be available.
- `task_001_display-content-provenance-states-frontend.md`: Consumes provenance projections.

---

## Impacted Components

- `backend/src/cms_planner/domain/provenance.py` (CREATE)
- `backend/src/cms_planner/application/provenance_service.py` (CREATE)
- `backend/src/cms_planner/api/provenance.py` (CREATE)

---

## Implementation Plan

1. Define the closed origin enum and current/historical revision projections.
2. Derive Reapproval required when an approved revision is followed by an edit.
3. Expose provenance without transferring historical approval to the current revision.

---

## Current Project State

- Greenfield repository; provenance projections and API do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `backend/src/cms_planner/domain/provenance.py` | Define the closed origin enum and revision projections. |
| CREATE | `backend/src/cms_planner/application/provenance_service.py` | Derive current, historical, and reapproval states. |
| CREATE | `backend/src/cms_planner/api/provenance.py` | Expose provenance without historical approval leakage. |

---

## External References

- [Python 3.14 enum](https://docs.python.org/3.14/library/enum.html)
- [Pydantic 2 enums](https://docs.pydantic.dev/latest/api/standard_library_types/#enums)

---

## Build Commands

- Use the backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical backend lint, type, and startup checks.
- [x] Verify integration tests cover the four origins, exactly-one-origin validation, approval invalidation, and retained approval history.

---

## Implementation Checklist

- [x] Define closed provenance and revision models. (AC-001)
- [x] Derive current reapproval state after an approved-content edit. (AC-002)
- [x] Expose current and historical provenance without label leakage. (AC-001, AC-002)
