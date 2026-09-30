# Task - TASK_002

## Requirement Reference
- **User Story:** US_004
- **Story Location:** .propel/context/tasks/EP-TECH/us_004/us_004.md
- **Acceptance Criteria:**
  - AC-001: pytest and HTTPX suites execute independently.
  - AC-002: Domain and application branch coverage below 80% fails with the deficient package identified.
- **Edge Cases:**
  - A suite with no collected tests fails.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Testing | pytest and HTTPX | pytest 9.x; HTTPX Compatible | TR-013 defines backend unit and API integration tests. |

---

## Task Overview
Configure backend unit and API integration test foundations. Estimated effort: 8 hours.

## Dependent Tasks
- US_001 TASK_002 - Requires the backend application.

## Impacted Components
- New pytest configuration, fixtures, and health integration test.

## Implementation Plan
- Configure strict test discovery and asynchronous HTTPX fixtures.
- Add representative unit and API checks.

## Current Project State
- The backend scaffold is planned without a complete pytest harness.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/tests/conftest.py | Define shared backend and HTTPX fixtures. |
| CREATE | backend/tests/integration/test_health.py | Prove API integration execution. |
| CREATE | backend/tests/unit/test_package.py | Prove unit-test discovery. |

## External References
- https://docs.pytest.org/
- https://www.python-httpx.org/advanced/transports/

## Build Commands
- `cd backend; python -m pytest`

## Implementation Validation Strategy
- [ ] pytest and HTTPX tests execute independently.
- [ ] Empty or misconfigured collection fails visibly.

## Implementation Checklist
- [ ] Configure strict pytest collection for AC-001.
- [ ] Provide HTTPX API fixtures for AC-001.
- [ ] Add collected unit and integration checks for AC-001.
- [ ] Identify domain and application packages as distinct branch-coverage measurement targets for AC-002.
