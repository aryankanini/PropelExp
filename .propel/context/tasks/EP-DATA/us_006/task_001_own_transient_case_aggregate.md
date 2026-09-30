# Task - TASK_001

## Requirement Reference
- **User Story:** US_006
- **Story Location:** .propel/context/tasks/EP-DATA/us_006/us_006.md
- **Parent Epic:** EP-DATA
- **Acceptance Criteria:**
  - AC-001: One backend repository port stores all case state changes in one session-scoped aggregate as the sole writer.
- **Edge Cases:**
  - A second active case write for the same session is rejected without replacing the current aggregate.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend Data | Python | 3.14.7 | TR-007 places transient aggregate ownership in the backend. |
| Backend Data | In-memory repository | None | DR-001 prohibits a durable case database. |
| Backend Data | Pydantic | 2.x | Typed aggregate state preserves case invariants. |

---

## Task Overview
Create the sole-writer, session-scoped transient case aggregate for US_006 under EP-DATA. Estimated effort: 8 hours.

## Dependent Tasks
- US_001 must provide the backend application and domain boundaries.

## Impacted Components
- New case aggregate, repository port, in-memory adapter, ownership errors, and tests.

## Implementation Plan
- Model document, job, provider, deficiency, POC, approval, and provenance state in one aggregate.
- Define an application-facing repository port as the sole mutation boundary.
- Implement a process-memory adapter keyed by authenticated session.
- Reject a second active case without replacing the current aggregate.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_006 depends on the planned US_001 backend boundaries; no database is approved, only an in-memory repository and temporary workspace.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/domain/case/aggregate.py | Model the complete session-scoped case aggregate. |
| CREATE | backend/src/domain/case/errors.py | Define active-case ownership errors. |
| CREATE | backend/src/application/ports/case_repository.py | Define the sole-writer repository contract. |
| CREATE | backend/src/adapters/repositories/in_memory_case_repository.py | Store one active aggregate per session in process memory. |
| CREATE | backend/tests/unit/domain/test_case_aggregate.py | Verify aggregate state transitions. |
| CREATE | backend/tests/integration/repositories/test_case_ownership.py | Verify session ownership and second-case rejection. |

## External References
- [Python 3.14 data classes](https://docs.python.org/3.14/library/dataclasses.html)
- [Pydantic 2 models](https://docs.pydantic.dev/2.12/concepts/models/)

## Build Commands
- [Backend data build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit-test structure covers every aggregate state category and sole-writer invariant.
- [x] Integration-test structure verifies session isolation and rejects a second active case without replacement.

## Implementation Checklist
- [x] Model all listed case state in one aggregate for AC-001.
- [x] Define the repository port as the sole writer for AC-001.
- [x] Store aggregates only in process memory and scope them by session for AC-001.
- [x] Reject a second active case without replacing current state for AC-001.
