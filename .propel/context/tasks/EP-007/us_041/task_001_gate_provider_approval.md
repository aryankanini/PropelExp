# Task - TASK_001

## Requirement Reference
- **User Story:** us_041
- **Story Location:** .propel/context/tasks/EP-007/us_041/us_041.md
- **Acceptance Criteria:**
  - AC-001: Approved provider configuration may become available.
  - AC-002: Missing approval blocks startup or invocation before transmission.
- **Edge Cases:**
  - Restarting after an approval change revokes availability without exposing secrets.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python, FastAPI, Pydantic | Python 3.14.7; FastAPI 0.141.1; Pydantic 2.x | NFR-005 and TR-010 require typed startup and invocation configuration gates. |

---

## Task Overview
**Estimated Effort:** 6 hours

Implement a fail-closed provider approval policy that validates BAA, retention, training-use, and risk approvals before an adapter is registered or invoked.

## Dependent Tasks
- US_003 typed provider configuration.

## Impacted Components
- Backend configuration models, provider approval policy, composition root, and provider facade.

## Implementation Plan
- Define typed approval fields and contradictions in infrastructure configuration.
- Centralize the approval decision in an application-owned policy.
- Apply the policy during adapter registration and immediately before invocation.
- Return safe configuration failures without serializing secret values.

## Current Project State
```text
backend/src/cms_planner/
|-- application/
|-- adapters/
|-- infrastructure/config/
`-- app.py
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/application/provider_approval.py | Own the fail-closed approval policy. |
| CREATE | backend/src/cms_planner/infrastructure/config/provider.py | Define validated provider approval settings. |
| MODIFY | backend/src/cms_planner/app.py | Register only approved provider adapters. |

## External References
- https://docs.pydantic.dev/2.12/concepts/config/
- https://fastapi.tiangolo.com/advanced/settings/

## Build Commands
- [Backend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests cover every approval flag and secret-safe validation output.
- [x] Integration tests prove blocked providers receive no invocation.

## Implementation Checklist
- [x] Define required approval fields with no permissive defaults. (AC-001, AC-002)
- [x] Reject missing or contradictory approval configuration at startup. (AC-002)
- [x] Gate adapter registration on the centralized approval policy. (AC-001, AC-002)
- [x] Revalidate approval immediately before transmitting provider content. (AC-002)
- [x] Ensure configuration errors and logs exclude provider secrets. (AC-002, Edge Case)
- [x] Confirm restart-time approval changes revoke provider availability. (AC-002, Edge Case)