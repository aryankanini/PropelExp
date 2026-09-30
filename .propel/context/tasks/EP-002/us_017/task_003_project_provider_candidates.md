# Task - TASK_003

## Requirement Reference
- **User Story:** US_017
- **Story Location:** .propel/context/tasks/EP-002/us_017/us_017.md
- **Acceptance Criteria:**
  - AC-001: Every provider value exposes page, snippet, confidence, and uncertainty.
  - AC-002: Invalid candidates never appear in case state.
- **Edge Cases:**
  - Conflicting provider names remain separate uncertain candidates.

---

## Design References
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | N/A |
| **Wireframe Status** | AVAILABLE |
| **Wireframe Type** | HTML |
| **Wireframe Path/URL** | .propel/context/wireframes/Hi-Fi/wireframe-SCR-004-extraction-review.html |
| **Screen Spec** | SCR-004 |
| **UXR Requirements** | N/A |
| **Design Tokens** | .propel/context/docs/designsystem.md |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React and TypeScript | React 19.3; TypeScript 7.0 | FR-004 requires evidence-linked provider presentation. |

---

## Task Overview
Render provider candidates with evidence, confidence, uncertainty, and conflicts on SCR-004. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_002 - Requires validated provider candidates.

## Impacted Components
- New extraction-review provider candidate components.

## Implementation Plan
- Render each candidate and synchronized evidence as separate records.
- Show conflicts as needs-review options without selecting a final value.

## Current Project State
- No extraction review feature source exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/features/extraction-review/ProviderCandidates.tsx | Render provider candidate evidence and status. |
| CREATE | frontend/src/features/extraction-review/ProviderEvidence.tsx | Present page and supporting snippet. |

## External References
- https://react.dev/reference/react

## Build Commands
- `cd frontend; npm run build; npm test -- --run`

## Implementation Validation Strategy
- [ ] Component tests prove complete evidence and separate conflict presentation.

## Implementation Checklist
- [ ] Show page, snippet, confidence, and uncertainty for AC-001.
- [ ] Keep conflicting names separate and marked for review for AC-001.
- [ ] Exclude rejected candidates from rendered case state for AC-002.
