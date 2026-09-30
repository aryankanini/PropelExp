# Task - TASK_005

## Requirement Reference
- **User Story:** US_011
- **Story Location:** .propel/context/tasks/EP-001/us_011/us_011.md
- **Acceptance Criteria:**
  - AC-001: The reviewer submits one supported file within 50 MB and 200 pages.
  - AC-002: Boundary rejection is shown without starting OCR or AI.
- **Edge Cases:**
  - A second concurrent upload is rejected while the first remains unchanged.

---

## Design References
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/wireframe-SCR-002-document-intake.html |
| **Screen Spec** | SCR-002 |
| **UXR Requirements** | UXR-001, UXR-602 |
| **Design Tokens** | .propel/context/docs/designsystem.md |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React, TypeScript, Vite | React 19.3; TypeScript 7.0; Vite 8.3 | TR-002 assigns intake interaction to the SPA. |

---

## Task Overview
Build the SCR-002 upload control, progress, limits, and rejection states. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_004 - Requires the case upload API.

## Impacted Components
- New document-intake feature slice.

## Implementation Plan
- Implement accessible selection, submission, and stable upload progress.
- Render server rejection and choose-another-file actions without losing the active upload state.

## Current Project State
- No frontend feature source exists; the wireframe defines the intended intake screen.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/features/document-intake/DocumentIntakePage.tsx | Render SCR-002 intake states. |
| CREATE | frontend/src/features/document-intake/useDocumentUpload.ts | Coordinate multipart upload state. |
| CREATE | frontend/src/features/document-intake/document-intake.css | Apply stable responsive intake styling. |

## External References
- https://react.dev/reference/react

## Build Commands
- `cd frontend; npm run build; npm test -- --run`

## Implementation Validation Strategy
- [x] Component tests cover accepted, rejected, and already-active upload states.

## Implementation Checklist
- [x] Present supported formats and 50 MB/200-page limits for AC-001.
- [x] Submit one file and show stable upload progress for AC-001.
- [x] Show boundary rejection and choose-another-file action for AC-002.
- [x] Preserve the first upload when a concurrent submission is rejected for AC-001.
