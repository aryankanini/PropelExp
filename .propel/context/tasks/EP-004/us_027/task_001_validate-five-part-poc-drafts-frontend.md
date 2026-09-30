# Task - TASK_001

## Requirement Reference

- **User Story**: US_027 - Validate five-part POC drafts
- **Story Location**: .propel/context/tasks/EP-004/us_027/us_027.md
- **Acceptance Criteria**:
	- **AC-001: Complete schema**
		- **Given**: Generated output contains affected residents, others at risk, corrective measures, monitoring, and completion date
		- **When**: Closed-schema validation runs
		- **Then**: The five sections are accepted in the fixed order with no unknown sections
	- **AC-002: Missing section**
		- **Given**: Generated output omits a required section
		- **When**: Validation runs
		- **Then**: The response is rejected as incomplete and is not stored as a completed draft
- **Edge Cases**:
	- A present but empty required section is incomplete.

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
| **Design Tokens** | .propel/context/docs/designsystem.md - semantic tokens and PocSection, Alert components |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | TR-002 |

---

## Task Overview

Render the fixed five-part POC structure in order and surface incomplete or unknown-section validation without presenting rejected output as completed. Estimated effort: 6 hours.

---

## Dependent Tasks

- US_026: Scoped generation must be available.
- No same-story task dependency.

---

## Impacted Components

- `frontend/src/features/poc-authoring/PocDraftView.tsx` (CREATE)
- `frontend/src/features/poc-authoring/PocValidationSummary.tsx` (CREATE)

---

## Implementation Plan

1. Render affected residents, others at risk, corrective measures, monitoring, and completion date in fixed order.
2. Display missing, empty, and unknown-section validation errors.
3. Keep rejected output out of completed-draft presentation and actions.

---

## Current Project State

- Greenfield repository; five-part POC rendering does not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `frontend/src/features/poc-authoring/PocDraftView.tsx` | Render exactly five POC sections in fixed order. |
| CREATE | `frontend/src/features/poc-authoring/PocValidationSummary.tsx` | Show missing, empty, reordered, and unknown-section errors. |

---

## External References

- [React rendering lists](https://react.dev/learn/rendering-lists)
- [WCAG error identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)

---

## Build Commands

- Use the frontend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical frontend build and type check.
- [ ] Verify component tests cover fixed ordering, missing and empty errors, unknown sections, and rejected-draft state.

---

## Implementation Checklist

- [ ] Render exactly five named POC sections in fixed order. (AC-001)
- [ ] Surface missing, empty, and unknown-section errors. (AC-001, AC-002)
- [ ] Prevent rejected output from appearing completed. (AC-002)
