# Task - TASK_001 Invalidate Approval on Revision

## Requirement Reference

- **User Story:** US_033
- **Story Location:** .propel/context/tasks/EP-005/us_033/us_033.md
- **Acceptance Criteria:**
  - **AC-001: Request changes**
    - **Given**: A leader reviews a POC
    - **When**: The leader requests changes
    - **Then**: The POC remains unapproved and returns to editing with export disabled
  - **AC-002: Edit approved content**
    - **Given**: A POC revision is approved
    - **When**: Any section is changed and saved
    - **Then**: Approval is revoked immediately and the current revision shows Reapproval required
- **Edge Cases:**
  - An edit that fails to save does not revoke approval for the unchanged current revision.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / FastAPI-compatible | FR-018 requires atomic approval invalidation only after a new revision is saved. |

---

## Task Overview

Implement the EP-005 / US_033 backend transition that keeps requested changes unapproved and revokes approval atomically when an approved POC section is successfully saved as a new revision. Estimated effort: 8 hours.

## Dependent Tasks

- US_032 - Same-Epic - Requires revision-bound approval.
- US_032 TASK_001 Implement Current Revision Approval - provides the approval state model.

## Impacted Components

- New revision invalidation policy and request-changes application service.
- New Pydantic reapproval-state contracts and FastAPI transition route.

## Implementation Plan

1. Define reapproval-required state and invalidation policy.
2. Couple invalidation to successful revision save as one application operation.
3. Keep unchanged approval when persistence of the new in-memory revision fails.
4. Expose request-changes and revision-state responses.

## Current Project State

```text
backend/src/cms_planner/
├── api/                            # Planned; backend implementation directory is not yet present
├── domain/
├── application/
└── modules/approval/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/domain/reapproval.py | Define approval invalidation and reapproval-required policy. |
| CREATE | backend/src/cms_planner/application/invalidate_approval.py | Apply invalidation only after a successful new revision save. |
| CREATE | backend/src/cms_planner/modules/approval/reapproval_schemas.py | Define request-changes and reapproval response contracts. |
| CREATE | backend/src/cms_planner/api/reapproval.py | Expose request-changes and reapproval-state transitions. |

## External References

- [Python 3.14 documentation](https://docs.python.org/3.14/)
- [FastAPI 0.141.1 documentation](https://fastapi.tiangolo.com/release-notes/#01411)
- [Pydantic 2 documentation](https://docs.pydantic.dev/2.12/)

## Build Commands

- [Backend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [x] Unit tests pass for request changes, successful save invalidation, and failed-save preservation.
- [x] Integration tests pass for reapproval state and export-disabled responses.

## Implementation Checklist

- [x] Keep request-changes transitions unapproved and return the POC to editing with export disabled. (AC-001)
- [x] Revoke approval immediately after any section is changed and successfully saved. (AC-002)
- [x] Preserve approval when the attempted edit fails to save and the revision remains unchanged. (AC-002)
