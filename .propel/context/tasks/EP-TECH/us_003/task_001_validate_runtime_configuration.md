# Task - TASK_001

## Requirement Reference
- **User Story:** US_003
- **Story Location:** .propel/context/tasks/EP-TECH/us_003/us_003.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: Typed startup configuration exposes origins, bind addresses, ports, workspace, limits, credentials, provider settings, timeouts, and retention values.
  - AC-002: Missing or contradictory configuration fails before traffic and reports only the safe setting name and reason.
- **Edge Cases:**
  - A provider marked approved without its required endpoint or key is rejected as contradictory configuration.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend Configuration | Python | 3.14.7 | TR-010 requires startup configuration in the backend runtime. |
| Backend Configuration | Pydantic | 2.x | Typed settings and cross-field validation enforce consistency. |
| Backend Configuration | FastAPI | 0.141.1 | Validation must complete before the API accepts traffic. |

---

## Task Overview
Implement typed, fail-fast runtime configuration for US_003 under EP-TECH. Estimated effort: 8 hours.

## Dependent Tasks
- US_001 backend scaffolding must provide the backend composition root.

## Impacted Components
- New backend settings model, safe startup error model, and configuration validation tests.

## Implementation Plan
- Model all required network, workspace, limit, credential, provider, timeout, and retention settings.
- Add cross-field validation for origins, bind addresses, provider approval, endpoints, and keys.
- Validate settings before constructing or serving the FastAPI application.
- Sanitize validation failures to setting names and reasons only.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_003 depends on the planned backend composition root from US_001.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/config/settings.py | Define typed runtime settings and cross-field rules. |
| CREATE | backend/src/config/errors.py | Represent sanitized setting-name and reason failures. |
| CREATE | backend/src/config/loader.py | Load and validate settings before API construction. |
| CREATE | backend/tests/unit/config/test_settings.py | Cover valid, missing, and contradictory settings. |
| CREATE | backend/tests/integration/test_startup_configuration.py | Verify invalid startup never accepts traffic. |

## External References
- [Pydantic 2 settings documentation](https://docs.pydantic.dev/2.12/concepts/pydantic_settings/)
- [FastAPI lifespan documentation](https://fastapi.tiangolo.com/advanced/events/)
- [Python 3.14 documentation](https://docs.python.org/3.14/)

## Build Commands
- [Backend configuration build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit-test structure covers every typed setting, cross-field contradiction, and sanitized error.
- [ ] Integration-test structure proves configuration validation finishes before the API can accept traffic.

## Implementation Checklist
- [ ] Expose every required typed runtime setting for AC-001.
- [ ] Reject missing settings before traffic for AC-002.
- [ ] Reject contradictory settings with safe names and reasons for AC-002.
- [ ] Reject an approved provider lacking its endpoint or key for AC-002.
