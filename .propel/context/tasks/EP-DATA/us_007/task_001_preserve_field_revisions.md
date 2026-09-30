# Task - TASK_001

## Requirement Reference
- **User Story:** US_007
- **Story Location:** .propel/context/tasks/EP-DATA/us_007/us_007.md
- **Parent Epic:** EP-DATA
- **Acceptance Criteria:**
  - AC-001: Editing an extracted value appends a current revision while preserving the original value and evidence unchanged.
- **Edge Cases:**
  - An edit based on a stale revision is rejected with the current revision identifier.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend Domain | Python | 3.14.7 | DR-002 places immutable revision rules in the backend domain. |
| Backend Domain | Pydantic | 2.x | Typed immutable value objects preserve revision metadata. |

---

## Task Overview
Implement immutable evidence-linked field revisions for US_007 under EP-DATA. Estimated effort: 8 hours.

## Dependent Tasks
- US_006 must provide the transient case aggregate and repository ownership.

## Impacted Components
- New extracted-field identity, immutable revision history, edit command, stale-revision error, and tests.

## Implementation Plan
- Model field identity, value, evidence, confidence, origin, and revision identifiers.
- Append edits as immutable revisions and advance only the current revision pointer.
- Compare expected and current revision identifiers before accepting an edit.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_007 depends on the planned US_006 transient aggregate; storage remains in-memory with no database.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/domain/case/field_revision.py | Model immutable evidence-linked revisions. |
| CREATE | backend/src/domain/case/extracted_field.py | Own revision history and the current revision pointer. |
| CREATE | backend/src/domain/case/revision_errors.py | Return the current identifier for stale edits. |
| CREATE | backend/src/application/commands/edit_extracted_field.py | Apply optimistic revision checks through the aggregate. |
| CREATE | backend/tests/unit/domain/test_field_revisions.py | Verify immutable append and evidence preservation. |
| CREATE | backend/tests/integration/test_stale_field_edit.py | Verify stale edits report the current revision identifier. |

## External References
- [Python 3.14 data classes](https://docs.python.org/3.14/library/dataclasses.html)
- [Pydantic 2 strict mode](https://docs.pydantic.dev/2.12/concepts/strict_mode/)

## Build Commands
- [Backend domain build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit-test structure proves original values and evidence remain unchanged after revision append.
- [x] Integration-test structure applies concurrent edit commands and verifies stale-revision diagnostics.

## Implementation Checklist
- [x] Model identity, evidence, confidence, origin, and revision data for AC-001.
- [x] Append a new current revision without mutating original value or evidence for AC-001.
- [x] Reject stale edits and return the current revision identifier for AC-001.
