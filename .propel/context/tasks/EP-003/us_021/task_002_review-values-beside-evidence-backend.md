# Task - TASK_002

## Requirement Reference

- **User Story**: US_021 - Review values beside evidence
- **Story Location**: .propel/context/tasks/EP-003/us_021/us_021.md
- **Acceptance Criteria**:
	- **AC-001: Synchronized evidence**
		- **Given**: Provider and deficiency candidates exist
		- **When**: The reviewer selects a value
		- **Then**: Its page, full snippet, confidence, uncertainty, and origin appear and the supporting evidence is highlighted
- **Edge Cases**:
	- Long SOD text remains complete and searchable without truncating the authoritative value.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / compatible | TR-003 |

---

## Task Overview

Expose an evidence-review query that returns each provider or deficiency candidate with its authoritative value, page, full snippet, confidence, uncertainty, origin, and highlight coordinates. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_017: Evidence-linked candidates must be available.
- `task_001_review-values-beside-evidence-frontend.md`: Consumes the response contract.

---

## Impacted Components

- `backend/src/cms_planner/domain/review.py` (CREATE)
- `backend/src/cms_planner/application/review_service.py` (CREATE)
- `backend/src/cms_planner/api/review.py` (CREATE)

---

## Implementation Plan

1. Define typed candidate and evidence response models that retain complete authoritative values and snippets.
2. Add a review service query that preserves candidate-to-evidence linkage and deterministic ordering.
3. Expose a FastAPI endpoint with explicit not-found and unavailable-evidence responses.

---

## Current Project State

- Greenfield repository; review domain, application, and API modules do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `backend/src/cms_planner/domain/review.py` | Define synchronized candidate and evidence response models. |
| CREATE | `backend/src/cms_planner/application/review_service.py` | Query complete candidate, evidence, provenance, and highlight details. |
| CREATE | `backend/src/cms_planner/api/review.py` | Expose the evidence-review endpoint and typed failure responses. |

---

## External References

- [FastAPI 0.141.1 response models](https://fastapi.tiangolo.com/tutorial/response-model/)
- [Pydantic 2 models](https://docs.pydantic.dev/latest/concepts/models/)
- [Python 3.14 documentation](https://docs.python.org/3.14/)

---

## Build Commands

- Use the backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical backend lint, type, and application startup checks.
- [x] Verify API integration tests cover candidate linkage, complete metadata, stable ordering, highlight coordinates, and untruncated long SOD values.
- [x] Verify contract tests cover typed not-found and unavailable-evidence responses.

---

## Implementation Checklist

- [x] Define candidate and evidence response models. (AC-001)
- [x] Implement the synchronized review query service. (AC-001)
- [x] Expose the evidence-review API endpoint and typed failure responses. (AC-001)
- [x] Ensure authoritative values and snippets are never truncated. (AC-001)
