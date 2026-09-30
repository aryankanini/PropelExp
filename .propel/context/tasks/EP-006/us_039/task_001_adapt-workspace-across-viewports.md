# Task - TASK_001 Adapt Workspace Across Viewports

## Requirement Reference

- **User Story:** US_039
- **Story Location:** .propel/context/tasks/EP-006/us_039/us_039.md
- **Acceptance Criteria:**
  - **AC-001: Desktop and tablet**
    - **Given**: A screen is 1440 or 768 pixels wide
    - **When**: Evidence work loads
    - **Then**: Desktop shows rail and multiple panes while tablet uses a collapsible rail and stacked evidence without losing page context
  - **AC-002: Essential mobile**
    - **Given**: A screen is 375 pixels wide
    - **When**: Review or recovery loads
    - **Then**: Status, evidence summary, confirmation, and recovery remain available while dense editing directs users to a larger viewport
- **Edge Cases:**
  - At 200% zoom, secondary panes collapse before horizontal scrolling is introduced.

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
| **UXR Requirements** | UXR-301 |
| **Design Tokens** | .propel/context/docs/designsystem.md#design-tokens; .propel/context/docs/designsystem.md#accessibility-requirements |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | UXR-301 requires desktop, tablet, essential mobile, and 200% zoom compositions. |

---

## Task Overview

Implement the EP-006 / US_039 responsive workspace composition for 1440px multi-pane evidence work, 768px stacked evidence, 375px essential review/recovery, and zoom-first pane collapse. Estimated effort: 8 hours.

## Dependent Tasks

- US_036 - Same-Epic - Requires the shared workspace structure.
- US_036 TASK_001 Build Persistent Workflow Rail - provides the responsive shell regions.

## Impacted Components

- New responsive shell styles and adaptive split-pane behavior.

## Implementation Plan

1. Define desktop, tablet, and essential-mobile layout rules.
2. Keep rail and multiple panes at 1440px.
3. Collapse the rail and stack evidence with page context at 768px.
4. Retain essential mobile actions and collapse secondary panes before overflow at 200% zoom.

## Current Project State

```text
frontend/src/
├── app/                            # Planned; frontend implementation directory is not yet present
└── shared/ui/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/app/responsive.css | Define 1440px, 768px, 375px, and zoom-reflow compositions. |
| CREATE | frontend/src/shared/ui/SplitPane.tsx | Adapt evidence panes while preserving page context. |
| CREATE | frontend/src/shared/ui/ViewportNotice.tsx | Direct dense mobile editing to a larger viewport. |

## External References

- [CSS Media Queries Level 5](https://www.w3.org/TR/mediaqueries-5/)
- [WCAG 2.2 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)
- [React 19.3 reference](https://react.dev/versions#react-19)

## Build Commands

- [Frontend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [ ] Unit tests pass for responsive state selection and larger-viewport guidance.
- [ ] Integration tests pass at 1440px, 768px, 375px, and 200% zoom without incoherent overlap.

## Implementation Checklist

- [ ] Show the rail and multiple panes at 1440px, and a collapsible rail with stacked evidence at 768px without losing page context. (AC-001)
- [ ] Keep status, evidence summary, confirmation, and recovery available at 375px while directing dense editing to a larger viewport. (AC-002)
- [ ] Collapse secondary panes before introducing horizontal scrolling at 200% zoom. (AC-001, AC-002)
