# Task - TASK_001

## Requirement Reference
- **User Story:** US_018
- **Story Location:** .propel/context/tasks/EP-002/us_018/us_018.md
- **Acceptance Criteria:**
  - AC-001: CMS-2567 structural markers identify the document and retain its layout pattern; unrecognized documents stop extraction.
  - AC-002: Each detected F-tag has a separate complete SOD record with source evidence.
  - AC-003: Deficiencies without a complete SOD remain unconfirmed and uncertain for review.
- **Edge Cases:**
  - Recognizable headers with no F-tags produce structure-detected with zero deficiencies.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | FR-005 requires deterministic CMS structure detection. |

---

## Task Overview
Detect and retain supported CMS-2567 layout patterns from normalized page text. Estimated effort: 8 hours.

## Dependent Tasks
- US_016 TASK_006 - Requires ordered normalized page text.

## Impacted Components
- New CMS structure detector and layout values.

## Implementation Plan
- Evaluate structural markers across ordered pages.
- Retain the detected layout or stop with an unrecognized result.

## Current Project State
- No CMS extraction module source exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/modules/extraction/cms_structure_detector.py | Detect CMS-2567 layout patterns. |
| CREATE | backend/src/cms_planner/domain/cms_layout.py | Represent recognized and unrecognized layouts. |

## External References
- https://www.cms.gov/medicare/health-safety-standards/certification-compliance/downloads/cms-2567.pdf

## Build Commands
- `cd backend; python -m pytest tests/unit/modules/extraction/test_cms_structure_detector.py`

## Implementation Validation Strategy
- [x] Fixtures cover recognized layouts, unrecognized documents, and zero-F-tag forms.

## Implementation Checklist
- [x] Detect CMS-2567 structural markers and retain layout for AC-001.
- [x] Stop extraction for unrecognized structure for AC-001.
- [x] Preserve structure-detected with zero deficiencies when no F-tag exists for AC-001.
- [x] Expose the retained recognized layout as the boundary detector input for separate evidence-linked records in AC-002.
- [x] Prevent deficiency candidate creation when structure is unrecognized so no incomplete record is promoted for AC-003.
