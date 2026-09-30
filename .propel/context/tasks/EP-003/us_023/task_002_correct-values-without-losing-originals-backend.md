# Task - TASK_002

## Requirement Reference

- **User Story**: US_023 - Correct values without losing originals
- **Story Location**: .propel/context/tasks/EP-003/us_023/us_023.md
- **Acceptance Criteria**:
	- **AC-001: Correct current value**
		- **Given**: An extracted provider, F-tag, or SOD value is inaccurate
		- **When**: The reviewer saves a correction
		- **Then**: A user-edited revision becomes current and the original value, evidence, and origin remain visible
- **Edge Cases**:
	- An empty correction is rejected without incrementing the revision number.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / compatible | TR-003 |

---

## Task Overview

Implement correction commands that append a User-edited current revision while preserving original values, evidence, origin, and revision sequence. Estimated effort: 6 hours.

---

## Dependent Tasks

- US_007: Immutable revision support must be available.
- `task_001_correct-values-without-losing-originals-frontend.md`: Uses the correction contract.

---

## Impacted Components

- `backend/src/cms_planner/domain/revisions.py` (CREATE)
- `backend/src/cms_planner/application/correction_service.py` (CREATE)
- `backend/src/cms_planner/api/corrections.py` (CREATE)

---

## Implementation Plan

1. Validate non-empty provider, F-tag, and SOD corrections.
2. Append User-edited revisions and retain immutable original evidence and origin links.
3. Return current and historical revision data without incrementing on rejected input.

---

## Current Project State

- Greenfield repository; correction APIs do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `backend/src/cms_planner/domain/revisions.py` | Define correction commands and current and historical revision responses. |
| CREATE | `backend/src/cms_planner/application/correction_service.py` | Append user-edited revisions while preserving originals and sequence integrity. |
| CREATE | `backend/src/cms_planner/api/corrections.py` | Expose correction operations and validation failures. |

---

## External References

- [FastAPI validation](https://fastapi.tiangolo.com/tutorial/body/)
- [Pydantic 2 fields](https://docs.pydantic.dev/latest/concepts/fields/)

---

## Build Commands

- Use the backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical backend lint, type, and startup checks.
- [x] Verify integration tests cover append-only correction, preserved originals, and no revision increment for empty input.

---

## Implementation Checklist

- [x] Define correction and revision response models. (AC-001)
- [x] Append User-edited revisions while retaining originals. (AC-001)
- [x] Reject empty corrections before allocating a revision. (AC-001)
