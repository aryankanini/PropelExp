# Task - TASK_002

## Requirement Reference
- **User Story:** US_003
- **Story Location:** .propel/context/tasks/EP-TECH/us_003/us_003.md
- **Acceptance Criteria:**
  - AC-001: Typed configuration exposes origins, addresses, ports, workspace, limits, credentials, provider settings, timeouts, and retention values.
  - AC-002: Missing or contradictory settings fail startup with only a safe setting name and reason.
- **Edge Cases:**
  - An approved provider without its required endpoint or key is rejected.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | TR-010 requires fail-fast cross-setting validation. |

---

## Task Overview
Implement safe validation for required and cross-dependent runtime settings. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001 - Requires typed settings.

## Impacted Components
- New configuration validation policies and safe errors.

## Implementation Plan
- Validate loopback, origin, limits, retention, credentials, and provider dependencies.
- Return setting names and safe reasons without values.

## Current Project State
- Typed setting definitions are planned without cross-field policies.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/infrastructure/config/validation.py | Enforce required and contradictory-setting rules. |
| CREATE | backend/src/cms_planner/infrastructure/config/errors.py | Define safe configuration failures. |

## External References
- https://docs.python.org/3.14/library/ipaddress.html

## Build Commands
- `cd backend; python -m pytest tests/unit/infrastructure/config`

## Implementation Validation Strategy
- [ ] Missing and contradictory settings fail deterministically.
- [ ] Failure messages contain no credentials, keys, or secret values.

## Implementation Checklist
- [ ] Validate every typed runtime setting group exposed for startup for AC-001.
- [ ] Reject missing required settings before traffic for AC-002.
- [ ] Reject contradictory bind, origin, limit, and provider settings for AC-002.
- [ ] Report only safe setting names and reasons for AC-002.
