# Task - TASK_006

## Requirement Reference
- **User Story:** US_016
- **Story Location:** .propel/context/tasks/EP-002/us_016/us_016.md
- **Acceptance Criteria:**
  - AC-001: Pages are classified before extraction.
  - AC-002: Native pages retain text and coordinates without OCR.
  - AC-003: OCR-required pages alone use OCR and retain coordinates.
  - AC-004: OCR failure creates failed page and stage state.
  - AC-005: Text is normalized before structure detection.
- **Edge Cases:**
  - Mixed routes preserve page order; normalization-empty native pages reroute to OCR.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | UC-002 requires one ordered page extraction pipeline. |

---

## Task Overview
Orchestrate classification, native extraction, OCR fallback, normalization, and failure state. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 through TASK_005 - Requires each extraction stage.

## Impacted Components
- New page extraction application service.

## Implementation Plan
- Execute stages in page order and reroute normalization-empty pages once.
- Preserve successful pages while recording typed page and stage failures.

## Current Project State
- Individual extraction stages are planned without orchestration.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/modules/extraction/page_extraction_service.py | Coordinate ordered mixed-document extraction. |

## External References
- https://docs.python.org/3.14/library/asyncio-task.html

## Build Commands
- `cd backend; python -m pytest tests/integration/extraction/test_page_pipeline.py`

## Implementation Validation Strategy
- [x] Mixed-document tests cover all routes, failures, order, and normalization.

## Implementation Checklist
- [x] Classify all pages before extraction for AC-001.
- [x] Retain native text without OCR for AC-002.
- [x] Send only required pages to OCR and retain coordinates for AC-003.
- [x] Preserve safe page and stage failure state for AC-004.
- [x] Normalize all successful page text before structure detection for AC-005.
