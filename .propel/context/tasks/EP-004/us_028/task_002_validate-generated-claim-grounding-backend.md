# Task - TASK_002

## Requirement Reference

- **User Story**: US_028 - Validate generated claim grounding
- **Story Location**: .propel/context/tasks/EP-004/us_028/us_028.md
- **Acceptance Criteria**:
	- **AC-001: Supported claim**
		- **Given**: A generated facility-specific claim references reviewed fields or evidence spans
		- **When**: Grounding validation runs
		- **Then**: The claim is retained with its support references
	- **AC-002: Unsupported claim**
		- **Given**: A facility-specific claim has no reviewed support
		- **When**: Grounding validation runs
		- **Then**: The claim is not presented as fact and is replaced by a typed missing-information marker
- **Edge Cases**:
	- Generic compliance guidance is not treated as facility-specific unless it asserts a case fact.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / compatible | TR-003 |

---

## Task Overview

Orchestrate grounding validation against reviewed fields and evidence spans, retaining supported claims and replacing unsupported facility facts with typed markers. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_027: A schema-valid POC draft must be available.
- `task_001_validate-generated-claim-grounding-frontend.md`: Consumes grounding results.

---

## Impacted Components

- `backend/src/cms_planner/domain/grounding.py` (CREATE)
- `backend/src/cms_planner/application/grounding_service.py` (CREATE)
- `backend/src/cms_planner/api/poc.py` (CREATE)

---

## Implementation Plan

1. Resolve claim support references only against reviewed fields and evidence spans for the deficiency.
2. Persist supported references and typed markers in the guarded draft projection.
3. Separate generic guidance from facility assertions unless it states a case fact.

---

## Current Project State

- Greenfield repository; grounding domain and orchestration do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `backend/src/cms_planner/domain/grounding.py` | Define supported claims, references, and typed missing markers. |
| CREATE | `backend/src/cms_planner/application/grounding_service.py` | Validate support against reviewed deficiency inputs and build guarded drafts. |
| CREATE | `backend/src/cms_planner/api/poc.py` | Expose deterministic grounding results. |

---

## External References

- [Pydantic 2 discriminated unions](https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions)
- [FastAPI response models](https://fastapi.tiangolo.com/tutorial/response-model/)

---

## Build Commands

- Use the backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical backend lint, type, and startup checks.
- [ ] Verify integration tests cover reviewed support, unsupported replacement, cross-deficiency rejection, and generic guidance.

---

## Implementation Checklist

- [ ] Define supported-claim and missing-marker models. (AC-001, AC-002)
- [ ] Validate references against reviewed deficiency inputs only. (AC-001, AC-002)
- [ ] Produce guarded draft projections with deterministic replacements. (AC-002)
- [ ] Preserve generic guidance that does not assert case facts. (AC-001, AC-002)
