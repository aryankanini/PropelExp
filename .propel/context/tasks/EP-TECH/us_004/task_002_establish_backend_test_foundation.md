# Task - TASK_002

## Requirement Reference
- **User Story:** US_004
- **Story Location:** .propel/context/tasks/EP-TECH/us_004/us_004.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: pytest and HTTPX suites execute independently.
  - AC-002: Domain and application branch coverage below 80% fails and identifies the deficient package.
- **Edge Cases:**
  - A suite with no collected tests fails instead of reporting a misleading successful coverage result.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend Testing | pytest | 9.x | TR-013 establishes backend unit and integration testing. |
| Backend Testing | HTTPX | Compatible with FastAPI 0.141.1 | HTTPX exercises the ASGI boundary in integration tests. |
| Backend Testing | Python | 3.14.7 | Tests run in the locked backend runtime. |

---

## Task Overview
Establish the independent backend test and coverage foundation for US_004 under EP-TECH. Estimated effort: 6 hours.

## Dependent Tasks
- US_001 backend scaffolding must provide the independent backend test command.

## Impacted Components
- New pytest configuration, shared fixtures, collection guard, coverage rules, and representative tests.

## Implementation Plan
- Configure pytest, HTTPX, and branch coverage for the backend boundary.
- Enforce 80% branch coverage for domain and application packages with package-specific reporting.
- Treat no collected tests as a failed suite.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_004 depends on the planned independent backend test command from US_001.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/pytest.ini | Configure independent collection and strict test behavior. |
| CREATE | backend/.coveragerc | Enforce 80% branch coverage for core packages. |
| CREATE | backend/tests/conftest.py | Provide shared backend and HTTPX fixtures. |
| CREATE | backend/tests/unit/test_collection.py | Provide a representative collected unit test. |
| CREATE | backend/tests/integration/test_health.py | Provide a representative HTTPX integration test. |
| CREATE | backend/tests/test_collection_guard.py | Fail explicitly when no tests are collected. |

## External References
- [pytest 9 documentation](https://docs.pytest.org/en/9.0.x/)
- [HTTPX documentation](https://www.python-httpx.org/)
- [coverage.py branch coverage](https://coverage.readthedocs.io/en/latest/branch.html)

## Build Commands
- [Backend test build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit-test structure executes with pytest and enforces package-specific branch thresholds.
- [ ] Integration-test structure exercises the ASGI boundary through HTTPX and rejects an empty suite.

## Implementation Checklist
- [ ] Configure independent pytest and HTTPX execution for AC-001.
- [ ] Enforce 80% branch coverage with deficient-package reporting for AC-002.
- [ ] Fail when no backend tests are collected for AC-001 and AC-002.
