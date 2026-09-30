# Task - TASK_002

## Requirement Reference
- **User Story:** US_015
- **Story Location:** .propel/context/tasks/EP-001/us_015/us_015.md
- **Acceptance Criteria:**
  - AC-001: Explicit confirmation precedes cleanup and empty intake.
  - AC-002: Cancel or cleanup failure keeps the case visible.
- **Edge Cases:**
  - Retrying failed cleanup is idempotent and cannot reuse the workspace prematurely.

---

## Design References
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/wireframe-SCR-008-approved-export.html |
| **Screen Spec** | SCR-002, SCR-008 |
| **UXR Requirements** | UXR-001, UXR-602 |
| **Design Tokens** | .propel/context/docs/designsystem.md |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React and TypeScript | React 19.3; TypeScript 7.0 | UC-009 and UXR-602 require explicit destructive confirmation. |

---

## Task Overview
Build the accessible end-session dialog and truthful success, cancel, failure, and retry states. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires the case termination API.

## Impacted Components
- New shared end-session dialog and cleanup controller.

## Implementation Plan
- Present the permanent-removal warning with confirm and cancel actions.
- Keep case content visible until confirmed cleanup succeeds.

## Current Project State
- No session termination UI exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/shared/session/EndSessionDialog.tsx | Render confirmation and failure states. |
| CREATE | frontend/src/shared/session/useEndSession.ts | Coordinate cleanup and navigation. |

## External References
- https://www.w3.org/WAI/ARIA/apg/patterns/alertdialog/

## Build Commands
- `cd frontend; npm run build; npm test -- --run`

## Implementation Validation Strategy
- [x] Component tests verify focus, cancel, success navigation, retained failure, and retry.

## Implementation Checklist
- [x] Require explicit removal confirmation before cleanup for AC-001.
- [x] Return to empty intake only after confirmed cleanup succeeds for AC-001.
- [x] Keep the case visible after cancel or cleanup failure for AC-002.
- [x] Offer an idempotent retry without claiming prior cleanup for AC-002.
