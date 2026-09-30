# Task - TASK_001

## Requirement Reference

- **User Story**: US_022 - Resolve uncertain candidates
- **Story Location**: .propel/context/tasks/EP-003/us_022/us_022.md
- **Acceptance Criteria**:
	- **AC-001: Select supported candidate**
		- **Given**: Competing candidates and evidence are displayed
		- **When**: The reviewer selects an evidence-supported candidate
		- **Then**: A resolved revision is appended and the uncertainty block is removed
	- **AC-002: Enter correction**
		- **Given**: No candidate is correct
		- **When**: The reviewer enters a correction
		- **Then**: Originals remain and the new revision is labeled user-edited
	- **AC-003: Leave unresolved**
		- **Given**: Evidence is insufficient
		- **When**: The reviewer leaves the value unresolved
		- **Then**: Confirmation and drafting remain blocked for that deficiency
- **Edge Cases**:
	- Concurrent resolution against a stale revision is rejected without losing either original candidate.

---

## Design References

| Reference Type | Value |
|---|---|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/wireframe-SCR-005-uncertainty-resolution.html |
| **Screen Spec** | SCR-005 |
| **UXR Requirements** | UXR-102, UXR-502 |
| **Design Tokens** | .propel/context/docs/designsystem.md - semantic tokens and CandidateComparison, FieldEditor, Alert components |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | TR-002 |

---

## Task Overview

Create the uncertainty-resolution UI for selecting a supported candidate, entering a correction, or leaving the value unresolved while showing downstream blocks. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_021: Synchronized evidence review must be available.
- No same-story task dependency.

---

## Impacted Components

- `frontend/src/features/extraction-review/CandidateComparison.tsx` (CREATE)
- `frontend/src/features/extraction-review/UncertaintyResolution.tsx` (CREATE)

---

## Implementation Plan

1. Present competing candidates with evidence and mutually exclusive resolution actions.
2. Capture corrections without hiding originals and show unresolved confirmation/drafting blocks.
3. Submit the expected revision and retain inputs when a stale conflict is returned.

---

## Current Project State

- Greenfield repository; uncertainty-resolution UI does not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `frontend/src/features/extraction-review/CandidateComparison.tsx` | Present competing candidates, evidence, and exclusive resolution actions. |
| CREATE | `frontend/src/features/extraction-review/UncertaintyResolution.tsx` | Handle selection, correction, unresolved blocking, and stale conflicts. |

---

## External References

- [React 19 forms](https://react.dev/reference/react-dom/components/form)
- [TypeScript documentation](https://www.typescriptlang.org/docs/)

---

## Build Commands

- Use the frontend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [x] Run the canonical frontend build and type check.
- [x] Verify component and integration tests cover all three resolution paths and stale-conflict input retention.
- [x] Verify accessibility checks cover grouped choices, validation messages, and blocked-state announcements.

---

## Implementation Checklist

- [x] Build candidate comparison and correction controls. (AC-001, AC-002)
- [x] Show resolved and unresolved blocked states. (AC-001, AC-003)
- [x] Submit expected revision data and preserve input on conflict. (AC-001, AC-002)
- [x] Keep original candidates visible throughout correction. (AC-002)
