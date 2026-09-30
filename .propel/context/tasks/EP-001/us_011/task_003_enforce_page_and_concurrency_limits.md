# Task - TASK_003

## Requirement Reference
- **User Story:** US_011
- **Story Location:** .propel/context/tasks/EP-001/us_011/us_011.md
- **Acceptance Criteria:**
  - AC-001: A supported document at most 200 pages starts validation.
  - AC-002: More than 200 pages is rejected before OCR or AI.
- **Edge Cases:**
  - A second concurrent upload is rejected while the first remains unchanged.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | NFR-003 and TR-005 require page and single-upload enforcement. |

---

## Task Overview
Enforce supported media, page count, and one-active-upload policy before processing. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_002 - Requires the streamed workspace file.

## Impacted Components
- New intake preflight and active-upload guard.

## Implementation Plan
- Inspect supported document metadata without invoking providers.
- Reserve and release one active upload atomically.

## Current Project State
- Streaming is planned without page-count or concurrency policy.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/modules/intake/preflight.py | Validate media and page boundaries. |
| CREATE | backend/src/cms_planner/modules/intake/upload_guard.py | Enforce one active upload. |

## External References
- https://docs.python.org/3.14/library/threading.html

## Build Commands
- `cd backend; python -m pytest tests/unit/modules/intake/test_preflight.py`

## Implementation Validation Strategy
- [x] Page limit and concurrent submissions have deterministic outcomes.

## Implementation Checklist
- [x] Accept supported documents with at most 200 pages for AC-001.
- [x] Reject over-200-page documents before provider work for AC-002.
- [x] Reject a second active upload without changing the first for AC-001.
