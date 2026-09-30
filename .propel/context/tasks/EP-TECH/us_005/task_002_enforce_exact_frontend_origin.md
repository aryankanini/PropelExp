# Task - TASK_002

## Requirement Reference
- **User Story:** US_005
- **Story Location:** .propel/context/tasks/EP-TECH/us_005/us_005.md
- **Acceptance Criteria:**
  - AC-001: Frontend and backend bind to distinct configurable loopback ports with independent health checks.
  - AC-002: Browser origins other than the configured local frontend origin are rejected without protected content.
- **Edge Cases:**
  - A wildcard origin fails startup validation.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | FastAPI | 0.141.1 | NFR-007 and TR-014 require exact-origin enforcement at the API boundary. |

---

## Task Overview
Configure exact local-origin validation and safe cross-origin rejection. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires configured frontend and backend endpoints.

## Impacted Components
- New API origin policy and middleware wiring.

## Implementation Plan
- Build the allow-list from one validated local frontend origin.
- Reject wildcard, null, malformed, and non-matching origins before protected responses.

## Current Project State
- Native process startup is planned without API origin middleware.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/api/origin_policy.py | Define exact-origin decisions. |
| CREATE | backend/src/cms_planner/api/middleware.py | Apply the validated origin policy. |

## External References
- https://fastapi.tiangolo.com/tutorial/cors/

## Build Commands
- `cd backend; python -m pytest tests/integration/test_origin_policy.py`

## Implementation Validation Strategy
- [ ] The configured exact origin is accepted.
- [ ] Other origins receive no protected response content.

## Implementation Checklist
- [ ] Consume the configured frontend loopback origin without owning frontend or backend process launch for AC-001.
- [ ] Configure one exact local frontend origin for AC-002.
- [ ] Reject wildcard, null, and non-matching origins for AC-002.
- [ ] Prevent protected content in rejected-origin responses for AC-002.
