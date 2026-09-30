# Figma Design Specification - CMS Deficiency Action Planner

## 1. Figma Specification

**Platform**: Responsive web, desktop-first. Desktop at 1440px is the primary authoring and review surface; tablet at 768px is fully supported; mobile at 375px supports essential review, status, and recovery actions while dense document comparison remains optimized for larger viewports.

---

## 2. Source References

### Primary Source

| Document | Path | Purpose |
|---|---|---|
| Requirements | `.propel/context/docs/spec.md` | Personas, FR-001 through FR-020, UC-001 through UC-010, alternatives, and UI-impacting outcomes |

### Optional Sources

| Document | Path | Purpose |
|---|---|---|
| Architecture design | `.propel/context/docs/design.md` | Local authentication, role boundaries, API states, transient lifecycle, and responsive frontend constraints |
| Design models | `.propel/context/docs/model.md` | Component boundaries, data relationships, processing sequences, and recovery paths |

### Related Documents

| Document | Path | Purpose |
|---|---|---|
| Design System | `.propel/context/docs/designsystem.md` | Aesthetic direction, tokens, components, responsive rules, and accessibility specifications |

---

## 3. UX Requirements

### UXR Requirements Table

| UXR-ID | Category | Requirement | Acceptance Criteria | Screens Affected | Basis |
|---|---|---|---|---|---|
| UXR-001 | Session lifecycle | [SOURCE:INPUT] The system MUST keep the transient nature of case data visible at upload, active work, timeout, and session end. | Intake identifies session-only storage; inactivity warning appears before expiry; end-session confirmation names the data removed; cleanup success or failure is explicit. | SCR-002, SCR-003, SCR-004, SCR-006, SCR-008 | FR-020 and the confirmed transient-session architecture require users to understand when work will be removed. |
| UXR-002 | Authorization | [SOURCE:INPUT] The system MUST expose actions according to the authenticated role and MUST distinguish unavailable, awaiting-approval, approved, and reapproval-required states. | Reviewers cannot activate approval; leaders can approve only complete current revisions; export is disabled with a reason until approval matches the current revision. | SCR-001, SCR-006, SCR-007, SCR-008 | FR-016 through FR-018 and NFR-004 define separate reviewer and compliance-leader authority. |
| UXR-101 | Usability | [SOURCE:INPUT] The system MUST provide a persistent workflow rail showing Intake, Review, POC Drafts, and Approval/Export status. | At 1440px the rail remains visible; completed, current, blocked, and unavailable stages use text and icon treatment; selecting an available stage preserves case context. | SCR-002 through SCR-008 | The user selected a persistent left workflow rail for the case workflow. |
| UXR-102 | Usability | [SOURCE:INPUT] The system MUST present each reviewed value beside its page, snippet, confidence, and uncertainty evidence. | Desktop review uses synchronized content/evidence panes; selecting a field highlights its evidence; tablet stacks panes without losing page and snippet context. | SCR-004, SCR-005, SCR-007 | FR-008 requires verification without manual source searching. |
| UXR-103 | Provenance | [SOURCE:INPUT] The system MUST preserve original, extracted, AI-generated, user-edited, and approved states in visible revision context. | Every editable value and POC section carries origin and revision labels; revision history exposes original and current values; an edit immediately shows reapproval required. | SCR-004, SCR-005, SCR-006, SCR-007, SCR-008 | FR-009, FR-015, and FR-018 require provenance and approval invalidation. |
| UXR-201 | Accessibility | [SOURCE:INPUT] The system MUST conform to WCAG 2.2 AA for keyboard, screen-reader, 200% zoom, contrast, and reduced-motion use. | All controls are keyboard operable; focus is visible at 3:1; body text meets 4.5:1; layouts remain usable at 200% zoom; reduced motion removes nonessential transitions. | SCR-001 through SCR-008 | The user selected WCAG 2.2 AA as the accessibility baseline. |
| UXR-202 | Accessibility | [SOURCE:INPUT] The system MUST announce asynchronous progress, validation, approval changes, and failures without relying on color alone. | Progress uses a polite live region; terminal errors use an assertive alert; status combines icon, text, and color; focus moves to the error summary after failed submission. | SCR-002, SCR-003, SCR-004, SCR-006, SCR-007, SCR-008 | The confirmed WCAG 2.2 AA baseline applies to the dynamic workflows required by FR-002, FR-007, and FR-014. |
| UXR-301 | Responsiveness | [SOURCE:INPUT] The system MUST use a desktop-first responsive composition with full tablet support and essential mobile review actions. | 1440px uses rail plus multi-pane work area; 768px uses collapsible rail and two-stage stacked evidence; 375px offers status, evidence summary, confirmation, and recovery while directing dense editing to a larger viewport. | SCR-001 through SCR-008 | The user selected the desktop-first responsive strategy with limited essential mobile actions. |
| UXR-401 | Visual design | [SOURCE:INPUT] The system MUST use a restrained, trust-focused visual system suitable for regulated compliance work. | Surfaces use cool tinted neutrals; color is reserved for actions and semantic status; decoration does not compete with evidence; all screens consume semantic tokens. | SCR-001 through SCR-008 | The user selected a new restrained, trust-focused design system. |
| UXR-501 | Interaction | [SOURCE:INPUT] The system MUST acknowledge local actions within 100ms and preserve stable dimensions during asynchronous work. | Press, focus, and save acknowledgement appears within 100ms; buttons retain width during loading; skeletons preserve final layout; jobs expose stage and percent. | SCR-001 through SCR-008 | NFR-001, TR-006, and the UI standards require responsive state feedback and ordered job progress. |
| UXR-502 | Interaction | [SOURCE:INPUT] The system MUST never represent uncertain, failed, incomplete, or stale content as complete or approved. | Unresolved fields remain visibly blocked; failed stages identify affected page or operation; incomplete POC sections block approval; stale approvals disable export. | SCR-003 through SCR-008 | FR-006, FR-007, FR-010, FR-014, FR-017, and FR-018 prohibit false completion. |
| UXR-601 | Error handling | [SOURCE:INPUT] The system MUST provide calm, precise, non-blaming errors with the failed operation, preserved work, retryability, and a recovery action. | Error states include a safe message, correlation ID, retained-work statement, and one primary recovery action; provider details and document content are absent. | SCR-001 through SCR-008 | The user selected calm compliance language, while TR-011 requires stable safe problem details. |
| UXR-602 | Error handling | [SOURCE:INPUT] The system MUST require confirmation before destructive session cleanup and MUST report cleanup completion or failure without ambiguity. | Confirmation explains permanent loss; cancel is non-destructive; success returns to empty intake; failure keeps the case visible and does not claim removal. | SCR-002, SCR-008 | UC-009 and FR-020 define warning, cancellation, idempotent cleanup, and truthful failure reporting. |

