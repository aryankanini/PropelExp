# Design Reference

> **Note**: This reference applies to the UI-impacting CMS Deficiency Action Planner workflow defined by FR-001 through FR-020 and UC-001 through UC-010.

## UI Impact Assessment

**Has UI Changes**: [x] Yes [ ] No

The project creates a new responsive web interface for authentication, document intake, extraction review, POC authoring, approval, export, recovery, and transient-session cleanup.

## User Story Design Context

**Story ID**: US-ALL
**Story Title**: Complete CMS deficiency review and POC workflow
**UI Impact Type**: New UI

### Aesthetic Direction

- **Direction**: Utilitarian `[SOURCE:INPUT]`
- **Rationale**: The interface serves compliance reviewers performing repeated, evidence-heavy tasks under regulatory and privacy constraints. A utilitarian direction prioritizes information density, keyboard efficiency, restrained semantic color, and clear workflow state while avoiding decoration that could compete with source evidence or suggest unsupported certainty.
- **Precedents**: Sentry, Grafana, PostHog.
- **Anti-brief**: Do not resemble a consumer wellness product, marketing dashboard, glassmorphic AI assistant, or literal government-form reproduction.
- **Basis**: This direction is inferred from the compliance domain, dense evidence-review workflow, and user-confirmed restrained trust-focused visual constraint.

### Design Source References

- **Figma Project**: Not yet created; this document defines the source structure for the future Figma file.
- **Design Images**: Not applicable; no upstream design images were provided.
- **Design System**: This document is the canonical design reference; `.propel/context/docs/figma_spec.md` is the canonical screen and flow specification.
- **Brand Guidelines**: No external brand guide. Use the trust-focused visual direction and do not use CMS or government marks.

### Screen-to-Design Mappings

**Option A: Figma Frame Mappings**

| Screen/Feature | Figma Frame ID | Direct Link | Description | Implementation Priority |
|---|---|---|---|---|
| Sign in | Pending | Pending Figma file | Local credential entry and safe authentication feedback | High |
| Document intake | Pending | Pending Figma file | Bounded CMS-2567 upload and validation | High |
| Processing progress | Pending | Pending Figma file | Ordered extraction/OCR stages and recovery | High |
| Extraction review | Pending | Pending Figma file | Evidence-linked provider and deficiency review | High |
| Uncertainty resolution | Pending | Pending Figma file | Candidate comparison and reviewer correction | High |
| POC authoring | Pending | Pending Figma file | Five-part generated and user-edited draft | High |
| Approval review | Pending | Pending Figma file | Leader-only current-revision approval | High |
| Approved export | Pending | Pending Figma file | Copy/download gate and transient session end | High |

### Design Tokens

~~~yaml
primitive_tokens:
  color:
    neutral:
      0: "oklch(0.995 0.003 205)"
      50: "oklch(0.975 0.006 205)"
      100: "oklch(0.945 0.008 205)"
      200: "oklch(0.890 0.010 205)"
      300: "oklch(0.805 0.012 205)"
      400: "oklch(0.675 0.014 205)"
      500: "oklch(0.555 0.016 205)"
      600: "oklch(0.445 0.017 205)"
      700: "oklch(0.335 0.018 205)"
      800: "oklch(0.235 0.018 205)"
      900: "oklch(0.145 0.016 205)"
      950: "oklch(0.090 0.014 205)"
    teal:
      50: "oklch(0.970 0.025 190)"
      100: "oklch(0.925 0.045 190)"
      200: "oklch(0.850 0.070 190)"
      300: "oklch(0.755 0.095 190)"
      400: "oklch(0.650 0.110 190)"
      500: "oklch(0.555 0.105 190)"
      600: "oklch(0.465 0.095 190)"
      700: "oklch(0.385 0.080 190)"
      800: "oklch(0.305 0.060 190)"
      900: "oklch(0.225 0.042 190)"
    red:
      50: "oklch(0.970 0.025 25)"
      100: "oklch(0.925 0.050 25)"
      500: "oklch(0.570 0.190 25)"
      700: "oklch(0.420 0.160 25)"
      900: "oklch(0.260 0.090 25)"
    amber:
      50: "oklch(0.975 0.025 85)"
      100: "oklch(0.930 0.060 85)"
      500: "oklch(0.700 0.150 75)"
      800: "oklch(0.390 0.090 75)"
    blue:
      50: "oklch(0.970 0.020 245)"
      100: "oklch(0.925 0.045 245)"
      500: "oklch(0.590 0.150 245)"
      800: "oklch(0.350 0.100 245)"
  spacing_px: [0, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96]
  radius_px: [0, 2, 4, 8, 9999]
  duration_ms: [80, 120, 180, 240, 320]

