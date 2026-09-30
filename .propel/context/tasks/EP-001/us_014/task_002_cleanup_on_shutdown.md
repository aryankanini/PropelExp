# Task - TASK_002

## Requirement Reference
- **User Story:** US_014
- **Story Location:** .propel/context/tasks/EP-001/us_014/us_014.md
- **Acceptance Criteria:**
  - AC-001: After 60 minutes without activity, metadata and files are removed with zero residue.
  - AC-002: Graceful backend shutdown runs verified cleanup for every active case.
- **Edge Cases:**
  - Deadline activity and cleanup cannot race with a retained write.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | FastAPI | 0.141.1 | NFR-006 requires cleanup in the backend lifecycle. |

---

## Task Overview
Run verified idempotent case cleanup during graceful FastAPI shutdown. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires the expiration cleanup service.

## Impacted Components
- New shutdown lifecycle coordinator.

## Implementation Plan
- Snapshot active case identifiers during graceful shutdown.
- Clean each aggregate and workspace and report residue without content.

## Current Project State
- No shutdown cleanup lifecycle exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/infrastructure/state/shutdown_cleanup.py | Clean all active cases during shutdown. |

## External References
- https://fastapi.tiangolo.com/advanced/events/

## Build Commands
- `cd backend; python -m pytest tests/integration/test_shutdown_cleanup.py`

## Implementation Validation Strategy
- [x] Graceful shutdown tests verify every active case and workspace is removed.

## Implementation Checklist
- [x] Invoke the shared cleanup contract that preserves the 60-minute expiration and zero-file verification invariant for AC-001.
- [x] Enumerate all active cases at graceful shutdown for AC-002.
- [x] Run the same idempotent cleanup for every case for AC-002.
- [x] Verify and report zero remaining case files for AC-002.
