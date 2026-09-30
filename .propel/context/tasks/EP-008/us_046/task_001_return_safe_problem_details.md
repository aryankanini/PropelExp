# Task - TASK_001

## Requirement Reference
- **User Story:** us_046
- **Story Location:** .propel/context/tasks/EP-008/us_046/us_046.md
- **Acceptance Criteria:** AC-001, AC-002
- **Edge Cases:** Unknown exceptions retain the correlation ID and map safely.

---

## Design References [CONDITIONAL: UI Impact = Yes]
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/ |
| **Screen Spec** | SCR-002 through SCR-008 |
| **UXR Requirements** | UXR-601 |
| **Design Tokens** | designsystem.md#design-tokens; C/Feedback/Alert |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python, FastAPI, Pydantic | Python 3.14.7; FastAPI 0.141.1; Pydantic 2.x | TR-011 defines safe problem envelopes. |

---

## Task Overview
**Estimated Effort:** 8 hours

Define stable problem schemas and centralized mappings for validation, authorization, provider, cancellation, and unknown failures.

## Dependent Tasks
- US_002 documented problem schemas.

## Impacted Components
- API problem models, exception handlers, job failure events, and correlation context.

## Implementation Plan
- Define a closed public problem model.
- Map typed application failures centrally.
- Sanitize serialization for API and job events.
- Preserve correlation across unknown exceptions.

## Current Project State
```text
backend/src/cms_planner/api/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/api/problems.py | Define safe problem schemas and mappings. |
| MODIFY | backend/src/cms_planner/app.py | Register centralized exception handlers. |
| CREATE | backend/src/cms_planner/application/failures.py | Define typed internal failure categories. |

## External References
- https://fastapi.tiangolo.com/tutorial/handling-errors/
- https://www.rfc-editor.org/rfc/rfc9457

## Build Commands
- [Backend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests cover every failure mapping and field error shape.
- [x] Integration tests scan API and job events for sensitive details.

## Implementation Checklist
- [x] Define stable code, safe message, correlation ID, retryability, and field errors. (AC-001)
- [x] Map validation, authorization, provider, cancellation, and internal failures. (AC-001)
- [x] Exclude stack traces, provider payloads, and sensitive content from serialization. (AC-002)
- [x] Use the same sanitized schema for API responses and job events. (AC-002)
- [x] Preserve correlation ID when mapping unknown exceptions. (AC-001, Edge Case)
