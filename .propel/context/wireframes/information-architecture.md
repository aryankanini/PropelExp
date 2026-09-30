# Information Architecture - CMS Deficiency Action Planner

## 1. Wireframe Specification

**Fidelity Level**: High  
**Screen Type**: Responsive web, desktop-first  
**Viewport**: 1440 x 1024 baseline; validated adaptations specified for 375, 768, and 1920 pixels

## 2. System Overview

The localhost application guides a compliance reviewer from CMS-2567 intake through evidence-linked extraction review and five-part POC authoring. A designated compliance leader approves the current revision before copy or download. Case content exists only for the transient working session.

## 3. Wireframe References

### Generated Wireframes

**Figma Wireframes**: No Figma file exists for this MVP.

**HTML/Image Wireframes**:

| Screen/Feature | File Path | Description | Fidelity | Date Created |
|---|---|---|---|---|
| SCR-002 Document intake | [Hi-Fi/wireframe-SCR-002-document-intake.html](Hi-Fi/wireframe-SCR-002-document-intake.html) | Bounded upload and session notice | High | 2026-09-23 |
| SCR-003 Processing progress | [Hi-Fi/wireframe-SCR-003-processing-progress.html](Hi-Fi/wireframe-SCR-003-processing-progress.html) | Ordered stages and retry | High | 2026-09-23 |
| SCR-004 Extraction review | [Hi-Fi/wireframe-SCR-004-extraction-review.html](Hi-Fi/wireframe-SCR-004-extraction-review.html) | Synchronized fields and evidence | High | 2026-09-23 |
| SCR-005 Uncertainty resolution | [Hi-Fi/wireframe-SCR-005-uncertainty-resolution.html](Hi-Fi/wireframe-SCR-005-uncertainty-resolution.html) | Candidate comparison and correction | High | 2026-09-23 |
| SCR-006 POC authoring | [Hi-Fi/wireframe-SCR-006-poc-authoring.html](Hi-Fi/wireframe-SCR-006-poc-authoring.html) | Five-part draft editing | High | 2026-09-23 |
| SCR-007 Approval review | [Hi-Fi/wireframe-SCR-007-approval-review.html](Hi-Fi/wireframe-SCR-007-approval-review.html) | Leader-only revision approval | High | 2026-09-23 |
| SCR-008 Approved export | [Hi-Fi/wireframe-SCR-008-approved-export.html](Hi-Fi/wireframe-SCR-008-approved-export.html) | Labeled copy, download, and cleanup | High | 2026-09-23 |

### Component Inventory

See [Component Inventory](component-inventory.md) for component placement, states, responsive behavior, reuse, and accessibility.

## 4. User Personas & Flows

### Persona 1: Compliance Reviewer

- **Role**: Uploads, verifies, corrects, generates, and edits.
- **Goals**: Confirm every deficiency against evidence and prepare a grounded POC.
- **Key Screens**: SCR-002 through SCR-006 and SCR-008.
- **Primary Flow**: Upload -> processing -> review -> resolve -> author POC.
- **Wireframe References**: SCR-002 through SCR-006.
- **Decision Points**: Replace invalid input, resolve or defer uncertain values, correct extracted values, and complete missing information.

### Persona 2: Compliance Leader

- **Role**: Reviews and approves the current complete POC revision.
- **Goals**: Verify evidence, provenance, completeness, and revision alignment before export.
- **Key Screens**: SCR-004, SCR-006, SCR-007, and SCR-008.
- **Primary Flow**: Review current revision -> approve or request changes -> export.
- **Wireframe References**: SCR-007 and SCR-008.
- **Decision Points**: Approve the current revision or return it for changes.

### User Flow Diagrams

- **FL-002**: SCR-002 -> SCR-003 -> SCR-004 <-> SCR-005.
- **FL-003**: SCR-004 -> SCR-006 -> SCR-007.
- **FL-004**: SCR-007 -> SCR-008, or SCR-007 -> SCR-006 for changes.
- **FL-005**: SCR-002 or SCR-008 -> end-session confirmation -> SCR-002 empty state.
- **FL-006**: SCR-003 or SCR-006 error -> retry -> review-ready state.

