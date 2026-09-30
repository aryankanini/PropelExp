# Task - TASK_004

## Requirement Reference
- **User Story:** US_016
- **Story Location:** .propel/context/tasks/EP-002/us_016/us_016.md
- **Acceptance Criteria:**
  - AC-001: Every page is classified as native-text or OCR-required with a retained reason before extraction.
  - AC-002: Complete native-text pages retain text and coordinates without OCR.
  - AC-003: Only incomplete pages reach the approved OCR port and retain coordinates.
  - AC-004: Failed OCR pages and stages are recorded without confirmed content.
  - AC-005: Extracted text is normalized without changing substantive content before CMS structure detection.
- **Edge Cases:**
  - Mixed extraction methods preserve page order.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-001 |
| **AI Pattern** | Hybrid |
| **Prompt Template Path** | Adapter-only task; no prompt template is used |
| **Guardrails Config** | backend/src/cms_planner/adapters/ocr/validation.py |
| **Model Provider** | Provider-neutral adapter; no provider is selected |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | Provider-neutral OCR adapter contract | Adapter contract v1 | AIR-001 requires approved, replaceable provider adapters. |

---

## Task Overview
Implement the guarded OCR adapter boundary without selecting a provider. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_003 - Requires the OCR port contract.

## Impacted Components
- New provider-neutral OCR adapter facade and validation.

## Implementation Plan
- Enforce approval before outbound invocation and minimize each page request.
- Validate coordinate-bearing results and map failures to safe outcomes.

## Current Project State
- No provider is approved; only the application-owned port is planned.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/adapters/ocr/adapter.py | Implement the provider-neutral guarded facade. |
| CREATE | backend/src/cms_planner/adapters/ocr/validation.py | Validate OCR responses and coordinates. |

## External References
- https://json-schema.org/draft/2020-12

## Build Commands
- `cd backend; python -m pytest tests/contract/test_ocr_adapter.py`

## Implementation Validation Strategy
- [x] Fake-adapter tests verify approval, payload minimization, coordinates, and failure mapping.

## Implementation Checklist
- [x] Require the retained OCR-required classification before adapter invocation for AC-001.
- [x] Refuse adapter invocation for complete native-text pages for AC-002.
- [x] Invoke OCR only for OCR-required pages through the port for AC-003.
- [x] Require approved configuration before invocation for AC-003.
- [x] Preserve returned page coordinates for AC-003.
- [x] Record safe page and stage failures with no confirmed content for AC-004.
- [x] Return raw substantive OCR text for downstream normalization without altering it for AC-005.
