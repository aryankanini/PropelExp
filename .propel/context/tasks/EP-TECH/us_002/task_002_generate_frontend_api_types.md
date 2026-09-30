# Task - TASK_002

## Requirement Reference
- **User Story:** US_002
- **Story Location:** .propel/context/tasks/EP-TECH/us_002/us_002.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: A versioned OpenAPI 3.1.0 document describes every REST, multipart, SSE, problem, and security operation.
  - AC-002: Frontend API types are generated from the backend contract and expose schema changes to compatibility validation.
- **Edge Cases:**
  - An SSE or multipart operation omitted from the contract causes the completeness check to fail.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | TypeScript | 7.0 | Generated API types provide the typed frontend contract boundary. |
| Frontend | Node.js | 24 LTS | The frontend generation tool runs in the locked Node.js runtime. |
| Frontend | OpenAPI | 3.1.0 | The published backend document is the sole generation input. |

---

## Task Overview
Generate deterministic frontend API types from the US_002 OpenAPI contract under EP-TECH. Estimated effort: 6 hours.

## Dependent Tasks
- TASK_001 in US_002 publishes the versioned OpenAPI document.
- US_001 frontend scaffolding supplies the frontend manifest and source boundary.

## Impacted Components
- New frontend contract-generation configuration, generated type module, and type-generation tests.

## Implementation Plan
- Add a pinned OpenAPI type-generation dependency and deterministic script.
- Generate types only from the versioned backend contract artifact.
- Verify generated coverage for REST, multipart, SSE, problem, and security schemas.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- This task depends on the planned US_001 frontend boundary and US_002 contract publication.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/openapi-types.config.ts | Pin the versioned contract input and generated output. |
| CREATE | frontend/src/api/generated/schema.ts | Hold deterministic generated API types. |
| CREATE | frontend/src/api/generated/index.ts | Expose generated types through the frontend API boundary. |
| CREATE | frontend/tests/contract/api-types.test.ts | Verify generated operation and schema coverage. |

## External References
- [OpenAPI 3.1.0 specification](https://spec.openapis.org/oas/v3.1.0)
- [TypeScript 7 documentation](https://www.typescriptlang.org/docs/)
- [Node.js 24 documentation](https://nodejs.org/docs/latest-v24.x/api/)

## Build Commands
- [Frontend contract build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit-test structure checks generated REST, multipart, SSE, problem, and security type exports.
- [ ] Integration-test structure regenerates from the published contract and verifies deterministic output.

## Implementation Checklist
- [ ] Accept only the versioned OpenAPI 3.1.0 contract with all required operation categories as generation input for AC-001.
- [ ] Configure deterministic OpenAPI 3.1.0 type generation for AC-002.
- [ ] Generate and expose frontend API types from the versioned contract for AC-002.
- [ ] Verify required operation and schema categories before accepting generated output for AC-002.
