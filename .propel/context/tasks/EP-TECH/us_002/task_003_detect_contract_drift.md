# Task - TASK_003

## Requirement Reference
- **User Story:** US_002
- **Story Location:** .propel/context/tasks/EP-TECH/us_002/us_002.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: The backend publishes a complete versioned OpenAPI 3.1.0 document.
  - AC-002: Contract compatibility validation identifies changed operations or schemas when generated frontend types are stale.
- **Edge Cases:**
  - An SSE or multipart operation omitted from the contract causes the completeness check to fail.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Contract Validation | Python | 3.14.7 | A neutral validator compares backend publication with committed generated artifacts. |
| Contract Validation | OpenAPI | 3.1.0 | The versioned document is the compatibility baseline. |
| Contract Validation | pytest | 9.x | TR-013 establishes backend and contract validation tests. |

---

## Task Overview
Detect publication omissions and generated-type drift for US_002 under EP-TECH. Estimated effort: 6 hours.

## Dependent Tasks
- TASK_001 in US_002 publishes the OpenAPI contract.
- TASK_002 in US_002 generates frontend API types.

## Impacted Components
- New contract snapshot, normalization helper, and compatibility test suite.

## Implementation Plan
- Normalize the live OpenAPI document into a stable versioned snapshot.
- Compare operation identifiers and component schemas with generated frontend types.
- Report the exact changed or omitted operation or schema.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- Validation depends on the planned US_002 publication and frontend type-generation tasks, which depend on US_001.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | contracts/openapi/v1/openapi.json | Store the normalized versioned contract baseline. |
| CREATE | contract-tests/pyproject.toml | Define isolated contract validation dependencies. |
| CREATE | contract-tests/src/openapi_normalizer.py | Produce deterministic operation and schema comparisons. |
| CREATE | contract-tests/tests/test_contract_completeness.py | Detect omitted REST, multipart, SSE, problem, or security operations. |
| CREATE | contract-tests/tests/test_generated_type_drift.py | Identify changed operations or schemas in stale frontend types. |

## External References
- [OpenAPI 3.1.0 specification](https://spec.openapis.org/oas/v3.1.0)
- [pytest 9 documentation](https://docs.pytest.org/en/9.0.x/)

## Build Commands
- [Contract validation build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit-test structure verifies deterministic normalization and precise operation/schema diagnostics.
- [ ] Integration-test structure compares a live backend document, the versioned snapshot, and generated frontend types.

## Implementation Checklist
- [ ] Normalize and snapshot the complete OpenAPI 3.1.0 document for AC-001.
- [ ] Detect omitted SSE and multipart operations for AC-001.
- [ ] Detect stale generated frontend types for AC-002.
- [ ] Identify each changed operation or schema in failure output for AC-002.
