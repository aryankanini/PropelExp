# Task - TASK_003

## Requirement Reference
- **User Story:** US_012
- **Story Location:** .propel/context/tasks/EP-001/us_012/us_012.md
- **Acceptance Criteria:**
  - AC-001: Valid documents are shown as extraction-ready.
  - AC-002: Invalid documents show the reason and choose-another-file action.
- **Edge Cases:**
  - Mixed readability is rejected when identity cannot be established.

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
| Frontend | React and TypeScript | React 19.3; TypeScript 7.0 | FR-002 requires clear intake validation feedback. |

---

## Task Overview
Render extraction-ready, validation, and choose-another-file states on SCR-002. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_002 - Requires validation state from the case API.

## Impacted Components
- New intake validation status components.

## Implementation Plan
- Render accepted readiness without implying extraction completion.
- Associate safe rejection reasons with the file control and recovery action.

## Current Project State
- The planned intake page has no CMS-2567 validation presentation.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/features/document-intake/DocumentValidationStatus.tsx | Render valid and invalid outcomes. |
| CREATE | frontend/src/features/document-intake/ChooseAnotherFileButton.tsx | Reset invalid intake for retry. |

## External References
- https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html

## Build Commands
- `cd frontend; npm run build; npm test -- --run`

## Implementation Validation Strategy
- [x] Component tests cover valid, unreadable, non-CMS, and mixed-document states.

## Implementation Checklist
- [x] Show extraction-ready status only for accepted documents for AC-001.
- [x] Show the server rejection reason for AC-002.
- [x] Provide an accessible choose-another-file action for AC-002.
