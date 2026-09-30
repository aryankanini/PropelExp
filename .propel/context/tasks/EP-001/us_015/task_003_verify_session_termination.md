# Task - TASK_003

## Requirement Reference
- **User Story:** US_015
- **Story Location:** .propel/context/tasks/EP-001/us_015/us_015.md
- **Acceptance Criteria:**
  - AC-001: Confirmed termination cleans memory and files before empty intake.
  - AC-002: Cancel or failed cleanup preserves the visible case.
- **Edge Cases:**
  - Repeated cleanup after failure is idempotent and prevents workspace reuse.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Testing | Playwright | 1.x | TR-013 requires end-to-end verification of session lifecycle workflows. |

---

## Task Overview
Implement end-to-end session termination tests across browser, API, memory, and workspace. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001, TASK_002 - Requires termination API and dialog.

## Impacted Components
- New Playwright session termination scenarios.

## Implementation Plan
- Exercise cancel, successful confirmation, cleanup failure, and retry.
- Verify visible state and workspace residue after each outcome.

## Current Project State
- Termination behavior is planned without end-to-end coverage.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/tests/e2e/end-session.spec.ts | Verify complete termination and recovery behavior. |

## External References
- https://playwright.dev/docs/test-assertions

## Build Commands
- `cd frontend; npm run test:e2e -- end-session.spec.ts`

## Implementation Validation Strategy
- [x] End-to-end scenarios prove cleanup truthfulness and retained state.

## Implementation Checklist
- [x] Verify confirmed cleanup precedes empty intake for AC-001.
- [x] Verify cancel preserves the active case for AC-002.
- [x] Verify failure preserves the case and exposes retry for AC-002.
- [x] Verify retry is idempotent and blocks workspace reuse for AC-002.
