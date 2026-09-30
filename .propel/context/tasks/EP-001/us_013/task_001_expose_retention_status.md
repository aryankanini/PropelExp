# Task - TASK_001

## Requirement Reference
- **User Story:** US_013
- **Story Location:** .propel/context/tasks/EP-001/us_013/us_013.md
- **Acceptance Criteria:**
  - AC-001: Session status identifies session-only storage and the remaining inactivity period.
- **Edge Cases:**
  - Reconnect refreshes the server-owned period rather than extending stale browser time.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | FastAPI | 0.141.1 | FR-020 requires server-owned transient retention status. |

---

## Task Overview
Expose authoritative session retention and inactivity deadline data. Estimated effort: 8 hours.

## Dependent Tasks
- US_006 - Requires active session state.

## Impacted Components
- New session status query and API projection.

## Implementation Plan
- Calculate remaining inactivity time from server-owned activity timestamps.
- Return session-only semantics without durable-retention claims.

## Current Project State
- No session status API source exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/application/session_status.py | Calculate authoritative retention state. |
| CREATE | backend/src/cms_planner/api/routes/session_status.py | Expose current session status. |

## External References
- https://docs.python.org/3.14/library/datetime.html

## Build Commands
- `cd backend; python -m pytest tests/unit/application/test_session_status.py`

## Implementation Validation Strategy
- [x] Server time controls remaining duration across reconnects.

## Implementation Checklist
- [x] Identify storage as session-only for AC-001.
- [x] Return the server-owned remaining inactivity period for AC-001.
- [x] Refresh status without extending the deadline on reconnect for AC-001.
