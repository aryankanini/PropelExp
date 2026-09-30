# Task - TASK_002

## Requirement Reference
- **User Story:** US_011
- **Story Location:** .propel/context/tasks/EP-001/us_011/us_011.md
- **Acceptance Criteria:**
  - AC-001: Accepted content streams to the session workspace.
  - AC-002: Files over 50 MB are rejected before processing and partial files are removed.
- **Edge Cases:**
  - A second concurrent upload leaves the first unchanged.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | DR-003 and TR-005 require randomized streamed temporary storage. |

---

## Task Overview
Implement bounded chunk streaming into the session-owned temporary workspace. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires the workspace port and intake outcomes.

## Impacted Components
- New filesystem upload adapter and intake service.

## Implementation Plan
- Stream chunks to a randomized server path while counting bytes.
- Remove partial output on limit, cancellation, or write failure.

## Current Project State
- No filesystem or intake implementation exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/adapters/filesystem/upload_workspace.py | Stream uploads to randomized session paths. |
| CREATE | backend/src/cms_planner/modules/intake/upload_service.py | Coordinate bounded upload state. |

## External References
- https://docs.python.org/3.14/library/tempfile.html

## Build Commands
- `cd backend; python -m pytest tests/unit/modules/intake/test_upload_service.py`

## Implementation Validation Strategy
- [x] Boundary-sized input is retained and oversized input leaves no partial file.

## Implementation Checklist
- [x] Stream accepted content without loading the full file for AC-001.
- [x] Enforce the 50 MB limit while reading for AC-002.
- [x] Delete every rejected partial file for AC-002.
