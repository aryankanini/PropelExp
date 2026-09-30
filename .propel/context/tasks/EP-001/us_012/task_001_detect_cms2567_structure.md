# Task - TASK_001

## Requirement Reference
- **User Story:** US_012
- **Story Location:** .propel/context/tasks/EP-001/us_012/us_012.md
- **Acceptance Criteria:**
  - AC-001: A readable supported CMS-2567 is accepted and marked extraction-ready.
  - AC-002: An unreadable or non-CMS-2567 document is rejected with no extraction result.
- **Edge Cases:**
  - Mixed readability is rejected when CMS-2567 identity cannot be established.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | FR-002 and TR-005 require deterministic structure validation before extraction. |

---

## Task Overview
Implement readable CMS-2567 identity validation and extraction-ready outcomes. Estimated effort: 8 hours.

## Dependent Tasks
- US_011 TASK_003 - Requires a completed bounded upload.

## Impacted Components
- New intake document validator and validation result types.

## Implementation Plan
- Detect supported readability and required CMS-2567 structural markers.
- Return accepted or typed rejection without creating extraction data.

## Current Project State
- Upload preflight is planned without CMS-2567 identity checks.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/modules/intake/cms2567_validator.py | Validate readability and document identity. |
| CREATE | backend/src/cms_planner/modules/intake/validation_result.py | Represent extraction-ready and rejection outcomes. |

## External References
- https://www.cms.gov/medicare/health-safety-standards/certification-compliance/downloads/cms-2567.pdf

## Build Commands
- `cd backend; python -m pytest tests/unit/modules/intake/test_cms2567_validator.py`

## Implementation Validation Strategy
- [x] Representative valid, unreadable, non-CMS, and mixed documents produce expected outcomes.

## Implementation Checklist
- [x] Mark readable structurally valid documents extraction-ready for AC-001.
- [x] Reject unreadable and non-CMS-2567 documents for AC-002.
- [x] Create no extraction result for rejected documents for AC-002.
