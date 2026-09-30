# Task - TASK_003

## Requirement Reference
- **User Story:** US_001
- **Story Location:** .propel/context/tasks/EP-TECH/us_001/us_001.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: Separate application setup artifacts are detected and cross-application source imports are prohibited.
  - AC-002: Domain and application packages contain no web-framework or provider-SDK imports.
- **Edge Cases:**
  - A cross-application source import fails the architecture check with the importing file identified.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Architecture Validation | Python | 3.14.7 | A repository-level validator can inspect both planned application boundaries without joining their runtimes. |

---

## Task Overview
Add structural architecture checks for US_001 under EP-TECH that enforce independent applications and inward dependencies. Estimated effort: 6 hours.

## Dependent Tasks
- TASK_001 in US_001 creates the planned frontend boundary.
- TASK_002 in US_001 creates the planned backend boundary.

## Impacted Components
- New repository-level architecture validation suite for frontend, backend, domain, and application boundaries.

## Implementation Plan
- Assert that each application owns its manifest, test command, environment example, and build output.
- Scan source imports in both directions and report the importing file for boundary violations.
- Scan backend domain and application imports for FastAPI, Uvicorn, and provider SDK dependencies.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- Validation depends on the planned US_001 frontend and backend scaffolding tasks.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | architecture-tests/pyproject.toml | Define the isolated architecture validation project. |
| CREATE | architecture-tests/tests/test_application_boundaries.py | Verify independent setup artifacts and prohibit cross-application imports. |
| CREATE | architecture-tests/tests/test_inward_dependencies.py | Prohibit framework and provider imports in domain and application packages. |
| CREATE | architecture-tests/src/import_scanner.py | Parse imports and retain the violating file path in diagnostics. |

## External References
- [Python 3.14 ast documentation](https://docs.python.org/3.14/library/ast.html)
- [pytest 9 documentation](https://docs.pytest.org/en/9.0.x/)

## Build Commands
- [Architecture validation build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit-test structure covers import classification and violation diagnostics.
- [ ] Integration-test structure scans representative frontend and backend trees and fails on missing setup artifacts or forbidden imports.

## Implementation Checklist
- [ ] Detect each independent application artifact required by AC-001.
- [ ] Reject cross-application source imports and identify the importing file for AC-001.
- [ ] Reject framework imports in domain and application packages for AC-002.
- [ ] Reject provider-SDK imports in domain and application packages for AC-002.
