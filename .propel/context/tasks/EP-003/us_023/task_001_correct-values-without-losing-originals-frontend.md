# Task - TASK_001

## Requirement Reference

- **User Story**: US_023 - Correct values without losing originals
- **Story Location**: .propel/context/tasks/EP-003/us_023/us_023.md
- **Acceptance Criteria**:
	- **AC-001: Correct current value**
		- **Given**: An extracted provider, F-tag, or SOD value is inaccurate
		- **When**: The reviewer saves a correction
		- **Then**: A user-edited revision becomes current and the original value, evidence, and origin remain visible
- **Edge Cases**:
	- An empty correction is rejected without incrementing the revision number.

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
| **UXR Requirements** | UXR-103 |
| **Design Tokens** | .propel/context/docs/designsystem.md - semantic tokens and FieldEditor, RevisionHistory components |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | TR-002 |

---

## Task Overview

Create correction and revision-history UI that distinguishes the current user-edited value from the original extraction, evidence, and origin. Estimated effort: 6 hours.

---

## Dependent Tasks

- US_007: Immutable revisions must be available.
- No same-story task dependency.

---

## Impacted Components

- `frontend/src/features/extraction-review/FieldEditor.tsx` (CREATE)
- `frontend/src/features/extraction-review/RevisionHistory.tsx` (CREATE)

---

## Implementation Plan

1. Provide correction editing for provider, F-tag, and SOD values.
2. Display current and original revisions with evidence and origin labels.
3. Reject empty corrections client-side without optimistic revision changes.

---

## Current Project State

- Greenfield repository; correction and revision history components do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `frontend/src/features/extraction-review/FieldEditor.tsx` | Edit provider, F-tag, and SOD values and reject empty corrections. |
| CREATE | `frontend/src/features/extraction-review/RevisionHistory.tsx` | Show current user-edited and original revisions with evidence and origin. |

---

## External References

- [React input documentation](https://react.dev/reference/react-dom/components/input)
- [WAI-ARIA status role](https://www.w3.org/WAI/ARIA/apg/practices/structural-roles/#status)

---

## Build Commands

- Use the frontend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [x] Run the canonical frontend build and type check.
- [x] Verify component tests cover valid corrections, original/current visibility, and empty correction rejection.

---

## Implementation Checklist

- [x] Create correction controls for supported value types. (AC-001)
- [x] Render original and current revision details together. (AC-001)
- [x] Prevent empty correction submission and revision changes. (AC-001)
