# Component Inventory - CMS Deficiency Action Planner

## Component Specification

**Fidelity Level**: High  
**Screen Type**: Responsive web  
**Viewport**: 1440 x 1024 baseline

## Component Summary

| Component Name | Type | Screens Used | Priority | Implementation Status |
|---|---|---|---|---|
| AppShell | Layout | SCR-001 through SCR-008 | High | Wireframed |
| WorkflowRail | Navigation | SCR-002 through SCR-008 | High | Wireframed |
| DeficiencyList | Navigation | SCR-004 | High | Wireframed |
| EvidenceViewer | Content | SCR-004, SCR-005, SCR-007 | High | Wireframed |
| FieldEditor | Interactive | SCR-004 | High | Wireframed |
| CandidateComparison | Interactive | SCR-005 | High | Wireframed |
| PocSection | Content/Interactive | SCR-006, SCR-007, SCR-008 | High | Wireframed |
| Button and IconButton | Interactive | All | High | Wireframed |
| Alert and Status | Feedback | All | High | Wireframed |
| StageTimeline | Feedback | SCR-003 | High | Wireframed |
| Modal and Toast | Feedback | SCR-002, SCR-006, SCR-008 | High | Wireframed |

## Detailed Component Specifications

### Layout Components

#### AppShell

- **Type**: Layout
- **Used In Screens**: All screens.
- **Wireframe References**: [Information architecture](information-architecture.md).
- **Description**: Header, workflow rail, main region, and optional context pane.
- **Variants**: Authentication, workspace, multi-pane.
- **Interactive States**: Default, loading, empty, error, validation.
- **Responsive Behavior**: 248px desktop rail; 72px tablet rail; compact mobile stage summary.
- **Implementation Notes**: Semantic landmarks and bounded workspace width.

### Navigation Components

#### WorkflowRail

- **Type**: Navigation
- **Used In Screens**: SCR-002 through SCR-008.
- **Wireframe References**: All workspace HTML files.
- **Description**: Shows Intake, Review, POC drafts, and Approval/Export state.
- **Variants**: Complete, current, blocked, available, unavailable.
- **Interactive States**: Default, hover, focus, active/current, disabled.
- **Responsive Behavior**: Expanded desktop, collapsed tablet, horizontal mobile summary.
- **Implementation Notes**: Use `aria-current="step"` for the current stage.

#### DeficiencyList

- **Type**: Navigation
- **Used In Screens**: SCR-004; drawer pattern on SCR-005 through SCR-007.
- **Wireframe References**: [SCR-004](Hi-Fi/wireframe-SCR-004-extraction-review.html).
- **Description**: Searchable F-tag list with independent review and POC status.
- **Variants**: Selected, confirmed, needs review, draft, approved.
- **Interactive States**: Default, hover, focus, active, loading, empty.
- **Responsive Behavior**: Persistent desktop list; bounded tablet/mobile list or drawer.
- **Implementation Notes**: Paginate after 25 records.

### Content Components

#### EvidenceViewer

- **Type**: Content
- **Used In Screens**: SCR-004, SCR-005, SCR-007.
- **Wireframe References**: [SCR-004](Hi-Fi/wireframe-SCR-004-extraction-review.html), [SCR-005](Hi-Fi/wireframe-SCR-005-uncertainty-resolution.html).
- **Description**: Page, extraction method, snippet, confidence, and highlighted support.
- **Variants**: Default, loading, empty, failed page, error, highlighted.
- **Interactive States**: Page navigation default, hover, focus, active, disabled.
- **Responsive Behavior**: Context pane on desktop; stacked region or drawer below 1100px.
- **Implementation Notes**: Keep authoritative content untruncated and near a 68-character measure.

#### PocSection

- **Type**: Content and interactive
- **Used In Screens**: SCR-006, SCR-007, SCR-008.
- **Wireframe References**: [SCR-006](Hi-Fi/wireframe-SCR-006-poc-authoring.html), [SCR-007](Hi-Fi/wireframe-SCR-007-approval-review.html), [SCR-008](Hi-Fi/wireframe-SCR-008-approved-export.html).
- **Description**: One of five fixed POC sections with content, provenance, and completion state.
- **Variants**: Editable, read-only, AI-generated, user-edited, missing information, approved.
- **Interactive States**: Default, focus, disabled/read-only, loading, error.
- **Responsive Behavior**: Full-width stacked sections at all breakpoints.
- **Implementation Notes**: Minimum editor height 160px; editing revokes approval.

### Interactive Components

#### FieldEditor and CandidateComparison

- **Type**: Interactive
- **Used In Screens**: SCR-004 and SCR-005.
- **Wireframe References**: Extraction review and uncertainty resolution.
- **Description**: Preserves original values while allowing correction or supported candidate selection.
- **Variants**: Extracted, user-edited, uncertain, conflict, confirmed.
- **Interactive States**: Default, hover, focus, active, disabled, loading, error.
- **Responsive Behavior**: Editor precedes evidence when stacked.
- **Implementation Notes**: Candidate selection and correction are mutually exclusive.

#### Button and IconButton

- **Type**: Interactive
- **Used In Screens**: All screens.
- **Wireframe References**: All HTML wireframes.
- **Description**: Primary, secondary, destructive, and compact utility commands.
- **Variants**: Primary, secondary, tertiary/ghost, destructive; small, medium, large.
- **Interactive States**: Default, hover, active, focus, disabled, loading, error where applicable.
- **Responsive Behavior**: At least 44px high; actions stack on narrow screens.
- **Implementation Notes**: Stable dimensions; blocked actions include a visible reason.

