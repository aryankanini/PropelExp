# Task - TASK_001

## Requirement Reference
- **User Story:** us_047
- **Story Location:** .propel/context/tasks/EP-008/us_047/us_047.md
- **Acceptance Criteria:** AC-001, AC-002
- **Edge Cases:** Required failed stages cannot emit completed terminal events.

---

## Design References [CONDITIONAL: UI Impact = Yes]
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/wireframe-SCR-003-processing-progress.html |
| **Screen Spec** | SCR-003, SCR-004 |
| **UXR Requirements** | UXR-601 |
| **Design Tokens** | designsystem.md#design-tokens; C/Feedback/Alert |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python, FastAPI, Pydantic | Python 3.14.7; FastAPI 0.141.1; Pydantic 2.x | FR-007 and UC-010 require truthful typed job state. |

---

## Task Overview
**Estimated Effort:** 7 hours

Represent page and stage failures explicitly while preserving independently validated case state and preventing false completion.

## Dependent Tasks
- US_006 typed job state.

## Impacted Components
- Job aggregate, stage transition policy, result projection, and terminal event builder.

## Implementation Plan
- Add affected-operation failure metadata.
- Exclude unconfirmed failed payloads.
- Preserve valid reviewed state through stage transitions.
- Guard completed terminal status.

## Current Project State
```text
backend/src/cms_planner/{domain,application,modules/extraction}/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/domain/job_failure.py | Model page and stage failures. |
| CREATE | backend/src/cms_planner/application/job_transitions.py | Enforce truthful terminal transitions. |
| MODIFY | backend/src/cms_planner/modules/extraction/service.py | Retain valid state and omit failed content. |

## External References
- https://docs.pydantic.dev/2.12/concepts/models/

## Build Commands
- [Backend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests cover mixed success/failure transitions.
- [x] Integration tests verify terminal events never claim false completion.

## Implementation Checklist
- [x] Record the affected page or stage for extraction and OCR failures. (AC-001)
- [x] Exclude failed unconfirmed payload content from projected results. (AC-001)
- [x] Preserve previously validated pages and deficiencies. (AC-002)
- [x] Keep retained work available without relabeling the job complete. (AC-002)
- [x] Reject completed terminal events while required stages remain failed. (Edge Case)
