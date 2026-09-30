# Task - TASK_001

## Requirement Reference
- **User Story:** US_020
- **Story Location:** .propel/context/tasks/EP-002/us_020/us_020.md
- **Acceptance Criteria:**
  - AC-001: Every event contains job ID, increasing event ID, stage, percent, timestamp, and terminal status.
  - AC-002: Reconnection after a known event ID resumes later events in order without replaying document text.
- **Edge Cases:**
  - A second active extraction request is rejected while the original stream remains resumable.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python and OpenAPI | Python 3.14.7; OpenAPI 3.1.0 | TR-006 requires typed ordered SSE events. |

---

## Task Overview
Define extraction progress event values and monotonic sequencing policy. Estimated effort: 8 hours.

## Dependent Tasks
- US_002 TASK_001 - Requires the documented SSE contract.

## Impacted Components
- New processing job event model.

## Implementation Plan
- Define required event fields and allowed stages and terminal states.
- Generate event IDs monotonically within each job.

## Current Project State
- No processing job event source exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/domain/job_event.py | Define typed progress events. |
| CREATE | backend/src/cms_planner/modules/extraction/event_sequence.py | Allocate increasing job event IDs. |

## External References
- https://html.spec.whatwg.org/multipage/server-sent-events.html

## Build Commands
- `cd backend; python -m pytest tests/unit/modules/extraction/test_event_sequence.py`

## Implementation Validation Strategy
- [ ] Unit tests verify required fields, percent bounds, and monotonic IDs.

## Implementation Checklist
- [ ] Require job ID, event ID, stage, percent, timestamp, and terminal status for AC-001.
- [ ] Allocate increasing event IDs per job for AC-001.
- [ ] Represent terminal status without document text for AC-001.
- [ ] Define the last-event cursor and ordered later-event projection without document text for AC-002.
