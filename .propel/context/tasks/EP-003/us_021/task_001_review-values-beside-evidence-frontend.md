# Task - TASK_001

## Requirement Reference

- **User Story**: US_021 - Review values beside evidence
- **Story Location**: .propel/context/tasks/EP-003/us_021/us_021.md
- **Acceptance Criteria**:
	- **AC-001: Synchronized evidence**
		- **Given**: Provider and deficiency candidates exist
		- **When**: The reviewer selects a value
		- **Then**: Its page, full snippet, confidence, uncertainty, and origin appear and the supporting evidence is highlighted
- **Edge Cases**:
	- Long SOD text remains complete and searchable without truncating the authoritative value.

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
| **UXR Requirements** | UXR-102 |
| **Design Tokens** | .propel/context/docs/designsystem.md - Design Tokens and Component References for EvidenceViewer and FieldEditor |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| Frontend | React / TypeScript / Vite | 19.3 / 7.0 / 8.3 | TR-002 |

---

## Task Overview

Create the extraction-review interface that keeps a selected provider or deficiency value synchronized with its page, full snippet, confidence, uncertainty, origin, and highlighted evidence. Preserve and search complete SOD text. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_017: Evidence-linked candidates must be available.
- No same-story task dependency.

---

## Impacted Components

- `frontend/src/features/extraction-review/FieldEditor.tsx` (CREATE)
- `frontend/src/features/extraction-review/EvidenceViewer.tsx` (CREATE)

---

## Implementation Plan

1. Render selectable candidate values with confidence, uncertainty, origin, revision context, and an accessible selected state.
2. Synchronize selection with the evidence page and full highlighted snippet without truncating the authoritative SOD value.
3. Add in-content search and explicit empty, loading, and error states without changing the selected value.

---

## Current Project State

- Greenfield repository; the extraction-review feature components do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `frontend/src/features/extraction-review/FieldEditor.tsx` | Render candidate values, metadata, selection state, and complete searchable SOD content. |
| CREATE | `frontend/src/features/extraction-review/EvidenceViewer.tsx` | Synchronize the selected value with its evidence page, full snippet, and highlight. |

---

## External References

- [React 19.3 documentation](https://react.dev/versions#react-19)
- [TypeScript documentation](https://www.typescriptlang.org/docs/)
- [Vite documentation](https://vite.dev/guide/)

---

## Build Commands

- Use the canonical frontend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [x] Run the canonical frontend build and type check.
- [x] Verify component tests cover selection-to-evidence synchronization, highlighting, metadata, search, and untruncated long SOD content.
- [x] Verify keyboard selection, focus visibility, labels, and status announcements.

---

## Implementation Checklist

- [x] Create the synchronized candidate and evidence components. (AC-001)
- [x] Render page, full snippet, confidence, uncertainty, origin, and highlight for the selected value. (AC-001)
- [x] Preserve and search complete SOD text without truncation. (AC-001)
- [x] Handle loading, empty, and evidence-load failure states accessibly. (AC-001)
