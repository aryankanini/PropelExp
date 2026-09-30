# Task - TASK_003

## Requirement Reference
- **User Story:** US_016
- **Story Location:** .propel/context/tasks/EP-002/us_016/us_016.md
- **Acceptance Criteria:**
  - AC-001: Every page is classified as native-text or OCR-required with a retained reason before extraction.
  - AC-002: Complete native-text pages retain text and coordinates without OCR.
  - AC-003: Only OCR-required pages are sent through the approved OCR port and return text with coordinates.
  - AC-004: OCR failure marks the page and stage failed with no confirmed content.
  - AC-005: Extracted text is normalized without changing substantive content before CMS structure detection.
- **Edge Cases:**
  - Mixed native and OCR pages retain page order.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-001 |
| **AI Pattern** | Hybrid |
| **Prompt Template Path** | Contract-only task; no prompt template is used |
| **Guardrails Config** | Closed request, response, and failure schema defined by this task |
| **Model Provider** | Provider-neutral contract; no provider is selected |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | Provider-neutral OCR adapter contract | Adapter contract v1 | AIR-001 requires an application-owned replaceable OCR port. |

---

## Task Overview
Define the provider-neutral OCR request, response, and failure contract. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires OCR-required page classifications.

## Impacted Components
- New application OCR port and result types.

## Implementation Plan
- Define minimum-necessary page requests and coordinate-bearing responses.
- Model safe failure without provider SDK types or confirmed content.

## Current Project State
- No OCR port or provider is approved or implemented.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/application/ports/ocr.py | Define adapter contract v1 OCR operations. |
| CREATE | backend/src/cms_planner/application/ports/ocr_types.py | Define provider-neutral requests, responses, and failures. |

## External References
- https://docs.python.org/3.14/library/typing.html

## Build Commands
- `cd backend; python -m pytest tests/unit/application/ports/test_ocr_port.py`

## Implementation Validation Strategy
- [x] Contract tests reject provider-specific types and missing coordinates.

## Implementation Checklist
- [x] Require retained OCR-required classification and page identity in OCR requests for AC-001.
- [x] Reject OCR requests for pages classified as complete native text for AC-002.
- [x] Define minimum-necessary OCR page requests for AC-003.
- [x] Require text and coordinates in successful OCR responses for AC-003.
- [x] Define page-and-stage failure without confirmed content for AC-004.
- [x] Return raw OCR text and coordinates without normalization so the downstream normalizer owns AC-005.
