# Task - TASK_002

## Requirement Reference
- **User Story:** US_013
- **Story Location:** .propel/context/tasks/EP-001/us_013/us_013.md
- **Acceptance Criteria:**
  - AC-001: Intake and active workspace screens show session-only storage and remaining inactivity time.
- **Edge Cases:**
  - Reconnect refreshes server-owned time instead of extending stale browser time.

---

## Design References
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/ |
| **Screen Spec** | SCR-002, SCR-003, SCR-004, SCR-006, SCR-008 |
| **UXR Requirements** | UXR-001 |
| **Design Tokens** | .propel/context/docs/designsystem.md |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React and TypeScript | React 19.3; TypeScript 7.0 | UXR-001 requires persistent truthful retention status. |

---

## Task Overview
Render reusable session-only retention status across intake and active workspaces. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires authoritative retention status.

## Impacted Components
- New shared retention indicator and session status hook.

## Implementation Plan
- Fetch and display server-provided retention semantics and remaining time.
- Refresh after reconnect and avoid deriving a new deadline locally.

## Current Project State
- No shared session status UI exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/shared/session/RetentionStatus.tsx | Render session-only retention and remaining time. |
| CREATE | frontend/src/shared/session/useSessionStatus.ts | Refresh authoritative session status. |

## External References
- https://react.dev/reference/react/useEffect

## Build Commands
- `cd frontend; npm run build; npm test -- --run`

## Implementation Validation Strategy
- [x] Component tests verify all target screens and reconnect refresh behavior.

## Implementation Checklist
- [x] Show session-only storage on every required screen for AC-001.
- [x] Show server-owned remaining inactivity time for AC-001.
- [x] Refresh after reconnect without extending stale time for AC-001.