semantic_tokens:
  light:
    text-primary: "{color.neutral.900}"
    text-secondary: "{color.neutral.700}"
    text-muted: "{color.neutral.600}"
    text-on-accent: "{color.neutral.0}"
    surface-canvas: "{color.neutral.50}"
    surface-raised: "{color.neutral.0}"
    surface-sunken: "{color.neutral.100}"
    surface-accent: "{color.teal.50}"
    border-subtle: "{color.neutral.200}"
    border-strong: "{color.neutral.400}"
    border-focus: "{color.teal.600}"
    action-primary: "{color.teal.700}"
    action-primary-hover: "{color.teal.800}"
    action-primary-active: "{color.teal.900}"
    action-primary-disabled: "{color.neutral.300}"
    feedback-success: "{color.teal.700}"
    feedback-warning: "{color.amber.800}"
    feedback-danger: "{color.red.700}"
    feedback-info: "{color.blue.800}"
  dark:
    text-primary: "{color.neutral.50}"
    text-secondary: "{color.neutral.200}"
    text-muted: "{color.neutral.300}"
    text-on-accent: "{color.neutral.950}"
    surface-canvas: "{color.neutral.950}"
    surface-raised: "{color.neutral.900}"
    surface-sunken: "{color.neutral.950}"
    surface-accent: "{color.teal.900}"
    border-subtle: "{color.neutral.700}"
    border-strong: "{color.neutral.500}"
    border-focus: "{color.teal.300}"
    action-primary: "{color.teal.300}"
    action-primary-hover: "{color.teal.200}"
    action-primary-active: "{color.teal.100}"
    action-primary-disabled: "{color.neutral.700}"
    feedback-success: "{color.teal.300}"
    feedback-warning: "{color.amber.500}"
    feedback-danger: "{color.red.500}"
    feedback-info: "{color.blue.500}"
  high_contrast:
    text-primary: "CanvasText"
    text-secondary: "CanvasText"
    text-muted: "CanvasText"
    text-on-accent: "ButtonText"
    surface-canvas: "Canvas"
    surface-raised: "Canvas"
    surface-sunken: "Canvas"
    surface-accent: "Highlight"
    border-subtle: "CanvasText"
    border-strong: "CanvasText"
    border-focus: "Highlight"
    action-primary: "ButtonFace"
    action-primary-hover: "Highlight"
    action-primary-active: "Highlight"
    action-primary-disabled: "GrayText"
    feedback-success: "CanvasText"
    feedback-warning: "CanvasText"
    feedback-danger: "CanvasText"
    feedback-info: "CanvasText"

typography:
  display_family: "IBM Plex Sans"
  body_family: "IBM Plex Sans"
  mono_family: "IBM Plex Mono"
  modular_ratio: 1.125
  weights:
    regular: 400
    medium: 500
    bold: 700
  scale:
    caption: {size: "12px", line_height: "16px", weight: 500}
    small: {size: "14px", line_height: "20px", weight: 400}
    body: {size: "16px", line_height: "24px", weight: 400}
    lead: {size: "18px", line_height: "28px", weight: 400}
    h5: {size: "18px", line_height: "24px", weight: 700}
    h4: {size: "20px", line_height: "28px", weight: 700}
    h3: {size: "23px", line_height: "32px", weight: 700}
    h2: {size: "26px", line_height: "32px", weight: 700}
    h1: {size: "29px", line_height: "36px", weight: 700}
    display: {size: "33px", line_height: "40px", weight: 700}
  numeric_columns: {font_variant_numeric: "tabular-nums"}