### UXR Categories

- **Session lifecycle**: Transient storage, inactivity, and cleanup visibility.
- **Authorization**: Role-aware controls and current-revision approval.
- **Usability**: Workflow orientation, evidence adjacency, and task efficiency.
- **Accessibility**: WCAG 2.2 AA, assistive technology, zoom, and motion preferences.
- **Responsiveness**: Desktop, tablet, and essential mobile behavior.
- **Visual design**: Trust-focused semantic-token usage.
- **Interaction**: Immediate feedback, stable loading, and truthful state.
- **Error handling**: Safe diagnostics and actionable recovery.

### UXR Derivation Logic

- Usability requirements derive from UC-001 through UC-008 success paths and the confirmed workflow rail.
- Accessibility requirements derive from the user-confirmed WCAG 2.2 AA baseline applied to dynamic processing and forms.
- Responsive requirements derive from the confirmed desktop-first strategy and 1440px, 768px, and 375px validation widths.
- Visual requirements derive from the confirmed restrained, trust-focused design-system direction.
- Interaction requirements derive from processing progress, revision, approval, and export state transitions.
- Error requirements derive from every use-case extension and UC-010 recovery behavior.

### UXR Numbering Convention

- UXR-0XX: Project-wide and lifecycle requirements.
- UXR-1XX: Usability and provenance requirements.
- UXR-2XX: Accessibility requirements.
- UXR-3XX: Responsiveness requirements.
- UXR-4XX: Visual-design requirements.
- UXR-5XX: Interaction requirements.
- UXR-6XX: Error-handling requirements.

---

## 4. Personas Summary

| Persona | Role | Primary Goals | Key Screens |
|---|---|---|---|
| Compliance Reviewer | Primary user who uploads, verifies, corrects, drafts, and edits | Process one CMS-2567 accurately; resolve uncertainty with evidence; create a complete grounded POC without losing reviewed work | SCR-001 through SCR-006, SCR-008 |
| Compliance Leader | Secondary user and designated approver | Review evidence and provenance; approve only the current complete revision; export a clearly labeled approved draft | SCR-001, SCR-004, SCR-006 through SCR-008 |
| External OCR Service | System actor represented through job status | Return text for incomplete pages without being exposed as a direct user surface | SCR-003 |
| External AI Service | System actor represented through extraction and drafting status | Return schema-valid candidates and grounded drafts without being exposed as a direct user surface | SCR-003, SCR-006 |

---

## 5. Information Architecture

### Site Map

~~~text
CMS Deficiency Action Planner
+-- Authentication
|   +-- Sign in
+-- Active Case Workspace
|   +-- Intake
|   |   +-- Document intake
|   |   +-- Processing progress
|   +-- Review
|   |   +-- Extraction review
|   |   +-- Uncertainty resolution
|   +-- POC Drafts
|   |   +-- POC authoring
|   +-- Approval and Export
|       +-- Approval review
|       +-- Approved export
+-- Session Utilities
  +-- Inactivity warning
  +-- End-session confirmation
  +-- Processing failure recovery
~~~

### Navigation Patterns

| Pattern | Type | Platform Behavior |
|---|---|---|
| Primary Nav | Persistent workflow rail | Desktop: 248px left rail with case and stage status. Tablet: collapsible 72px rail. Mobile: compact stage summary and current-task navigation; dense editing actions defer to larger screens. |
| Secondary Nav | Breadcrumb and local tabs | Breadcrumb identifies case and deficiency. Tabs switch Evidence, Revisions, and POC views without losing the selected deficiency. |
| Utility Nav | Header user menu | Shows role, session time remaining, end-session action, and sign out; destructive cleanup remains a separate confirmation. |
| Context Nav | Deficiency list | Desktop: persistent list beside the work area. Tablet/mobile: searchable drawer preserving selection and completion status. |

---

## 6. Screen Inventory

### Screen List

