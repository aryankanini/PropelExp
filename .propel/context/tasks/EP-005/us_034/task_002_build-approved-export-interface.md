# Task - TASK_002 Build Approved Export Interface

## Requirement Reference

- **User Story:** US_034
- **Story Location:** .propel/context/tasks/EP-005/us_034/us_034.md
- **Acceptance Criteria:**
  - **AC-001: Current approval**
    - **Given**: Approval matches the current POC revision
    - **When**: Copy or download is requested
    - **Then**: The approved current content is returned in the requested format
  - **AC-002: Missing or stale approval**
    - **Given**: Approval is absent, revoked, or belongs to another revision
    - **When**: Export is requested
    - **Then**: Export is blocked with an approval-required reason
  - **AC-003: Formatting failure**
    - **Given**: Download formatting fails
    - **When**: The failure is returned
    - **Then**: Approval remains unchanged and retry or copy is offered
- **Edge Cases:**
  - Export authorization is rechecked server-side even when the UI action appears enabled.

---

## Design References

| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A - pending Figma file |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/wireframe-SCR-008-approved-export.html |
| **Screen Spec** | SCR-008 |
| **UXR Requirements** | UXR-002 |
| **Design Tokens** | .propel/context/docs/designsystem.md#design-tokens; .propel/context/docs/designsystem.md#accessibility-requirements |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | UXR-002 requires approval-aware copy/download controls and explicit blocked reasons. |

---

## Task Overview

Implement the EP-005 / US_034 approved export interface for current content, disabled approval-required states, and non-destructive formatting recovery. Estimated effort: 6 hours.

## Dependent Tasks

- US_032 - Same-Epic - Requires current-revision approval.
- TASK_001 Authorize Current Revision Export - provides export authorization and response contracts.

## Impacted Components

- New approved export screen and typed export client.
- New recovery modal for download failure with retry and copy actions.

## Implementation Plan

1. Map export API contracts to typed view states.
2. Present copy and download only for current approved content.
3. Show approval-required reasons for blocked export.
4. Offer retry or copy after formatting failure without altering approval display.

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
| CREATE | frontend/src/features/approval-export/ApprovedExport.tsx | Render approved content and copy/download actions. |
| CREATE | frontend/src/features/approval-export/ExportFailureModal.tsx | Offer retry or copy after formatting failure. |
| CREATE | frontend/src/shared/api/export.ts | Call the authorized export endpoint. |
| CREATE | frontend/src/shared/model/export.ts | Define export and approval-required view states. |
| CREATE | frontend/src/shared/ui/Modal.tsx | Provide accessible focus-managed recovery dialogs. |

## External References

- [React 19.3 reference](https://react.dev/versions#react-19)
- [TypeScript 7.0 documentation](https://www.typescriptlang.org/docs/)
- [Vite 8 guide](https://vite.dev/guide/)

## Build Commands

- [Frontend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [x] Unit tests pass for approved, blocked, formatting-failure, retry, and copy states.
- [x] Integration tests pass for current and stale approval export responses.

## Implementation Checklist

- [x] Render approved current content and request copy or download in the selected format. (AC-001)
- [x] Disable export and display the approval-required reason for absent, revoked, or stale approval. (AC-002)
- [x] Preserve approved state and offer retry or copy when download formatting fails. (AC-003)
