# Task - TASK_001 Make Workspace WCAG Accessible

## Requirement Reference

- **User Story:** US_037
- **Story Location:** .propel/context/tasks/EP-006/us_037/us_037.md
- **Acceptance Criteria:**
  - **AC-001: Keyboard and focus**
    - **Given**: Any application screen
    - **When**: The workflow is operated by keyboard
    - **Then**: Every control is reachable in logical order and visible focus meets 3:1 contrast
  - **AC-002: Zoom and motion**
    - **Given**: The browser is at 200% zoom or reduced motion is enabled
    - **When**: A screen renders
    - **Then**: Content remains usable in reading order and nonessential transitions are removed
- **Edge Cases:**
  - A modal traps focus while open and returns focus to its trigger on cancel.

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
| **UXR Requirements** | UXR-201 |
| **Design Tokens** | .propel/context/docs/designsystem.md#design-tokens; .propel/context/docs/designsystem.md#accessibility-requirements |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | UXR-201 requires WCAG 2.2 AA keyboard, focus, zoom, and reduced-motion behavior. |

---

## Task Overview

Implement the EP-006 / US_037 shared accessibility foundations for logical keyboard order, 3:1 visible focus, 200% zoom reflow, reduced motion, and modal focus management. Estimated effort: 8 hours.

## Dependent Tasks

- US_036 - Same-Epic - Requires the shared workspace shell.
- US_036 TASK_001 Build Persistent Workflow Rail - provides the shell and primary navigation order.

## Impacted Components

- New accessible modal, split-pane, and shell accessibility styles.

## Implementation Plan

1. Establish landmark, skip-link, and logical focus order in the shell.
2. Define focus-visible and reduced-motion styles from semantic tokens.
3. Make split panes reflow in reading order at 200% zoom.
4. Trap modal focus and restore it to the cancel trigger.

## Current Project State

```text
frontend/src/
├── app/                            # Planned; frontend implementation directory is not yet present
└── shared/ui/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/app/accessibility.css | Define focus, reflow, reduced-motion, and skip-link behavior. |
| CREATE | frontend/src/shared/ui/Modal.tsx | Trap focus while open and restore focus on cancel. |
| CREATE | frontend/src/shared/ui/SplitPane.tsx | Preserve reading order and reflow at 200% zoom. |
| CREATE | frontend/src/shared/ui/SkipLink.tsx | Provide keyboard access to primary content. |

## External References

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA APG modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
- [React 19.3 reference](https://react.dev/versions#react-19)

## Build Commands

- [Frontend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [ ] Unit tests pass for keyboard order, focus restoration, and reduced-motion behavior.
- [ ] Integration tests pass at 200% zoom and with keyboard-only modal operation.

## Implementation Checklist

- [ ] Make every control keyboard reachable in logical order with visible focus meeting 3:1 contrast. (AC-001)
- [ ] Preserve usable reading order at 200% zoom and remove nonessential transitions for reduced motion. (AC-002)
- [ ] Trap focus in open modals and return it to the trigger on cancel. (AC-001)
