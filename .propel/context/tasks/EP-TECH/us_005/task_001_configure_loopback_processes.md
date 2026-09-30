# Task - TASK_001

## Requirement Reference
- **User Story:** US_005
- **Story Location:** .propel/context/tasks/EP-TECH/us_005/us_005.md
- **Acceptance Criteria:**
  - AC-001: Frontend and backend bind to distinct configurable loopback ports with independent health checks.
  - AC-002: The backend rejects origins other than the configured local frontend origin without protected content.
- **Edge Cases:**
  - A non-loopback bind address fails startup validation.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| DevOps | Node.js and Python | Node.js 24 LTS; Python 3.14.7 | TR-014 requires separate native localhost processes. |

---

## Task Overview
Define separate native startup commands constrained to configurable loopback addresses. Estimated effort: 8 hours.

## Dependent Tasks
- US_003 TASK_003 - Requires validated bind and port settings.

## Impacted Components
- New native development launcher and environment examples.

## Implementation Plan
- Add independent frontend and backend launch commands.
- Validate distinct loopback addresses and expose separate health probes.

## Current Project State
- Application scaffolds are planned without coordinated native startup commands.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | scripts/start_frontend.ps1 | Start Vite on the configured loopback endpoint. |
| CREATE | scripts/start_backend.ps1 | Start FastAPI on the configured loopback endpoint. |

## External References
- https://nodejs.org/docs/latest-v24.x/api/
- https://docs.python.org/3.14/

## Build Commands
- `./scripts/start_backend.ps1`
- `./scripts/start_frontend.ps1`

## Implementation Validation Strategy
- [ ] Both processes bind to distinct loopback ports.
- [ ] Each health check succeeds independently.

## Implementation Checklist
- [ ] Add separate configurable native launch commands for AC-001.
- [ ] Restrict both process bind addresses to loopback for AC-001.
- [ ] Verify distinct ports and independent health checks for AC-001.
- [ ] Expose the configured frontend loopback origin for exact backend origin validation in AC-002.
