# Task - TASK_003 Enforce AI Export Guardrail

## Requirement Reference

- **User Story:** US_034
- **Story Location:** .propel/context/tasks/EP-005/us_034/us_034.md
- **Acceptance Criteria:**
  - **AC-001: Current approval**
    - **Given**: Approval matches the current POC revision
    - **When**: Copy or download is requested
    - **Then**: The approved current content is returned in the requested format
  - **AC-002: Missing or stale approval**
    - **Given**: Approval is absent, revoked, or belongs to another revision
    - **When**: Export is requested
    - **Then**: Export is blocked with an approval-required reason
- **Edge Cases:**
  - Export authorization is rechecked server-side even when the UI action appears enabled.

---

## AI References

| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-005 |
| **AI Pattern** | Provider-neutral guarded output |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | backend/src/cms_planner/adapters/ai/export_guardrails.py |
| **Model Provider** | Provider-neutral |

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | Provider-neutral OCR/LLM adapters / Adapter contract | Provider-neutral / v1 | AIR-005 forbids AI output from bypassing approval and export gates. |

---

## Task Overview

Implement the EP-005 / US_034 provider-neutral AI export guardrail so adapter output cannot initiate export or represent absent, revoked, or stale approval as current. Estimated effort: 4 hours.

## Dependent Tasks

- US_032 - Same-Epic - Requires current-revision approval.
- TASK_001 Authorize Current Revision Export - defines the authoritative export decision.

## Impacted Components

- New provider-neutral export guardrail and JSON Schema 2020-12 output contract.

## Implementation Plan

1. Define a closed guarded export schema without provider-controlled authorization.
2. Reject export-ready claims that lack a current backend approval decision.
3. Pass only current approved content to the deterministic export service.

## Current Project State

```text
backend/src/cms_planner/
├── adapters/ai/                    # Planned; backend implementation directory is not yet present
└── modules/export/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/adapters/ai/export_guardrails.py | Prevent provider output from bypassing export authorization. |
| CREATE | backend/src/cms_planner/adapters/ai/schemas/export_output.schema.json | Validate guarded export output with JSON Schema 2020-12. |

## External References

- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)
- [Python 3.14 documentation](https://docs.python.org/3.14/)

## Build Commands

- [AI adapter build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [x] Unit tests pass for current, absent, revoked, stale, and provider-asserted export states.
- [x] Integration tests pass between guarded adapter output and export authorization.

## Implementation Checklist

- [x] Allow adapter output to reach export only when backend approval matches the current revision. (AC-001)
- [x] Block provider-asserted export readiness for absent, revoked, or stale approval. (AC-002)
