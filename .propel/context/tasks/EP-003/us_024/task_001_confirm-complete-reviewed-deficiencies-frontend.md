# Task - TASK_001

## Requirement Reference

- **User Story**: US_024 - Confirm complete reviewed deficiencies
- **Story Location**: .propel/context/tasks/EP-003/us_024/us_024.md
- **Acceptance Criteria**:
	- **AC-001: Confirm complete deficiency**
		- **Given**: The F-tag, complete SOD, and supporting evidence are resolved
		- **When**: The reviewer confirms the deficiency
		- **Then**: The current revision is confirmed and POC generation becomes available
	- **AC-002: Deny incomplete deficiency**
		- **Given**: Any required value or evidence is unresolved
		- **When**: Confirmation is requested
		- **Then**: Confirmation is denied and every blocking field is identified
- **Edge Cases**:
	- A confirmation based on a stale revision is denied until the reviewer reloads the current values.

---

## Design References

| Reference Type | Value |
|---|---|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/wireframe-SCR-004-extraction-review.html |
| **Screen Spec** | SCR-004 |
| **UXR Requirements** | UXR-502 |
| **Design Tokens** | .propel/context/docs/designsystem.md - semantic tokens and FieldEditor, Alert, StatusBadge components |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | TR-002 |

---

## Task Overview

Add confirmation controls that expose all blocking fields, unlock POC generation only after success, and require reload after stale revision conflicts. Estimated effort: 7 hours.

---

## Dependent Tasks

- US_022: Uncertainty resolution must be available.
- No same-story task dependency.

---

## Impacted Components

- `frontend/src/features/extraction-review/ConfirmationPanel.tsx` (CREATE)
- `frontend/src/features/extraction-review/DeficiencyStatus.tsx` (CREATE)

---

## Implementation Plan

1. Present F-tag, complete SOD, and evidence readiness with every blocking field named.
2. Submit confirmation against the displayed revision and expose POC generation after success.
3. On stale conflict, keep confirmation denied and require current-value reload.

---

## Current Project State

- Greenfield repository; deficiency confirmation UI does not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `frontend/src/features/extraction-review/ConfirmationPanel.tsx` | Show readiness, blockers, confirmation controls, and stale reload handling. |
| CREATE | `frontend/src/features/extraction-review/DeficiencyStatus.tsx` | Display confirmation and POC-generation eligibility states. |

---

## External References

- [React conditional rendering](https://react.dev/learn/conditional-rendering)
- [WCAG error identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)

---

## Build Commands

- Use the frontend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [x] Run the canonical frontend build and type check.
- [x] Verify integration tests cover complete, incomplete, and stale confirmation states plus POC action availability.

---

## Implementation Checklist

- [x] Display confirmation readiness and all blockers. (AC-001, AC-002)
- [x] Enable POC generation only after successful confirmation. (AC-001)
- [x] Handle stale conflicts with a required reload action. (AC-001, AC-002)
