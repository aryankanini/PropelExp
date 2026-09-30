# Task - TASK_001

## Requirement Reference
- **User Story:** US_011
- **Story Location:** .propel/context/tasks/EP-001/us_011/us_011.md
- **Acceptance Criteria:**
  - AC-001: One supported file up to 50 MB and 200 pages streams to the session workspace and starts validation.
  - AC-002: Exceeded limits are rejected before OCR or AI and partial files are removed.
- **Edge Cases:**
  - A second concurrent upload is rejected while the first remains unchanged.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | TR-005 requires an application-owned bounded upload contract. |

---

## Task Overview
Define the intake command, result types, and workspace port for bounded streaming. Estimated effort: 8 hours.

## Dependent Tasks
- US_008 - Requires temporary workspace ownership.

## Impacted Components
- New intake application contracts and ports.

## Implementation Plan
- Define streamed chunks, upload limits, accepted result, and typed rejection outcomes.
- Keep filesystem, OCR, AI, and FastAPI details outside the application contract.

## Current Project State
- No application source exists; design.md only recommends the backend module layout.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/application/ports/workspace.py | Define streamed workspace ownership operations. |
| CREATE | backend/src/cms_planner/modules/intake/commands.py | Define upload command and result types. |
| CREATE | backend/src/cms_planner/modules/intake/errors.py | Define bounded intake failures. |

## External References
- https://docs.python.org/3.14/library/typing.html

## Build Commands
- `cd backend; python -m pytest tests/unit/modules/intake`

## Implementation Validation Strategy
- [x] Unit tests verify accepted, exceeded, and concurrent-upload outcomes.

## Implementation Checklist
- [x] Define the streamed upload command and accepted result for AC-001.
- [x] Define byte, page, and active-upload rejection outcomes for AC-002.
- [x] Keep provider invocation outside the upload contract for AC-002.
