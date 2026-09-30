# Task - TASK_002

## Requirement Reference
- **User Story:** US_018
- **Story Location:** .propel/context/tasks/EP-002/us_018/us_018.md
- **Acceptance Criteria:**
  - AC-001: CMS-2567 structural markers identify the document and retain its layout pattern; unrecognized documents stop extraction.
  - AC-002: Every detected F-tag has a separate complete SOD record with source evidence.
  - AC-003: Missing complete SOD boundaries remain unconfirmed and uncertain.
- **Edge Cases:**
  - Repeated F-tag labels with distinct SOD sections remain separate.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | FR-005 requires deterministic deficiency boundary preservation. |

---

## Task Overview
Identify F-tag and SOD boundaries across ordered pages without merging repeated labels. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires a recognized CMS layout.

## Impacted Components
- New deficiency boundary detector.

## Implementation Plan
- Detect starts and ends using the retained layout and page coordinates.
- Emit separate complete or incomplete boundary candidates.

## Current Project State
- CMS layout detection is planned without deficiency segmentation.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/modules/extraction/deficiency_boundaries.py | Segment F-tag and SOD regions. |

## External References
- https://docs.python.org/3.14/library/re.html

## Build Commands
- `cd backend; python -m pytest tests/unit/modules/extraction/test_deficiency_boundaries.py`

## Implementation Validation Strategy
- [x] Boundary fixtures cover multi-page, repeated-tag, and incomplete SOD cases.

## Implementation Checklist
- [x] Require a retained recognized CMS-2567 layout before identifying deficiency boundaries for AC-001.
- [x] Create one boundary per detected F-tag and SOD for AC-002.
- [x] Retain source page evidence for each boundary for AC-002.
- [x] Keep repeated F-tags as separate records for AC-002.
- [x] Mark incomplete SOD boundaries unconfirmed and uncertain for AC-003.
