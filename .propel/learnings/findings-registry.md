<!-- Schema: ./findings-registry-schema.md -->
# Findings Registry

## Index

| File | Finding IDs |
|------|-------------|
| backend/src/cms_planner/application/confirmation_service.py | F001 |

## Entries

```yaml
- id: F001
  file: backend/src/cms_planner/application/confirmation_service.py
  cat: bug-triage
  type: finding
  severity: HIGH
  issue: Provider failure made confirmation retries stale
  cause: Confirmation committed before generation but repeat confirmation was not idempotent
  date: 2026-10-28
  workflow: implementation
```
