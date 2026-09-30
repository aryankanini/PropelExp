# Task - TASK_003

## Requirement Reference
- **User Story:** US_019
- **Story Location:** .propel/context/tasks/EP-002/us_019/us_019.md
- **Acceptance Criteria:**
  - AC-001: Closed valid responses enter as unconfirmed candidates.
  - AC-002: Invalid responses create no candidates and record safe typed failure.
- **Edge Cases:**
  - Out-of-range confidence and artifact-only text are rejected.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Testing | pytest | 9.x | TR-013 requires adapter contract verification. |

---

## Task Overview
Implement contract and integration tests for atomic extraction schema enforcement. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001, TASK_002 - Requires schema and runtime validator.

## Impacted Components
- New extraction schema contract and repository integration tests.

## Implementation Plan
- Parameterize valid, missing, unknown, range, and empty-content responses.
- Assert candidate state and typed failure state after each response.

## Current Project State
- Schema enforcement is planned without exhaustive test fixtures.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/tests/contract/test_extraction_response_contract.py | Verify closed response behavior. |
| CREATE | backend/tests/integration/extraction/test_schema_storage_gate.py | Verify all-or-nothing case writes. |

## External References
- https://docs.pytest.org/

## Build Commands
- `cd backend; python -m pytest tests/contract/test_extraction_response_contract.py tests/integration/extraction/test_schema_storage_gate.py`

## Implementation Validation Strategy
- [x] Contract and integration matrices cover every acceptance and edge condition.

## Implementation Checklist
- [x] Verify valid responses enter state only as unconfirmed for AC-001.
- [x] Verify missing and unknown fields reject every candidate for AC-002.
- [x] Verify safe typed failure state for AC-002.
- [x] Verify range and empty-content rejection for AC-002.