## 5. Screen Hierarchy

### Level 1: Active Case Workspace

- **SCR-002 Document intake** (P0 - Critical) - Upload, limits, validation, and cleanup entry.
- **SCR-003 Processing progress** (P0 - Critical) - Ordered extraction stages and failed-operation recovery.
- **SCR-004 Extraction review** (P0 - Critical) - Deficiency navigation, editable values, and page evidence.
- **SCR-005 Uncertainty resolution** (P0 - Critical) - Supported candidate selection or user-authored correction.
- **SCR-006 POC authoring** (P0 - Critical) - Fixed five-section editor and revision state.
- **SCR-007 Approval review** (P0 - Critical) - Read-only leader approval package.
- **SCR-008 Approved export** (P0 - Critical) - Revision-matched copy, download, and session end.

### Screen Priority Legend (closed set)

- **P0**: Critical path screens.
- **P1**: High-priority supporting screens.
- **P2**: Medium-priority screens.
- **P3**: Low-priority screens.

### Modal/Dialog/Overlay Inventory

| Modal/Dialog Name | Type | Trigger Context | Parent Screen | Wireframe Reference | Priority |
|---|---|---|---|---|---|
| Inactivity warning | Modal | Session approaches timeout | SCR-002 through SCR-008 | Parent state specification | P0 |
| End session | Confirmation dialog | End session command | SCR-002, SCR-008 | Embedded in parent wireframes | P0 |
| Replace document | Confirmation dialog | Invalid replacement upload | SCR-002 | Parent state specification | P1 |
| Deficiency navigator | Drawer | Narrow viewport list command | SCR-004 through SCR-007 | Responsive parent behavior | P0 |
| Evidence detail | Drawer | Expand source evidence | SCR-004, SCR-005, SCR-007 | Parent evidence pane | P1 |
| Revision history | Drawer | Open provenance or revision | SCR-004 through SCR-008 | Parent state specification | P1 |
| Copy confirmation | Toast | Copy approved draft | SCR-008 | Embedded in SCR-008 | P0 |
| Processing failure details | Modal | Open safe diagnostics | SCR-003, SCR-006 | Embedded in SCR-006; state in SCR-003 | P0 |

Modal focus is trapped, Escape cancels non-destructive overlays, and focus returns to the trigger. On mobile, drawers and dialogs use the available viewport without obscuring recovery actions.

## 6. Navigation Architecture

```text
Intake (SCR-002)
+-- Processing (SCR-003)
    +-- Extraction review (SCR-004)
        +-- Uncertainty resolution (SCR-005)
        +-- POC authoring (SCR-006)
            +-- Approval review (SCR-007)
                +-- Approved export (SCR-008)
```

### Navigation Patterns

- **Primary Navigation**: Persistent four-stage workflow rail with current, complete, blocked, and unavailable text states.
- **Secondary Navigation**: Deficiency list and local breadcrumb preserve case and F-tag context.
- **Mobile Navigation**: Compact horizontal stage summary; deficiency navigation becomes a bounded list or drawer.

## 7. Interaction Patterns

### Pattern 1: Evidence-Linked Review

- **Trigger**: Select a deficiency or extracted field.
- **Flow**: Select value -> inspect synchronized page evidence -> correct or confirm -> save revision.
- **Screens Involved**: SCR-004 and SCR-005.
- **Feedback**: Provenance, confidence, save confirmation, and explicit blockers.
- **Components Used**: DeficiencyList, FieldEditor, CandidateComparison, EvidenceViewer, Alert.

### Pattern 2: Current-Revision Approval

- **Trigger**: A complete POC is sent for approval.
- **Flow**: Review evidence and five sections -> approve or request changes -> export if approved.
- **Screens Involved**: SCR-006, SCR-007, and SCR-008.
- **Feedback**: Revision status, completeness checklist, approval identity, and export lock reason.
- **Components Used**: PocSection, RevisionStatus, CompletenessChecklist, Button, DraftPreview.

