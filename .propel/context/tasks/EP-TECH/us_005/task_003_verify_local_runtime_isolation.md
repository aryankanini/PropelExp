# Task - TASK_003

## Requirement Reference
- **User Story:** US_005
- **Story Location:** .propel/context/tasks/EP-TECH/us_005/us_005.md
- **Acceptance Criteria:**
  - AC-001: Separate processes expose independent health checks on distinct loopback ports.
  - AC-002: Unconfigured origins are rejected without protected content.
- **Edge Cases:**
  - Wildcard origins and non-loopback addresses fail startup validation.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Testing | Node.js and Python | Node.js 24 LTS; Python 3.14.7 | NFR-007 requires executable verification of localhost isolation. |

---

## Task Overview
Add runtime checks for loopback binding, health independence, and origin denial. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001, TASK_002 - Requires native launch and exact-origin enforcement.

## Impacted Components
- New localhost runtime integration tests.

## Implementation Plan
- Start each application independently on configured test ports.
- Probe health, listening addresses, accepted origin, and rejected origins.

## Current Project State
- Runtime and origin controls are planned without end-to-end isolation checks.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/tests/integration/test_local_runtime_isolation.py | Verify bind, port, health, and origin behavior. |

## External References
- https://docs.python.org/3.14/library/ipaddress.html

## Build Commands
- `cd backend; python -m pytest tests/integration/test_local_runtime_isolation.py`

## Implementation Validation Strategy
- [ ] Listening endpoints are loopback-only and distinct.
- [ ] Origin-denial probes expose no protected content.

## Implementation Checklist
- [ ] Verify separate process ports and health checks for AC-001.
- [ ] Verify both listening addresses are loopback-only for AC-001.
- [ ] Verify exact-origin acceptance and all other-origin denial for AC-002.
