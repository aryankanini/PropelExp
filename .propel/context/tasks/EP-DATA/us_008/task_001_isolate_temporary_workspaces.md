# Task - TASK_001

## Requirement Reference
- **User Story:** US_008
- **Story Location:** .propel/context/tasks/EP-DATA/us_008/us_008.md
- **Parent Epic:** EP-DATA
- **Acceptance Criteria:**
  - AC-001: Uploads stream to randomized session-owned workspace paths independent of client filenames, and failures remove every partial file.
- **Edge Cases:**
  - A filename containing traversal segments is retained only as metadata and never affects the filesystem path.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend Filesystem | Python | 3.14.7 | DR-003 requires controlled temporary workspace operations. |
| Backend Filesystem | Temporary workspace | None | Case files remain transient and isolated without database storage. |

---

## Task Overview
Create randomized, session-owned temporary upload workspaces for US_008 under EP-DATA. Estimated effort: 8 hours.

## Dependent Tasks
- US_006 must provide authenticated session ownership.

## Impacted Components
- New workspace port, secure temporary adapter, streamed upload service, metadata model, and tests.

## Implementation Plan
- Allocate unpredictable workspace and file paths beneath the configured temporary root.
- Preserve the client filename only as inert metadata.
- Stream bytes without deriving any path component from client input.
- Remove partial files and workspace residue after stream or validation failure.

## Current Project State
- The repository is planning-only under `.propel/`; no `frontend/`, `backend/`, `app/`, or `server/` source directories exist.
- US_008 depends on planned US_006 session ownership; persistence is limited to a temporary workspace and in-memory repository.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | backend/src/application/ports/workspace.py | Define session-owned temporary workspace operations. |
| CREATE | backend/src/domain/documents/upload_metadata.py | Retain client filename as metadata only. |
| CREATE | backend/src/adapters/filesystem/temporary_workspace.py | Allocate randomized paths beneath the configured root. |
| CREATE | backend/src/application/services/stream_upload.py | Stream uploads and clean failed partial writes. |
| CREATE | backend/tests/unit/filesystem/test_workspace_paths.py | Prove client filenames never control paths. |
| CREATE | backend/tests/integration/test_failed_upload_cleanup.py | Verify failed streams and validation leave no partial files. |

## External References
- [Python 3.14 tempfile documentation](https://docs.python.org/3.14/library/tempfile.html)
- [Python 3.14 pathlib documentation](https://docs.python.org/3.14/library/pathlib.html)

## Build Commands
- [Backend filesystem build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit-test structure covers randomized paths, session ownership, and traversal filenames as metadata only.
- [x] Integration-test structure interrupts streaming and validation to verify all partial files are removed.

## Implementation Checklist
- [x] Allocate randomized session-owned workspace paths for AC-001.
- [x] Keep client filenames out of every filesystem path for AC-001.
- [x] Stream upload bytes into the owned temporary workspace for AC-001.
- [x] Remove every partial file after stream or validation failure for AC-001.
