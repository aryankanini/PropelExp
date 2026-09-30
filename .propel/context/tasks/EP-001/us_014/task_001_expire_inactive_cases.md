# Task - TASK_001

## Requirement Reference
- **User Story:** US_014
- **Story Location:** .propel/context/tasks/EP-001/us_014/us_014.md
- **Acceptance Criteria:**
  - AC-001: After 60 minutes without activity, metadata and files are removed with zero residue.
  - AC-002: Graceful shutdown runs the same verified cleanup for every active transient case.
- **Edge Cases:**
  - Activity at the deadline is ordered deterministically against cleanup.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | NFR-006 requires deterministic inactivity cleanup. |

---

## Task Overview
Implement inactivity tracking and idempotent expiration of active cases. Estimated effort: 8 hours.

## Dependent Tasks
- US_009 - Requires idempotent lifecycle cleanup.

## Impacted Components
- New inactivity policy and expiration service.

## Implementation Plan
- Track authenticated activity against a monotonic deadline.
- Serialize deadline activity and cleanup, then verify zero files remain.

## Current Project State
- No lifecycle source exists; design.md defines the 60-minute policy.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/application/inactivity_policy.py | Determine expiration from server activity. |
| CREATE | backend/src/cms_planner/application/expire_case.py | Coordinate idempotent case cleanup. |

## External References
- https://docs.python.org/3.14/library/asyncio-sync.html

## Build Commands
- `cd backend; python -m pytest tests/unit/application/test_expire_case.py`

## Implementation Validation Strategy
- [x] Clock-controlled tests verify expiration and deadline ordering.

## Implementation Checklist
- [x] Expire cases after exactly 60 inactive minutes for AC-001.
- [x] Remove metadata and temporary files idempotently for AC-001.
- [x] Verify zero remaining case files after cleanup for AC-001.
- [x] Order deadline activity and cleanup deterministically for AC-001.
- [x] Expose the same idempotent verified cleanup operation for graceful shutdown invocation in AC-002.
