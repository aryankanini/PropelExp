# Task - TASK_003

## Requirement Reference

- **User Story**: US_028 - Validate generated claim grounding
- **Story Location**: .propel/context/tasks/EP-004/us_028/us_028.md
- **Acceptance Criteria**:
	- **AC-001: Supported claim**
		- **Given**: A generated facility-specific claim references reviewed fields or evidence spans
		- **When**: Grounding validation runs
		- **Then**: The claim is retained with its support references
	- **AC-002: Unsupported claim**
		- **Given**: A facility-specific claim has no reviewed support
		- **When**: Grounding validation runs
		- **Then**: The claim is not presented as fact and is replaced by a typed missing-information marker
- **Edge Cases**:
	- Generic compliance guidance is not treated as facility-specific unless it asserts a case fact.

---

## AI References

| Reference Type | Value |
|---|---|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-004 |
| **AI Pattern** | Provider-neutral structured generation with deterministic guardrails |
| **Prompt Template Path** | prompts/poc/ |
| **Guardrails Config** | backend/src/cms_planner/adapters/ai/guardrails.py |
| **Model Provider** | Runtime-selected BAA-approved LLM adapter |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|---|---|---|---|
| AI/ML | Provider-neutral adapter contract / JSON Schema / Pydantic | v1 / 2020-12 / 2.x | AIR-004 / TR-008 |

---

## Task Overview

Define structured claim-support output and deterministic grounding guardrails that prevent unsupported facility facts from reaching reviewers. Estimated effort: 8 hours.

---

## Dependent Tasks

- US_027: Closed five-part output must be available.
- `task_002_validate-generated-claim-grounding-backend.md`: Supplies reviewed support inputs and consumes guarded output.

---

## Impacted Components

- `prompts/poc/grounded_claims.md` (CREATE)
- `backend/src/cms_planner/adapters/ai/guardrails.py` (CREATE)
- `backend/src/cms_planner/adapters/ai/contracts.py` (CREATE)

---

## Implementation Plan

1. Extend the provider-neutral contract with claim type, support references, and typed missing-information output.
2. Prompt the adapter to distinguish generic guidance from facility-specific case assertions.
3. Deterministically verify references and replace unsupported facility claims with markers.

---

## Current Project State

- Greenfield repository; grounding prompt and AI guardrails do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `prompts/poc/grounded_claims.md` | Define provider-neutral claim and support-reference guidance. |
| CREATE | `backend/src/cms_planner/adapters/ai/guardrails.py` | Validate references and replace unsupported facility claims. |
| CREATE | `backend/src/cms_planner/adapters/ai/contracts.py` | Define structured claim and support-reference contracts. |

---

## External References

- [JSON Schema 2020-12 applicator vocabulary](https://json-schema.org/draft/2020-12/json-schema-core#name-applicator-vocabulary)
- [Pydantic 2 JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/)

---

## Build Commands

- Use the AI and backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical schema validation and backend type checks.
- [ ] Verify contract tests cover supported, missing, invalid, cross-deficiency, and generic-guidance fixtures across adapters.

---

## Implementation Checklist

- [ ] Define structured claims and support-reference contracts. (AC-001, AC-002)
- [ ] Create the provider-neutral grounding prompt. (AC-001, AC-002)
- [ ] Enforce deterministic support validation and marker replacement. (AC-001, AC-002)
- [ ] Verify generic guidance classification across adapters. (AC-001, AC-002)
