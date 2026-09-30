# Task - TASK_004

## Requirement Reference
- **User Story:** US_001
- **Story Location:** .propel/context/tasks/EP-TECH/us_001/us_001.md
- **Acceptance Criteria:**
  - AC-001: Independent manifests, test commands, environment examples, and build outputs exist without cross-application imports.
  - AC-002: Core backend packages have inward dependencies.
- **Edge Cases:**
  - A cross-application source import fails with the importing file identified.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| DevOps | Node.js and Python | Node.js 24 LTS; Python 3.14.7 | TR-001 and NFR-009 require repository-wide boundary verification. |

---

## Task Overview
Add a repository check that verifies independent application assets and prohibited imports. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_001, TASK_002, TASK_003 - Requires both application boundaries and backend import rules.

## Impacted Components
- New repository architecture verification script.

## Implementation Plan
- Verify required manifests, environment examples, commands, and output roots.
- Scan both source trees for cross-application imports and invoke backend architecture checks.

## Current Project State
- Separate application scaffolds and backend package checks are planned independently.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | scripts/verify_application_boundaries.py | Verify application separation and report offending files. |

## External References
- https://docs.python.org/3.14/library/pathlib.html

## Build Commands
- `python scripts/verify_application_boundaries.py`

## Implementation Validation Strategy
- [x] The check recognizes both independent applications.
- [x] Deliberate cross-boundary imports fail with actionable paths.

## Implementation Checklist
- [x] Verify independent manifests, commands, examples, and outputs for AC-001.
- [x] Reject frontend-to-backend and backend-to-frontend source imports for AC-001.
- [x] Include the core dependency test result for AC-002.
