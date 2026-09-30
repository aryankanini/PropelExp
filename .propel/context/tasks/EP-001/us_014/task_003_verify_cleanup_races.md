# Task - TASK_003

## Requirement Reference
- **User Story:** US_014
- **Story Location:** .propel/context/tasks/EP-001/us_014/us_014.md
- **Acceptance Criteria:**
  - AC-001: Inactivity cleanup removes metadata and files with zero residue.
  - AC-002: Shutdown cleanup covers every active case.
- **Edge Cases:**
  - Activity exactly at the deadline cannot race with a retained write.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Testing | pytest | 9.x | NFR-006 requires executable lifecycle and race verification. |

---

## Task Overview
Implement lifecycle tests for inactivity, shutdown, idempotency, and deadline races. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001, TASK_002 - Requires both cleanup triggers.

## Impacted Components
- New lifecycle integration and concurrency tests.

## Implementation Plan
- Use controlled clocks and synchronization barriers around deadline activity.
- Assert memory and workspace residue after repeated and shutdown cleanup.

## Current Project State
- Cleanup services are planned without cross-trigger verification.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/tests/integration/test_case_cleanup_lifecycle.py | Verify inactivity and shutdown cleanup behavior. |

## External References
- https://docs.pytest.org/

## Build Commands
- `cd backend; python -m pytest tests/integration/test_case_cleanup_lifecycle.py`

## Implementation Validation Strategy
- [x] Controlled tests cover all triggers, retries, and exact-deadline ordering.

## Implementation Checklist
- [x] Verify 60-minute cleanup and zero residue for AC-001.
- [x] Verify every active case is cleaned at shutdown for AC-002.
- [x] Verify repeated cleanup remains idempotent for AC-001 and AC-002.
- [x] Verify exact-deadline activity cannot race with retained writes for AC-001.
