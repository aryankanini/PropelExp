# Task - TASK_001

## Requirement Reference
- **User Story:** us_045
- **Story Location:** .propel/context/tasks/EP-007/us_045/us_045.md
- **Acceptance Criteria:** AC-001, AC-002
- **Edge Cases:** External outages affect timing exclusions only.

---

## AI References [CONDITIONAL: AI Impact = Yes]
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | Yes |
| **AIR Requirements** | AIR-006 |
| **AI Pattern** | Hybrid structured generation with deterministic validation |
| **Prompt Template Path** | N/A |
| **Guardrails Config** | backend/evaluation/config/acceptance.yaml |
| **Model Provider** | Runtime-selected BAA-approved adapter |

---

## Applicable Technology Stack
| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| AI/ML | Python, pytest | Python 3.14.7; pytest 9.x | NFR-002 and AIR-006 require repeatable release evidence. |

---

## Task Overview
**Estimated Effort:** 8 hours

Build a deterministic release evaluation harness for extraction latency, field accuracy, uncertainty surfacing, and unsupported-claim detection.

## Dependent Tasks
- TASK_001 from US_044.

## Impacted Components
- Evaluation dataset loader, scorers, timing policy, and release report.

## Implementation Plan
- Load immutable approved evaluation manifests.
- Record repeated run outcomes and documented outages.
- Score exact fields, uncertainty misses, and claim grounding.
- Produce a machine-readable pass/fail report.

## Current Project State
```text
backend/evaluation/
```

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/evaluation/run.py | Execute the approved evaluation set. |
| CREATE | backend/evaluation/scoring.py | Calculate AIR-006 metrics. |
| CREATE | backend/evaluation/config/acceptance.yaml | Record thresholds and dataset identity. |

## External References
- https://docs.python.org/3.14/library/time.html
- https://docs.pytest.org/en/9.0.x/

## Build Commands
- [Backend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests verify metric calculations and threshold boundaries.
- [x] Integration tests verify immutable, reproducible evaluation reports.

## Implementation Checklist
- [x] Measure repeated valid 100-page runs against the five-minute threshold. (AC-001)
- [x] Require at least 95% qualifying timing runs. (AC-001)
- [x] Exclude documented outages from timing only. (AC-001, Edge Case)
- [x] Score provider name, F-tag, and complete SOD at 95% or better. (AC-002)
- [x] Require every miss to be surfaced as uncertain. (AC-002)
- [x] Fail release evidence when any unsupported facility claim is present. (AC-002)
