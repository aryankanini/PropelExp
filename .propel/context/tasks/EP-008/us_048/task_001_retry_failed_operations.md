# Task - TASK_001

## Requirement Reference
- **User Story:** us_048
- **Story Location:** .propel/context/tasks/EP-008/us_048/us_048.md
- **Acceptance Criteria:** AC-001, AC-002, AC-003
- **Edge Cases:** Duplicate retry commands cannot create concurrent calls.

---

## Design References [CONDITIONAL: UI Impact = Yes]
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/ |
| **Screen Spec** | SCR-003, SCR-006 |
| **UXR Requirements** | UXR-601 |
| **Design Tokens** | designsystem.md#design-tokens; C/Feedback/Alert |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python, FastAPI, Pydantic | Python 3.14.7; FastAPI 0.141.1; Pydantic 2.x | FR-014 and UC-010 require selective idempotent recovery. |

---

## Task Overview
**Estimated Effort:** 8 hours

Implement idempotent recovery commands that rerun only the typed failed operation and preserve confirmed work.

## Dependent Tasks
- TASK_001 from US_047.

## Impacted Components
- Recovery command handler, operation lock, extraction/generation services, and job events.

## Implementation Plan
- Validate source and failed-operation eligibility.
- Serialize retries per operation.
- Dispatch only the failed operation.
- Preserve retained state and return review-ready output.

## Current Project State
```text
backend/src/cms_planner/application/recovery/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/application/recovery/commands.py | Define selective retry commands and results. |
| CREATE | backend/src/cms_planner/application/recovery/service.py | Coordinate idempotent operation retries. |
| CREATE | backend/src/cms_planner/api/routes/recovery.py | Expose the recovery endpoint. |

## External References
- https://fastapi.tiangolo.com/tutorial/body/
- https://docs.python.org/3.14/library/asyncio-sync.html#lock

## Build Commands
- [Backend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests cover operation selection and retained-state invariants.
- [x] Integration tests prove duplicate commands produce one provider call.

## Implementation Checklist
- [x] Rerun only the typed failed extraction, OCR, or generation operation. (AC-001)
- [x] Return successful retry output as unconfirmed review-ready state. (AC-001)
- [x] Block extraction retry for invalid input and return replacement-upload action. (AC-002)
- [x] Preserve confirmed deficiencies and retained POC work after exhaustion. (AC-003)
- [x] Keep later retry available after provider exhaustion. (AC-003)
- [x] Coalesce duplicate retry commands for one active attempt. (Edge Case)
