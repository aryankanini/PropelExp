# Task - TASK_002 Preview Required Export Label

## Requirement Reference

- **User Story:** US_035
- **Story Location:** .propel/context/tasks/EP-005/us_035/us_035.md
- **Acceptance Criteria:**
  - **AC-001: Required export prefix**
    - **Given**: Current approved content is copied or downloaded
    - **When**: The export is produced
    - **Then**: It begins with `DRAFT - Approved for compliance handling; not submitted to CMS.`
  - **AC-002: No external submission**
    - **Given**: An export completes
    - **When**: Network interactions are inspected
    - **Then**: No POC content is submitted to CMS or a survey agency
- **Edge Cases:**
  - Empty or whitespace-only approved content cannot produce an export containing only the label.

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
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | UXR-002 requires a clear approved-export preview without implying external submission. |

---

## Task Overview

Implement the EP-005 / US_035 export preview that visibly begins with the exact required label, disables empty-content export, and describes copy/download as local actions only. Estimated effort: 4 hours.

## Dependent Tasks

- US_034 - Same-Epic - Requires approved current export content.
- TASK_001 Prefix and Isolate Export Content - provides labeled local-only export payloads.

## Impacted Components

- New labeled export preview and empty-content state within SCR-008.

## Implementation Plan

1. Render the server-provided required label as the first preview content.
2. Keep copy/download language local and avoid submission affordances.
3. Disable actions and show a precise reason for empty approved content.

## Current Project State

```text
frontend/src/
├── features/approval-export/       # Planned; frontend implementation directory is not yet present
├── shared/model/
└── shared/ui/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/features/approval-export/LabeledExportPreview.tsx | Preview the exact label before approved content. |
| CREATE | frontend/src/shared/model/labeledExport.ts | Define labeled and empty export view states. |
| CREATE | frontend/src/shared/ui/Alert.tsx | Present semantic empty-content and local-delivery notices. |

## External References

- [React 19.3 reference](https://react.dev/versions#react-19)
- [TypeScript 7.0 documentation](https://www.typescriptlang.org/docs/)
- [Vite 8 guide](https://vite.dev/guide/)

## Build Commands

- [Frontend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [x] Unit tests pass for exact label placement, local-only copy, and empty-content disabled state.
- [x] Integration tests pass for labeled copy/download previews.

## Implementation Checklist

- [x] Show `DRAFT - Approved for compliance handling; not submitted to CMS.` as the first export preview content. (AC-001)
- [x] Present copy and download as local actions with no CMS or survey-agency submission affordance. (AC-002)
- [x] Disable export when approved content is empty or whitespace-only. (AC-001)
