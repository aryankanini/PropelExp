# Task - TASK_001 Build Persistent Workflow Rail

## Requirement Reference

- **User Story:** US_036
- **Story Location:** .propel/context/tasks/EP-006/us_036/us_036.md
- **Acceptance Criteria:**
  - **AC-001: Desktop rail**
    - **Given**: The workspace is 1440 pixels wide
    - **When**: A case stage loads
    - **Then**: Intake, Review, POC Drafts, and Approval/Export remain visible with text and icon states for complete, current, blocked, and unavailable
  - **AC-002: Available-stage navigation**
    - **Given**: A stage is available
    - **When**: The user selects it
    - **Then**: The stage opens while preserving the active case and selected deficiency
- **Edge Cases:**
  - Selecting a blocked stage leaves the current screen unchanged and states the blocker.

---

## Design References

| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A - pending Figma file |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/ |
| **Screen Spec** | SCR-002, SCR-003, SCR-004, SCR-005, SCR-006, SCR-007, SCR-008 |
| **UXR Requirements** | UXR-101 |
| **Design Tokens** | .propel/context/docs/designsystem.md#design-tokens; .propel/context/docs/designsystem.md#accessibility-requirements |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | UXR-101 requires persistent, semantic workflow orientation and context-preserving navigation. |

---

## Task Overview

Implement the EP-006 / US_036 shared workspace rail with visible desktop stages, semantic status states, context-preserving navigation, and blocked-stage explanations. Estimated effort: 8 hours.

## Dependent Tasks

- US_001 - Foundational - Requires the shared React shell.

## Impacted Components

- New application shell, workflow rail, and workflow-state model.

## Implementation Plan

1. Define stage availability and semantic status view models.
2. Compose the persistent rail inside the application shell.
3. Preserve active case and selected deficiency during available-stage navigation.
4. Prevent blocked navigation and expose its blocker without changing screens.

## Current Project State

```text
frontend/src/
├── app/                            # Planned; frontend implementation directory is not yet present
├── shared/model/
└── shared/ui/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/app/AppShell.tsx | Compose persistent workflow navigation and active workspace content. |
| CREATE | frontend/src/app/WorkflowRail.tsx | Render stages and semantic complete/current/blocked/unavailable states. |
| CREATE | frontend/src/shared/model/workflow.ts | Define stages, availability, blockers, and retained case context. |
| CREATE | frontend/src/shared/ui/StatusBadge.tsx | Render text-and-icon stage status without color-only meaning. |

## External References

- [React 19.3 reference](https://react.dev/versions#react-19)
- [WAI-ARIA Authoring Practices navigation landmarks](https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/)
- [Vite 8 guide](https://vite.dev/guide/)

## Build Commands

- [Frontend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [ ] Unit tests pass for all stage states and blocked selection.
- [ ] Integration tests pass for available-stage navigation with retained case and deficiency context.

## Implementation Checklist

- [ ] Keep Intake, Review, POC Drafts, and Approval/Export visible at 1440px with text and icon states. (AC-001)
- [ ] Open available stages while preserving the active case and selected deficiency. (AC-002)
- [ ] Leave the current screen unchanged and state the blocker when a blocked stage is selected. (AC-002)
