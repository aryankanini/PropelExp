# Task - TASK_005

## Requirement Reference
- **User Story:** US_016
- **Story Location:** .propel/context/tasks/EP-002/us_016/us_016.md
- **Acceptance Criteria:**
  - AC-001: Every page is classified as native-text or OCR-required with a retained reason before extraction.
  - AC-002: Complete native-text pages retain text and coordinates without OCR.
  - AC-003: Only incomplete native-text pages are sent through the approved OCR port with page coordinates retained.
  - AC-004: OCR failure marks the page and OCR stage failed without confirming page content.
  - AC-005: Whitespace, line breaks, encoding artifacts, and OCR noise are normalized without changing substantive content.
- **Edge Cases:**
  - Text empty after artifact removal is routed to OCR rather than passed as native text.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | FR-003 requires normalized text before CMS structure detection. |

---

## Task Overview
Implement conservative page-text normalization with substantive-content safeguards. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_002, TASK_004 - Requires native and OCR text spans.

## Impacted Components
- New deterministic extraction text normalizer.

## Implementation Plan
- Normalize encoding artifacts, whitespace, line breaks, and known OCR noise.
- Preserve source coordinates and flag pages that become substantively empty.

## Current Project State
- Native and OCR extraction are planned without shared normalization.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/modules/extraction/text_normalizer.py | Normalize page text conservatively. |

## External References
- https://docs.python.org/3.14/library/unicodedata.html

## Build Commands
- `cd backend; python -m pytest tests/unit/modules/extraction/test_text_normalizer.py`

## Implementation Validation Strategy
- [x] Golden tests prove artifact cleanup without substantive text changes.

## Implementation Checklist
- [x] Preserve the retained page classification and reason through normalization for AC-001.
- [x] Preserve native-text coordinates while normalizing complete page text for AC-002.
- [x] Preserve OCR page coordinates while normalizing returned text for AC-003.
- [x] Skip normalization and confirm no content for pages carrying an OCR failure for AC-004.
- [x] Normalize whitespace, line breaks, encoding artifacts, and OCR noise for AC-005.
- [x] Preserve substantive text and page evidence for AC-005.
- [x] Mark normalization-empty native pages OCR-required for AC-005.
