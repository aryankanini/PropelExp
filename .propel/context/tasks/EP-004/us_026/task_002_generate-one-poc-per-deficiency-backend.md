# Task - TASK_002

## Requirement Reference

- **User Story**: US_026 - Generate one POC per deficiency
- **Story Location**: .propel/context/tasks/EP-004/us_026/us_026.md
- **Acceptance Criteria**:
	- **AC-001: Scoped generation**
		- **Given**: A deficiency has a confirmed current revision
		- **When**: The reviewer requests a POC
		- **Then**: Only that deficiency's reviewed fields and evidence are sent for generation and one unapproved draft is returned
	- **AC-002: Unconfirmed request**
		- **Given**: A deficiency is unconfirmed
		- **When**: Generation is requested
		- **Then**: The request is denied without invoking the provider
- **Edge Cases**:
	- Concurrent requests for the same revision produce at most one current draft revision.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / compatible | TR-003 |

---

## Task Overview

Implement deficiency-scoped POC generation orchestration that verifies confirmation before provider invocation and idempotently retains one unapproved current draft per confirmed revision. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_024: Confirmed current deficiency revisions must be available.
- `task_001_generate-one-poc-per-deficiency-frontend.md`: Uses the generation endpoint.

---

## Impacted Components

- `backend/src/cms_planner/domain/poc.py` (CREATE)
- `backend/src/cms_planner/application/poc_generation_service.py` (CREATE)
- `backend/src/cms_planner/api/poc.py` (CREATE)

---

## Implementation Plan

1. Build generation input solely from the requested deficiency's confirmed current fields and evidence.
2. Deny unconfirmed requests before calling the provider.
3. Use the deficiency revision as an idempotency boundary and append at most one current unapproved draft.

---

## Current Project State

- Greenfield repository; POC domain and generation endpoint do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `backend/src/cms_planner/domain/poc.py` | Define deficiency-scoped generation and draft models. |
| CREATE | `backend/src/cms_planner/application/poc_generation_service.py` | Enforce confirmation, input scope, and idempotent draft creation. |
| CREATE | `backend/src/cms_planner/api/poc.py` | Expose generation and typed denial outcomes. |

---

## External References

- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Python 3.14 asyncio synchronization](https://docs.python.org/3.14/library/asyncio-sync.html)

---

## Build Commands

- Use the backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical backend lint, type, and startup checks.
- [ ] Verify integration tests cover input scoping, no-call denial, unapproved status, and concurrent idempotency.

---

## Implementation Checklist

- [ ] Define deficiency-scoped generation models. (AC-001)
- [ ] Enforce confirmation before provider invocation. (AC-002)
- [ ] Build input from only the requested reviewed fields and evidence. (AC-001)
- [ ] Make current-draft creation idempotent per confirmed revision. (AC-001)
