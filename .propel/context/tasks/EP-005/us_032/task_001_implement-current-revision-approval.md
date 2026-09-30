# Task - TASK_001 Implement Current Revision Approval

## Requirement Reference

- **User Story:** US_032
- **Story Location:** .propel/context/tasks/EP-005/us_032/us_032.md
- **Acceptance Criteria:**
  - **AC-001: Approve complete revision**
    - **Given**: The leader sees evidence, provenance, completeness, five sections, and the current revision
    - **When**: The leader approves
    - **Then**: Approval is bound to that revision and copy and download become available
  - **AC-002: Stale or incomplete package**
    - **Given**: The package is incomplete or its revision changed
    - **When**: Approval is requested
    - **Then**: Approval is denied without changing state and exact blockers are shown
- **Edge Cases:**
  - Two leaders approving the same unchanged revision produce one current approval state.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / FastAPI-compatible | FR-016 and UC-007 require server-authoritative, revision-bound approval with validated API contracts. |

---

## Task Overview

Implement the EP-005 / US_032 backend approval capability that validates package completeness and revision currency, records one approval for the exact reviewed revision, and returns exact blockers without mutating state. Estimated effort: 8 hours.

## Dependent Tasks

- None; US_032 declares no story dependency, and this is the first task in the story sequence.

## Impacted Components

- New approval domain model for revision-bound approval state and idempotent approval decisions.
- New approval application service for completeness, currency, and blocker evaluation.
- New FastAPI approval route and Pydantic request/response contracts.

## Implementation Plan

1. Define immutable approval and blocker models keyed to the current POC revision.
2. Implement approval evaluation that rejects stale or incomplete packages before state mutation.
3. Make repeated approvals of the same unchanged revision idempotent.
4. Expose a validated FastAPI endpoint returning approval state or exact blockers.

## Current Project State

```text
backend/
└── src/
    └── cms_planner/                 # Planned; backend implementation directory is not yet present
        ├── api/
        ├── domain/
        ├── application/
        └── modules/
            └── approval/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/domain/approval.py | Define revision-bound approval state and blocker models. |
| CREATE | backend/src/cms_planner/application/approve_revision.py | Validate completeness and revision currency, then produce an idempotent approval decision. |
| CREATE | backend/src/cms_planner/modules/approval/schemas.py | Define Pydantic approval request, success, and blocker contracts. |
| CREATE | backend/src/cms_planner/api/approval.py | Expose the current-revision approval endpoint. |

## External References

- [Python 3.14 documentation](https://docs.python.org/3.14/)
- [FastAPI 0.141.1 documentation](https://fastapi.tiangolo.com/release-notes/#01411)
- [Pydantic 2 documentation](https://docs.pydantic.dev/2.12/)

## Build Commands

- [Backend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [x] Unit tests pass for complete, incomplete, stale, and duplicate approval decisions.
- [x] Integration tests pass for approval endpoint state transitions and blocker responses.

## Implementation Checklist

- [x] Implement revision-bound approval state and current-revision validation. (AC-001, AC-002)
- [x] Deny stale or incomplete requests without changing approval state and return exact blockers. (AC-002)
- [x] Make concurrent or repeated approval of the same unchanged revision produce one current approval state. (AC-001)
