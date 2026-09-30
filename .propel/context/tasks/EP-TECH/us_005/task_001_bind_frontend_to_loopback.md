# Task - TASK_001

## Requirement Reference
- **User Story:** US_005
- **Story Location:** .propel/context/tasks/EP-TECH/us_005/us_005.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: The frontend starts on a distinct configurable loopback port and exposes an independent health check.
- **Edge Cases:**
  - A wildcard origin or non-loopback bind address fails startup validation.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend Runtime | Vite | 8.3 | TR-014 defines the native frontend development process. |
| Frontend Runtime | Node.js | 24 LTS | The frontend process runs in the locked native runtime. |
| Frontend Runtime | TypeScript | 7.0 | Runtime configuration remains typed. |

---

## Task Overview
Bind the US_005 frontend runtime to a configurable loopback address and port under EP-TECH. Estimated effort: 6 hours.

## Dependent Tasks
- US_003 must provide validated bind and port configuration.
- US_001 must provide the frontend Vite application boundary.

## Impacted Components
- New frontend runtime configuration, loopback validator, health endpoint behavior, and tests.

## Implementation Plan
- Read the frontend host and port from validated environment settings.
- Accept only loopback host forms and reject wildcard or network-facing values.
- Expose an independent frontend health response on its configured port.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_005 depends on the planned US_003 validated settings and US_001 frontend boundary.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/src/config/runtime.ts | Parse typed frontend host, port, and backend origin settings. |
| CREATE | frontend/src/config/loopback.ts | Validate loopback-only host values. |
| CREATE | frontend/src/runtime/health.ts | Define the independent frontend health response. |
| CREATE | frontend/tests/unit/loopback.test.ts | Cover loopback and wildcard host validation. |
| CREATE | frontend/tests/integration/runtime-bind.test.ts | Verify binding and health behavior on the configured port. |

## External References
- [Vite 8 server options](https://vite.dev/config/server-options)
- [Node.js 24 net documentation](https://nodejs.org/docs/latest-v24.x/api/net.html)

## Build Commands
- [Frontend runtime build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit-test structure accepts loopback hosts and rejects wildcard or non-loopback addresses.
- [ ] Integration-test structure starts the frontend on a configurable distinct port and verifies its health response.

## Implementation Checklist
- [ ] Load a configurable frontend loopback host and port for AC-001.
- [ ] Reject wildcard and non-loopback bind addresses for AC-001.
- [ ] Expose an independent frontend health check for AC-001.
