# Task - TASK_001

## Requirement Reference
- **User Story:** US_004
- **Story Location:** .propel/context/tasks/EP-TECH/us_004/us_004.md
- **Parent Epic:** EP-TECH
- **Acceptance Criteria:**
  - AC-001: Vitest and React Testing Library suites execute independently.
  - AC-002: Domain and application branch coverage below 80% fails and identifies the deficient package.
- **Edge Cases:**
  - A suite with no collected tests fails instead of reporting a misleading successful coverage result.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend Testing | Vitest | 4.x | TR-013 establishes frontend unit and integration testing. |
| Frontend Testing | React Testing Library | Compatible with React 19.3 | Component behavior is tested through user-observable interactions. |
| Frontend Testing | TypeScript | 7.0 | Tests share the locked frontend type system. |

---

## Task Overview
Establish the independent frontend test and coverage foundation for US_004 under EP-TECH. Estimated effort: 6 hours.

## Dependent Tasks
- US_001 frontend scaffolding must provide the independent frontend test command.

## Impacted Components
- New Vitest configuration, browser-like test setup, collection guard, and representative tests.

## Implementation Plan
- Configure Vitest and React Testing Library for the frontend source boundary.
- Enforce 80% branch coverage for frontend domain and application packages.
- Fail explicitly when the suite collects no tests and report deficient packages.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_004 depends on the planned independent frontend test command from US_001.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/vitest.config.ts | Configure independent tests and 80% branch thresholds. |
| CREATE | frontend/tests/setup.ts | Install React Testing Library test behavior. |
| CREATE | frontend/tests/unit/test-collection.test.ts | Provide a representative collected unit test. |
| CREATE | frontend/tests/integration/app-render.test.tsx | Provide a representative component integration test. |
| CREATE | frontend/scripts/verify-test-collection.ts | Fail when Vitest collects no tests. |

## External References
- [Vitest 4 guide](https://vitest.dev/guide/)
- [React Testing Library documentation](https://testing-library.com/docs/react-testing-library/intro/)

## Build Commands
- [Frontend test build commands](.propel/build/)

## Implementation Validation Strategy
- [ ] Unit-test structure executes with Vitest and enforces the frontend branch threshold.
- [ ] Integration-test structure renders React behavior and the collection guard rejects an empty suite.

## Implementation Checklist
- [ ] Configure independent Vitest and React Testing Library execution for AC-001.
- [ ] Enforce 80% branch coverage with deficient-package reporting for AC-002.
- [ ] Fail when no frontend tests are collected for AC-001 and AC-002.
