# Task - TASK_003

## Requirement Reference
- **User Story:** US_003
- **Story Location:** .propel/context/tasks/EP-TECH/us_003/us_003.md
- **Acceptance Criteria:**
  - AC-001: Valid typed configuration is available when the backend starts.
  - AC-002: Invalid configuration prevents the API from accepting traffic.
- **Edge Cases:**
  - An approved provider without its endpoint or key prevents startup.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | FastAPI | 0.141.1 | TR-010 places validation before API readiness. |

---

## Task Overview
Wire validated settings into backend startup and readiness. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001, TASK_002 - Requires typed settings and validation policies.

## Impacted Components
- New application startup lifecycle and readiness state.

## Implementation Plan
- Load and validate configuration before constructing adapters or routes.
- Expose readiness only after successful validation.

## Current Project State
- The planned composition root has no startup configuration lifecycle.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/infrastructure/config/startup.py | Validate configuration before composition. |
| CREATE | backend/src/cms_planner/api/routes/health.py | Expose safe liveness and readiness states. |

## External References
- https://fastapi.tiangolo.com/advanced/events/

## Build Commands
- `cd backend; python -m pytest tests/integration/test_startup_configuration.py`

## Implementation Validation Strategy
- [ ] Valid settings allow readiness.
- [ ] Invalid settings stop startup before routes accept traffic.

## Implementation Checklist
- [ ] Supply validated typed settings during startup for AC-001.
- [ ] Delay readiness until configuration succeeds for AC-001.
- [ ] Abort startup with safe diagnostics for AC-002.
