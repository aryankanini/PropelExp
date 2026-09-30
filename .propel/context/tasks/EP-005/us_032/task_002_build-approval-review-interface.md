# Task - TASK_002 Build Approval Review Interface

## Requirement Reference

- **User Story:** US_032
- **Story Location:** .propel/context/tasks/EP-005/us_032/us_032.md
- **Acceptance Criteria:**
  - **AC-001: Approve complete revision**
    - **Given**: The leader sees evidence, provenance, completeness, five sections, and the current revision
    - **When**: The leader approves
    - **Then**: Approval is bound to that revision and copy and download become available
  - **AC-002: Stale or incomplete package**
    - **Given**: The package is incomplete or its revision changed
    - **When**: Approval is requested
    - **Then**: Approval is denied without changing state and exact blockers are shown
- **Edge Cases:**
  - Two leaders approving the same unchanged revision produce one current approval state.

---

## Design References

| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A - pending Figma file |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/wireframe-SCR-007-approval-review.html |
| **Screen Spec** | SCR-007 |
| **UXR Requirements** | UXR-002 |
| **Design Tokens** | .propel/context/docs/designsystem.md#design-tokens; .propel/context/docs/designsystem.md#accessibility-requirements |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | UXR-002 requires a role-aware approval review experience tied to current revision state. |

---

## Task Overview

Implement the EP-005 / US_032 approval review screen so leaders can inspect evidence, provenance, completeness, all five sections, and current revision status before approval. Estimated effort: 8 hours.

## Dependent Tasks

- TASK_001 Implement Current Revision Approval - provides the approval and blocker API behavior.

## Impacted Components

- New approval review feature composition and typed approval API client.
- New revision history and approval-state presentation within SCR-007.

## Implementation Plan

1. Define approval review view models and typed API calls.
2. Compose evidence, provenance, completeness, five-section, and revision views.
3. Gate approval controls by role and current completeness state.
4. Render exact blockers and refresh state after approval without optimistic authority changes.

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
| CREATE | frontend/src/features/approval-export/ApprovalReview.tsx | Compose the current-revision approval review screen. |
| CREATE | frontend/src/features/approval-export/RevisionHistory.tsx | Present revision and provenance context for the reviewed package. |
| CREATE | frontend/src/shared/api/approval.ts | Call the typed approval endpoint and expose blocker responses. |
| CREATE | frontend/src/shared/model/approval.ts | Define approval review and blocker view types. |

## External References

- [React 19.3 reference](https://react.dev/versions#react-19)
- [TypeScript 7.0 documentation](https://www.typescriptlang.org/docs/)
- [Vite 8 guide](https://vite.dev/guide/)

## Build Commands

- [Frontend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [x] Unit tests pass for approval control, blocker, and revision-history states.
- [x] Integration tests pass for complete, stale, incomplete, duplicate, and role-restricted approval flows.

## Implementation Checklist

- [x] Show evidence, provenance, completeness, five sections, and current revision before approval. (AC-001)
- [x] Enable copy and download only after the API confirms current-revision approval. (AC-001)
- [x] Preserve the displayed state and show exact blockers when approval is denied. (AC-002)
