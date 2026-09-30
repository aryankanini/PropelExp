# Task - TASK_001 Authorize Current Revision Export

## Requirement Reference

- **User Story:** US_034
- **Story Location:** .propel/context/tasks/EP-005/us_034/us_034.md
- **Acceptance Criteria:**
  - **AC-001: Current approval**
    - **Given**: Approval matches the current POC revision
    - **When**: Copy or download is requested
    - **Then**: The approved current content is returned in the requested format
  - **AC-002: Missing or stale approval**
    - **Given**: Approval is absent, revoked, or belongs to another revision
    - **When**: Export is requested
    - **Then**: Export is blocked with an approval-required reason
  - **AC-003: Formatting failure**
    - **Given**: Download formatting fails
    - **When**: The failure is returned
    - **Then**: Approval remains unchanged and retry or copy is offered
- **Edge Cases:**
  - Export authorization is rechecked server-side even when the UI action appears enabled.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / FastAPI-compatible | FR-017 and UC-008 require server-authoritative export authorization and safe formatting failures. |

---

## Task Overview

Implement the EP-005 / US_034 backend export service that rechecks current-revision approval for every request, returns approved content in the requested format, and preserves approval on formatting failure. Estimated effort: 8 hours.

## Dependent Tasks

- US_032 - Same-Epic - Requires current-revision approval.
- US_032 TASK_001 Implement Current Revision Approval - provides authoritative approval state.

## Impacted Components

- New export authorization policy, application service, contracts, and route.
- New isolated formatter boundary that cannot mutate approval state.

## Implementation Plan

1. Define copy/download formats and approval-required responses.
2. Recheck approval against the current revision inside every export operation.
3. Isolate formatting from approval state and return retry/copy recovery metadata.
4. Expose the authorized export endpoint with validated contracts.

## Current Project State

```text
backend/src/cms_planner/
├── api/                            # Planned; backend implementation directory is not yet present
├── domain/
├── application/
└── modules/export/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/domain/export_policy.py | Define current-revision export authorization rules. |
| CREATE | backend/src/cms_planner/application/export_approved_revision.py | Recheck approval and orchestrate copy/download formatting. |
| CREATE | backend/src/cms_planner/modules/export/schemas.py | Define export request, content, and failure contracts. |
| CREATE | backend/src/cms_planner/api/export.py | Expose the authorized current-revision export endpoint. |

## External References

- [Python 3.14 documentation](https://docs.python.org/3.14/)
- [FastAPI 0.141.1 documentation](https://fastapi.tiangolo.com/release-notes/#01411)
- [Pydantic 2 documentation](https://docs.pydantic.dev/2.12/)

## Build Commands

- [Backend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [x] Unit tests pass for current, absent, revoked, stale, and formatting-failure export decisions.
- [x] Integration tests pass for server-side authorization and copy/download responses.

## Implementation Checklist

- [x] Return approved current content in the requested copy or download format. (AC-001)
- [x] Recheck approval server-side and block absent, revoked, or stale approval with an approval-required reason. (AC-002)
- [x] Preserve approval when download formatting fails and return retry or copy recovery. (AC-003)
