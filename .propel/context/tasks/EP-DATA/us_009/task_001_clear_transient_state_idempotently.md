# Task - TASK_001

## Requirement Reference
- **User Story:** US_009
- **Story Location:** .propel/context/tasks/EP-DATA/us_009/us_009.md
- **Parent Epic:** EP-DATA
- **Acceptance Criteria:**
  - AC-001: Repeated cleanup leaves the aggregate and workspace absent and reports completed with zero remaining files.
  - AC-002: Failure to clear either store reports failed without document content in status.
- **Edge Cases:**
  - Repeating cleanup after partial deletion converges on the same completed state.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend Lifecycle | Python | 3.14.7 | DR-004 coordinates transient memory and filesystem cleanup. |
| Backend Lifecycle | In-memory repository and temporary workspace | None | Both transient stores must converge on absence. |
| Backend Lifecycle | Pydantic | 2.x | Typed status responses prevent content leakage. |

---

## Task Overview
Implement truthful, idempotent cleanup across transient case memory and files for US_009 under EP-DATA. Estimated effort: 8 hours.

## Dependent Tasks
- US_006 must provide aggregate ownership and removal.
- US_008 must provide workspace ownership and removal.

## Impacted Components
- New cleanup coordinator, content-free status model, cleanup errors, and convergence tests.

## Implementation Plan
- Coordinate aggregate and workspace deletion without treating absence as failure.
- Count remaining files only after both deletion attempts complete.
- Return completed only when both stores are absent and zero files remain.
- Return a content-free failed status when either store cannot be cleared.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_009 depends on the planned US_006 in-memory aggregate and US_008 temporary workspace.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/domain/lifecycle/cleanup_status.py | Model completed or failed status without document content. |
| CREATE | backend/src/application/services/cleanup_case.py | Coordinate idempotent memory and workspace removal. |
| CREATE | backend/src/application/services/cleanup_errors.py | Represent store-specific cleanup failures safely. |
| CREATE | backend/tests/unit/lifecycle/test_cleanup_status.py | Verify truthful content-free status values. |
| CREATE | backend/tests/integration/test_case_cleanup.py | Verify repeat, partial-deletion, and failure convergence. |

## External References
- [Python 3.14 shutil documentation](https://docs.python.org/3.14/library/shutil.html)
- [Pydantic 2 serialization](https://docs.pydantic.dev/2.12/concepts/serialization/)

## Build Commands
- [Backend lifecycle build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit-test structure validates completed and failed statuses without document content.
- [x] Integration-test structure repeats cleanup after complete and partial deletion and verifies convergence to zero residue.

## Implementation Checklist
- [x] Remove aggregate and workspace together and report zero remaining files for AC-001.
- [x] Make repeated cleanup converge on the same completed state for AC-001.
- [x] Report failed when either transient store cannot be cleared for AC-002.
- [x] Exclude document content from every cleanup status for AC-002.