### Feedback Components

#### Alert, StageTimeline, Modal, Toast

- **Type**: Feedback
- **Used In Screens**: All screens; specialized timeline on SCR-003.
- **Wireframe References**: Processing, authoring, and export wireframes.
- **Description**: Announces validation, progress, terminal failure, destructive confirmation, and copy success.
- **Variants**: Info, success, warning, danger; persistent/dismissible; determinate/indeterminate.
- **Interactive States**: Default, focus, loading, error.
- **Responsive Behavior**: Stable inline regions; modals use available mobile width.
- **Implementation Notes**: Polite status for progress; assertive alert for terminal failure; modal focus restoration.

## Component Relationships

```text
AppShell
+-- AppHeader
+-- WorkflowRail
+-- Primary Content
|   +-- DeficiencyList
|   +-- FieldEditor / CandidateComparison / PocSection
|   +-- Alert / StageTimeline
+-- Context Pane
    +-- EvidenceViewer / CompletenessChecklist
+-- Overlays
    +-- Modal / Drawer / Toast
```

## Component States Matrix

| Component | Default | Hover | Active | Focus | Disabled | Error | Loading | Empty |
|---|---|---|---|---|---|---|---|---|
| Button/IconButton | Yes | Yes | Yes | Yes | Yes | Contextual | Yes | N/A |
| TextField/TextArea | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| WorkflowRail | Yes | Yes | Current | Yes | Yes | N/A | N/A | N/A |
| DeficiencyList | Yes | Yes | Selected | Yes | Yes | Yes | Yes | Yes |
| EvidenceViewer | Yes | N/A | Highlighted | Region | N/A | Yes | Yes | Yes |
| PocSection | Yes | N/A | Edited | Yes | Read-only | Yes | Yes | Yes |
| Modal | Yes | N/A | N/A | Trapped | N/A | Yes | Loading | N/A |

## Reusability Analysis

| Component | Reuse Count | Screens | Recommendation |
|---|---:|---|---|
| AppShell | 8 | All | Shared application component |
| WorkflowRail | 7 | SCR-002 through SCR-008 | Shared navigation component |
| Button | 8 | All | Shared action component |
| Alert | 8 | All | Shared feedback component |
| EvidenceViewer | 3 | SCR-004, SCR-005, SCR-007 | Shared feature component |
| PocSection | 3 | SCR-006 through SCR-008 | Shared editable/read-only variants |

## Responsive Breakpoints Summary

| Breakpoint | Width | Components Affected | Key Adaptations |
|---|---:|---|---|
| Mobile | 375px | AppShell, rail, panes, actions, modal | Single column, stage summary, stacked actions |
| Tablet | 768px | AppShell, rail, evidence, list | Collapsed rail and stacked evidence |
| Desktop | 1440px | All | Expanded rail and synchronized panes |
| Large | 1920px+ | AppShell and text regions | Max-width caps and bounded measures |

## Implementation Priority Matrix

### High Priority (Core Components)

- [ ] AppShell and WorkflowRail - Required across the active case.
- [ ] Button, fields, Alert, and Modal - Required for all interactions and recovery.
- [ ] EvidenceViewer and FieldEditor - Required for evidence verification.
- [ ] PocSection and RevisionStatus - Required for authoring and approval.

### Medium Priority (Feature Components)

- [ ] Deficiency drawer and RevisionHistory - Important responsive and provenance support.
- [ ] StageTimeline and DiagnosticDetails - Processing transparency and recovery.

### Low Priority (Enhancement Components)

- [ ] Evidence find control - Useful for long SOD review after measured need.

## Framework-Specific Notes

**Detected Framework**: Planned React 19.3 and TypeScript 7.0; no implementation package exists yet.  
**Component Library**: Custom components using the documented design system and Lucide icons.

### Framework Patterns Applied

- Feature-sliced ownership for intake, extraction review, POC authoring, and approval/export.
- Semantic native controls with controlled state and generated API contracts.

### Component Library Mappings

| Wireframe Component | Framework Component | Customization Required |
|---|---|---|
| Button | `shared/ui/Button` | Variants, stable loading width, blocked-state reason |
| EvidenceViewer | `features/extraction-review/EvidenceViewer` | Source page, snippet, confidence, failure states |
| PocSection | `features/poc-authoring/PocSection` | Five section types and provenance |
| Modal | `shared/ui/Modal` | Focus trap, Escape rules, restoration |

## Accessibility Considerations

| Component | ARIA Attributes | Keyboard Navigation | Screen Reader Notes |
|---|---|---|---|
| WorkflowRail | Navigation label, `aria-current="step"` | Tab through available stages | Announces stage and state text |
| CandidateComparison | Fieldset/legend or radiogroup | Tab then arrow keys | Announces candidate evidence and confidence |
| EvidenceViewer | Named region and description | Page controls by Tab/Enter | Includes page and extraction method |
| Alert | `role="alert"` for terminal errors | Focus summary after submit | Announces once with recovery action |
| Modal | `role="dialog"`, `aria-modal` | Trapped Tab; Escape cancels | Title and description announced |

## Design System Integration

**Design System Reference**: [Design system](../docs/designsystem.md)

### Components Matching Design System

- [x] AppShell, WorkflowRail, Button, fields, EvidenceViewer, PocSection, Alert, StageTimeline, Modal, and Toast use semantic intent.
- [x] Interactive controls expose required states and 44px minimum targets.

### New Components to Add to Design System

- [ ] None. The wireframes remain within the declared component set.