| Screen ID | Screen Name | Derived From | Personas Covered | States Required |
|---|---|---|---|---|
| SCR-001 | Sign in | UC-001 precondition; architecture authentication boundary | Compliance Reviewer, Compliance Leader | Default, Loading, Empty, Error, Validation |
| SCR-002 | Document intake | UC-001, UC-009 | Compliance Reviewer | Default, Loading, Empty, Error, Validation |
| SCR-003 | Processing progress | UC-002, UC-010 | Compliance Reviewer | Default, Loading, Empty, Error, Validation |
| SCR-004 | Extraction review | UC-002, UC-004 | Compliance Reviewer, Compliance Leader | Default, Loading, Empty, Error, Validation |
| SCR-005 | Uncertainty resolution | UC-003 | Compliance Reviewer | Default, Loading, Empty, Error, Validation |
| SCR-006 | POC authoring | UC-005, UC-006, UC-010 | Compliance Reviewer, Compliance Leader | Default, Loading, Empty, Error, Validation |
| SCR-007 | Approval review | UC-007 | Compliance Leader | Default, Loading, Empty, Error, Validation |
| SCR-008 | Approved export | UC-008, UC-009 | Compliance Reviewer, Compliance Leader | Default, Loading, Empty, Error, Validation |

### Screen-to-Persona Coverage Matrix

| Screen | Compliance Reviewer | Compliance Leader | External OCR Service | External AI Service | Notes |
|---|---|---|---|---|---|
| SCR-001 Sign in | Primary | Primary | - | - | Role comes from configured account, never user selection. |
| SCR-002 Document intake | Primary | Secondary | - | - | Reviewer starts the active case; leader may inspect session status. |
| SCR-003 Processing progress | Primary | Secondary | Status only | Status only | Provider identity appears only as safe stage metadata. |
| SCR-004 Extraction review | Primary | Secondary | - | Result provenance | Shared evidence package; only reviewer can correct or confirm. |
| SCR-005 Uncertainty resolution | Primary | Secondary | Result provenance | Result provenance | Reviewer resolves; leader may inspect read-only history. |
| SCR-006 POC authoring | Primary | Secondary | - | Result provenance | Reviewer edits; leader reads before approval. |
| SCR-007 Approval review | Secondary | Primary | - | Result provenance | Approval control appears only for a compliance leader. |
| SCR-008 Approved export | Primary | Primary | - | - | Export remains locked to the approved current revision. |

### Modal/Overlay Inventory

| Name | Type | Trigger | Parent Screen(s) |
|---|---|---|---|
| Inactivity warning | Modal | Session approaches the 60-minute inactivity limit | SCR-002 through SCR-008 |
| End session | Confirmation dialog | User selects End session | SCR-002 through SCR-008 |
| Replace document | Confirmation dialog | User uploads a replacement after invalid intake | SCR-002 |
| Deficiency navigator | Drawer | Tablet/mobile user opens deficiency list | SCR-004 through SCR-007 |
| Evidence detail | Drawer | User expands page snippet or source coordinates | SCR-004, SCR-005, SCR-007 |
| Revision history | Drawer | User selects revision or provenance label | SCR-004 through SCR-008 |
| Copy confirmation | Toast | Approved content is copied | SCR-008 |
| Processing failure details | Modal | User opens safe diagnostic details | SCR-003, SCR-006 |

**Screen State Specifications**

| Screen | Default State | Loading State | Empty State | Error State | Validation State |
|---|---|---|---|---|---|
| SCR-001 Sign in | Username, password, Sign in, local-only notice, and no role selector | Fixed-width button spinner; fields disabled; polite status text | First-run configuration unavailable message with administrator action | Safe authentication-service failure with correlation ID and retry | Field-level required errors plus non-specific invalid-credentials summary; focus moves to summary |
| SCR-002 Document intake | Drop zone, file chooser, limits, supported formats, transient-data notice, and Upload action | Stream progress with bytes sent; replace/remove disabled | Primary first-use state with Select CMS-2567 action | Rejection reason, preserved empty session, and Choose another file action | Unsupported type, over-50-MB, unreadable, non-CMS-2567, and over-200-page errors linked to upload field |
| SCR-003 Processing progress | Ordered stages, current percent, elapsed time, cancel control, and reconnect status | Skeleton stage details before first event; current stage pulses without layout shift | Accepted case with no job yet and Start extraction action | Failed stage/page, retained-work statement, retryability, correlation ID, and Retry failed operation | Start blocked when another job is active or document validation is incomplete |
| SCR-004 Extraction review | Provider fields, deficiency list, editable values, confidence, evidence pane, origin labels, and Confirm action | Stable split-pane skeleton with controls disabled | No deficiency candidates state that requires reviewer attention rather than claiming success | Projection load failure with retry; retained review state remains identified | Unresolved evidence, missing F-tag, incomplete SOD, and stale revision conflicts are listed and focused |
| SCR-005 Uncertainty resolution | Candidate comparison, page/snippet evidence, confidence, correction input, and Resolve action | Candidate and evidence skeletons retain comparison geometry | No unresolved candidates; Continue review action returns to SCR-004 | Evidence unavailable or revision conflict with retry/reload choice | Resolution requires a supported candidate or explicit user-authored correction; insufficient evidence may remain unresolved |
| SCR-006 POC authoring | Five named sections, deficiency context, provenance per section, missing-information markers, revision status, Save, and Generate/Regenerate | Generation progress preserves confirmed deficiency; editors disabled only while replacing draft | Confirmed deficiency has no POC; Generate POC action | Provider/schema failure states preserved reviewed data and offer Retry | Empty required sections, unresolved markers, stale revision, and unsupported claim errors block approval readiness |
| SCR-007 Approval review | Read-only evidence and five-part POC, provenance, completeness summary, Approve, and Request changes | Review package skeleton; approval action retains dimensions | No POC ready for approval; return to available drafts | Authorization, stale revision, or save failure leaves export disabled and state unchanged | Incomplete sections, unresolved missing information, or mismatched revision identify exact blockers |
| SCR-008 Approved export | Approval identity/time, current revision match, draft label preview, Copy, Download, and End session | Export formatting progress with approval retained | No approved POC; link to approval queue or drafts | Formatting/download failure offers retry and Copy fallback; cleanup failure keeps case visible | Export disabled with reason when approval is absent, revoked, or stale |

