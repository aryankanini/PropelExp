# Task - TASK_001

## Requirement Reference

- **User Story**: US_025 - Display content provenance states
- **Story Location**: .propel/context/tasks/EP-003/us_025/us_025.md
- **Acceptance Criteria**:
	- **AC-001: Closed provenance labels**
		- **Given**: A value or draft section is displayed
		- **When**: Its current revision loads
		- **Then**: It shows exactly one origin from Extracted, AI-generated, User-edited, or Approved and displays its revision
	- **AC-002: Stale approval**
		- **Given**: Approved content receives an edit
		- **When**: The new revision is displayed
		- **Then**: It shows User-edited and Reapproval required rather than Approved
- **Edge Cases**:
	- Historical approval remains in revision history but never labels the edited current revision.

---

## Design References

| Reference Type | Value |
|---|---|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/ |
| **Screen Spec** | SCR-004, SCR-005 |
| **UXR Requirements** | UXR-103, UXR-502 |
| **Design Tokens** | .propel/context/docs/designsystem.md - semantic tokens and RevisionHistory, StatusBadge components |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | TR-002 |

---

## Task Overview

Render exactly one closed-set origin label and revision for current values and draft sections, including Reapproval required after edits to approved content. Estimated effort: 6 hours.

---

## Dependent Tasks

- US_007: Immutable origin and revision data must be available.
- No same-story task dependency.

---

## Impacted Components

- `frontend/src/features/extraction-review/ProvenanceLabel.tsx` (CREATE)
- `frontend/src/features/extraction-review/RevisionHistory.tsx` (CREATE)

---

## Implementation Plan

1. Map current revisions to exactly one label: Extracted, AI-generated, User-edited, or Approved.
2. Display revision identifiers and Reapproval required for edits following approval.
3. Keep historical approval visible only in revision history.

---

## Current Project State

- Greenfield repository; provenance presentation components do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `frontend/src/features/extraction-review/ProvenanceLabel.tsx` | Render one closed-set origin, revision, and reapproval state. |
| CREATE | `frontend/src/features/extraction-review/RevisionHistory.tsx` | Separate historical approvals from current origin labeling. |

---

## External References

- [React rendering lists](https://react.dev/learn/rendering-lists)
- [WCAG use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

---

## Build Commands

- Use the frontend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [x] Run the canonical frontend build and type check.
- [x] Verify component tests cover each closed origin, revision display, edited approval, and historical approval labeling.

---

## Implementation Checklist

- [x] Create the closed-set provenance label component. (AC-001)
- [x] Display revision and reapproval status without color-only meaning. (AC-001, AC-002)
- [x] Separate historical approval from current origin labeling. (AC-002)
