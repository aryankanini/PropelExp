# Task - TASK_002

## Requirement Reference
- **User Story:** US_001
- **Story Location:** .propel/context/tasks/EP-TECH/us_001/us_001.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: Separate frontend and backend manifests, test commands, environment examples, and build outputs are detected without cross-application source imports.
  - AC-002: Domain and application packages contain no web-framework or provider-SDK imports.
- **Edge Cases:**
  - A cross-application source import fails the architecture check with the importing file identified.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | TR-003 establishes the backend runtime. |
| Backend | FastAPI | 0.141.1 | TR-003 defines the independent API boundary. |
| Backend | Pydantic | 2.x | TR-003 requires typed backend models. |
| Backend | Uvicorn | Compatible with FastAPI 0.141.1 | TR-003 provides the ASGI runtime. |

---

## Task Overview
Create the standalone backend application boundary and inward-facing package structure for US_001 under EP-TECH. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 in US_001 scaffolds the independent frontend boundary.

## Impacted Components
- New `backend/` application boundary with domain, application, and API composition packages.

## Implementation Plan
- Define an independent Python project manifest, environment example, build output, and test command.
- Add the FastAPI composition root without coupling domain or application packages to the framework.
- Establish dependency direction from API adapters toward application and domain packages.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_001 has no upstream story dependency; this task depends only on the planned frontend boundary task for complete AC-001 coverage.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/pyproject.toml | Define the independent backend package, build, and test metadata. |
| CREATE | backend/.env.example | Document non-secret backend environment keys. |
| CREATE | backend/src/domain/__init__.py | Establish the framework-independent domain package. |
| CREATE | backend/src/application/__init__.py | Establish the framework-independent application package. |
| CREATE | backend/src/api/__init__.py | Establish the inbound API adapter package. |
| CREATE | backend/src/api/main.py | Create the FastAPI composition root. |
| CREATE | backend/tests/__init__.py | Establish the backend test package. |

## External References
- [Python 3.14 documentation](https://docs.python.org/3.14/)
- [FastAPI 0.141.1 documentation](https://fastapi.tiangolo.com/)
- [Pydantic 2 documentation](https://docs.pydantic.dev/2.12/)

## Build Commands
- [Backend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit-test structure verifies domain and application code without web-framework or provider-SDK imports.
- [x] Integration-test structure verifies the backend manifest, environment example, test command, build output, and composition root independently.

## Implementation Checklist
- [x] Create the independent backend manifest and environment example for AC-001.
- [x] Create the backend build and test entry points for AC-001.
- [x] Establish domain and application packages with inward dependencies for AC-002.
- [x] Add the API composition root without cross-application source imports for AC-001 and AC-002.
