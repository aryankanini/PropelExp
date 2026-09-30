# Task - TASK_001

## Requirement Reference

- **User Story**: US_029 - Resolve missing POC information
- **Story Location**: .propel/context/tasks/EP-004/us_029/us_029.md
- **Acceptance Criteria**:
	- **AC-001: Display guarded draft**
		- **Given**: A grounded draft contains typed missing-information markers
		- **When**: The draft is displayed
		- **Then**: Each marker names the needed fact and keeps approval readiness blocked
	- **AC-002: Supply missing fact**
		- **Given**: A reviewer enters a supported missing fact
		- **When**: The draft is saved
		- **Then**: A user-edited revision replaces the marker and preserves its revision history
- **Edge Cases**:
	- Removing a required value restores the missing marker and incomplete state.

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
| **Design Tokens** | .propel/context/docs/designsystem.md - semantic tokens and PocSection, TextField, Alert components |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | TR-002 |

---

## Task Overview

Display named missing-information markers, block approval readiness, and let reviewers replace markers with supported facts while preserving revision context. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_028: Typed grounding results must be available.
- No same-story task dependency.

---

## Impacted Components

- `frontend/src/features/poc-authoring/MissingInformationEditor.tsx` (CREATE)
- `frontend/src/features/poc-authoring/PocReadiness.tsx` (CREATE)

---

## Implementation Plan

1. Render each marker with the needed fact and an explicit approval-readiness block.
2. Capture a supported replacement and submit it against the current draft revision.
3. Restore the marker and incomplete state when a required replacement is removed.

---

## Current Project State

- Greenfield repository; missing-information editing UI does not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `frontend/src/features/poc-authoring/MissingInformationEditor.tsx` | Capture supported replacement facts against the current revision. |
| CREATE | `frontend/src/features/poc-authoring/PocReadiness.tsx` | Display named markers and approval-readiness blocks. |

---

## External References

- [React textarea documentation](https://react.dev/reference/react-dom/components/textarea)
- [WCAG labels or instructions](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html)

---

## Build Commands

- Use the frontend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical frontend build and type check.
- [ ] Verify integration tests cover named markers, readiness blocking, supported replacement, and marker restoration.

---

## Implementation Checklist

- [ ] Render named markers and blocked readiness. (AC-001)
- [ ] Capture supported replacement facts with revision context. (AC-002)
- [ ] Restore markers when required values are removed. (AC-001, AC-002)
- [ ] Display User-edited origin after successful replacement. (AC-002)
