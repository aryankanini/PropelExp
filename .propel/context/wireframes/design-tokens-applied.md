# Design Tokens Applied - CMS Deficiency Action Planner

## Aesthetic Direction

**Direction**: Utilitarian `[SOURCE:INPUT]`

The high-fidelity wireframes preserve the declared compliance-workspace direction: dense evidence review, restrained semantic color, clear state distinctions, and no decorative imagery. Precedents are Sentry, Grafana, and PostHog. The interface avoids consumer wellness, marketing dashboard, glassmorphic assistant, and literal government-form treatments.

## Token Sources

- Canonical definitions: [Design system](../docs/designsystem.md).
- Screen and component usage: [Figma specification](../docs/figma_spec.md).
- Synthetic UX records: [Sample data](data/sample-data.json).
- HTML files declare primitive custom properties only in `:root`; component rules consume semantic aliases such as `--text`, `--canvas`, `--action`, `--warning`, and `--danger`.

## Token Application by Screen

| Screen | Token Emphasis | Notes |
|---|---|---|
| SCR-001 | Raised authentication surface, information notice, primary action | Dark and reduced-motion preferences included |
| SCR-002 | Canvas/raised upload hierarchy, danger cleanup action | Dashed upload boundary uses strong border intent |
| SCR-003 | Success/current/pending timeline states | Stable progress geometry and tabular percentage |
| SCR-004 | Accent selection and evidence highlight | Four-pane desktop composition |
| SCR-005 | Warning uncertainty and selected candidate | Correction remains visually distinct from extraction |
| SCR-006 | Information, edited, and missing-information provenance | 160px minimum editor dimensions |
| SCR-007 | Current revision and complete readiness | Approval action isolated in decision pane |
| SCR-008 | Approved status, warning draft label, destructive cleanup | Export output begins with required draft label |

## Drift Notes

- The wireframes use no new semantic status category or component outside the design system inventory.
- Responsive CSS applies 768px and mobile adaptations; large-desktop content remains bounded by screen-specific max widths.
- SCR-002 through SCR-008 use a repeated embedded shell for standalone reviewability. Production React must consolidate this into the shared AppShell and WorkflowRail.
- Dark-mode token resolution is demonstrated on SCR-001; production implementation must apply the complete documented light, dark, and high-contrast maps across all shared components.