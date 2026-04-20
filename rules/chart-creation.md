---
paths:
  - sgept-analytics/**
  - "*/data-queries/**"
  - "**/*.R"
  - "**/*.py"
---

# Chart Creation Standards

## Pre-Creation (BLOCKING)

Before creating ANY chart, read `.claude/protocols/data-visualization.md` for:

1. **Product variant** — determine GTA Publication vs SGEPT Analytical Product (see variant table)
2. **GTA Visual Identity template** — cowplot composition, #E8EEF5 background, navy top bar, vertical alignment principle, manual legends, source caption, logo placement
3. **Knaflic principles** — chart type selection, decluttering, attention hierarchy, anti-patterns
4. **Reference implementations** — study an existing chart in the codebase before coding

## Tool Selection

| Context | Tool | Why |
|---------|------|-----|
| GTA-branded publication charts | R + ggplot2 + cowplot | GTA VI template is built for cowplot |
| SGEPT analytical products | Python matplotlib OK | Scenario monitors, briefing charts, LinkedIn visuals |
| Exploratory / quick look | Python matplotlib OK | Not for publication |
| Interactive dashboards | Shiny / Plotly | Different workflow |
| Flowcharts, decision trees, process maps | HTML/CSS + Playwright | `diagram-generator` skill |

**Default to R for GTA-branded publication charts.** Python/matplotlib is acceptable for:
- SGEPT analytical products (scenario monitors, briefing charts, LinkedIn visuals)
- Time-series line charts where cowplot composition adds no value
- Projects with an existing Python `.venv`

When using Python for publication, follow the SGEPT Analytical Product variant in `data-visualization.md`.

## Mandatory Elements (GTA VI)

Every **GTA-branded** publication chart must have (SGEPT products follow the variant table in `data-visualization.md`):

- [ ] **Light blue background** (#E8EEF5)
- [ ] **Bold statement title** (finding, not description)
- [ ] **Grey subtitle** (what the data shows)
- [ ] **Manual legend** (draw_line + draw_label, not ggplot legend)
- [ ] **Vertical alignment** (title, subtitle, legend, y-axis, source share LEFT_X)
- [ ] **Source caption** (bottom-left)
- [ ] **No chart border, no gridlines** (or minimal)
- [ ] **Bold ISO/category labels** on Y-axis
- [ ] **Y-axis on the right** (for horizontal bars)
- [ ] **Both desktop and mobile versions** (see dimensions below)

## Output Dimensions

| Format | Ratio | Size | Pixels at 300 DPI | Use |
|--------|-------|------|--------------------|-----|
| Desktop | ~3:2 | 10×6.8" | 3000×2040 | Reports, presentations |
| GTA desktop | ~12:7 | 12×7" | 3600×2100 | GTA website |
| Mobile / LinkedIn | 4:5 | 7.2×9.0" | 2160×2700 | Social media, mobile feeds |

All outputs at **300 DPI**.

## Anti-Patterns (BLOCKING)

- Using `labs(title=...)` for publication charts (use cowplot draw_label)
- White background on GTA-branded charts (use #E8EEF5; white is correct for SGEPT products)
- ggplot default legend (use manual line segments)
- Rainbow colour palette (use grey + strategic colour, or GTA palette)
- Python matplotlib for GTA-branded charts (use R + cowplot; Python is fine for SGEPT products)
