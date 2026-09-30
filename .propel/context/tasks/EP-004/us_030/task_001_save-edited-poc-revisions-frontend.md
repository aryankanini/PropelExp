# Task - TASK_001

## Requirement Reference

- **User Story**: US_030 - Save edited POC revisions
- **Story Location**: .propel/context/tasks/EP-004/us_030/us_030.md
- **Acceptance Criteria**:
	- **AC-001: Save edit**
		- **Given**: A current POC draft exists
		- **When**: The reviewer edits one or more sections and saves
		- **Then**: A user-edited unapproved revision is appended and each changed section shows its origin
	- **AC-002: Save failure**
		- **Given**: An edit cannot be retained
		- **When**: Save fails
		- **Then**: The last retained revision remains current and the user receives a safe retry action
- **Edge Cases**:
	- A stale revision conflict does not overwrite the newer draft.

---

## Design References

| Reference Type | Value |
|---|---|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/wireframe-SCR-006-poc-authoring.html |
| **Screen Spec** | SCR-006 |
| **UXR Requirements** | N/A |
| **Design Tokens** | .propel/context/docs/designsystem.md - semantic tokens and PocSection, RevisionHistory, Alert components |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | TR-002 |

---

## Task Overview

Create five-section POC editing and safe save behavior that shows changed-section origins, retains local edits after failure, and prevents stale overwrite. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_027: The five stable sections must be available.
- No same-story task dependency.

---

## Impacted Components

- `frontend/src/features/poc-authoring/PocEditor.tsx` (CREATE)
- `frontend/src/features/poc-authoring/PocSaveStatus.tsx` (CREATE)

---

## Implementation Plan

1. Edit one or more stable POC sections and submit the current revision identifier.
2. On success, render the new unapproved User-edited revision and changed-section origins.
3. On failure or conflict, retain edits, keep the last retained revision current, and offer a safe retry or reload.

---

## Current Project State

- Greenfield repository; POC editing and save-state UI do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `frontend/src/features/poc-authoring/PocEditor.tsx` | Edit stable POC sections and submit the current revision identifier. |
| CREATE | `frontend/src/features/poc-authoring/PocSaveStatus.tsx` | Display appended revisions, changed origins, failures, retries, and conflicts. |

---

## External References

- [React textarea documentation](https://react.dev/reference/react-dom/components/textarea)
- [WCAG status messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)

---

## Build Commands

- Use the frontend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical frontend build and type check.
- [ ] Verify integration tests cover multi-section save, changed origins, retained edits on failure, retry, and stale conflict reload.

---

## Implementation Checklist

- [ ] Create stable five-section editing controls. (AC-001)
- [ ] Submit edits with the current revision identifier. (AC-001, AC-002)
- [ ] Display the appended unapproved revision and changed origins. (AC-001)
- [ ] Preserve edits and offer safe recovery after failure or conflict. (AC-002)
