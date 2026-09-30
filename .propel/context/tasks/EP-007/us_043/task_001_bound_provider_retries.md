# Task - TASK_001

## Requirement Reference
- **User Story:** us_043
- **Story Location:** .propel/context/tasks/EP-007/us_043/us_043.md
- **Acceptance Criteria:** AC-001, AC-002
- **Edge Cases:** Do not retry non-transient schema errors.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python, FastAPI | Python 3.14.7; FastAPI 0.141.1 | NFR-008 and TR-008 require bounded provider calls. |

---

## Task Overview
**Estimated Effort:** 6 hours

Implement a shared provider execution policy with 120-second attempt timeouts, at most two retries, bounded backoff, and typed exhaustion.

## Dependent Tasks
- TASK_001 from US_042.

## Impacted Components
- Provider executor, transient failure taxonomy, and state mutation boundary.

## Implementation Plan
- Classify transient and terminal failures.
- Execute provider calls with timeout and bounded retry policy.
- Commit state only after a successful typed result.

## Current Project State
```text
backend/src/cms_planner/application/providers/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/application/providers/executor.py | Enforce timeout, retry, and backoff limits. |
| CREATE | backend/src/cms_planner/application/providers/results.py | Define typed exhausted-retry results. |

## External References
- https://docs.python.org/3.14/library/asyncio-task.html#timeouts

## Build Commands
- [Backend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests cover transient, timeout, schema, and exhaustion paths.
- [x] Integration tests verify failed attempts do not mutate reviewed state.

## Implementation Checklist
- [x] Classify only timeout, throttling, and transient transport failures as retryable. (AC-001, Edge Case)
- [x] Limit every attempt to the configured maximum of 120 seconds. (AC-001)
- [x] Permit at most two retries with bounded backoff. (AC-001)
- [x] Return a typed exhausted-retry result after the final failure. (AC-002)
- [x] Preserve reviewed state until a successful result is committed. (AC-002)
