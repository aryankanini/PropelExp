# Task - TASK_001 Prefix and Isolate Export Content

## Requirement Reference

- **User Story:** US_035
- **Story Location:** .propel/context/tasks/EP-005/us_035/us_035.md
- **Acceptance Criteria:**
  - **AC-001: Required export prefix**
    - **Given**: Current approved content is copied or downloaded
    - **When**: The export is produced
    - **Then**: It begins with `DRAFT - Approved for compliance handling; not submitted to CMS.`
  - **AC-002: No external submission**
    - **Given**: An export completes
    - **When**: Network interactions are inspected
    - **Then**: No POC content is submitted to CMS or a survey agency
- **Edge Cases:**
  - Empty or whitespace-only approved content cannot produce an export containing only the label.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / FastAPI-compatible | FR-019 requires deterministic labeling and local-only export delivery. |

---

## Task Overview

Implement the EP-005 / US_035 backend export formatter that prefixes every copy/download result exactly, rejects empty approved content, and performs no CMS or survey-agency submission. Estimated effort: 6 hours.

## Dependent Tasks

- US_034 - Same-Epic - Requires approved current export content.
- US_034 TASK_001 Authorize Current Revision Export - supplies authorized content to format.

## Impacted Components

- New deterministic labeled-export formatter and local-only delivery policy.

## Implementation Plan

1. Define the immutable required prefix and non-empty content rule.
2. Format copy and download payloads with the prefix as the first content.
3. Keep delivery inside the response path with no external submission adapter.
4. Reject empty or whitespace-only approved content before formatting.

## Current Project State

```text
backend/src/cms_planner/
├── domain/                         # Planned; backend implementation directory is not yet present
├── application/
└── modules/export/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/domain/export_label.py | Define the exact required prefix and non-empty content invariant. |
| CREATE | backend/src/cms_planner/application/format_labeled_export.py | Produce local copy/download payloads without external submission. |
| CREATE | backend/src/cms_planner/modules/export/labeled_content.py | Define labeled export result contracts. |

## External References

- [Python 3.14 documentation](https://docs.python.org/3.14/)
- [FastAPI 0.141.1 custom responses](https://fastapi.tiangolo.com/advanced/custom-response/)
- [Pydantic 2 documentation](https://docs.pydantic.dev/2.12/)

## Build Commands

- [Backend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [x] Unit tests pass for exact prefix, copy/download formatting, and empty-content rejection.
- [x] Integration tests pass with network inspection confirming local-only response delivery.

## Implementation Checklist

- [x] Prefix every copied or downloaded approved export with `DRAFT - Approved for compliance handling; not submitted to CMS.` (AC-001)
- [x] Keep export delivery local and submit no POC content to CMS or a survey agency. (AC-002)
- [x] Reject empty or whitespace-only content before a label-only export can be produced. (AC-001)
