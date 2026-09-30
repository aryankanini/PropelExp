# Task - TASK_001

## Requirement Reference

- **User Story**: US_026 - Generate one POC per deficiency
- **Story Location**: .propel/context/tasks/EP-004/us_026/us_026.md
- **Acceptance Criteria**:
	- **AC-001: Scoped generation**
		- **Given**: A deficiency has a confirmed current revision
		- **When**: The reviewer requests a POC
		- **Then**: Only that deficiency's reviewed fields and evidence are sent for generation and one unapproved draft is returned
	- **AC-002: Unconfirmed request**
		- **Given**: A deficiency is unconfirmed
		- **When**: Generation is requested
		- **Then**: The request is denied without invoking the provider
- **Edge Cases**:
	- Concurrent requests for the same revision produce at most one current draft revision.

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
| **Design Tokens** | .propel/context/docs/designsystem.md - semantic tokens and PocSection, Alert, StatusBadge components |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | TR-002 |

---

## Task Overview

Add per-deficiency POC generation controls that are available only for confirmed current revisions and display one unapproved draft result. Estimated effort: 7 hours.

---

## Dependent Tasks

- US_024: Confirmed deficiency state must be available.
- No same-story task dependency.

---

## Impacted Components

- `frontend/src/features/poc-authoring/GeneratePocAction.tsx` (CREATE)
- `frontend/src/features/poc-authoring/PocDraftView.tsx` (CREATE)

---

## Implementation Plan

1. Scope generation actions to the selected confirmed deficiency and revision.
2. Disable and explain generation for unconfirmed deficiencies.
3. Coalesce repeated submissions while pending and render the single returned unapproved draft.

---

## Current Project State

- Greenfield repository; POC authoring UI does not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `frontend/src/features/poc-authoring/GeneratePocAction.tsx` | Scope generation to a confirmed deficiency and coalesce pending requests. |
| CREATE | `frontend/src/features/poc-authoring/PocDraftView.tsx` | Display the single returned unapproved draft. |

---

## External References

- [React transitions](https://react.dev/reference/react/startTransition)
- [TypeScript documentation](https://www.typescriptlang.org/docs/)

---

## Build Commands

- Use the frontend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical frontend build and type check.
- [ ] Verify integration tests cover confirmed generation, blocked unconfirmed state, pending deduplication, and unapproved result display.

---

## Implementation Checklist

- [ ] Create the deficiency-scoped generation action. (AC-001)
- [ ] Block unconfirmed deficiencies with an explicit reason. (AC-002)
- [ ] Prevent duplicate pending submissions and display one draft. (AC-001)