---

## 7. Content & Tone

### Voice & Tone

- **Overall Tone**: Calm, precise, non-blaming, and action-oriented. Use established CMS terms where they improve accuracy, then explain the next action in plain language.
- **Error Messages**: Name the operation that failed, what work remains safe, whether retry is available, and the next action. Never expose provider payloads, document content, or stack traces.
- **Empty States**: State why no content is present and provide one relevant action. Avoid celebratory or promotional language.
- **Success Messages**: Briefly confirm the state change and current workflow status, such as "Deficiency confirmed. POC generation is now available."

### Content Guidelines

- **Headings**: Sentence case; use the object or task name, not generic labels such as "Overview."
- **CTAs**: Specific verbs and objects: "Upload CMS-2567," "Confirm deficiency," "Generate POC," "Approve current revision," and "Download draft."
- **Labels**: Match accessible names exactly; use "Compliance leader" and "Compliance reviewer" consistently.
- **Placeholder Text**: Use realistic examples only when necessary; never place instructions solely in placeholder text.
- **Uncertainty**: Use "Needs review" with the affected field and evidence status; do not imply the system selected a final value.
- **Provenance**: Use the closed labels "Extracted," "AI-generated," "User-edited," and "Approved."
- **Export Label**: Begin copied and downloaded content with "DRAFT - Approved for compliance handling; not submitted to CMS."

---

## 8. Data & Edge Cases

### Data Scenarios

| Scenario | Description | Handling |
|---|---|---|
| No Data | No active case or approved POC exists | Show the relevant empty state and one primary action; do not render inactive data scaffolding as content. |
| First Use | Authenticated reviewer has not uploaded a document | Explain supported CMS-2567 formats, 50 MB/200-page limits, and session-only retention beside the upload control. |
| Large Data | Document approaches 200 pages or contains many deficiencies | Paginate deficiency list at 25 items; search by F-tag; virtualize page thumbnails only after measured need; keep selected evidence stable. |
| Slow Connection | External provider stage exceeds 3 seconds | Preserve the stage timeline, show elapsed time and percent when known, and announce progress without repeated live-region noise. |
| Offline/API unavailable | Browser loses the local API connection | Freeze editing, identify unsaved local input, retry the health check, and never imply server retention until save succeeds. |
| SSE disconnect | Progress stream disconnects while the job continues | Show reconnecting status and resume from the last event ID without duplicating document text. |
| Mixed document | Native and OCR pages coexist | Label extraction method at page level only when relevant to confidence or failure. |
| Multiple deficiencies | One document contains several independent F-tags | Preserve independent review, POC, approval, and export status for every deficiency. |

### Edge Cases

| Case | Screen(s) Affected | Solution |
|---|---|---|
| Long SOD text | SCR-004, SCR-005, SCR-007 | Use a readable 68-character text measure inside a scrollable document region; provide expand and find controls; never truncate the authoritative current value. |
| Long provider name or F-tag label | SCR-002 through SCR-008 | Wrap to two lines in headers and lists; expose full text; do not resize controls or overlap status. |
| Low confidence or conflicting candidates | SCR-004, SCR-005 | Pair confidence with "Needs review," show alternatives and evidence, and keep confirmation disabled until resolved. |
| OCR page failure | SCR-003 through SCR-005 | Identify the page and stage, exclude failed content from confirmed results, and offer retry for the affected operation. |
| Form validation | SCR-001, SCR-002, SCR-004 through SCR-007 | Show a top summary plus inline errors linked with `aria-describedby`; move focus to the summary after submission. |
| Session timeout | SCR-002 through SCR-008 | Warn with remaining time and Continue session action; after expiry, return to sign in and state that transient content was removed. |
| Approval becomes stale | SCR-006 through SCR-008 | Immediately change status to Reapproval required, disable export, and preserve prior approval in revision history only. |
| Cleanup fails | SCR-002, SCR-008 | Keep the case visible, show Cleanup failed with correlation ID, deny workspace reuse, and allow retry. |
| Browser zoom at 200% | All | Collapse secondary panes before horizontal scrolling; keep primary controls and headings in reading order. |
| Mobile dense editing | SCR-004 through SCR-007 | Permit review of status and evidence summary; direct complex SOD/POC editing and approval comparison to tablet or desktop without hiding recovery. |

---

## 9. Branding & Visual Direction

### Aesthetic Direction

- **Direction**: Utilitarian `[SOURCE:INPUT]`
- **Rationale**: Compliance reviewers work inside a regulated, evidence-heavy workflow where speed, accuracy, and clear state distinctions matter more than decorative expression. A utilitarian direction supports dense side-by-side review, keyboard-first operation, restrained semantic color, and unambiguous provenance while the selected trust-focused system prevents the interface from feeling improvised or promotional.
- **Precedents**: Sentry, Grafana, PostHog.
- **Anti-brief**: The product must not resemble a consumer wellness app, a marketing dashboard, a glassmorphic AI assistant, or a government-form facsimile with dense uninterrupted fields and little workflow guidance.
- **Basis**: The utilitarian direction is inferred from the compliance domain, evidence density, repeated review actions, and the user's confirmed restrained trust-focused visual constraint.

