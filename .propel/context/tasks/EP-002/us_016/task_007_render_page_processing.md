# Task - TASK_007

## Requirement Reference
- **User Story:** US_016
- **Story Location:** .propel/context/tasks/EP-002/us_016/us_016.md
- **Acceptance Criteria:**
  - AC-001: Page routing decisions are retained.
  - AC-002: Complete native-text pages retain text and coordinates without OCR.
  - AC-003: Only incomplete native-text pages are sent through the approved OCR port with page coordinates retained.
  - AC-004: OCR failures identify the page and failed stage without confirmed content.
  - AC-005: Extracted text is normalized without changing substantive content before CMS structure detection.
- **Edge Cases:**
  - Mixed documents can use native text and OCR while retaining page order.

---

## Design References
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | HTML wireframe is the approved design source |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/wireframe-SCR-003-processing-progress.html |
| **Screen Spec** | SCR-003 |
| **UXR Requirements** | SCR-003 processing and failure-state requirements |
| **Design Tokens** | .propel/context/docs/designsystem.md |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React and TypeScript | React 19.3; TypeScript 7.0 | SCR-003 presents page-level processing and failure status. |

---

## Task Overview
Render page extraction routes and safe OCR failure states on SCR-003. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_006 - Requires orchestrated page status.

## Impacted Components
- New page processing timeline components.

## Implementation Plan
- Present ordered page route and stage state without document text replay.
- Identify failed pages as unconfirmed while preserving successful progress.

## Current Project State
- No processing progress feature source exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/features/extraction-review/PageProcessingList.tsx | Render ordered page route and state. |
| CREATE | frontend/src/features/extraction-review/PageFailureStatus.tsx | Render safe page-stage failures. |

## External References
- https://react.dev/reference/react

## Build Commands
- `cd frontend; npm run build; npm test -- --run`

## Implementation Validation Strategy
- [ ] Component tests cover mixed routes and failed unconfirmed pages.

## Implementation Checklist
- [ ] Show retained page routing decisions in order for AC-001.
- [ ] Present complete native-text pages as processed without an OCR request for AC-002.
- [ ] Present only affected incomplete pages as OCR-routed while retaining page identity for AC-003.
- [ ] Identify the failed OCR page and stage for AC-004.
- [ ] Never present failed page content as confirmed for AC-004.
- [ ] Present normalized processing completion without altering or re-normalizing substantive page text for AC-005.
