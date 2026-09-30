# Task - TASK_003

## Requirement Reference

- **User Story**: US_029 - Resolve missing POC information
- **Story Location**: .propel/context/tasks/EP-004/us_029/us_029.md
- **Acceptance Criteria**:
	- **AC-001: Display guarded draft**
		- **Given**: A grounded draft contains typed missing-information markers
		- **When**: The draft is displayed
		- **Then**: Each marker names the needed fact and keeps approval readiness blocked
	- **AC-002: Supply missing fact**
		- **Given**: A reviewer enters a supported missing fact
		- **When**: The draft is saved
		- **Then**: A user-edited revision replaces the marker and preserves its revision history
- **Edge Cases**:
	- Removing a required value restores the missing marker and incomplete state.

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

Define typed missing-information marker semantics and deterministic revalidation so required gaps remain explicit after edits or removals. Estimated effort: 6 hours.

---

## Dependent Tasks

- US_028: Grounding guardrails must produce typed markers.
- `task_002_resolve-missing-poc-information-backend.md`: Supplies edited drafts for revalidation.

---

## Impacted Components

- `prompts/poc/missing_information.md` (CREATE)
- `backend/src/cms_planner/adapters/ai/guardrails.py` (CREATE)
- `backend/src/cms_planner/adapters/ai/contracts.py` (CREATE)

---

## Implementation Plan

1. Define marker types that name the required fact and affected POC section.
2. Keep marker production deterministic and independent of provider prose.
3. Revalidate edited drafts and restore markers whenever required supported content is absent.

---

## Current Project State

- Greenfield repository; missing-information contracts and revalidation guardrails do not exist.

---

## Expected Changes

| Action | File Path | Description |
|---|---|---|
| CREATE | `prompts/poc/missing_information.md` | Define provider-neutral missing-information guidance. |
| CREATE | `backend/src/cms_planner/adapters/ai/guardrails.py` | Revalidate edited drafts and restore required markers. |
| CREATE | `backend/src/cms_planner/adapters/ai/contracts.py` | Define typed marker and required-fact contracts. |

---

## External References

- [JSON Schema 2020-12 validation](https://json-schema.org/draft/2020-12/json-schema-validation)
- [Pydantic 2 discriminated unions](https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions)

---

## Build Commands

- Use the AI and backend commands documented under [.propel/build/](../../../../build/).

---

## Implementation Validation Strategy

- [ ] Run the canonical schema validation and backend type checks.
- [ ] Verify contract tests cover marker naming, supported replacement, absent required facts, and marker restoration across adapters.

---

## Implementation Checklist

- [ ] Define typed marker contracts and required-fact identifiers. (AC-001, AC-002)
- [ ] Create provider-neutral missing-information prompt guidance. (AC-001, AC-002)
- [ ] Enforce deterministic marker restoration after revalidation. (AC-001, AC-002)
