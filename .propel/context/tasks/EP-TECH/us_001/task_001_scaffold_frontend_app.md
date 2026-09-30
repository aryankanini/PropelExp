# Task - TASK_001

## Requirement Reference
- **User Story:** US_001
- **Story Location:** .propel/context/tasks/EP-TECH/us_001/us_001.md
- **Acceptance Criteria:**
  - AC-001: Separate frontend and backend manifests, test commands, environment examples, and build outputs are detected without cross-application source imports.
  - AC-002: Domain and application package scans find no web-framework or provider-SDK imports.
- **Edge Cases:**
  - A cross-application source import fails the architecture check with the importing file identified.

---

## Applicable Technology Stack

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Frontend | React | 19.3 | TR-002 establishes the standalone SPA boundary. |
| Frontend | TypeScript | 7.0 | TR-002 requires typed frontend source. |
| Frontend | Vite | 8.3 | TR-002 defines the independent frontend build toolchain. |
| Frontend | Node.js | 24 LTS | TR-001 requires an independently buildable frontend runtime. |

---

## Task Overview
Create the standalone React application boundary with its own manifest, source root, build configuration, and output directory.

Estimated effort: 8 hours.

## Dependent Tasks
- None. This is the first implementation task for US_001.

## Impacted Components
- New `frontend/` application boundary and `frontend/src/app/` composition root.

## Implementation Plan
- Define the frontend package manifest and locked dependency graph.
- Configure TypeScript and Vite for an isolated build rooted in `frontend/`.
- Add the minimal React composition root and application entry point.
- Keep all imports within the frontend application boundary.

## Current Project State
- `.propel/` contains planning artifacts.
- `frontend/` does not exist and will be created by this task.
- `backend/` does not exist and is outside this task's technology layer.

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | frontend/package.json | Define independent frontend build and test scripts. |
| CREATE | frontend/package-lock.json | Lock the approved frontend dependency versions. |
| CREATE | frontend/tsconfig.json | Configure strict TypeScript compilation within the frontend boundary. |
| CREATE | frontend/vite.config.ts | Configure the standalone Vite build output. |
| CREATE | frontend/index.html | Provide the SPA document entry point. |
| CREATE | frontend/src/main.tsx | Mount the React application. |
| CREATE | frontend/src/app/App.tsx | Define the initial application composition root. |

## External References
- [React 19 documentation](https://react.dev/versions)
- [TypeScript 7 documentation](https://www.typescriptlang.org/docs/)
- [Vite 8 guide](https://vite.dev/guide/)

## Build Commands
- [Frontend build commands](.propel/build/)

## Implementation Validation Strategy
- [x] Unit tests pass.
- [x] Integration tests pass.

## Implementation Checklist
- [x] Create the independent frontend manifest and locked dependencies for AC-001.
- [x] Configure isolated TypeScript compilation for AC-001.
- [x] Configure Vite to emit the frontend build output for AC-001.
- [x] Add the React entry point and composition root for AC-001.
- [x] Define independent frontend build and test commands for AC-001.
- [x] Keep all frontend source imports inside the frontend boundary for AC-001.
- [x] Keep the frontend manifest free of backend framework and provider SDK dependencies to preserve the architecture scan boundary for AC-002.
