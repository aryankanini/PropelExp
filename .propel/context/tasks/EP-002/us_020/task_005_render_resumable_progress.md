# Task - TASK_005

## Requirement Reference
- **User Story:** US_020
- **Story Location:** .propel/context/tasks/EP-002/us_020/us_020.md
- **Acceptance Criteria:**
  - AC-001: Ordered events show job, stage, percent, timestamp, and terminal status.
  - AC-002: Disconnect and reconnect resume later progress without document text replay.
- **Edge Cases:**
  - A second extraction request is rejected while original progress remains visible and resumable.

---

## Design References
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/wireframe-SCR-003-processing-progress.html |
| **Screen Spec** | SCR-003 |
| **UXR Requirements** | N/A |
| **Design Tokens** | .propel/context/docs/designsystem.md |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React and TypeScript | React 19.3; TypeScript 7.0 | SCR-003 requires stable processing and reconnect states. |

---

## Task Overview
Build the ordered progress timeline, reconnect status, and terminal states for SCR-003. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_004 - Requires the typed resumable SSE client.

## Impacted Components
- New processing progress page and state controller.

## Implementation Plan
- Render stable ordered stages, percent, elapsed status, and terminal outcome.
- Show reconnecting without clearing accepted progress or exposing document text.

## Current Project State
- No processing progress page source exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/features/extraction-review/ProcessingProgressPage.tsx | Render SCR-003 progress and terminal states. |
| CREATE | frontend/src/features/extraction-review/useExtractionProgress.ts | Integrate resumable event state. |

## External References
- https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html

## Build Commands
- `cd frontend; npm run build; npm test -- --run`

## Implementation Validation Strategy
- [ ] Component tests verify ordered progress, reconnect, terminal state, and active-job rejection.

## Implementation Checklist
- [ ] Show job, stage, percent, timestamp, and terminal status for AC-001.
- [ ] Keep accepted progress stable and ordered for AC-001.
- [ ] Show reconnecting and resume only later events for AC-002.
- [ ] Keep original progress visible when a second job is rejected for AC-002.
