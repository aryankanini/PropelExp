# Task - TASK_005

## Requirement Reference
- **User Story:** US_018
- **Story Location:** .propel/context/tasks/EP-002/us_018/us_018.md
- **Acceptance Criteria:**
  - AC-001: CMS-2567 structural markers identify the document and retain its layout pattern; unrecognized documents stop extraction.
  - AC-002: Each detected F-tag has a separate complete SOD record with source evidence.
  - AC-003: A deficiency without a complete SOD remains unconfirmed and uncertain for review.
- **Edge Cases:**
  - Repeated F-tag labels remain independently reviewable.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | DR-001 and FR-005 require explicit unconfirmed candidate state. |

---

## Task Overview
Model uncertain deficiency state without promoting incomplete content. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_004 - Requires validated deficiency candidates.

## Impacted Components
- New deficiency candidate domain state and policy.

## Implementation Plan
- Represent complete and incomplete evidence independently from confirmation.
- Prevent incomplete candidates from acquiring confirmed status.

## Current Project State
- No deficiency domain state exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/domain/deficiency_candidate.py | Model candidate evidence and uncertainty. |
| CREATE | backend/src/cms_planner/domain/deficiency_policy.py | Prevent invalid confirmation transitions. |

## External References
- https://docs.python.org/3.14/library/dataclasses.html

## Build Commands
- `cd backend; python -m pytest tests/unit/domain/test_deficiency_policy.py`

## Implementation Validation Strategy
- [x] Domain tests prohibit confirmation of incomplete SOD candidates.

## Implementation Checklist
- [x] Retain the recognized CMS-2567 layout reference without creating records for unrecognized documents for AC-001.
- [x] Preserve separate F-tag record identity and source evidence for complete records for AC-002.
- [x] Retain incomplete SOD records for review for AC-003.
- [x] Mark incomplete records uncertain and unconfirmed for AC-003.
- [x] Keep repeated F-tag candidates independently identifiable for AC-003.
