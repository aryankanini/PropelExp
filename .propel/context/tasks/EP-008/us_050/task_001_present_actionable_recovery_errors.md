# Task - TASK_001

## Requirement Reference
- **User Story:** us_050
- **Story Location:** .propel/context/tasks/EP-008/us_050/us_050.md
- **Acceptance Criteria:** AC-001, AC-002
- **Edge Cases:** Non-retryable failures offer a valid alternative action.

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
| Frontend | React, TypeScript, Vite | React 19.3; TypeScript 7.0; Vite 8.3 | UXR-601 requires safe, actionable, accessible recovery errors. |

---

## Task Overview
**Estimated Effort:** 6 hours

Create a shared recovery error presentation that names the failure, retained work, retryability, correlation ID, and one valid primary action.

## Dependent Tasks
- TASK_001 from US_046.
- TASK_002 from US_048.

## Impacted Components
- Shared alert, recovery action mapper, and feature-level error states.

## Implementation Plan
- Map safe problems and terminal events into one view model.
- Render calm content and exactly one primary action.
- Announce terminal failures once with assertive semantics.
- Exclude provider and document detail from all variants.

## Current Project State
```text
frontend/src/shared/ui/
frontend/src/features/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/shared/ui/RecoveryError.tsx | Render the shared actionable failure state. |
| CREATE | frontend/src/shared/model/problem.ts | Map safe problems and terminal failures. |
| MODIFY | frontend/src/shared/ui/Alert.tsx | Support correlation ID and one recovery action. |

## External References
- https://react.dev/learn/conditional-rendering
- https://www.w3.org/WAI/ARIA/apg/practices/structural-roles/#alert

## Build Commands
- [Frontend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests cover retryable and non-retryable action mapping.
- [x] Accessibility tests verify one assertive announcement per terminal error.

## Implementation Checklist
- [x] Show failed operation, retained work, retryability, and correlation ID. (AC-001)
- [x] Render exactly one valid primary recovery action. (AC-001)
- [x] Use replacement, return, or later retry when immediate retry is unavailable. (AC-001, Edge Case)
- [x] Announce a newly rendered terminal failure once as an assertive alert. (AC-002)
- [x] Exclude provider details and document content from visible and accessible text. (AC-002)