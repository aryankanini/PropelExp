# Task - TASK_001

## Requirement Reference
- **User Story:** US_002
- **Story Location:** .propel/context/tasks/EP-TECH/us_002/us_002.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: A versioned OpenAPI 3.1.0 document describes every REST, multipart, SSE, problem, and security operation.
  - AC-002: Contract compatibility checks identify changed operations or schemas when generated frontend types are stale.
- **Edge Cases:**
  - An SSE or multipart operation omitted from the contract causes the completeness check to fail.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | FastAPI | 0.141.1 | TR-004 makes FastAPI-generated OpenAPI the contract source. |
| Backend | OpenAPI | 3.1.0 | TR-004 requires a versioned machine-readable contract. |
| Backend | Pydantic | 2.x | Typed schemas supply contract components. |

---

## Task Overview
Publish and verify the versioned OpenAPI contract for US_002 under EP-TECH. Estimated effort: 8 hours.

## Dependent Tasks
- US_001 backend scaffolding must provide the FastAPI composition root.

## Impacted Components
- New backend contract metadata, schema components, publication route, and completeness tests.

## Implementation Plan
- Configure OpenAPI 3.1.0 metadata with an explicit API version.
- Model REST, multipart, SSE, problem, and security contract components.
- Add completeness checks that compare registered operations with the published document.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_002 depends on the planned separated applications from US_001.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/api/contract.py | Configure versioned OpenAPI 3.1.0 publication metadata. |
| CREATE | backend/src/api/schemas/problem.py | Define reusable problem response schemas. |
| CREATE | backend/src/api/schemas/security.py | Define reusable security contract schemas. |
| CREATE | backend/src/api/schemas/events.py | Define SSE event contract schemas. |
| CREATE | backend/tests/contract/test_openapi_publication.py | Verify version and required operation coverage. |
| CREATE | backend/tests/contract/test_openapi_completeness.py | Fail when REST, multipart, SSE, problem, or security details are omitted. |

## External References
- [OpenAPI 3.1.0 specification](https://spec.openapis.org/oas/v3.1.0)
- [FastAPI OpenAPI documentation](https://fastapi.tiangolo.com/how-to/extending-openapi/)
- [Pydantic 2 JSON Schema](https://docs.pydantic.dev/2.12/concepts/json_schema/)

## Build Commands
- [Backend contract build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit-test structure verifies reusable problem, security, event, and multipart schemas.
- [ ] Integration-test structure requests the published document and checks every registered operation for OpenAPI completeness.

## Implementation Checklist
- [ ] Publish an explicitly versioned OpenAPI 3.1.0 document for AC-001.
- [ ] Describe REST and multipart operations for AC-001.
- [ ] Describe SSE, problem, and security operations for AC-001.
- [ ] Fail completeness checks when an SSE or multipart operation is omitted for AC-001.
- [ ] Keep operation and schema identifiers deterministic for the generated-type compatibility check in AC-002.
