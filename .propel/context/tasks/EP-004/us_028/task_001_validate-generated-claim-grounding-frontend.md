# Task - TASK_001

## Requirement Reference

- **User Story**: US_028 - Validate generated claim grounding
- **Story Location**: .propel/context/tasks/EP-004/us_028/us_028.md
- **Acceptance Criteria**:
	- **AC-001: Supported claim**
		- **Given**: A generated facility-specific claim references reviewed fields or evidence spans
		- **When**: Grounding validation runs
		- **Then**: The claim is retained with its support references
	- **AC-002: Unsupported claim**
		- **Given**: A facility-specific claim has no reviewed support
		- **When**: Grounding validation runs
		- **Then**: The claim is not presented as fact and is replaced by a typed missing-information marker
- **Edge Cases**:
	- Generic compliance guidance is not treated as facility-specific unless it asserts a case fact.

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

Display supported facility claims with reviewed support references and unsupported claims as typed missing-information markers rather than facts. Estimated effort: 7 hours.

---

## Dependent Tasks

- US_027: A schema-valid draft must be available.
- No same-story task dependency.

---

## Impacted Components

- `frontend/src/features/poc-authoring/GroundedClaim.tsx` (CREATE)
- `frontend/src/features/poc-authoring/MissingInformationMarker.tsx` (CREATE)

---

## Implementation Plan

1. Render supported facility-specific claims with navigable field or evidence-span references.
2. Render unsupported claims as typed missing-information markers without factual styling.
3. Present generic compliance guidance normally unless the response classifies it as a case assertion.

---

## Current Project State

- Greenfield repository; grounding-result components do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `frontend/src/features/poc-authoring/GroundedClaim.tsx` | Render supported claims with navigable reviewed support references. |
| CREATE | `frontend/src/features/poc-authoring/MissingInformationMarker.tsx` | Render unsupported claims as typed missing-information markers. |

---

## External References

- [React conditional rendering](https://react.dev/learn/conditional-rendering)
- [WCAG link purpose](https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html)

---

## Build Commands

- Use the frontend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical frontend build and type check.
- [ ] Verify component tests cover supported references, unsupported markers, and generic-guidance classification.

---

## Implementation Checklist

- [ ] Render grounded claims with support references. (AC-001)
- [ ] Render unsupported claims as typed missing-information markers. (AC-002)
- [ ] Distinguish generic guidance from facility-specific assertions. (AC-001, AC-002)
