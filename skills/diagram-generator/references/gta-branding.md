# GTA visual identity

Reference for GTA-branded diagrams. Apply when the user says yes to "Should this use GTA branding?" in Phase 1. When branding is off, ask the user for colour palette and visual preferences instead.

## Mandatory elements (when GTA branding is active)

| Element | Specification |
|---|---|
| Background | `#E8EEF5` |
| Primary navy | `#003366` |
| Header | Linear gradient `#1874CD` to `#0F599D`, 5px navy top stripe |
| Font | Roboto via Google Fonts CDN (weights 300, 400, 500, 700) |
| Header icon | `GTA Icon Color dark.png` (DOM ID: `header-icon-img`) |
| Footer logo | `GTA Logo Color light.png` (DOM ID: `footer-logo`) |
| Footer text | `Source: Global Trade Alert \| globaltradealert.org` |

## Logo asset locations

- Canonical: `jf-ceo/sgept-backoffice/assets/gta-logos/`
- Also available in: `jf-thought/sgept-analytics/us-tariff-barrier-estimates/styling/`

Pass to the renderer via `--header-icon` and `--footer-logo` CLI flags so the templates remain portable across projects.
