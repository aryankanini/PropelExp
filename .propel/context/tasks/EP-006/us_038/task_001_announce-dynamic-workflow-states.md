# Task - TASK_001 Announce Dynamic Workflow States

## Requirement Reference

- **User Story:** US_038
- **Story Location:** .propel/context/tasks/EP-006/us_038/us_038.md
- **Acceptance Criteria:**
  - **AC-001: Progress announcement**
    - **Given**: An asynchronous job changes stage or percent
    - **When**: The update reaches the UI
    - **Then**: A polite live region announces the meaningful change once using text and status semantics
  - **AC-002: Terminal failure**
    - **Given**: Submission or processing reaches a terminal error
    - **When**: The error appears
    - **Then**: An assertive alert announces it and focus moves to the linked error summary
- **Edge Cases:**
  - Frequent progress events are coalesced to avoid repeated announcements without hiding terminal status.

---

## Design References

| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A - pending Figma file |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/ |
| **Screen Spec** | SCR-002, SCR-003, SCR-004, SCR-006, SCR-007, SCR-008 |
| **UXR Requirements** | UXR-202 |
| **Design Tokens** | .propel/context/docs/designsystem.md#design-tokens; .propel/context/docs/designsystem.md#accessibility-requirements |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | UXR-202 requires meaningful live-region and alert semantics for dynamic workflows. |

---

## Task Overview

Implement the EP-006 / US_038 shared announcement system that coalesces meaningful progress updates, announces terminal failures assertively, and moves focus to linked error summaries. Estimated effort: 8 hours.

## Dependent Tasks

- US_020 - Foundational - Requires ordered progress events.

## Impacted Components

- New announcement model, polite live region, assertive alert, and error summary.

## Implementation Plan

1. Map ordered events to meaningful stage/percent announcement messages.
2. Coalesce repeated progress while preserving terminal events.
3. Render polite status updates once per meaningful change.
4. Announce terminal errors assertively and focus their linked summary.

## Current Project State

```text
frontend/src/
├── shared/model/                   # Planned; frontend implementation directory is not yet present
└── shared/ui/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/shared/model/announcements.ts | Coalesce ordered events into meaningful announcement states. |
| CREATE | frontend/src/shared/ui/LiveRegion.tsx | Announce polite progress changes once. |
| CREATE | frontend/src/shared/ui/Alert.tsx | Announce terminal failures assertively. |
| CREATE | frontend/src/shared/ui/ErrorSummary.tsx | Link failures and receive focus after terminal errors. |

## External References

- [WAI-ARIA live regions](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/)
- [WCAG 2.2 status messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)
- [React 19.3 reference](https://react.dev/versions#react-19)

## Build Commands

- [Frontend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [ ] Unit tests pass for event coalescing, one-time polite announcements, and terminal alerts.
- [ ] Integration tests pass for screen-reader semantics and focus movement to linked errors.

## Implementation Checklist

- [ ] Announce each meaningful stage or percent change once through a polite text status region. (AC-001)
- [ ] Announce terminal errors assertively and move focus to the linked error summary. (AC-002)
- [ ] Coalesce frequent progress events without hiding terminal status. (AC-001, AC-002)
