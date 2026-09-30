# Task - TASK_003

## Requirement Reference

- **User Story**: US_027 - Validate five-part POC drafts
- **Story Location**: .propel/context/tasks/EP-004/us_027/us_027.md
- **Acceptance Criteria**:
	- **AC-001: Complete schema**
		- **Given**: Generated output contains affected residents, others at risk, corrective measures, monitoring, and completion date
		- **When**: Closed-schema validation runs
		- **Then**: The five sections are accepted in the fixed order with no unknown sections
	- **AC-002: Missing section**
		- **Given**: Generated output omits a required section
		- **When**: Validation runs
		- **Then**: The response is rejected as incomplete and is not stored as a completed draft
- **Edge Cases**:
	- A present but empty required section is incomplete.

---

## AI References

| Reference Type | Value |
|---|---|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-003 |
| **AI Pattern** | Provider-neutral structured generation with deterministic guardrails |
| **Prompt Template Path** | prompts/poc/ |
| **Guardrails Config** | backend/src/cms_planner/adapters/ai/guardrails.py |
| **Model Provider** | Runtime-selected BAA-approved LLM adapter |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| AI/ML | Provider-neutral adapter contract / JSON Schema / Pydantic | v1 / 2020-12 / 2.x | AIR-003 / TR-008 |

---

## Task Overview

Define provider-neutral structured generation and deterministic guardrails for exactly five required, ordered, non-empty POC sections. Estimated effort: 7 hours.

---

## Dependent Tasks

- US_026: Scoped generation input must be available.
- `task_002_validate-five-part-poc-drafts-backend.md`: Owns persistence enforcement for validated output.

---

## Impacted Components

- `prompts/poc/five_part_draft.md` (CREATE)
- `backend/src/cms_planner/adapters/ai/guardrails.py` (CREATE)
- `backend/src/cms_planner/adapters/ai/contracts.py` (CREATE)

---

## Implementation Plan

1. Define the provider-neutral response contract and closed JSON Schema for five ordered sections.
2. Instruct structured generation without provider-specific prompt syntax.
3. Reject missing, empty, reordered, or unknown sections deterministically before handoff.

---

## Current Project State

- Greenfield repository; POC prompts, AI contracts, and guardrails do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `prompts/poc/five_part_draft.md` | Define the provider-neutral structured POC prompt. |
| CREATE | `backend/src/cms_planner/adapters/ai/guardrails.py` | Enforce closed-schema, order, and non-empty guardrails. |
| CREATE | `backend/src/cms_planner/adapters/ai/contracts.py` | Define the provider-neutral five-part response contract. |

---

## External References

- [JSON Schema 2020-12 validation](https://json-schema.org/draft/2020-12/json-schema-validation)
- [Pydantic 2 JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/)

---

## Build Commands

- Use the AI and backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical schema validation and backend type checks.
- [ ] Verify contract tests use valid, missing, empty, reordered, and extra-section provider fixtures across adapter implementations.

---

## Implementation Checklist

- [ ] Define the provider-neutral five-part response contract. (AC-001, AC-002)
- [ ] Create the structured POC prompt. (AC-001)
- [ ] Enforce closed-schema, order, and non-empty guardrails. (AC-001, AC-002)
- [ ] Verify equivalent behavior across runtime-selected adapters. (AC-001, AC-002)