### Branding Assets

- **Logo**: Text wordmark "CMS Deficiency Action Planner" for the MVP; no CMS seal, government mark, or implied agency endorsement.
- **Icon Style**: Consistent outlined icons with 1.75px stroke, rounded joins, visible text labels for commands, and tooltips for unfamiliar utility icons.
- **Illustration Style**: None in task surfaces. Empty states use simple component arrangements and status icons, not decorative scenes.
- **Photography Style**: Not applicable; resident, facility, and stock healthcare photography is excluded from the compliance workspace.

---

## 10. Component Specifications

### Component Library Reference

**Source**: `.propel/context/docs/designsystem.md` (Component References and Implementation Scenarios sections)

### Required Components per Screen

| Screen ID | Components Required | Notes |
|---|---|---|
| SCR-001 | AppShell, TextField (2), Button (1), Alert, LocalOnlyNotice | Credential errors remain non-specific; role is not selectable. |
| SCR-002 | AppShell, WorkflowRail, FileUpload, FileSummary, Button (2), LimitList, Alert, SessionNotice | Upload control supports drag, browse, progress, error, remove, and retry. |
| SCR-003 | AppShell, WorkflowRail, StageTimeline, ProgressBar, StatusBadge, Button (2), Alert, DiagnosticDetails | Timeline preserves ordered SSE events and reconnect status. |
| SCR-004 | AppShell, WorkflowRail, DeficiencyList, EvidenceViewer, FieldEditor, ConfidenceIndicator, ProvenanceTag, Tabs, Button (2) | Desktop split panes synchronize selection; current value and original evidence remain distinct. |
| SCR-005 | AppShell, WorkflowRail, CandidateComparison, EvidenceViewer, RadioGroup, TextArea, ConfidenceIndicator, Button (2), Alert | Selection and correction are mutually exclusive resolution paths. |
| SCR-006 | AppShell, WorkflowRail, DeficiencyHeader, PocSectionEditor (5), MissingInformationMarker, ProvenanceTag, RevisionStatus, Button (3), Alert | Editor preserves section order and dimensions during generation or save. |
| SCR-007 | AppShell, WorkflowRail, ReviewSummary, EvidenceViewer, PocSectionReadOnly (5), CompletenessChecklist, RevisionStatus, Button (2), Alert | Approve is leader-only and bound to displayed revision. |
| SCR-008 | AppShell, WorkflowRail, ApprovalSummary, DraftPreview, Button (3), IconButton (copy), Alert, Toast | Copy/download remain disabled until current approval is verified. |

### Component Summary

| Category | Components | Variants |
|---|---|---|
| Actions | Button, IconButton, Link | Primary/Secondary/Tertiary/Ghost x S/M/L x Default/Hover/Focus/Active/Disabled/Loading/Error; icons None/Leading/Trailing |
| Inputs | TextField, TextArea, FileUpload, RadioGroup, Select | S/M/L x Default/Hover/Focus/Active/Disabled/Read-only/Loading/Error; required and optional |
| Navigation | AppHeader, WorkflowRail, Breadcrumb, Tabs, DeficiencyList | Expanded/Collapsed/Drawer; stage Complete/Current/Blocked/Available; orientation horizontal/vertical |
| Content | EvidenceViewer, FieldEditor, CandidateComparison, PocSectionEditor, DraftPreview, RevisionHistory | Editable/Read-only; origin Extracted/AI-generated/User-edited/Approved; confidence High/Medium/Low/Conflict |
| Feedback | Alert, StatusBadge, ProgressBar, StageTimeline, Modal, Drawer, Toast, Tooltip, Skeleton | Info/Success/Warning/Danger; determinate/indeterminate; persistent/dismissible |
| Layout | AppShell, SplitPane, Stack, Grid, Divider, ScrollRegion | Desktop/Tablet/Mobile; Fill/Hug behavior documented; maximum four nested auto-layout levels |

### Component Constraints

- Use only components defined in `.propel/context/docs/designsystem.md`.
- Do not create one-off status colors, provenance labels, or spacing values.
- Every interactive component supports Default, Hover, Focus, Active, Disabled, Loading, and Error where applicable.
- Disabled actions include adjacent explanatory text or a discoverable tooltip; color alone never communicates availability.
- Components use `C/<Category>/<Name>` naming and semantic/component tokens only.
- Auto layout is required for every frame except overlays; stable controls never resize between interaction states.
- Desktop content panes use Fill width with bounded reading measures; labels and controls use Hug content where appropriate.
- Focus order follows header, workflow rail, local navigation, primary content, evidence pane, and actions.

---

## 11. Prototype Flows

### Flow: FL-001 - Authenticate Local User

**Flow ID**: FL-001
**Derived From**: UC-001 precondition, architecture authentication boundary, NFR-004
**Personas Covered**: Compliance Reviewer, Compliance Leader
**Description**: Authenticate a configured local account and enter the empty or active workspace with server-assigned authority.

#### Flow Sequence

~~~text
1. Entry: Sign in / Default
  - Trigger: User opens the loopback application
  |
  v
