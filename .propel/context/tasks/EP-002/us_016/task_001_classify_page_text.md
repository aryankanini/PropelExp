# Task - TASK_001

## Requirement Reference
- **User Story:** US_016
- **Story Location:** .propel/context/tasks/EP-002/us_016/us_016.md
- **Acceptance Criteria:**
  - AC-001: Every page is classified as native-text or OCR-required with a retained reason before extraction.
  - AC-002: Complete native-text pages retain text and coordinates without OCR.
  - AC-003: Only incomplete native-text pages are sent through the approved OCR port with page coordinates retained.
  - AC-004: OCR failure marks the page and OCR stage failed without confirming page content.
  - AC-005: Extracted text is normalized without changing substantive content before CMS structure detection.
- **Edge Cases:**
  - A page empty after artifact removal is treated as OCR-required.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | FR-003 requires deterministic page-level routing before extraction. |

---

## Task Overview
Classify each page’s native-text completeness and retain the routing rationale. Estimated effort: 8 hours.

## Dependent Tasks
- US_012 - Requires a validated document.

## Impacted Components
- New page classification policy in the extraction module.

## Implementation Plan
- Assess ordered pages for substantive native text.
- Persist native-text or OCR-required classification with a closed reason.

## Current Project State
- No extraction source exists; design.md only defines the planned extraction module.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/modules/extraction/page_classifier.py | Classify page extraction routes. |
| CREATE | backend/src/cms_planner/domain/page.py | Define page route and reason values. |

## External References
- https://docs.python.org/3.14/library/enum.html

## Build Commands
- `cd backend; python -m pytest tests/unit/modules/extraction/test_page_classifier.py`

## Implementation Validation Strategy
- [x] Unit tests cover complete, incomplete, blank, and mixed page classifications.

## Implementation Checklist
- [x] Assess every page before extraction for AC-001.
- [x] Retain the native-text or OCR-required decision and reason for AC-001.
- [x] Route normalized-empty pages to OCR for AC-001.
- [x] Emit the native-text route consumed by extraction without an OCR request for AC-002.
- [x] Emit the OCR-required route only for the affected incomplete page for AC-003.
- [x] Retain page identity and routing state for safe OCR failure reporting in AC-004.
- [x] Classify pages that become empty after normalization as OCR-required for AC-005.
