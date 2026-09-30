# Task - TASK_001

## Requirement Reference
- **User Story:** US_017
- **Story Location:** .propel/context/tasks/EP-002/us_017/us_017.md
- **Acceptance Criteria:**
  - AC-001: Provider values include page, snippet, confidence, and uncertainty.
  - AC-002: Candidates lacking a page or supporting snippet are rejected before entering case state.
- **Edge Cases:**
  - Conflicting provider names remain separate uncertain candidates.

---

## AI References
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-002 |
| **AI Pattern** | Hybrid |
| **Prompt Template Path** | Contract-only task; no prompt template is used |
| **Guardrails Config** | backend/src/cms_planner/application/ports/extraction_schema.json |
| **Model Provider** | Provider-neutral contract; no provider is selected |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | JSON Schema and adapter contract | JSON Schema 2020-12; adapter contract v1 | AIR-002 requires closed evidence-linked extraction responses. |

---

## Task Overview
Define the provider-neutral provider-field extraction contract and closed schema. Estimated effort: 8 hours.

## Dependent Tasks
- US_016 TASK_006 - Requires normalized page text and coordinates.

## Impacted Components
- New extraction port contract and provider candidate schema.

## Implementation Plan
- Define minimum-necessary page-text input and candidate output.
- Require evidence, confidence, and uncertainty while preserving conflicts.

## Current Project State
- No provider extraction port or approved model provider exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/application/ports/provider_extraction.py | Define adapter contract v1 operations. |
| CREATE | backend/src/cms_planner/application/ports/extraction_schema.json | Define the closed JSON Schema 2020-12 candidate shape. |

## External References
- https://json-schema.org/draft/2020-12

## Build Commands
- `cd backend; python -m pytest tests/contract/test_provider_extraction_port.py`

## Implementation Validation Strategy
- [x] Contract tests require all evidence fields and preserve conflicting candidates.

## Implementation Checklist
- [x] Require page, snippet, confidence, and uncertainty for AC-001.
- [x] Preserve conflicting provider names as separate uncertain candidates for AC-001.
- [x] Keep the contract provider-neutral for AC-001.
- [x] Reject response candidates without both page and supporting snippet before case-state mapping for AC-002.