2. Step: Sign in / Validation
  - Action: Submit credentials; show inline errors when fields are empty
  |
  v
3. Decision Point:
  +-- Valid credentials -> Document intake / Empty or current authorized screen
  +-- Invalid credentials -> Sign in / Error
  +-- API unavailable -> Sign in / Error with retry
~~~

#### Required Interactions

- Submit credentials using Enter or the Sign in button.
- Move focus to the error summary on failure without revealing which credential was incorrect.
- Rotate the session and expose the configured role only after successful authentication.

### Flow: FL-002 - Upload Through Confirmed Extraction

**Flow ID**: FL-002
**Derived From**: UC-001, UC-002, UC-003, UC-004
**Personas Covered**: Compliance Reviewer
**Description**: Upload one CMS-2567, follow extraction, resolve uncertainty, and confirm each deficiency with evidence.

#### Flow Sequence

~~~text
1. Entry: Document intake / Empty
  - Trigger: Reviewer selects a CMS-2567 file
  |
  v
2. Step: Document intake / Loading
  - Action: Stream and validate the upload
  |
  v
3. Decision Point:
  +-- Valid -> Processing progress / Default
  +-- Invalid -> Document intake / Error -> choose another file
  |
  v
4. Step: Processing progress / Loading
  - Action: Receive ordered extraction and OCR progress
  |
  v
5. Decision Point:
  +-- Review ready -> Extraction review / Default
  +-- Failed -> Processing progress / Error -> FL-006
  |
  v
6. Decision Point:
  +-- Candidate uncertain -> Uncertainty resolution / Default -> resolve -> Extraction review
  +-- Evidence complete -> Confirm deficiency -> Extraction review / Default
~~~

#### Required Interactions

- Drag or browse to upload, with type and size validation before processing.
- Reconnect SSE from the last event ID without duplicate progress announcements.
- Synchronize selected values with page evidence and preserve originals after correction.
- Keep Generate POC unavailable until F-tag, SOD, and evidence are confirmed.

### Flow: FL-003 - Generate and Edit POC

**Flow ID**: FL-003
**Derived From**: UC-005, UC-006
**Personas Covered**: Compliance Reviewer, Compliance Leader (read-only)
**Description**: Generate one grounded five-part POC for a confirmed deficiency, resolve missing information, and save a user-edited revision.

#### Flow Sequence

~~~text
1. Entry: Extraction review / Default
  - Trigger: Reviewer selects Generate POC on a confirmed deficiency
  |
  v
2. Step: POC authoring / Loading
  - Action: Generate a schema-constrained draft from reviewed data
  |
  v
3. Decision Point:
  +-- Complete draft -> POC authoring / Default
  +-- Missing information -> POC authoring / Validation
  +-- Generation failure -> POC authoring / Error -> FL-006
  |
  v
4. Step: POC authoring / Default
  - Action: Edit one or more sections and save a new revision
  |
  v
5. Decision Point:
  +-- Complete current revision -> Approval review / Default
  +-- Incomplete -> POC authoring / Validation
~~~

#### Required Interactions

- Keep the five section names and order fixed.
- Label generated and user-edited content at section level.
- Mark unsupported facility facts as missing information instead of completed claims.
- Revoke existing approval immediately when a new revision is saved.

### Flow: FL-004 - Approve and Export Current Revision

**Flow ID**: FL-004
**Derived From**: UC-007, UC-008
**Personas Covered**: Compliance Leader, Compliance Reviewer
**Description**: Review evidence and provenance, approve the complete current revision, and obtain a labeled draft.

#### Flow Sequence

~~~text
1. Entry: Approval review / Default
  - Trigger: Compliance leader opens a complete POC
  |
  v
2. Step: Approval review / Default
  - Action: Review deficiency, evidence, provenance, and all five sections
  |
  v
3. Decision Point:
  +-- Approve -> Approved export / Default
  +-- Request changes -> POC authoring / Default
  +-- Stale or incomplete -> Approval review / Validation
  |
  v
4. Step: Approved export / Default
  - Action: Verify approval matches current revision
  |
  v
5. Decision Point:
  +-- Copy -> Approved export / success toast
  +-- Download -> Approved export / file response
  +-- Formatting failure -> Approved export / Error with copy fallback
~~~

#### Required Interactions

- Expose approval only to the compliance-leader role.
- Bind approval and export to the displayed revision number.
- Prefix copied and downloaded content with the required draft label.
- Preserve approval if export formatting fails.

### Flow: FL-005 - End Transient Session

**Flow ID**: FL-005
**Derived From**: UC-009
**Personas Covered**: Compliance Reviewer, Compliance Leader
**Description**: Confirm permanent removal of active case content and report cleanup truthfully.

#### Flow Sequence

~~~text
1. Entry: Any active workspace screen / Default
  - Trigger: User selects End session
  |
  v
2. Step: End session / Confirmation dialog
  - Action: Explain document, review, draft, and approval removal
  |
  v
3. Decision Point:
  +-- Cancel -> Return to unchanged parent screen
  +-- Confirm -> Cleanup in progress
  |
  v
4. Decision Point:
  +-- Zero remaining files -> Document intake / Empty
  +-- Cleanup failed -> Parent screen / Error with retry
~~~

#### Required Interactions

- Place focus in the dialog and return it to the trigger on cancel.
- Require an explicit destructive confirmation; Escape cancels.
- Do not show a cleared state until memory and workspace cleanup complete.

### Flow: FL-006 - Recover Failed Processing

