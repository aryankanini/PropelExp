# Task - TASK_001

## Requirement Reference
- **User Story:** US_010
- **Story Location:** .propel/context/tasks/EP-DATA/us_010/us_010.md
- **Parent Epic:** EP-DATA
- **Acceptance Criteria:**
  - AC-001: Restart leaves zero case records recoverable from database, cache, backup, or migration mechanisms.
  - AC-002: Source and API responses contain no credential hashes, session secrets, provider keys, or approval flags.
- **Edge Cases:**
  - An ignored local environment file may supply secrets but cannot be committed by the configured ignore rules.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend Privacy/Configuration | Python | 3.14.7 | DR-005 and DR-006 enforce transient state and external protected configuration. |
| Backend Privacy/Configuration | Pydantic | 2.x | Typed settings can exclude secrets from serialization and diagnostics. |
| Backend Privacy/Configuration | Database | None | The approved architecture prohibits durable case persistence. |

---

## Task Overview
Prevent durable case recovery and keep protected configuration external for US_010 under EP-DATA. Estimated effort: 8 hours.

## Dependent Tasks
- US_003 must provide typed startup configuration.

## Impacted Components
- New transient-storage policy checks, protected settings model, response leak tests, and ignore rules.

## Implementation Plan
- Restrict case repository construction to the in-memory adapter and temporary workspace.
- Scan backend configuration and packaging for database, cache, backup, or migration mechanisms.
- Load protected values from ignored local environment only and exclude them from serialization and API schemas.
- Verify a simulated restart cannot recover prior case state.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_010 depends on planned US_003 typed configuration; the approved data layer is None, using only an in-memory repository and temporary workspace.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/config/protected_settings.py | Load protected values while excluding them from serialization. |
| CREATE | backend/src/application/policies/transient_storage.py | Prohibit durable case-storage mechanisms. |
| CREATE | backend/tests/unit/config/test_protected_settings.py | Verify protected values never serialize or enter diagnostics. |
| CREATE | backend/tests/integration/test_empty_restart.py | Verify no case records survive process restart. |
| CREATE | backend/tests/integration/test_api_secret_exposure.py | Inspect API schemas and responses for prohibited protected values. |
| CREATE | backend/tests/architecture/test_no_durable_storage.py | Reject database, cache, backup, or migration case recovery mechanisms. |
| CREATE | backend/.gitignore | Prevent local environment files from being committed. |

## External References
- [Pydantic 2 secret types](https://docs.pydantic.dev/2.12/api/types/#pydantic.types.SecretStr)
- [Python 3.14 os documentation](https://docs.python.org/3.14/library/os.html)
- [Git ignore documentation](https://git-scm.com/docs/gitignore)

## Build Commands
- [Backend privacy build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit-test structure verifies protected settings are external, redacted, and excluded from serialization.
- [x] Integration-test structure simulates restart and inspects source-facing schemas and API responses for prohibited recovery or secret exposure.

## Implementation Checklist
- [x] Prohibit database, cache, backup, and migration recovery mechanisms for AC-001.
- [x] Verify restart begins with zero recoverable case records for AC-001.
- [x] Keep credential hashes, session secrets, provider keys, and approval flags out of source and API responses for AC-002.
- [x] Allow ignored local environment input while preventing its commit for AC-002.