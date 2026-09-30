# Task - TASK_004

## Requirement Reference
- **User Story:** US_020
- **Story Location:** .propel/context/tasks/EP-002/us_020/us_020.md
- **Acceptance Criteria:**
  - AC-001: The client receives complete ordered events.
  - AC-002: Reconnect continues after the last event without duplicate document content.
- **Edge Cases:**
  - A second active extraction rejection does not replace the original stream.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | TypeScript | 7.0 | TR-002 and TR-006 require a typed shared SSE transport. |

---

## Task Overview
Implement a typed extraction SSE client with ordered resume handling. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_003 - Requires the extraction SSE endpoint.

## Impacted Components
- New shared API event transport and parser.

## Implementation Plan
- Parse generated event types and track the last accepted event ID.
- Reconnect from that ID, ignore duplicates, and retain the active job identity.

## Current Project State
- No frontend SSE transport exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/shared/api/extractionEvents.ts | Connect, parse, order, and resume SSE events. |

## External References
- https://html.spec.whatwg.org/multipage/server-sent-events.html

## Build Commands
- `cd frontend; npm run build; npm test -- --run`

## Implementation Validation Strategy
- [ ] Transport tests cover order, duplicate IDs, reconnect, terminal events, and second-job rejection.

## Implementation Checklist
- [ ] Parse all required progress fields for AC-001.
- [ ] Deliver events in increasing event-ID order for AC-001.
- [ ] Resume after the last accepted event ID for AC-002.
- [ ] Avoid duplicate payload handling and preserve the original job for AC-002.
