# Task - TASK_003

## Requirement Reference
- **User Story:** US_020
- **Story Location:** .propel/context/tasks/EP-002/us_020/us_020.md
- **Acceptance Criteria:**
  - AC-001: SSE emits complete ordered progress events.
  - AC-002: `Last-Event-ID` reconnect resumes later events without document text.
- **Edge Cases:**
  - A second extraction request is rejected while the stream remains resumable.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | FastAPI and OpenAPI | FastAPI 0.141.1; OpenAPI 3.1.0 | TR-006 defines the versioned SSE API boundary. |

---

## Task Overview
Expose ordered extraction events through the documented SSE endpoint. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_002 - Requires resumable buffered events.

## Impacted Components
- New job event route and SSE serializer.

## Implementation Plan
- Stream typed events from `GET /api/v1/jobs/{jobId}/events`.
- Parse `Last-Event-ID`, preserve order, and close after terminal status.

## Current Project State
- No job event route exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/api/routes/job_events.py | Expose the extraction SSE stream. |
| CREATE | backend/src/cms_planner/api/sse.py | Serialize typed events safely. |

## External References
- https://html.spec.whatwg.org/multipage/server-sent-events.html

## Build Commands
- `cd backend; python -m pytest tests/integration/api/test_job_events.py`

## Implementation Validation Strategy
- [ ] HTTP stream tests verify fields, ordering, resume, terminal close, and no text replay.

## Implementation Checklist
- [ ] Emit every required event field in increasing order for AC-001.
- [ ] Resume after `Last-Event-ID` for AC-002.
- [ ] Prevent document text from entering SSE payloads for AC-002.
- [ ] Keep the original stream resumable after second-job rejection for AC-002.
