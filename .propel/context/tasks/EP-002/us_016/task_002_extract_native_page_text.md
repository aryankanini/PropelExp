# Task - TASK_002

## Requirement Reference
- **User Story:** US_016
- **Story Location:** .propel/context/tasks/EP-002/us_016/us_016.md
- **Acceptance Criteria:**
  - AC-001: Every page is classified as native-text or OCR-required with a retained reason before extraction.
  - AC-002: Complete native text and coordinates are retained without OCR.
  - AC-003: Only incomplete native-text pages are sent through the approved OCR port with page coordinates retained.
  - AC-004: OCR failure marks the page and OCR stage failed without confirming page content.
  - AC-005: Extracted text is normalized without changing substantive content before CMS structure detection.
- **Edge Cases:**
  - Mixed documents preserve page order across extraction methods.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | FR-003 requires native text and coordinates for complete pages. |

---

## Task Overview
Extract native page text and coordinates while preserving document order. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires page routing decisions.

## Impacted Components
- New native document extraction adapter.

## Implementation Plan
- Read only pages classified for native extraction.
- Return page-numbered text spans and coordinates in source order.

## Current Project State
- Page classification is planned without a native extraction adapter.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/adapters/filesystem/native_text_extractor.py | Extract ordered native text spans. |
| CREATE | backend/src/cms_planner/domain/text_span.py | Represent page text and coordinates. |

## External References
- https://docs.python.org/3.14/library/dataclasses.html

## Build Commands
- `cd backend; python -m pytest tests/unit/adapters/filesystem/test_native_text_extractor.py`

## Implementation Validation Strategy
- [x] Native pages retain text, coordinates, and page order without OCR calls.

## Implementation Checklist
- [x] Require a retained page classification before native extraction begins for AC-001.
- [x] Extract complete native text and coordinates for AC-002.
- [x] Preserve source page order in returned spans for AC-002.
- [x] Avoid OCR invocation for native-text pages for AC-002.
- [x] Return incomplete pages to the OCR-required route without invoking a provider in this layer for AC-003.
- [x] Return no confirmed native content for a page routed to failed OCR processing for AC-004.
- [x] Preserve raw substantive text and coordinates as normalization input for AC-005.
