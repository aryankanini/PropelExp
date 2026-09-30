# Task - TASK_002

## Requirement Reference

- **User Story**: US_027 - Validate five-part POC drafts
- **Story Location**: .propel/context/tasks/EP-004/us_027/us_027.md
- **Acceptance Criteria**:
	- **AC-001: Complete schema**
		- **Given**: Generated output contains affected residents, others at risk, corrective measures, monitoring, and completion date
		- **When**: Closed-schema validation runs
		- **Then**: The five sections are accepted in the fixed order with no unknown sections
	- **AC-002: Missing section**
		- **Given**: Generated output omits a required section
		- **When**: Validation runs
		- **Then**: The response is rejected as incomplete and is not stored as a completed draft
- **Edge Cases**:
	- A present but empty required section is incomplete.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / compatible | TR-003 |

---

## Task Overview

Enforce the closed five-part POC model before accepting generated output as a completed draft, rejecting missing, empty, reordered, or unknown sections. Estimated effort: 7 hours.

---

## Dependent Tasks

- US_026: Scoped generation must be available.
- `task_001_validate-five-part-poc-drafts-frontend.md`: Consumes validation results.

---

## Impacted Components

- `backend/src/cms_planner/domain/poc.py` (CREATE)
- `backend/src/cms_planner/application/poc_validation_service.py` (CREATE)
- `backend/src/cms_planner/api/poc.py` (CREATE)

---

## Implementation Plan

1. Define a strict Pydantic model with the five required non-empty sections in fixed order and forbidden extras.
2. Validate generated output before completed-draft persistence.
3. Return typed section-level rejection details for missing, empty, reordered, or unknown content.

---

## Current Project State

- Greenfield repository; POC validation domain and endpoint do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `backend/src/cms_planner/domain/poc.py` | Define the strict five-section POC model. |
| CREATE | `backend/src/cms_planner/application/poc_validation_service.py` | Validate output before completed-draft persistence. |
| CREATE | `backend/src/cms_planner/api/poc.py` | Return typed section-level validation failures. |

---

## External References

- [Pydantic 2 strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/)
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12)

---

## Build Commands

- Use the backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical backend lint, type, and startup checks.
- [ ] Verify contract and integration tests cover valid order, missing, empty, reordered, extra sections, and persistence denial.

---

## Implementation Checklist

- [ ] Define the strict five-section POC model. (AC-001, AC-002)
- [ ] Validate output before completed-draft persistence. (AC-001, AC-002)
- [ ] Return typed section-level validation failures. (AC-002)
