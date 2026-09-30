# Task - TASK_004

## Requirement Reference
- **User Story:** US_011
- **Story Location:** .propel/context/tasks/EP-001/us_011/us_011.md
- **Acceptance Criteria:**
  - AC-001: Submitting a supported bounded file starts validation.
  - AC-002: Exceeded limits return rejection before OCR or AI.
- **Edge Cases:**
  - A second concurrent upload is rejected while the first remains unchanged.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | FastAPI and OpenAPI | FastAPI 0.141.1; OpenAPI 3.1.0 | TR-004 and TR-005 define the multipart case endpoint. |

---

## Task Overview
Expose the streamed multipart case creation endpoint and safe problem responses. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001, TASK_002, TASK_003 - Requires intake contracts and limits.

## Impacted Components
- New case route and multipart schemas.

## Implementation Plan
- Adapt multipart chunks to the upload service.
- Map bounded failures to stable problem details without protected content.

## Current Project State
- No case intake routes exist.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/api/routes/cases.py | Expose `POST /api/v1/cases`. |
| CREATE | backend/src/cms_planner/api/schemas/intake.py | Define multipart metadata and intake responses. |

## External References
- https://fastapi.tiangolo.com/tutorial/request-files/

## Build Commands
- `cd backend; python -m pytest tests/integration/api/test_case_upload.py`

## Implementation Validation Strategy
- [x] HTTP tests verify accepted, oversized, over-page, and concurrent submissions.

## Implementation Checklist
- [x] Stream accepted multipart content into validation for AC-001.
- [x] Return safe byte and page limit problems for AC-002.
- [x] Preserve the active case on concurrent rejection for AC-001.