## 8. Error Handling

### Error Scenario 1: Processing Failure

- **Trigger**: OCR, extraction, or drafting provider failure.
- **Error Screen/State**: SCR-003 or SCR-006 Error preview.
- **User Action**: Review safe diagnostics and retry the failed operation.
- **Recovery Flow**: Preserve reviewed work -> retry only failed stage -> return output for review.

### Error Scenario 2: Validation or Stale Approval

- **Trigger**: Required value unresolved, section incomplete, or approval revision mismatch.
- **Error Screen/State**: Validation preview on SCR-004 through SCR-008.
- **User Action**: Resolve the named blocker or obtain reapproval.
- **Recovery Flow**: Return to owning screen -> correct current revision -> re-enter approval.

## 9. Responsive Strategy

| Breakpoint | Width | Layout Changes | Navigation Changes | Component Adaptations |
|---|---:|---|---|---|
| Mobile | 375px | Single column; dense panes stack | Compact stage summary | 44px targets; evidence follows primary task |
| Tablet | 768px | Two-stage stacked workspace | 72px collapsed rail | Evidence stacks below editor |
| Desktop | 1440px | Rail plus multi-pane work area | Expanded 248px rail | Synchronized list, editor, and evidence panes |
| Large | 1920px+ | Workspace max-width cap | Expanded rail | Readable measures remain bounded |

### Responsive Wireframe Variants

- **Mobile variants**: Responsive CSS within each canonical file.
- **Tablet variants**: Responsive CSS within each canonical file.
- **Desktop variants**: Canonical 1440px HTML files.

## 10. Accessibility

### WCAG Compliance

- **Target Level**: WCAG 2.2 AA.
- **Color Contrast**: Semantic tokens are designed for 4.5:1 text and 3:1 UI/focus thresholds.
- **Keyboard Navigation**: Native controls, visible focus, logical reading order, and Escape dismissal.
- **Screen Reader Support**: Landmarks, associated labels, alerts, status regions, and current-step semantics.

### Accessibility Considerations by Screen

| Screen | Key Accessibility Features | Wireframe Notes |
|---|---|---|
| SCR-002 | Named upload, dialog focus restoration | Limits remain visible near control |
| SCR-003 | Progress semantics and status feedback | Terminal failure announced once |
| SCR-004 | Named regions and synchronized selection | Source and current values stay distinct |
| SCR-005 | Radio group and mutually exclusive correction | Unresolved path remains available |
| SCR-006 | Section headings and provenance | Missing information is textual, not color-only |
| SCR-007 | Read-only review and role-aware action | Approval bound to visible revision |
| SCR-008 | Status toast, functional copy/download | Export label included in output |

### Focus Order

Header -> workflow rail -> local navigation -> primary content -> evidence/context pane -> page actions. Modal focus begins at the safest action and returns to its trigger.

## 11. Content Strategy

### Content Hierarchy

- **H1**: Current task or object.
- **H2**: Major evidence, POC, or decision region.
- **Body Text**: Calm, precise, action-oriented compliance language.
- **Placeholder Content**: No lorem ipsum; high-fidelity screens use synthetic domain records from [data/sample-data.json](data/sample-data.json).

### Content Types by Screen

| Screen | Content Types | Wireframe Reference |
|---|---|---|
| SCR-002 | File input, limits, validation, cleanup | Document intake |
| SCR-003 | Stage timeline, progress, failure recovery | Processing progress |
| SCR-004 | Deficiency list, editable fields, evidence | Extraction review |
| SCR-005 | Candidates, correction, source snippet | Uncertainty resolution |
| SCR-006 | Five text sections, provenance, revision | POC authoring |
| SCR-007 | Read-only POC, checklist, approval | Approval review |
| SCR-008 | Approval metadata, draft preview, export | Approved export |