# Task - TASK_004

## Requirement Reference
- **User Story:** US_004
- **Story Location:** .propel/context/tasks/EP-TECH/us_004/us_004.md
- **Acceptance Criteria:**
  - AC-001: Playwright executes independently with the layered test stack.
  - AC-002: Core branch coverage below 80% fails and names the deficient package.
- **Edge Cases:**
  - A suite with no collected tests fails instead of passing coverage.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Testing | Playwright and coverage tooling | Playwright 1.x; coverage tooling Compatible | TR-013 and NFR-009 require end-to-end execution and 80% core branch coverage. |

---

## Task Overview
Configure independent end-to-end execution and enforce backend core branch coverage. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001, TASK_002, TASK_003 - Requires frontend, backend, and contract test foundations.

## Impacted Components
- New Playwright configuration and coverage enforcement scripts.

## Implementation Plan
- Configure a minimal localhost E2E project and smoke test.
- Aggregate domain/application branch coverage and report deficient packages.

## Current Project State
- Unit and contract suites are planned without E2E or consolidated coverage gates.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/playwright.config.ts | Configure independent localhost E2E execution. |
| CREATE | frontend/tests/e2e/app.spec.ts | Prove browser-suite collection. |
| CREATE | scripts/check_core_coverage.py | Enforce 80% branch coverage by core package. |

## External References
- https://playwright.dev/docs/test-configuration
- https://coverage.readthedocs.io/

## Build Commands
- `cd frontend; npm run test:e2e`
- `cd backend; python -m pytest --cov-branch; cd ..; python scripts/check_core_coverage.py`

## Implementation Validation Strategy
- [ ] Playwright runs independently and collects a test.
- [ ] Coverage below 80% fails with the deficient package.

## Implementation Checklist
- [ ] Configure independent Playwright execution for AC-001.
- [ ] Add a collected end-to-end smoke test for AC-001.
- [ ] Enforce 80% domain and application branch coverage for AC-002.
- [ ] Report each deficient core package and fail empty suites for AC-002.
