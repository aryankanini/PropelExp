# Task - TASK_003

## Requirement Reference
- **User Story:** US_001
- **Story Location:** .propel/context/tasks/EP-TECH/us_001/us_001.md
- **Acceptance Criteria:**
  - AC-001: Separate application boundaries expose independent manifests, commands, examples, and outputs without cross-application source imports.
  - AC-002: Domain and application packages contain no web-framework or provider-SDK imports.
- **Edge Cases:**
  - A cross-application source import fails the architecture check with the importing file identified.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend | Python | 3.14.7 | NFR-009 requires framework-independent core packages and architecture checks. |

---

## Task Overview
Create inward-facing domain and application package boundaries with automated import rules. Estimated effort: 8 hours.

## Dependent Tasks
- TASK_002 - Requires the backend package structure.

## Impacted Components
- New backend core packages and architecture tests.

## Implementation Plan
- Establish domain and application package roots.
- Scan imports and report forbidden framework or provider dependencies by file.

## Current Project State
- The backend composition root is planned; core package boundaries do not exist.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/cms_planner/domain/__init__.py | Establish the framework-independent domain package. |
| CREATE | backend/src/cms_planner/application/__init__.py | Establish the application package that owns ports. |
| CREATE | backend/tests/architecture/test_dependency_boundaries.py | Enforce inward dependencies and report offending imports. |

## External References
- https://docs.python.org/3.14/library/ast.html

## Build Commands
- `cd backend; python -m pytest tests/architecture/test_dependency_boundaries.py`

## Implementation Validation Strategy
- [x] The architecture test passes for allowed imports.
- [x] A fixture with a FastAPI or provider import fails with its path.

## Implementation Checklist
- [x] Include the backend package boundary in setup checks without importing frontend source for AC-001.
- [x] Create framework-independent domain and application packages for AC-002.
- [x] Detect web-framework imports in core packages for AC-002.
- [x] Detect provider-SDK imports and identify the importing file for AC-002.
