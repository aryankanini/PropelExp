# CMS Deficiency Action Planner

CMS Deficiency Action Planner is a local, session-scoped web application for
processing CMS-2567 survey documents. It extracts provider identity, F/K/L and
other alphabetic deficiency tags, complete Statements of Deficiency (SOD), and
source-page evidence. Reviewers can confirm a deficiency, generate and edit a
five-part Plan of Correction (POC), approve the current revision, and copy or
download the approved POC as plain paragraphs.

The application stores case state in memory and uploaded files in a temporary
workspace. It does not use a durable database. Restarting the backend clears
active case state.

## Features

- Streamed CMS-2567 PDF intake with 50 MB and 200-page limits.
- CMS layout recognition across common header and OCR variations.
- Coordinate-aware extraction of the SOD column, excluding the POC column and
  repeated continuation-page headers and footers.
- Provider name and provider/CLIA identification-number extraction.
- Support for alphabetic tags such as `E0000`, `K0000`, `K0222`, `L0000`, and
  `F0686`.
- Multi-page deficiency coalescing with evidence retained by source page.
- Numbered point and subpoint handling (`1.`, `A.`, `i.`, `a.`).
- Evidence-linked review, corrections, confirmation, and revision tracking.
- Guarded AI-assisted POC generation with provider approval controls.
- Compliance-leader approval and stale-revision protection.
- Copy and `.txt` export of approved POC content as plain paragraphs.
- Automatic session cleanup and no durable case storage.

## Repository Layout

```text
backend/                 FastAPI application, domain logic, adapters, and tests
frontend/                React/Vite application and browser/component tests
scripts/                 Repository verification utilities
prompts/                 Prompt experiments and supporting material
.propel/                 PropelIQ configuration, rules, and local knowledge map
TECHNICAL_SPECIFICATIONS.md
```

## Prerequisites

- Python 3.14.x, as required by `backend/pyproject.toml`.
- Node.js with npm. Use a currently supported LTS release.
- Tesseract OCR only when scanned pages must use the OCR route.
- An approved HTTPS AI provider when AI POC generation is required.

## Backend Setup

From PowerShell:

```powershell
Set-Location backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
Copy-Item .env.example .env
```

Review `.env` before enabling provider calls. Never commit real credentials.
Environment files are examples only; ensure the variables are loaded into the
backend process by your shell or development tooling.

Start the API:

```powershell
python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

The API is available at `http://127.0.0.1:8000`. FastAPI documentation is
available at `http://127.0.0.1:8000/docs` during local development.

## Frontend Setup

Open a second PowerShell terminal:

```powershell
Set-Location frontend
npm install
Copy-Item .env.example .env
npm run dev
```

The frontend is available at `http://127.0.0.1:5173`. Its default API origin is
`http://127.0.0.1:8000`, controlled by `VITE_BACKEND_ORIGIN`.

## Application Flow

1. **Intake**: Upload one CMS-2567 PDF for the active local session.
2. **Extraction**: The backend classifies pages, reads native text or routes the
   page to OCR, identifies CMS structure, extracts provider metadata, separates
   SOD from the form's POC column, and builds deficiency boundaries.
3. **Review**: Verify provider identity, each normalized tag, complete SOD text,
   point hierarchy, and source-page evidence.
4. **Confirmation**: Confirm the current deficiency revision. Incomplete or
   unresolved evidence blocks progression.
5. **POC authoring**: Generate and edit affected-resident, risk, corrective,
   monitoring, and completion-date content.
6. **Approval**: A compliance leader approves the current POC revision. Editing
   an approved revision requires reapproval.
7. **Export**: Copy or download the approved POC. The export retains the required
   draft-status label and emits the POC body as plain paragraphs without section
   headings.
8. **End session**: Remove the case and temporary uploaded files.

```mermaid
flowchart LR
    A["Upload CMS-2567"] --> B["Extract provider and SOD"]
    B --> C["Review tags and evidence"]
    C --> D["Confirm deficiency"]
    D --> E["Generate and edit POC"]
    E --> F["Compliance approval"]
    F --> G["Copy or download"]
    G --> H["End session and clean up"]
```

## Configuration

Backend variables are documented in `backend/.env.example`:

| Variable | Purpose |
|---|---|
| `BACKEND_HOST`, `BACKEND_PORT` | Local API binding values for development tooling. |
| `WORKSPACE_ROOT` | Optional temporary upload location when supplied by composition. |
| `FRONTEND_ORIGIN` | Expected local frontend origin. |
| `PROVIDER_ENDPOINT` | HTTPS chat-completions-compatible provider endpoint. |
| `PROVIDER_API_KEY` | Provider credential. |
| `PROVIDER_MODEL` | Provider model identifier. |
| `PROVIDER_TIMEOUT_SECONDS` | Provider timeout, limited to 120 seconds. |
| `PROVIDER_*_APPROVED` | BAA, retention, training-use, and risk approvals. |
| `CREDENTIAL_HASH`, `SESSION_SECRET` | Protected local authentication settings. |

Provider use fails closed unless the required approvals and valid configuration
are present. Basic deterministic extraction can still operate without an AI
provider, but AI POC generation will be unavailable.

## Testing

Run all backend tests:

```powershell
Set-Location backend
python -m pytest
```

Run frontend component tests, type checking, and production build:

```powershell
Set-Location frontend
npm test
npm run typecheck
npm run build
```

Run Playwright tests:

```powershell
Set-Location frontend
npx playwright install chromium
npm run test:e2e
```

## Operational Notes

- One active case is supported per session.
- The frontend currently uses the local session ID `local-session` and stores
  only the active case ID in browser session storage.
- Backend case and POC repositories are process-memory implementations.
- Temporary uploads use randomized paths under the operating system's temporary
  directory by default and are removed on session cleanup or application exit.
- The default composition does not enable an OCR provider. OCR-routed pages need
  an approved adapter configuration.
- Previously extracted cases are not migrated after parser changes. Restart the
  backend and re-upload or rerun extraction to see updated results.

## Further Documentation

See [TECHNICAL_SPECIFICATIONS.md](TECHNICAL_SPECIFICATIONS.md) for architecture,
data contracts, extraction rules, API groups, security controls, and constraints.