spacing:
  space-inset-sm: "{spacing.8}"
  space-inset-md: "{spacing.16}"
  space-inset-lg: "{spacing.24}"
  space-inset-xl: "{spacing.32}"
  space-stack-xs: "{spacing.4}"
  space-stack-sm: "{spacing.8}"
  space-stack-md: "{spacing.16}"
  space-stack-lg: "{spacing.24}"
  space-stack-xl: "{spacing.40}"
  space-inline-sm: "{spacing.8}"
  space-inline-md: "{spacing.12}"
  space-inline-lg: "{spacing.20}"

radius:
  radius-control: "{radius.4}"
  radius-surface: "{radius.8}"
  radius-indicator: "{radius.9999}"

elevation:
  resting: "none"
  raised: "0 1px 3px oklch(0.20 0.015 205 / 0.16)"
  floating: "0 8px 24px oklch(0.14 0.018 205 / 0.22)"

motion:
  easing_standard: "cubic-bezier(0.4, 0, 0.2, 1)"
  easing_entry: "cubic-bezier(0, 0, 0.2, 1)"
  easing_exit: "cubic-bezier(0.4, 0, 1, 1)"
  easing_emphasized: "cubic-bezier(0.2, 0, 0, 1)"
  duration_micro: "{duration.80}"
  duration_standard: "{duration.180}"
  duration_emphasized: "{duration.320}"
  reduced_motion: "Replace transform movement with opacity cross-fades no longer than 80ms; use instant focus rings and progress updates."

component_tokens:
  button-primary-background: "{action-primary}"
  button-primary-background-hover: "{action-primary-hover}"
  input-border-default: "{border-strong}"
  input-border-focus: "{border-focus}"
  workflow-stage-current: "{surface-accent}"
  evidence-highlight: "{surface-accent}"
  provenance-extracted: "{feedback-info}"
  provenance-ai-generated: "{feedback-warning}"
  provenance-user-edited: "{text-primary}"
  provenance-approved: "{feedback-success}"
~~~

Token consumers reference semantic or component names only. Raw color, spacing, radius, duration, and shadow values remain confined to the primitive definitions above. The palette must be contrast-tested in every mode before Figma publication.

### Component References

**Option A: Figma Component References**

