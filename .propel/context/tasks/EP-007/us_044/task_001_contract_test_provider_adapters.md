# Task - TASK_001

## Requirement Reference
- **User Story:** us_044
- **Story Location:** .propel/context/tasks/EP-007/us_044/us_044.md
- **Acceptance Criteria:** AC-001, AC-002
- **Edge Cases:** Reject unknown provider fields.

---

## AI References [CONDITIONAL: AI Impact = Yes]
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-002, AIR-003, AIR-004 |
| **AI Pattern** | Hybrid structured generation with deterministic validation |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | backend/src/cms_planner/adapters/ai/schemas/ |
| **Model Provider** | Runtime-selected BAA-approved adapter |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | Pydantic, JSON Schema, pytest | Pydantic 2.x; JSON Schema 2020-12; pytest 9.x | TR-008 and AIR-002 through AIR-004 require closed response contracts. |

---

## Task Overview
**Estimated Effort:** 8 hours

Create reusable provider contract fixtures for valid extraction/POC responses, closed-schema rejection, and retry exhaustion.

## Dependent Tasks
- TASK_001 from US_043.

## Impacted Components
- Adapter contract fixtures and provider conformance suite.

## Implementation Plan
- Define shared valid and invalid fixtures.
- Run each adapter through one conformance suite.
- Assert application-owned results and atomic failures.

## Current Project State
```text
backend/tests/contract/providers/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/tests/contract/providers/conftest.py | Provide shared provider fixtures. |
| CREATE | backend/tests/contract/providers/test_adapter_contract.py | Verify every adapter against one contract. |

## External References
- https://docs.pytest.org/en/9.0.x/how-to/fixtures.html
- https://docs.pydantic.dev/2.12/concepts/models/#extra-data

## Build Commands
- [Backend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Contract suite passes for each configured adapter.
- [x] Invalid fixtures return no partial payload.

## Implementation Checklist
- [x] Accept schema-valid extraction and five-part POC fixtures. (AC-001)
- [x] Assert only application-owned typed results cross the port. (AC-001)
- [x] Reject missing, malformed, and unknown response fields. (AC-002, Edge Case)
- [x] Assert retry exhaustion returns the expected typed failure. (AC-002)
- [x] Assert invalid responses expose no partial payload. (AC-002)
