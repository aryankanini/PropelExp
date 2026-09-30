# Task - TASK_001

## Requirement Reference
- **User Story:** US_003
- **Story Location:** .propel/context/tasks/EP-TECH/us_003/us_003.md
- **Acceptance Criteria:**
  - AC-001: Typed configuration exposes origins, addresses, ports, workspace, limits, credentials, provider settings, timeouts, and retention values.
  - AC-002: Missing or contradictory settings fail startup before traffic with only a safe setting name and reason.
- **Edge Cases:**
  - An approved provider without its required endpoint or key is contradictory.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | TR-010 requires typed environment-backed runtime configuration. |

---

## Task Overview
Define typed runtime settings and safe environment loading. Estimated effort: 8 hours.

## Dependent Tasks
- US_001 TASK_002 - Requires the backend package.

## Impacted Components
- New configuration models and environment loader.

## Implementation Plan
- Model every required setting group with explicit types and safe defaults only.
- Load secrets from environment without exposing values in representations.

## Current Project State
- No backend configuration module exists.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/infrastructure/config/settings.py | Define typed runtime settings. |
| CREATE | backend/src/cms_planner/infrastructure/config/loader.py | Load and redact environment configuration. |

## External References
- https://docs.python.org/3.14/library/os.html

## Build Commands
- `cd backend; python -m pytest tests/unit/infrastructure/config`

## Implementation Validation Strategy
- [ ] Valid environment values produce typed settings.
- [ ] Secret values are absent from representations and errors.

## Implementation Checklist
- [ ] Model all required configuration groups for AC-001.
- [ ] Load protected values only from environment inputs for AC-001.
- [ ] Expose safe typed values to the composition root for AC-001.
- [ ] Expose safe setting names and typed constraints for startup validation without revealing protected values for AC-002.