| Component Name | Figma Component | Code Location | UI Changes Required |
|---|---|---|---|
| C/Actions/Button | Pending component key | `frontend/src/shared/ui/Button.tsx` | Type Primary/Secondary/Tertiary/Ghost; Size S/M/L; Icon None/Leading/Trailing; all required interaction states |
| C/Actions/IconButton | Pending component key | `frontend/src/shared/ui/IconButton.tsx` | S/M/L; accessible name required; tooltip for unfamiliar icons; fixed square dimensions |
| C/Inputs/TextField | Pending component key | `frontend/src/shared/ui/TextField.tsx` | Default/Hover/Focus/Active/Disabled/Read-only/Loading/Error; required, helper, and error slots |
| C/Inputs/TextArea | Pending component key | `frontend/src/shared/ui/TextArea.tsx` | Same states as TextField; character count; minimum and maximum height; no content truncation |
| C/Inputs/FileUpload | Pending component key | `frontend/src/features/document-intake/FileUpload.tsx` | Empty/Drag-over/Selected/Uploading/Rejected/Disabled; bytes, pages, media type, remove, retry |
| C/Inputs/RadioGroup | Pending component key | `frontend/src/shared/ui/RadioGroup.tsx` | Roving focus; selected, unselected, disabled, and error variants |
| C/Navigation/WorkflowRail | Pending component key | `frontend/src/app/WorkflowRail.tsx` | Expanded/Collapsed/Drawer; stage Complete/Current/Blocked/Available; status text and icon |
| C/Navigation/Tabs | Pending component key | `frontend/src/shared/ui/Tabs.tsx` | Horizontal/Vertical; selected, hover, focus, disabled; arrow-key navigation |
| C/Navigation/DeficiencyList | Pending component key | `frontend/src/features/extraction-review/DeficiencyList.tsx` | Searchable list; selected, confirmed, needs-review, draft, approved states |
| C/Content/EvidenceViewer | Pending component key | `frontend/src/features/extraction-review/EvidenceViewer.tsx` | Page number, snippet, confidence, coordinates, highlighted span, load/error/failed-page states |
| C/Content/FieldEditor | Pending component key | `frontend/src/features/extraction-review/FieldEditor.tsx` | Original/current values, origin, confidence, uncertainty, revision, edit/confirm states |
| C/Content/CandidateComparison | Pending component key | `frontend/src/features/extraction-review/CandidateComparison.tsx` | Two or more candidates, evidence link, confidence, supported selection, correction path |
| C/Content/PocSection | Pending component key | `frontend/src/features/poc-authoring/PocSection.tsx` | Five section types; editable/read-only; generated/edited/approved; missing-information state |
| C/Content/RevisionHistory | Pending component key | `frontend/src/shared/ui/RevisionHistory.tsx` | Ordered revisions, actor, origin, current/approved markers, no destructive actions |
| C/Feedback/Alert | Pending component key | `frontend/src/shared/ui/Alert.tsx` | Info/Success/Warning/Danger; persistent/dismissible; title, body, correlation ID, action |
| C/Feedback/StatusBadge | Pending component key | `frontend/src/shared/ui/StatusBadge.tsx` | Text plus icon for Needs review/Confirmed/Draft/Reapproval required/Approved/Failed |
| C/Feedback/StageTimeline | Pending component key | `frontend/src/features/extraction-review/StageTimeline.tsx` | Pending/Active/Complete/Failed/Canceled; determinate and indeterminate progress |
| C/Feedback/Modal | Pending component key | `frontend/src/shared/ui/Modal.tsx` | Confirmation/Warning/Details; focus trap, Escape close where safe, focus restoration |
| C/Layout/AppShell | Pending component key | `frontend/src/app/AppShell.tsx` | Desktop/tablet/mobile grids, skip link, header, rail, main, contextual pane |
| C/Layout/SplitPane | Pending component key | `frontend/src/shared/ui/SplitPane.tsx` | 5/7 and 6/6 desktop ratios; stacked tablet/mobile; bounded scroll regions |

### New Visual Assets

~~~yaml
screenshots:
  location: "Not applicable until the Figma file is created"
  files: []

new_assets:
  icons:
    - name: "lucide-icon-set"
      source: "Lucide library; use one consistent outlined set"
      purpose: "Upload, file, evidence, warning, retry, edit, approval, copy, download, close, and navigation commands"
  images: []
  restrictions:
    - "Do not use CMS seals, federal agency marks, facility photography, resident photography, or decorative AI imagery."
    - "Icons supplement visible labels for primary actions and never carry status alone."
~~~

### Task Design Mapping

~~~yaml
TASK-UI-001:
  title: "Implement local authentication UI"
  ui_impact: true
  visual_references:
    figma_frames: ["SignIn/Default", "SignIn/Loading", "SignIn/Empty", "SignIn/Error", "SignIn/Validation"]
  components_affected: ["AppShell", "TextField", "Button", "Alert", "LocalOnlyNotice"]
  visual_validation_required: true

TASK-UI-002:
  title: "Implement bounded document intake"
  ui_impact: true
  visual_references:
    figma_frames: ["DocumentIntake/Default", "DocumentIntake/Loading", "DocumentIntake/Empty", "DocumentIntake/Error", "DocumentIntake/Validation"]
  components_affected: ["WorkflowRail", "FileUpload", "FileSummary", "SessionNotice", "Alert"]
  visual_validation_required: true

TASK-UI-003:
  title: "Implement extraction progress and recovery"
  ui_impact: true
  visual_references:
    figma_frames: ["ProcessingProgress/Default", "ProcessingProgress/Loading", "ProcessingProgress/Empty", "ProcessingProgress/Error", "ProcessingProgress/Validation"]
  components_affected: ["StageTimeline", "ProgressBar", "StatusBadge", "DiagnosticDetails"]
  visual_validation_required: true

