# Task - TASK_002

## Requirement Reference
- **User Story:** us_047
- **Story Location:** .propel/context/tasks/EP-008/us_047/us_047.md
- **Acceptance Criteria:** AC-001, AC-002
- **Edge Cases:** Required failed stages cannot appear completed.

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
| **Design Tokens** | designsystem.md#design-tokens; semantic status tokens |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React, TypeScript, Vite | React 19.3; TypeScript 7.0; Vite 8.3 | FR-007 requires visible failed page and stage state. |

---

## Task Overview
**Estimated Effort:** 5 hours

Render failed stages and retained valid work without representing incomplete processing as confirmed.

## Dependent Tasks
- TASK_001 from US_047.

## Impacted Components
- Processing timeline, extraction result projection, and failure alert.

## Implementation Plan
- Map typed job failure events into view state.
- Render affected page/stage and retained-work status.
- Prevent completed visual state for failed required stages.

## Current Project State
```text
frontend/src/features/{document-intake,extraction-review}/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/features/document-intake/FailedStageAlert.tsx | Present failed operation and retained work. |
| MODIFY | frontend/src/features/document-intake/StageTimeline.tsx | Render explicit failed stage status. |
| MODIFY | frontend/src/features/extraction-review/resultProjection.ts | Exclude failed unconfirmed content. |

## External References
- https://react.dev/learn/conditional-rendering
- https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html

## Build Commands
- [Frontend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests cover mixed retained and failed states.
- [x] Integration tests verify no false completed presentation.

## Implementation Checklist
- [x] Display the affected failed page or stage. (AC-001)
- [x] Omit failed unconfirmed payload content from result views. (AC-001)
- [x] Keep independently valid reviewed work visible. (AC-002)
- [x] Prevent completed styling and labels while required stages remain failed. (AC-002, Edge Case)
