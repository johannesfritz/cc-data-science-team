---
name: diagram-generator
description: "Generate structured diagrams (flowcharts, decision trees, process maps) as high-DPI PNG images using HTML/CSS + Playwright. Use when user needs a visual diagram with nodes, connectors, or structured layout. NOT for data charts (use R+cowplot via chart-creation rules) or AI-generated images (use header-image-generator)."
allowed-tools: Read, Bash, Write, AskUserQuestion
---

# Diagram Generator

Generate publication-quality structured diagrams using HTML/CSS templates rendered via Playwright at 4x DPI. Covers flowcharts, decision trees, process maps, scorecards, and structured infographics.

## Routing

| Use This Skill | Use Instead |
|---|---|
| Flowcharts, decision trees | |
| Process maps, timelines | |
| Scorecards, comparison cards | |
| Structured infographics with nodes/connectors | |
| | Data charts with axes/series: `chart-creation.md` + R+cowplot |
| | AI-generated header art: `header-image-generator` skill |
| | Interactive dashboards: Shiny / Plotly |

## Workflow

```
Phase 1: Structure Brief (interactive — stops for user input)
  1. Read source material, identify logical structure
  2. Propose diagram type + layout + GTA branding (yes/no)
  3. Present structure sketch to user via AskUserQuestion
  4. User approves, modifies, or redirects

Phase 2: Build + Render (autonomous)
  5. Write HTML/CSS template in project styling/ folder
  6. Render via render_diagram.py
  7. Verify output (file size, dimensions)

Phase 3: Iterate (interactive)
  8. Present result description to user
  9. User requests adjustments
  10. Modify HTML/CSS, re-render, repeat
```

## GTA Visual Identity (Optional)

Ask during Phase 1: "Should this use GTA branding?" When active, apply the GTA mandatory elements (colours, header gradient, logos, font) — full spec in `references/gta-branding.md`. When not active, ask the user for their colour palette and branding preferences.

## Output Formats

| Format | CSS Size | Scale | Pixel Output | Use |
|---|---|---|---|---|
| Portrait 4:5 (default) | 1080x1350 | 4x | 4320x5400 | Social media, LinkedIn |
| Landscape 16:9 | 1456x816 | 4x | 5824x3264 | Blog headers, presentations |
| Square 1:1 | 1080x1080 | 4x | 4320x4320 | Instagram, Twitter |

## Renderer

Use the shared renderer script:

```bash
python3 /path/to/cc-data-science-team/skills/diagram-generator/scripts/render_diagram.py \
  --template styling/my-diagram.html \
  --output results/my-diagram.png \
  --width 1080 --height 1350 --scale 4 \
  --header-icon /path/to/GTA\ Icon\ Color\ dark.png \
  --footer-logo /path/to/GTA_logo.png
```

**Arguments:**

| Flag | Default | Description |
|---|---|---|
| `--template` | (required) | HTML file path |
| `--output` | (required) | Output PNG path |
| `--width` | 1080 | Viewport width in CSS pixels |
| `--height` | 1350 | Viewport height in CSS pixels |
| `--scale` | 4 | Device scale factor (4 = 300+ DPI) |
| `--selector` | `.card` | CSS selector for the element to screenshot |
| `--header-icon` | none | Path to header icon image |
| `--footer-logo` | none | Path to footer logo image |
| `--wait` | 1200 | Milliseconds to wait for fonts/images |

## HTML Template Rules

1. **Google Fonts in `<head>`**: `<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap">`
2. **All styling in `<style>` block** — no external CSS files
3. **Fixed pixel dimensions** on the root `.card` element matching the chosen format
4. **Logo placeholders** with `id="header-icon-img"` and `id="footer-logo"` for dynamic injection
5. **CSS reset** at top: `* { margin: 0; padding: 0; box-sizing: border-box; }`
6. **Self-contained**: the HTML must render correctly when opened in a browser (minus logos)

## CSS Design Patterns

See `references/css-patterns.md` for the catalogue: layouts (3-column decision-tree spine), connectors (vertical lines, arrow heads, horizontal arms, fork/split), node styles (decision, outcome, badge), colour semantics (severity → hex), and pre-render height estimation. Pull what fits; you don't have to use the whole catalogue.

## Quality Checklist

- [ ] PNG output at 4x scale factor (300+ DPI)
- [ ] All text readable at target display size (test at ~375px wide for mobile)
- [ ] Connectors aligned (no visual gaps between nodes and lines)
- [ ] Colour semantics consistent (same outcome type = same colour everywhere)
- [ ] Arrow heads visible and pointing in the correct direction
- [ ] If GTA branded: header icon, footer logo, Roboto font, #E8EEF5 bg, source caption
- [ ] No browser default styles leaking through
- [ ] Inspect output PNG files via `file` or `ls -la` (Bash) rather than the Read tool — Read processes PNGs as multimodal images, and corrupt/invalid PNGs trigger an API error that crashes the session

## Reference Implementation

The S232 metals tariff decision tree is the worked example for this skill:

- **HTML template:** `jf-thought/sgept-analytics/us-tariff-barrier-estimates/styling/s232-flowchart.html`
- **Project renderer:** `jf-thought/sgept-analytics/us-tariff-barrier-estimates/code/metal-s232-flowchart/generate_s232_flowchart_v2.py`
- **Output:** `results/metal-s232-flowchart/s232_flowchart_portrait.png` (4320x5400px, 4:5)

## Requirements

- `playwright` Python package: `pip install playwright`
- Chromium browser: `python -m playwright install chromium`
- Project must have `styling/` folder (for HTML templates) and `results/` folder (for output)
- Google Fonts CDN access (Roboto). Offline fallback: system sans-serif