TASK-UI-004:
  title: "Implement evidence-linked extraction review"
  ui_impact: true
  visual_references:
    figma_frames: ["ExtractionReview/Default", "ExtractionReview/Loading", "ExtractionReview/Empty", "ExtractionReview/Error", "ExtractionReview/Validation"]
  components_affected: ["DeficiencyList", "EvidenceViewer", "FieldEditor", "ConfidenceIndicator", "ProvenanceTag"]
  visual_validation_required: true

TASK-UI-005:
  title: "Implement uncertainty resolution"
  ui_impact: true
  visual_references:
    figma_frames: ["UncertaintyResolution/Default", "UncertaintyResolution/Loading", "UncertaintyResolution/Empty", "UncertaintyResolution/Error", "UncertaintyResolution/Validation"]
  components_affected: ["CandidateComparison", "EvidenceViewer", "RadioGroup", "TextArea", "Alert"]
  visual_validation_required: true

TASK-UI-006:
  title: "Implement grounded POC authoring"
  ui_impact: true
  visual_references:
    figma_frames: ["PocAuthoring/Default", "PocAuthoring/Loading", "PocAuthoring/Empty", "PocAuthoring/Error", "PocAuthoring/Validation"]
  components_affected: ["PocSection", "MissingInformationMarker", "ProvenanceTag", "RevisionStatus"]
  visual_validation_required: true

TASK-UI-007:
  title: "Implement leader approval review"
  ui_impact: true
  visual_references:
    figma_frames: ["ApprovalReview/Default", "ApprovalReview/Loading", "ApprovalReview/Empty", "ApprovalReview/Error", "ApprovalReview/Validation"]
  components_affected: ["ReviewSummary", "EvidenceViewer", "PocSection", "CompletenessChecklist", "RevisionStatus"]
  visual_validation_required: true

TASK-UI-008:
  title: "Implement approved export and session end"
  ui_impact: true
  visual_references:
    figma_frames: ["ApprovedExport/Default", "ApprovedExport/Loading", "ApprovedExport/Empty", "ApprovedExport/Error", "ApprovedExport/Validation"]
  components_affected: ["ApprovalSummary", "DraftPreview", "Button", "IconButton", "Modal", "Toast"]
  visual_validation_required: true
~~~

### Visual Validation Criteria

~~~typescript
const requiresVisualValidation = true;

const visualValidation = {
  screenshotComparison: {
    maxDifference: "5%",
    breakpoints: [375, 768, 1440, 1920],
  },
  componentValidation: {
    colorAccuracy: true,
    spacingAccuracy: true,
    typographyMatch: true,
    stableAsyncDimensions: true,
  },
  accessibilityValidation: {
    wcag: "2.2 AA",
    keyboardOnly: true,
    screenReader: true,
    zoomPercent: 200,
    reducedMotion: true,
    focusVisibility: true,
  },
};
~~~

### Implementation Scenarios

#### For New UI Components

~~~yaml
new_components:
  - name: "WorkflowRail"
    figma_reference: "C/Navigation/WorkflowRail"
    file_location: "frontend/src/app/WorkflowRail.tsx"
    design_specifications:
      desktop_width: "248px"
      tablet_width: "72px collapsed"
      mobile_behavior: "Current-stage summary plus drawer"
      states: ["available", "current", "complete", "blocked", "disabled"]
      accessibility: "Navigation landmark with current step text and aria-current=step"
  - name: "EvidenceViewer"
    figma_reference: "C/Content/EvidenceViewer"
    file_location: "frontend/src/features/extraction-review/EvidenceViewer.tsx"
    design_specifications:
      width: "Fill parent with bounded scroll region"
      content_measure: "68 characters for extracted text"
      states: ["default", "loading", "empty", "failed-page", "error", "highlighted"]
      accessibility: "Named region; page and snippet context included in accessible description"
  - name: "PocSection"
    figma_reference: "C/Content/PocSection"
    file_location: "frontend/src/features/poc-authoring/PocSection.tsx"
    design_specifications:
      width: "100%"
      minimum_editor_height: "160px"
      states: ["generated", "edited", "missing-information", "approved", "error", "read-only"]
      accessibility: "Section heading labels editor; provenance and errors are programmatically associated"
