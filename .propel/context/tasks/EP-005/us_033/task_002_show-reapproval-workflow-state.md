# Task - TASK_002 Show Reapproval Workflow State

## Requirement Reference

- **User Story:** US_033
- **Story Location:** .propel/context/tasks/EP-005/us_033/us_033.md
- **Acceptance Criteria:**
  - **AC-001: Request changes**
    - **Given**: A leader reviews a POC
    - **When**: The leader requests changes
    - **Then**: The POC remains unapproved and returns to editing with export disabled
  - **AC-002: Edit approved content**
    - **Given**: A POC revision is approved
    - **When**: Any section is changed and saved
    - **Then**: Approval is revoked immediately and the current revision shows Reapproval required
- **Edge Cases:**
  - An edit that fails to save does not revoke approval for the unchanged current revision.

---

## Design References

| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A - pending Figma file |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/ |
| **Screen Spec** | SCR-006, SCR-007, SCR-008 |
| **UXR Requirements** | UXR-002 |
| **Design Tokens** | .propel/context/docs/designsystem.md#design-tokens; .propel/context/docs/designsystem.md#accessibility-requirements |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | UXR-002 requires visible unapproved and reapproval-required workflow states. |

---

## Task Overview

Implement the EP-005 / US_033 interface states for requested changes, disabled export, and immediate Reapproval required feedback after a successful edit. Estimated effort: 6 hours.

## Dependent Tasks

- US_032 - Same-Epic - Requires revision-bound approval.
- TASK_001 Invalidate Approval on Revision - provides authoritative reapproval state.

## Impacted Components

- New reapproval status presentation across authoring, approval, and export screens.
- New typed client for request-changes and reapproval responses.

## Implementation Plan

1. Map backend approval states to explicit UI labels and disabled reasons.
2. Return requested changes to editing and disable export.
3. Refresh revision state after successful saves and show Reapproval required.
4. Retain approved UI state when a save fails and no new revision exists.

## Current Project State

```text
frontend/src/
├── features/approval-export/       # Planned; frontend implementation directory is not yet present
├── shared/api/
├── shared/model/
└── shared/ui/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/features/approval-export/ReapprovalStatus.tsx | Render editing, unapproved, and reapproval-required states. |
| CREATE | frontend/src/shared/api/reapproval.ts | Call request-changes and revision-state endpoints. |
| CREATE | frontend/src/shared/model/reapproval.ts | Define reapproval view states and disabled reasons. |
| CREATE | frontend/src/shared/ui/StatusBadge.tsx | Render semantic text-and-icon workflow status. |

## External References

- [React 19.3 reference](https://react.dev/versions#react-19)
- [TypeScript 7.0 documentation](https://www.typescriptlang.org/docs/)
- [Vite 8 guide](https://vite.dev/guide/)

## Build Commands

- [Frontend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [x] Unit tests pass for editing, disabled-export, failed-save, and reapproval-required states.
- [x] Integration tests pass for request changes and successful revision-save invalidation.

## Implementation Checklist

- [x] Return requested changes to editing while displaying an unapproved state and disabled export reason. (AC-001)
- [x] Show Reapproval required immediately after a changed section saves successfully. (AC-002)
- [x] Keep the unchanged approved revision visible when an edit fails to save. (AC-002)