**Flow ID**: FL-006
**Derived From**: UC-010, UC-002, UC-005
**Personas Covered**: Compliance Reviewer
**Description**: Retry only the failed extraction, OCR, or generation operation while preserving valid reviewed work.

#### Flow Sequence

~~~text
1. Entry: Processing progress or POC authoring / Error
  - Trigger: Operation reaches a retryable or terminal failure
  |
  v
2. Step: Error details
  - Action: Review failed stage, retained work, retryability, and correlation ID
  |
  v
3. Decision Point:
  +-- Retryable -> Retry failed operation -> Loading
  +-- Replacement required -> Document intake / Error
  +-- Retry later -> Preserve current screen and state
  |
  v
4. Decision Point:
  +-- Success -> Review-ready Default state
  +-- Retries exhausted -> Error with retained-work statement
~~~

#### Required Interactions

- Retry only the failed stage and retain all confirmed or edited values.
- Announce terminal status once; avoid repeated live-region updates.
- Never expose provider payloads or document text in diagnostics.

---

## 12. Export Requirements

### JPG Export Settings

| Setting | Value |
|---|---|
| Format | JPG |
| Quality | High (85%) |
| Scale - Mobile | 2x |
| Scale - Web | 2x |
| Color Profile | sRGB |

### Export Naming Convention

`CMSDeficiencyActionPlanner__<Platform>__<ScreenName>__<State>__v1.jpg`

### Export Manifest

| Screen | State | Platform | Filename |
|---|---|---|---|
| SignIn | Default | Web | CMSDeficiencyActionPlanner__Web__SignIn__Default__v1.jpg |
| SignIn | Loading | Web | CMSDeficiencyActionPlanner__Web__SignIn__Loading__v1.jpg |
| SignIn | Empty | Web | CMSDeficiencyActionPlanner__Web__SignIn__Empty__v1.jpg |
| SignIn | Error | Web | CMSDeficiencyActionPlanner__Web__SignIn__Error__v1.jpg |
| SignIn | Validation | Web | CMSDeficiencyActionPlanner__Web__SignIn__Validation__v1.jpg |
| DocumentIntake | Default | Web | CMSDeficiencyActionPlanner__Web__DocumentIntake__Default__v1.jpg |
| DocumentIntake | Loading | Web | CMSDeficiencyActionPlanner__Web__DocumentIntake__Loading__v1.jpg |
| DocumentIntake | Empty | Web | CMSDeficiencyActionPlanner__Web__DocumentIntake__Empty__v1.jpg |
| DocumentIntake | Error | Web | CMSDeficiencyActionPlanner__Web__DocumentIntake__Error__v1.jpg |
| DocumentIntake | Validation | Web | CMSDeficiencyActionPlanner__Web__DocumentIntake__Validation__v1.jpg |
| ProcessingProgress | Default | Web | CMSDeficiencyActionPlanner__Web__ProcessingProgress__Default__v1.jpg |
| ProcessingProgress | Loading | Web | CMSDeficiencyActionPlanner__Web__ProcessingProgress__Loading__v1.jpg |
| ProcessingProgress | Empty | Web | CMSDeficiencyActionPlanner__Web__ProcessingProgress__Empty__v1.jpg |
| ProcessingProgress | Error | Web | CMSDeficiencyActionPlanner__Web__ProcessingProgress__Error__v1.jpg |
| ProcessingProgress | Validation | Web | CMSDeficiencyActionPlanner__Web__ProcessingProgress__Validation__v1.jpg |
| ExtractionReview | Default | Web | CMSDeficiencyActionPlanner__Web__ExtractionReview__Default__v1.jpg |
| ExtractionReview | Loading | Web | CMSDeficiencyActionPlanner__Web__ExtractionReview__Loading__v1.jpg |
| ExtractionReview | Empty | Web | CMSDeficiencyActionPlanner__Web__ExtractionReview__Empty__v1.jpg |
| ExtractionReview | Error | Web | CMSDeficiencyActionPlanner__Web__ExtractionReview__Error__v1.jpg |
| ExtractionReview | Validation | Web | CMSDeficiencyActionPlanner__Web__ExtractionReview__Validation__v1.jpg |
| UncertaintyResolution | Default | Web | CMSDeficiencyActionPlanner__Web__UncertaintyResolution__Default__v1.jpg |
| UncertaintyResolution | Loading | Web | CMSDeficiencyActionPlanner__Web__UncertaintyResolution__Loading__v1.jpg |
| UncertaintyResolution | Empty | Web | CMSDeficiencyActionPlanner__Web__UncertaintyResolution__Empty__v1.jpg |
| UncertaintyResolution | Error | Web | CMSDeficiencyActionPlanner__Web__UncertaintyResolution__Error__v1.jpg |
| UncertaintyResolution | Validation | Web | CMSDeficiencyActionPlanner__Web__UncertaintyResolution__Validation__v1.jpg |
| PocAuthoring | Default | Web | CMSDeficiencyActionPlanner__Web__PocAuthoring__Default__v1.jpg |
| PocAuthoring | Loading | Web | CMSDeficiencyActionPlanner__Web__PocAuthoring__Loading__v1.jpg |
| PocAuthoring | Empty | Web | CMSDeficiencyActionPlanner__Web__PocAuthoring__Empty__v1.jpg |
| PocAuthoring | Error | Web | CMSDeficiencyActionPlanner__Web__PocAuthoring__Error__v1.jpg |
| PocAuthoring | Validation | Web | CMSDeficiencyActionPlanner__Web__PocAuthoring__Validation__v1.jpg |
| ApprovalReview | Default | Web | CMSDeficiencyActionPlanner__Web__ApprovalReview__Default__v1.jpg |
| ApprovalReview | Loading | Web | CMSDeficiencyActionPlanner__Web__ApprovalReview__Loading__v1.jpg |
| ApprovalReview | Empty | Web | CMSDeficiencyActionPlanner__Web__ApprovalReview__Empty__v1.jpg |
| ApprovalReview | Error | Web | CMSDeficiencyActionPlanner__Web__ApprovalReview__Error__v1.jpg |
| ApprovalReview | Validation | Web | CMSDeficiencyActionPlanner__Web__ApprovalReview__Validation__v1.jpg |
| ApprovedExport | Default | Web | CMSDeficiencyActionPlanner__Web__ApprovedExport__Default__v1.jpg |
| ApprovedExport | Loading | Web | CMSDeficiencyActionPlanner__Web__ApprovedExport__Loading__v1.jpg |
| ApprovedExport | Empty | Web | CMSDeficiencyActionPlanner__Web__ApprovedExport__Empty__v1.jpg |
| ApprovedExport | Error | Web | CMSDeficiencyActionPlanner__Web__ApprovedExport__Error__v1.jpg |
| ApprovedExport | Validation | Web | CMSDeficiencyActionPlanner__Web__ApprovedExport__Validation__v1.jpg |