~~~

#### For UI Enhancements

~~~yaml
ui_enhancements:
  existing_component: "Shared async action controls"
  changes_required:
    - "Preserve button and field dimensions while loading"
    - "Use semantic status text with icons rather than color alone"
    - "Add visible 2px focus outline with 2px offset"
    - "Use transform and opacity only for state motion"
    - "Provide disabled-state explanation when workflow policy blocks an action"
  figma_reference: "02_Components interaction-state matrices"
~~~

#### For Backend/API Tasks (No Design Needed)

~~~yaml
backend_task:
  ui_impact: false
  design_references: "Not applicable to domain, provider-adapter, repository, workspace, or configuration implementation without a changed user-visible state."
  validation_type: "Unit, API integration, contract, security, cleanup, and log-redaction tests"
~~~

### Accessibility Requirements

- **WCAG Level**: WCAG 2.2 AA for all screens and modified components.
- **Color Contrast**: Body text at least 4.5:1; large text and UI boundaries at least 3:1; focus indication at least 3:1 against adjacent colors; verify light, dark, and high-contrast modes.
- **Focus States**: Every interactive component uses a visible 2px focus outline with a 2px offset. Focus order follows skip link, header, workflow rail, local navigation, primary content, evidence pane, and actions.
- **Screen Reader**: Use semantic landmarks, unique page titles, programmatic labels, descriptive headings, `aria-current` for workflow position, and associated descriptions for evidence and errors.
- **Keyboard**: All actions are reachable by keyboard. Tabs, radio groups, menus, and listboxes use arrow-key navigation; Enter/Space activate; Escape closes non-destructive overlays; modal focus is trapped and restored.
- **Dynamic Content**: Use polite live regions for progress and save confirmation, assertive alerts for terminal failures, and one announcement per meaningful stage transition.
- **Forms**: Visible labels match accessible names; required state is programmatic; error summary links to fields; each error uses `aria-describedby`; placeholders are never the only instruction.
- **Zoom and Reflow**: At 200% zoom, primary tasks remain available without two-dimensional page scrolling; content panes stack before controls overlap.
- **Motion**: Honor `prefers-reduced-motion`; remove translation and scale animation, preserve only opacity transitions up to 80ms where needed for state legibility.
- **Touch and Pointer**: Interactive targets are at least 44x44px on mobile/tablet and maintain spacing that prevents accidental activation.
- **Status and Provenance**: Combine icon, text, and semantic color; never communicate uncertainty, error, approval, or provenance by color alone.

Responsive implementation notes:

- At 1440px, use a 12-column grid with a 248px workflow rail, bounded deficiency list, primary work pane, and contextual evidence pane.
- At 768px, collapse the workflow rail, stack source evidence below the active editor, and preserve deficiency navigation in a drawer.
- At 375px, expose workflow status, evidence summary, confirmation, retry, and session actions; direct dense SOD and POC editing/comparison to a larger viewport with an explicit message.
- At 1920px and above, cap the application workspace so evidence text and controls do not stretch beyond readable measures.

### Design Review Checklist

**Complete only if ui_impact: true**

- [x] Figma frame names and five mandatory states are specified for all UI changes.
- [x] Primitive, semantic, and component tokens are defined with light, dark, and high-contrast resolution.
- [x] Component specifications, variants, interaction states, auto-layout behavior, and code targets are documented.
- [x] Visual validation criteria define screenshot, token, responsive, stable-dimension, and accessibility checks.
- [x] Responsive behavior is specified for mobile, tablet, desktop, and large desktop.
- [x] WCAG 2.2 AA, keyboard, screen-reader, zoom, focus, live-region, reduced-motion, and touch requirements are documented.
- [x] The aesthetic direction is declared with rationale, precedents, anti-brief, source attribution, and basis.
- [x] No decorative photography, government marks, mixed icon sets, or unsupported brand assets are introduced.

**Skip if ui_impact: false**

- Not applicable; the project has UI impact.
