# Task - TASK_003 Enforce AI Approval Guardrail

## Requirement Reference

- **User Story:** US_032
- **Story Location:** .propel/context/tasks/EP-005/us_032/us_032.md
- **Acceptance Criteria:**
  - **AC-001: Approve complete revision**
    - **Given**: The leader sees evidence, provenance, completeness, five sections, and the current revision
    - **When**: The leader approves
    - **Then**: Approval is bound to that revision and copy and download become available
  - **AC-002: Stale or incomplete package**
    - **Given**: The package is incomplete or its revision changed
    - **When**: Approval is requested
    - **Then**: Approval is denied without changing state and exact blockers are shown
- **Edge Cases:**
  - Two leaders approving the same unchanged revision produce one current approval state.

---

## AI References

| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-005 |
| **AI Pattern** | Provider-neutral guarded output |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | backend/src/cms_planner/adapters/ai/approval_guardrails.py |
| **Model Provider** | Provider-neutral |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | Provider-neutral OCR/LLM adapters / Adapter contract | Provider-neutral / v1 | AIR-005 requires deterministic human-approval gates around all AI output. |

---

## Task Overview

Implement the EP-005 / US_032 provider-neutral AI guardrail that prevents generated output from representing itself as approved or bypassing current-revision approval checks. Estimated effort: 4 hours.

## Dependent Tasks

- TASK_001 Implement Current Revision Approval - defines the authoritative approval decision consumed by the guardrail.

## Impacted Components

- New provider-neutral approval guardrail at the AI adapter boundary.
- New JSON Schema 2020-12 contract for guarded AI approval-state output.

## Implementation Plan

1. Define a closed schema that excludes provider-asserted approval authority.
2. Reject generated approval claims and normalize output to unapproved candidate state.
3. Require the backend approval decision before output can be exposed as approved.

## Current Project State

```text
backend/src/cms_planner/
├── adapters/ai/                    # Planned; backend implementation directory is not yet present
└── modules/approval/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/adapters/ai/approval_guardrails.py | Enforce provider-neutral human approval boundaries. |
| CREATE | backend/src/cms_planner/adapters/ai/schemas/approval_output.schema.json | Validate guarded output with JSON Schema 2020-12. |

## External References

- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)
- [Python 3.14 documentation](https://docs.python.org/3.14/)

## Build Commands

- [AI adapter build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [x] Unit tests pass for generated approval claims, incomplete output, and guarded current-revision output.
- [x] Integration tests pass between the adapter guardrail and authoritative approval service.

## Implementation Checklist

- [x] Prevent provider output from asserting approval without the authoritative current-revision decision. (AC-001)
- [x] Reject stale or incomplete generated approval state without changing authoritative state. (AC-002)
