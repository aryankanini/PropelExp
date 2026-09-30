# Task - TASK_002

## Requirement Reference
- **User Story:** US_020
- **Story Location:** .propel/context/tasks/EP-002/us_020/us_020.md
- **Acceptance Criteria:**
  - AC-001: Progress events remain ordered.
  - AC-002: Reconnect resumes after the known event ID without document-text replay.
- **Edge Cases:**
  - A second extraction request is rejected while the original stream remains resumable.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | TR-006 requires an in-memory resumable event stream. |

---

## Task Overview
Implement bounded per-job event buffering and last-event resume semantics. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires typed extraction events.

## Impacted Components
- New in-memory job event buffer and active-job guard.

## Implementation Plan
- Append and read events under one ordered job sequence.
- Resume strictly after the supplied event ID and exclude document text.

## Current Project State
- Typed events are planned without retention or resume behavior.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/infrastructure/state/job_event_buffer.py | Buffer and resume ordered events. |
| CREATE | backend/src/cms_planner/modules/extraction/active_job_guard.py | Reject a second active extraction. |

## External References
- https://docs.python.org/3.14/library/collections.html

## Build Commands
- `cd backend; python -m pytest tests/unit/infrastructure/state/test_job_event_buffer.py`

## Implementation Validation Strategy
- [ ] Tests cover ordered append, resume cursor, terminal state, and active-job rejection.

## Implementation Checklist
- [ ] Preserve event order for AC-001.
- [ ] Resume strictly after the known event ID for AC-002.
- [ ] Exclude document text from buffered and replayed events for AC-002.
- [ ] Reject a second job without disrupting the resumable stream for AC-002.
