# Task - TASK_003

## Requirement Reference
- **User Story:** US_004
- **Story Location:** .propel/context/tasks/EP-TECH/us_004/us_004.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: Contract tests and adapter tests execute independently.
  - AC-002: Core branch coverage below 80% fails and identifies the deficient package.
- **Edge Cases:**
  - A suite with no collected tests fails instead of reporting a misleading successful coverage result.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Contract/Adapter Testing | pytest | 9.x | TR-013 establishes isolated contract and adapter validation. |
| Contract/Adapter Testing | HTTPX | Compatible with FastAPI 0.141.1 | Adapter integration can exercise HTTP boundaries without external traffic. |
| Contract/Adapter Testing | OpenAPI | 3.1.0 | Contract fixtures validate the approved API format. |

---

## Task Overview
Establish independently executable contract and adapter test foundations for US_004 under EP-TECH. Estimated effort: 6 hours.

## Dependent Tasks
- US_001 provides independent application boundaries.
- US_002 provides the planned versioned API contract.

## Impacted Components
- New isolated contract and adapter test configuration, fixtures, collection guard, and sample tests.

## Implementation Plan
- Separate contract and adapter markers from backend unit and integration suites.
- Add OpenAPI and HTTP adapter fixtures that require no live provider.
- Enforce collection and core branch-coverage failures with package diagnostics.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- This task depends on the planned US_001 boundaries and US_002 contract artifacts.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/tests/contract/conftest.py | Provide versioned OpenAPI contract fixtures. |
| CREATE | backend/tests/contract/test_contract_foundation.py | Prove independent contract-suite execution. |
| CREATE | backend/tests/adapters/conftest.py | Provide deterministic adapter fakes and HTTPX fixtures. |
| CREATE | backend/tests/adapters/test_adapter_foundation.py | Prove independent adapter-suite execution. |
| CREATE | backend/tests/support/verify_suite_collection.py | Reject empty contract or adapter selections. |

## External References
- [pytest 9 markers](https://docs.pytest.org/en/9.0.x/example/markers.html)
- [HTTPX transports](https://www.python-httpx.org/advanced/transports/)
- [OpenAPI 3.1.0 specification](https://spec.openapis.org/oas/v3.1.0)

## Build Commands
- [Contract and adapter test build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit-test structure validates contract normalization and adapter fakes under coverage rules.
- [ ] Integration-test structure executes contract and adapter selections independently and rejects empty selections.

## Implementation Checklist
- [ ] Establish independent contract-test execution for AC-001.
- [ ] Establish independent adapter-test execution for AC-001.
- [ ] Enforce 80% core branch coverage with deficient-package reporting for AC-002.
- [ ] Fail when either selected suite collects no tests for AC-001 and AC-002.
