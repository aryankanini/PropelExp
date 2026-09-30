# Task - TASK_002

## Requirement Reference
- **User Story:** US_005
- **Story Location:** .propel/context/tasks/EP-TECH/us_005/us_005.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: The backend starts on a distinct configurable loopback port and exposes an independent health check.
  - AC-002: Requests from any origin other than the exact configured local frontend origin are rejected without protected content.
- **Edge Cases:**
  - A wildcard origin or non-loopback bind address fails startup validation.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend Runtime/Security | FastAPI | 0.141.1 | The API enforces exact browser origins and health behavior. |
| Backend Runtime/Security | Uvicorn | Compatible with FastAPI 0.141.1 | TR-014 defines the native backend bind process. |
| Backend Runtime/Security | Python | 3.14.7 | Runtime and origin validation use the locked backend runtime. |

---

## Task Overview
Enforce loopback-only backend binding and exact frontend-origin access for US_005 under EP-TECH. Estimated effort: 8 hours.

## Dependent Tasks
- US_003 must provide validated bind, port, and origin configuration.
- TASK_001 in US_005 establishes the distinct frontend loopback origin.

## Impacted Components
- New backend bind validator, exact-origin middleware, health route, and security integration tests.

## Implementation Plan
- Reject wildcard and non-loopback backend bind addresses before startup.
- Require one exact configured loopback frontend origin without wildcard matching.
- Reject disallowed origins before protected response content is produced.
- Expose an independent backend health route on its distinct configured port.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_005 depends on planned US_003 configuration and the frontend origin from TASK_001 in US_005.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/runtime/loopback.py | Validate loopback bind addresses and distinct ports. |
| CREATE | backend/src/api/middleware/exact_origin.py | Enforce the single configured frontend origin. |
| CREATE | backend/src/api/routes/health.py | Expose the independent backend health response. |
| CREATE | backend/tests/unit/runtime/test_loopback.py | Cover wildcard and non-loopback rejection. |
| CREATE | backend/tests/integration/test_exact_origin.py | Verify disallowed origins receive no protected content. |
| CREATE | backend/tests/integration/test_backend_health.py | Verify the configured port and health route. |

## External References
- [FastAPI CORS documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [Uvicorn settings](https://www.uvicorn.org/settings/)
- [Python 3.14 ipaddress documentation](https://docs.python.org/3.14/library/ipaddress.html)

## Build Commands
- [Backend runtime build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit-test structure validates exact loopback hosts, ports, and origins without wildcard acceptance.
- [ ] Integration-test structure verifies independent health and rejects every non-configured origin before protected content.

## Implementation Checklist
- [ ] Bind the backend to a configurable distinct loopback port for AC-001.
- [ ] Expose an independent backend health check for AC-001.
- [ ] Enforce the exact configured local frontend origin for AC-002.
- [ ] Reject wildcard origins, non-loopback binds, and protected-content leakage for AC-001 and AC-002.
