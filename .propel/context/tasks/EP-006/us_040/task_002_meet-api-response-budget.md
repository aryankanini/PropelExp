# Task - TASK_002 Meet API Response Budget

## Requirement Reference

- **User Story:** US_040
- **Story Location:** .propel/context/tasks/EP-006/us_040/us_040.md
- **Acceptance Criteria:**
  - **AC-003: API responsiveness**
    - **Given**: One authenticated user sends at least 1,000 non-processing requests
    - **When**: Steady-state performance is measured
    - **Then**: p95 is below 300 ms with fewer than 0.5% application errors
- **Edge Cases:**
  - The longest localized status label wraps without resizing fixed-format controls.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python / FastAPI / Pydantic / Uvicorn | 3.14.7 / 0.141.1 / 2.x / FastAPI-compatible | NFR-001 defines the single-user non-processing latency and error budget. |

---

## Task Overview

Implement the EP-006 / US_040 backend request instrumentation and bounded non-processing response path needed to demonstrate p95 below 300ms and fewer than 0.5% application errors over at least 1,000 authenticated requests. Estimated effort: 8 hours.

## Dependent Tasks

- US_036 - Same-Epic - Requires shared shell tokens and layout regions.
- TASK_001 Render Stable Semantic Feedback - provides the frontend feedback contract consuming response states.

## Impacted Components

- New non-processing request metrics and lightweight response-budget middleware.

## Implementation Plan

1. Define latency and application-error measurements for authenticated non-processing routes.
2. Add low-overhead timing and outcome instrumentation.
3. Exclude processing operations from the measured route classification.
4. Emit aggregate measurements suitable for the required steady-state validation.

## Current Project State

```text
backend/src/cms_planner/
├── api/                            # Planned; backend implementation directory is not yet present
└── infrastructure/observability/
```

## Expected Changes

| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/infrastructure/observability/request_metrics.py | Measure non-processing latency and application errors without content logging. |
| CREATE | backend/src/cms_planner/api/response_budget.py | Classify and instrument authenticated non-processing requests. |

## External References

- [Python 3.14 time documentation](https://docs.python.org/3.14/library/time.html)
- [FastAPI 0.141.1 middleware documentation](https://fastapi.tiangolo.com/tutorial/middleware/)
- [Uvicorn settings](https://www.uvicorn.org/settings/)

## Build Commands

- [Backend build and validation commands](.propel/build/)

## Implementation Validation Strategy

- [ ] Unit tests pass for route classification, timing, percentile aggregation, and application-error counting.
- [ ] Integration performance validation passes with at least 1,000 authenticated non-processing requests, p95 below 300ms, and fewer than 0.5% application errors.

## Implementation Checklist

- [ ] Instrument authenticated non-processing requests without recording case content. (AC-003)
- [ ] Demonstrate p95 below 300ms across at least 1,000 steady-state requests from one authenticated user. (AC-003)
- [ ] Keep application errors below 0.5% for the measured request set. (AC-003)