### Total Export Count

- **Screens**: 8
- **States per screen**: 5
- **Total JPGs**: 40 primary web-state exports. Responsive behavior is additionally validated at 375px, 768px, and 1440px before export.

---

## 13. Figma File Structure

### Page Organization

~~~text
CMS Deficiency Action Planner Figma File
+-- 00_Cover
|   +-- Project metadata, version, stakeholders, last updated
+-- 01_Foundations
|   +-- Primitive and semantic color tokens: Light, Dark, High Contrast
|   +-- IBM Plex Sans and IBM Plex Mono typography scale
|   +-- Spacing, radius, elevation, grid, and motion tokens
+-- 02_Components
|   +-- C/Actions/[Button, IconButton, Link]
|   +-- C/Inputs/[TextField, TextArea, FileUpload, RadioGroup, Select]
|   +-- C/Navigation/[AppHeader, WorkflowRail, Breadcrumb, Tabs, DeficiencyList]
|   +-- C/Content/[EvidenceViewer, FieldEditor, CandidateComparison, PocSection, RevisionHistory]
|   +-- C/Feedback/[Alert, StatusBadge, ProgressBar, StageTimeline, Modal, Drawer, Toast, Tooltip, Skeleton]
|   +-- C/Layout/[AppShell, SplitPane, Stack, Grid, Divider, ScrollRegion]
+-- 03_Patterns
|   +-- Authentication form
|   +-- Bounded file intake
|   +-- Processing timeline and retry
|   +-- Evidence-linked field review
|   +-- Five-part POC editor
|   +-- Approval and export gate
|   +-- Error, empty, loading, validation, and destructive confirmation
+-- 04_Screens
|   +-- SignIn/[Default, Loading, Empty, Error, Validation]
|   +-- DocumentIntake/[Default, Loading, Empty, Error, Validation]
|   +-- ProcessingProgress/[Default, Loading, Empty, Error, Validation]
|   +-- ExtractionReview/[Default, Loading, Empty, Error, Validation]
|   +-- UncertaintyResolution/[Default, Loading, Empty, Error, Validation]
|   +-- PocAuthoring/[Default, Loading, Empty, Error, Validation]
|   +-- ApprovalReview/[Default, Loading, Empty, Error, Validation]
|   +-- ApprovedExport/[Default, Loading, Empty, Error, Validation]
+-- 05_Prototype
|   +-- FL-001 Authenticate local user
|   +-- FL-002 Upload through confirmed extraction
|   +-- FL-003 Generate and edit POC
|   +-- FL-004 Approve and export current revision
|   +-- FL-005 End transient session
|   +-- FL-006 Recover failed processing
+-- 06_Handoff
  +-- Token usage rules and mode mappings
  +-- Component properties and naming
  +-- 375px, 768px, 1440px, and >=1920px responsive behavior
  +-- Long SOD, many deficiencies, stale approval, timeout, and cleanup edge cases
  +-- Focus order, landmarks, live regions, labels, and keyboard interactions
  +-- Assumptions and implementation traceability
~~~

---

## 14. Quality Checklist

### Pre-Export Validation

- [x] All screens specify Default, Loading, Empty, Error, and Validation states.
- [x] All components are constrained to semantic or component tokens with no consumer hard-coded values.
- [x] Color requirements specify WCAG 2.2 AA contrast of at least 4.5:1 for body text and 3:1 for UI and large text.
- [x] Focus states and focus order are specified for every interactive surface.
- [x] Touch targets are at least 44x44px on mobile and tablet.
- [x] Six prototype flows include entry, steps, decisions, success, cancellation, and error exits.
- [x] Screen, state, component, and export naming conventions are specified.
- [x] The 40-frame export manifest is complete.

### Post-Generation

- [x] The design system document is defined at `.propel/context/docs/designsystem.md`.
- [x] The export manifest is included in this specification.
- [x] JPG filenames follow the required app, platform, screen, state, and version convention.
- [x] The `06_Handoff` page contents are specified for implementation.
