# Task - TASK_007

## Requirement Reference
- **User Story:** US_018
- **Story Location:** .propel/context/tasks/EP-002/us_018/us_018.md
- **Acceptance Criteria:**
  - AC-001: Recognized and unrecognized CMS structure states are visible.
  - AC-002: Every F-tag and complete SOD is separately reviewable with evidence.
  - AC-003: Incomplete SOD records are visibly uncertain and unconfirmed.
- **Edge Cases:**
  - Repeated tags remain separate; zero deficiencies is not labeled unrecognized.

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
| Frontend | React and TypeScript | React 19.3; TypeScript 7.0 | FR-005 requires independent evidence-linked deficiency review. |

---

## Task Overview
Render CMS layout outcome and separate deficiency candidates on SCR-004. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_006 - Requires stored extraction projection.

## Impacted Components
- New deficiency list, SOD evidence, and uncertainty presentation.

## Implementation Plan
- Render stable identities for repeated tags and complete evidence.
- Distinguish unrecognized, recognized-empty, complete, and uncertain states.

## Current Project State
- No deficiency review UI source exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/features/extraction-review/DeficiencyList.tsx | Render separate deficiency candidates. |
| CREATE | frontend/src/features/extraction-review/DeficiencyEvidence.tsx | Render complete SOD and source evidence. |

## External References
- https://react.dev/learn/rendering-lists

## Build Commands
- `cd frontend; npm run build; npm test -- --run`

## Implementation Validation Strategy
- [ ] Component tests cover repeated tags, complete SOD, uncertainty, zero results, and unrecognized state.

## Implementation Checklist
- [ ] Show recognized and unrecognized layout outcomes for AC-001.
- [ ] Render every F-tag and complete SOD as a separate record for AC-002.
- [ ] Show source evidence for each deficiency for AC-002.
- [ ] Mark incomplete SOD records uncertain and unconfirmed for AC-003.
