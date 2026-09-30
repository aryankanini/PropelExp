# Task - TASK_002

## Requirement Reference
- **User Story:** us_048
- **Story Location:** .propel/context/tasks/EP-008/us_048/us_048.md
- **Acceptance Criteria:** AC-001, AC-002, AC-003
- **Edge Cases:** Repeated commands do not create concurrent attempts.

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
| Frontend | React, TypeScript, Vite | React 19.3; TypeScript 7.0; Vite 8.3 | UC-010 defines retry, replacement, and retry-later interactions. |

---

## Task Overview
**Estimated Effort:** 6 hours

Connect typed recovery semantics to retry, replacement upload, and retry-later UI actions while retaining reviewed work.

## Dependent Tasks
- TASK_001 from US_048.

## Impacted Components
- Recovery action model, processing failure UI, and POC generation failure UI.

## Implementation Plan
- Map recovery results to one valid primary action.
- Disable repeated submission during an active attempt.
- Preserve current reviewed view state through recovery.

## Current Project State
```text
frontend/src/features/{document-intake,poc-authoring}/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/shared/model/recovery.ts | Define typed recovery actions. |
| CREATE | frontend/src/shared/ui/RecoveryAction.tsx | Render and submit the primary action. |
| MODIFY | frontend/src/features/poc-authoring/PocFailureState.tsx | Preserve retained work during generation retry. |

## External References
- https://react.dev/reference/react/useActionState
- https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html

## Build Commands
- [Frontend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests cover retry, replacement, and later-retry actions.
- [x] Integration tests verify retained work and single active submission.

## Implementation Checklist
- [x] Render retry only for retryable failed operations. (AC-001)
- [x] Preserve reviewed values while retry output returns unconfirmed. (AC-001)
- [x] Render replacement upload for invalid or unreadable sources. (AC-002)
- [x] Keep later retry available after exhausted providers. (AC-003)
- [x] Prevent duplicate submissions while recovery is active. (Edge Case)
