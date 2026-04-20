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

Ask during Phase 1: "Should this use GTA branding?"

When active, apply these mandatory elements:

| Element | Specification |
|---|---|
| Background | `#E8EEF5` |
| Primary navy | `#003366` |
| Header | Linear gradient `#1874CD` to `#0F599D`, 5px navy top stripe |
| Font | Roboto via Google Fonts CDN (weights 300, 400, 500, 700) |
| Header icon | `GTA Icon Color dark.png` (ID: `header-icon-img`) |
| Footer logo | `GTA Logo Color light.png` (ID: `footer-logo`) |
| Footer text | `Source: Global Trade Alert \| globaltradealert.org` |
| Logo assets | `jf-ceo/sgept-backoffice/assets/gta-logos/` |
| Also in | `jf-thought/sgept-analytics/us-tariff-barrier-estimates/styling/` |

When NOT active, ask user for colour palette and branding preferences.

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

### Layout: Vertical spine with horizontal exits (decision trees)

3-column CSS Grid where the decision node is centred and exits branch to one side:

```css
.row {
  display: grid;
  grid-template-columns: 1fr 320px 1fr;
  align-items: center;
}
/* Column 1: empty | Column 2: decision node | Column 3: exit outcome */
```

### Connectors (CSS-only, no SVG)

**Vertical line:**
```css
.v-line { width: 2.5px; height: 20px; background: #003366; border-radius: 1px; }
```

**Arrow head (down):**
```css
.arrow-down {
  width: 0; height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 7px solid #003366;
}
```

**Horizontal arm with right-pointing arrow:**
```css
.h-line {
  flex: 1; height: 2.5px; position: relative;
  background: #1E8449; min-width: 16px;
}
.h-line::after {
  content: '';
  position: absolute; right: -1px; top: 50%;
  transform: translateY(-50%);
  border-top: 6px solid transparent;
  border-bottom: 6px solid transparent;
  border-left: 8px solid #1E8449;
}
```

**Fork/split (inverted T):**
```css
.split-fork { display: flex; flex-direction: column; align-items: center; }
.v-stem { width: 2.5px; height: 14px; background: #003366; }
.h-bar { height: 2.5px; background: #003366; align-self: stretch; margin: 0 160px; }
```

### Node styles

**Decision node:** white bg, navy border, rounded, shadow
```css
.decision-box {
  background: white; border: 2.5px solid #003366; border-radius: 10px;
  padding: 12px 20px; text-align: center; font-size: 15px; font-weight: 500;
  color: #1a1a2e; box-shadow: 0 2px 8px rgba(0,51,102,0.08);
}
```

**Outcome node:** solid colour bg, white text
```css
.outcome {
  padding: 8px 16px; border-radius: 10px; color: white; font-weight: 700;
  font-size: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
```

**Badge/label:** pill shape
```css
.annex-badge {
  background: #003366; color: white; padding: 5px 18px; border-radius: 20px;
  font-size: 12px; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase;
}
```

### Colour semantics for outcome nodes

| Severity | Hex | Use |
|---|---|---|
| Extreme (e.g. +200%) | `#9B1B30` | Deep red |
| High (e.g. +50%) | `#C0392B` | Red |
| Medium-high (e.g. +25%) | `#D4880F` | Amber |
| Medium (e.g. +15%) | `#B8860B` | Dark amber |
| Standard (e.g. +10%) | `#1874CD` | GTA blue |
| Special/complex | `#003366` | Navy |
| Exempt/none | `#1E8449` | Dark green (WCAG-safe on white text) |

Each colour variant needs matching: line colour, arrow border colour, tag text colour, and tag background (8% opacity version).

### Height estimation

| Element | Height (approx.) |
|---|---|
| Header (GTA branded) | 90-110px |
| Decision node + vertical connector | 80-100px per step |
| Branch section (fork + sub-tree) | 150-300px depending on depth |
| Notes section | 40-60px |
| Footer | 50-70px |

Calculate total before setting the card height. If content exceeds the format height, either compress spacing or increase the card height (accepting a non-standard aspect ratio).

## Quality Checklist

- [ ] PNG output at 4x scale factor (300+ DPI)
- [ ] All text readable at target display size (test at ~375px wide for mobile)
- [ ] Connectors aligned (no visual gaps between nodes and lines)
- [ ] Colour semantics consistent (same outcome type = same colour everywhere)
- [ ] Arrow heads visible and pointing in the correct direction
- [ ] If GTA branded: header icon, footer logo, Roboto font, #E8EEF5 bg, source caption
- [ ] No browser default styles leaking through
- [ ] NEVER use Read tool on output PNG files — use `file` and `ls -la` via Bash

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
