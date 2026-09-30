# Task - TASK_001

## Requirement Reference
- **User Story:** us_042
- **Story Location:** .propel/context/tasks/EP-007/us_042/us_042.md
- **Acceptance Criteria:** AC-001, AC-002, AC-003
- **Edge Cases:** Reject requests containing unrelated deficiency text.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python, FastAPI, Pydantic | Python 3.14.7; FastAPI 0.141.1; Pydantic 2.x | NFR-005 and TR-008 require typed configuration and application-owned ports. |

---

## Task Overview
**Estimated Effort:** 8 hours

Create provider configuration and application-owned OCR/LLM ports that enforce TLS and minimum-necessary request shaping.

## Dependent Tasks
- TASK_001 from US_041.

## Impacted Components
- Configuration models, application provider ports, outbound HTTP adapters, and composition root.

## Implementation Plan
- Model required endpoint, key, timeout, and TLS constraints.
- Define provider-neutral request/result protocols.
- Shape requests in application services before adapter invocation.
- Wire conforming adapters only through the composition root.

## Current Project State
```text
backend/src/cms_planner/{application,adapters,infrastructure/config,app.py}
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/application/ports/providers.py | Define OCR and LLM ports and minimum payload contracts. |
| CREATE | backend/src/cms_planner/infrastructure/config/providers.py | Load required provider environment settings. |
| CREATE | backend/src/cms_planner/adapters/ocr/http_adapter.py | Implement the TLS OCR adapter. |
| MODIFY | backend/src/cms_planner/app.py | Inject configured adapters into application services. |

## External References
- https://docs.pydantic.dev/2.12/concepts/pydantic_settings/
- https://fastapi.tiangolo.com/advanced/settings/

## Build Commands
- [Backend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests cover configuration and request minimization.
- [x] Integration tests verify TLS-only adapter invocation.

## Implementation Checklist
- [x] Require endpoint, API key, and timeout from environment configuration. (AC-001)
- [x] Fail startup for missing, invalid, default, or non-TLS configuration. (AC-001)
- [x] Define provider-neutral OCR and LLM application ports. (AC-002, AC-003)
- [x] Shape requests to required pages, fields, and evidence only. (AC-002, Edge Case)
- [x] Keep provider SDK types outside domain and application modules. (AC-003)
