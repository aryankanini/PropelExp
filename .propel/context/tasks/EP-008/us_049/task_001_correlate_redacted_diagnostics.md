# Task - TASK_001

## Requirement Reference
- **User Story:** us_049
- **Story Location:** .propel/context/tasks/EP-008/us_049/us_049.md
- **Acceptance Criteria:** AC-001, AC-002
- **Edge Cases:** Log-like malicious values remain redacted data.

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Monitoring | Python structured logging | Python 3.14 standard logging | NFR-010 and TR-012 define correlated safe diagnostics. |

---

## Task Overview
**Estimated Effort:** 8 hours

Propagate one correlation identifier across API, jobs, events, and structured logs while enforcing an allow-listed diagnostic schema.

## Dependent Tasks
- TASK_001 from US_046.

## Impacted Components
- Correlation middleware, job context, structured formatter, and redaction filter.

## Implementation Plan
- Establish or accept a validated correlation identifier.
- Propagate immutable context into jobs and events.
- Emit allow-listed structured fields.
- Redact prohibited keys and values before formatting.

## Current Project State
```text
backend/src/cms_planner/infrastructure/observability/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/infrastructure/observability/correlation.py | Propagate request and job correlation context. |
| CREATE | backend/src/cms_planner/infrastructure/observability/logging.py | Configure allow-listed structured diagnostics. |
| MODIFY | backend/src/cms_planner/app.py | Register correlation middleware and logging. |

## External References
- https://docs.python.org/3.14/library/logging.html
- https://docs.python.org/3.14/library/contextvars.html

## Build Commands
- [Backend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests cover field allow-listing and redaction.
- [x] Integration tests link API, event, job, and log records by correlation ID.

## Implementation Checklist
- [x] Assign one correlation ID at API request or job creation. (AC-001)
- [x] Propagate correlation ID through responses, events, jobs, and logs. (AC-001)
- [x] Emit timestamp, level, actor, route/stage, duration, result code, and provider. (AC-002)
- [x] Exclude document, SOD, POC, credential, and provider payload content. (AC-002)
- [x] Treat malicious log-like input as redacted data, not structure. (AC-002, Edge Case)
