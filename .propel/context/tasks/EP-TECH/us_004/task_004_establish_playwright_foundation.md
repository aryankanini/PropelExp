# Task - TASK_004

## Requirement Reference
- **User Story:** US_004
- **Story Location:** .propel/context/tasks/EP-TECH/us_004/us_004.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: Playwright suites execute independently.
  - AC-002: Core branch coverage enforcement remains owned by the unit and integration foundations.
- **Edge Cases:**
  - A suite with no collected tests fails instead of reporting a misleading successful coverage result.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| E2E Testing | Playwright | 1.x | TR-013 establishes browser-based end-to-end verification. |
| E2E Testing | Node.js | 24 LTS | Playwright runs in the locked frontend toolchain runtime. |

---

## Task Overview
Establish an independently executable Playwright foundation for US_004 under EP-TECH. Estimated effort: 6 hours.

## Dependent Tasks
- US_001 provides independently startable frontend and backend applications.
- TASK_001 and TASK_002 in US_004 provide lower-layer test foundations.

## Impacted Components
- New Playwright configuration, fixtures, representative browser test, and collection guard.

## Implementation Plan
- Configure Playwright against configurable local frontend and backend processes.
- Add deterministic health and application-shell fixtures.
- Reject execution when no end-to-end tests are collected.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- This task depends on the planned US_001 processes and complements the US_004 coverage-owning test layers.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/playwright.config.ts | Configure independent local end-to-end execution. |
| CREATE | frontend/tests/e2e/fixtures.ts | Provide local process and browser fixtures. |
| CREATE | frontend/tests/e2e/application-shell.spec.ts | Supply a representative browser journey. |
| CREATE | frontend/scripts/verify-e2e-collection.ts | Fail when Playwright collects no tests. |

## External References
- [Playwright Test documentation](https://playwright.dev/docs/test-intro)
- [Playwright configuration](https://playwright.dev/docs/test-configuration)
- [Node.js 24 documentation](https://nodejs.org/docs/latest-v24.x/api/)

## Build Commands
- [End-to-end test build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit-test structure checks configuration parsing and collection-guard behavior.
- [ ] Integration-test structure starts the configured local processes and executes the representative Playwright journey independently.

## Implementation Checklist
- [ ] Configure independent Playwright execution for AC-001.
- [ ] Add local frontend and backend process fixtures for AC-001.
- [ ] Fail when no end-to-end tests are collected for AC-001.
- [ ] Keep core branch coverage enforcement in the unit and integration suites for AC-002.
