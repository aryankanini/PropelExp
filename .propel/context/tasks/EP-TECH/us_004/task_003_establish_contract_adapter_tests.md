# Task - TASK_003

## Requirement Reference
- **User Story:** US_004
- **Story Location:** .propel/context/tasks/EP-TECH/us_004/us_004.md
- **Acceptance Criteria:**
  - AC-001: Contract and adapter suites execute independently.
  - AC-002: Domain and application branch coverage below 80% fails with the deficient package identified.
- **Edge Cases:**
  - A suite with no collected tests fails.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Testing | pytest | 9.x | TR-013 requires generated-contract and provider-adapter contract suites. |

---

## Task Overview
Create independent contract and provider-adapter test suite entry points. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_002 - Requires the backend pytest foundation.
- US_002 TASK_001 - Requires the OpenAPI contract.

## Impacted Components
- New contract and adapter test conventions with deterministic fakes.

## Implementation Plan
- Define suite markers and shared adapter contract fixtures.
- Ensure each suite collects and runs independently.

## Current Project State
- Backend tests and API contracts are planned without adapter suite conventions.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/tests/contract/conftest.py | Define contract-test fixtures and markers. |
| CREATE | backend/tests/contract/test_provider_adapter_protocol.py | Prove adapter contract execution with a fake. |

## External References
- https://docs.pytest.org/en/stable/how-to/mark.html

## Build Commands
- `cd backend; python -m pytest tests/contract`

## Implementation Validation Strategy
- [ ] Contract and adapter tests can run without other suites.
- [ ] Empty contract collection fails.

## Implementation Checklist
- [ ] Establish an independently runnable contract suite for AC-001.
- [ ] Establish provider-adapter contract fixtures for AC-001.
- [ ] Require at least one collected contract test for AC-001.
- [ ] Keep contract and adapter coverage separate from the domain and application threshold denominator for AC-002.
