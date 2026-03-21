# Data Visualization Protocol

**Source:** Cole Nussbaumer Knaflic, *Storytelling with Data: A Data Visualization Guide for Business Professionals* (2015)

**Purpose:** Ensure charts COMMUNICATE effectively, not just display data correctly. The existing visualization-reviewer.md checks whether charts are *technically correct* (labels, resolution, accessibility); this protocol checks whether they *tell a story* and *guide the audience to action*.

---

## The Core Problem

> "There is a story in your data. But your tools don't know what that story is."

Charts often fail not because they are technically wrong, but because they:
- Show data without guiding attention to what matters
- Include clutter that distracts from the message
- Use chart types poorly suited to the data
- Present information without context or call to action
- Leave the audience wondering "so what?"

---

## The Six Core Questions

Before creating ANY chart, ask these six questions:

### 1. CONTEXT: Who is the audience and what should they DO?

**The problem:** Visualizations created without clear audience and purpose tend to show everything without highlighting anything. The audience is left to find meaning on their own.

**Ask:**
- Who is the specific audience for this chart?
- What do they already know? What do they need to know?
- What action should they take after seeing this?
- What is the single most important thing to communicate?

**The 3-minute story test:** Can you tell this story in 3 minutes? Can you tell it in 1 sentence?

---

### 2. SELECTION: Is this the right chart type?

**The problem:** Choosing chart types by habit or software defaults rather than by what the data requires. Bar charts for time series. Pie charts for comparisons. Lines for categories.

**Chart Selection Guide:**

| Data Type | Recommended | Why | Avoid |
|-----------|-------------|-----|-------|
| **Single number** | Text callout | Charts add noise | Any chart |
| **Few values (2-5)** | Simple table | Direct reading | Complex visuals |
| **Trends over time** | Line graph | Shows continuity | Bar chart |
| **Category comparison** | Horizontal bar | Easy label reading | Vertical bar (usually) |
| **Part-to-whole** | Horizontal stacked bar | Shows both parts and total | Pie/donut charts |
| **Two points in time** | Slopegraph | Shows change directly | Line graph |
| **Correlation** | Scatterplot | Shows relationship | Bar chart |

**The chart type decision tree:**
```
Is it a single number? → Text callout
Is it comparing categories? → Horizontal bar
Is it showing change over time? → Line graph
Is it part of a whole? → Horizontal stacked bar
Is it showing relationship? → Scatterplot
```

---

### 3. CLUTTER: Is every pixel earning its place?

**The problem:** Default chart settings include borders, gridlines, markers, legends, and other elements that add visual noise without adding information. Clutter is a barrier between your audience and your data.

**The data-ink ratio:** Maximize the share of ink devoted to data. Every non-data element should be questioned.

**The 6-step decluttering process:**

| Step | Remove/Reduce | Before | After |
|------|---------------|--------|-------|
| 1 | Chart border | Box around chart | No border |
| 2 | Gridlines | Dark gridlines | Light grey or none |
| 3 | Data markers | Points on every value | Points only at key moments |
| 4 | Axis labels | "1,234,567.89" | "1.2M" |
| 5 | Legend | Separate legend box | Label data directly |
| 6 | Colour | Rainbow palette | Grey baseline + strategic colour |

**Gestalt principles to leverage:**
- **Proximity:** Group related elements
- **Similarity:** Use consistent encoding
- **Enclosure:** Lightly shade related areas
- **Connection:** Lines connect related points
- **Continuity:** Align elements to create flow

---

### 4. ATTENTION: Does the eye go where it should?

**The problem:** When everything is emphasized, nothing is. Charts need visual hierarchy to guide attention to what matters.

**Preattentive attributes** (processed in milliseconds):

| Attribute | Use For | Example |
|-----------|---------|---------|
| **Colour intensity** | Highlighting key data | One blue bar, rest grey |
| **Colour hue** | Categories (sparingly) | Max 3-4 distinct colours |
| **Size** | Importance or magnitude | Larger = more important |
| **Position** | Primary comparison | Left-to-right, top-to-bottom |
| **Bold text** | Key labels | Bold the punchline |

**The squint test:** Squint at your chart. What stands out? Is that what should stand out?

**Strategic colour hierarchy:**
```
Grey = baseline, context, supporting data
Colour = the story, the exception, what matters
```

---

### 5. DESIGN: Would a designer approve this?

**The problem:** Charts are often created by analysts, not designers. Basic design principles improve comprehension.

**Designer thinking:**

| Principle | Application |
|-----------|-------------|
| **Affordances** | Make interactive elements look clickable |
| **Accessibility** | Colorblind-safe, WCAG contrast, alt text |
| **Aesthetics** | Clean, professional, intentional whitespace |
| **Alignment** | Create visual order through alignment |
| **Consistency** | Same encoding throughout |

**Text hierarchy:**
- Title: What is this about?
- Subtitle: The key insight
- Axis labels: What is being measured
- Annotations: Guide interpretation
- Source: Data provenance

---

### 6. STORY: Does this tell a story, not just show data?

**The problem:** Data presentations often show data without narrative structure. The audience sees numbers but not meaning.

**Story structure for data:**

| Element | Purpose | Example |
|---------|---------|---------|
| **Beginning** | Set context, introduce characters | "Last year, we set a goal..." |
| **Middle** | Build tension, show conflict | "But Q3 results showed..." |
| **End** | Resolution, call to action | "To hit our target, we need to..." |

**Narrative arc questions:**
- What is the setting? (Context)
- Who is the main character? (Data focus)
- What is the conflict? (The problem or opportunity)
- What is the resolution? (Recommendation)

**The "so what?" test:** After every chart, the audience should know what to do or think differently. If they're left asking "so what?", the visualization fails.

---

## Anti-Patterns (BLOCKING)

These patterns are serious enough to reject a chart:

| Anti-Pattern | Problem | Alternative |
|--------------|---------|-------------|
| **Pie chart** | Humans struggle with angles | Horizontal bar chart |
| **Donut chart** | Worse than pie (less area) | Horizontal bar chart |
| **3D effects** | Distorts perception | 2D only, always |
| **Secondary y-axis** | Confusing, easily manipulated | Two separate charts |
| **Non-zero baseline (bars)** | Visually exaggerates differences | Start bars at zero |
| **Truncated axis (bars)** | Misleading proportion | Start at zero |
| **Rainbow colour palette** | No visual hierarchy | Strategic colour |
| **Chart junk** | Distracts from data | Remove decorations |
| **Spaghetti graph** | Too many lines | Small multiples or highlight one |

**The dark background exception:** Knaflic's only non-negotiable: "I rarely use dark backgrounds." Dark backgrounds reduce legibility and should be avoided unless specifically required for presentation context.

---

## Checklist for Visualization Review

### Before Creating

- [ ] CONTEXT: I know my audience and the action they should take
- [ ] CONTEXT: I can tell this story in one sentence
- [ ] SELECTION: I have chosen the right chart type for this data

### During Creation

- [ ] CLUTTER: I have removed the chart border
- [ ] CLUTTER: I have lightened or removed gridlines
- [ ] CLUTTER: I have removed unnecessary data markers
- [ ] CLUTTER: I have simplified axis labels
- [ ] CLUTTER: I have labelled data directly (not using legend where possible)
- [ ] ATTENTION: I am using grey as baseline, colour strategically
- [ ] ATTENTION: The squint test shows the right thing emphasized
- [ ] ALIGNMENT: Title, subtitle, legend, y-axis, and source share one vertical edge (horizontal bar charts)

### After Creation

- [ ] DESIGN: Text hierarchy is clear (title → subtitle → labels → annotations)
- [ ] DESIGN: Chart is colorblind-safe
- [ ] STORY: There is a clear narrative arc
- [ ] STORY: The audience will know what to do
- [ ] ANTI-PATTERNS: No pie charts, no 3D, no secondary y-axis, bars start at zero

---

## The "Big Idea" Framework

For executive presentations, distill to one sentence:

> **[Subject] + [What it should do] + [Why it matters]**

Example: "Proposed budget **reallocates marketing spend** to drive **23% more qualified leads** without increasing total spend."

This becomes your title and organizing principle.

---

## Common Mistakes Catalogue

| Mistake | Example | Knaflic Fix |
|---------|---------|-------------|
| **Data dump** | "Here's everything" | Focus on one message |
| **Exploratory as explanatory** | Dashboard for presentation | Choose the insight to highlight |
| **Passive title** | "Q3 Sales Data" | Active: "Q3 sales exceeded target by 12%" |
| **Legend instead of labels** | Separate legend box | Label data directly on chart |
| **Default colours** | Excel rainbow | Grey + one strategic colour |
| **Pie for comparison** | Pie chart with 8 slices | Horizontal bar chart |
| **No clear takeaway** | "Here's what happened" | "Here's what we should do" |
| **Too much text** | Paragraphs on slides | Visuals + spoken words |
| **Cluttered axes** | "1,234,567.89" | "1.2M" |

---

## GTA Visual Identity

All GTA-published charts follow a branded template using **cowplot composition** (not just ggplot). The chart area, title, legend, decorative bar, source caption, and logo are assembled externally via `cowplot::ggdraw()`.

### Typography

**Typeface:** Roboto (Google Fonts, variable weight). Install via `sysfonts::font_add_google("Roboto")` in R or `matplotlib.font_manager` in Python.

| Weight | Use |
|--------|-----|
| Roboto Medium (500) | Titles, endpoint labels, legend headers |
| Roboto Light (300) | Subtitles, body text, axis labels, source captions |

### Template Elements

| Element | Specification |
|---------|---------------|
| **Top bar** | Full-width edge-to-edge dark navy (#003366) horizontal rule, 3pt, x = c(0, 1) |
| **Title** | ~24pt bold, black (#1a1a2e), below top bar |
| **Subtitle** | ~11pt grey, below title |
| **Legend** | Manual line segments + labels, positioned below subtitle |
| **Y-axis** | On the RIGHT (especially for percentage charts) |
| **X-axis** | Dark line at bottom (grey30) |
| **Gridlines** | Horizontal only, light grey (#grey85), no vertical |
| **Background** | Light blue #E8EEF5 throughout |
| **Source** | "Source: Global Trade Alert", bottom-left, 9pt grey |
| **Logo** | GTA Logo Color light.png, bottom-right |

### Vertical Alignment Principle

**One vertical alignment edge runs from title to source.** Title, subtitle, legend keys, the y-axis (bar origin), and source caption should all share the same left x-coordinate. Country or category labels sit to the left of this line; bars and data extend to the right. This creates a calm, structured chart with a clear visual through-line.

**When to use:** Horizontal bar charts, grouped bars, stacked bars, and any chart where the y-axis can serve as the alignment spine. Most GTA charts qualify.

**When it does not apply:** Line charts, scatterplots, or charts where the y-axis is numerical and the x-axis carries categories (vertical bars). In those cases, align title/subtitle/source to the plot area's left edge instead.

**Implementation:** Build the canvas manually with `ggdraw()` instead of `gta_wrap()`. Define a shared `LEFT_X` constant and place all left-edge elements at that coordinate. Calibrate `plot.margin.left` in the inner ggplot so the y-axis falls at `LEFT_X` in canvas coordinates.

```r
# Layout constants — all left-edge elements share LEFT_X
LEFT_X <- 0.07          # desktop (12" wide)
# LEFT_X <- 0.12        # portrait (7" wide)

# Calibrate: at 12" * 72pt/in = 864pt, LEFT_X = 0.07 → 60.5pt.
# ISO codes at size 11 bold ≈ 24pt + margin ≈ 5pt = 29pt.
# plot.margin.left = 60.5 - 29 ≈ 32pt.
MARGIN_LEFT <- 32

p_inner <- ggplot(...) +
  theme(plot.margin = margin(t = 2, r = 10, b = 2, l = MARGIN_LEFT, unit = "pt"))

p <- ggdraw() +
  draw_label(title,   x = LEFT_X, y = 0.965, hjust = 0, ...) +
  draw_label(subtitle, x = LEFT_X, y = 0.925, hjust = 0, ...) +
  draw_line(x = c(LEFT_X, LEFT_X + 0.06), y = c(0.875, 0.875), ...) +
  draw_plot(p_inner, x = 0, y = 0.07, width = 1, height = 0.76) +
  draw_label(source,  x = LEFT_X, y = 0.025, hjust = 0, ...)
```

**Reference implementation:** `code/s232_deal_caps/chart_s232_vs_ieepa.R`

### GTA Logo

Located at: `jf-ceo/sgept-backoffice/assets/gta-logos/`
- Light backgrounds: `GTA Logo Color light.png`
- Dark backgrounds: `GTA Logo Color dark.png`

### GTA Colour Palette

| Name | Hex | Use |
|------|-----|-----|
| Navy | #003366 | Top bar, emphasis lines, primary series |
| Light blue | #6BAED6 | Secondary lines, context series |
| Equity stake | #1f77b4 | Blue data series |
| Debt purchase | #2ca02c | Green data series |
| State loan | #ff7f0e | Orange data series |
| Loan guarantee | #d62728 | Red data series |
| Financial grant | #9467bd | Purple data series |
| Neutral grey | #D3D3D3 | De-emphasis, context bars |
| Background | #E8EEF5 | Chart background |
| Text dark | #1a1a2e | Titles |

### Reference Implementation

See `r-code-standards.md` for the full R code template. Working example: `sgept-analytics/TL/260126-sc-launch-pieces/code/chart_intermediary_actions.R`.

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `labs(title=...)` for publication charts | Use `cowplot::draw_label()` externally |
| Y-axis on the left | Set `scale_y_continuous(position = "right")` |
| Legend via ggplot | Use `draw_line()` + `draw_label()` in cowplot |
| Missing GTA logo | Add via `draw_image()` bottom-right |
| Missing navy top bar | Add via `draw_line(x = c(0, 1), y = c(0.96, 0.96))` edge-to-edge |
| Title with line break | Keep title on single line; use subtitle for context |
| White background (GTA template) | Use `bg = "#E8EEF5"` in ggsave and `fill = "#E8EEF5"` in theme. White is correct for SGEPT products. |

### Product Variants

Not all publication charts are GTA-branded. SGEPT analytical products (scenario monitors, briefing charts, LinkedIn visuals) use a lighter template.

| Element | GTA Publication | SGEPT Analytical Product |
|---------|----------------|--------------------------|
| Background | #E8EEF5 light blue | White |
| Top bar | Navy #003366, full-width | None |
| Logo | GTA logo, bottom-right | None (or SGEPT wordmark) |
| Font | Roboto | Roboto |
| Composition | cowplot `ggdraw()` | matplotlib fig/ax or cowplot |
| Source caption | "Source: Global Trade Alert" | "Source: SGEPT [Product Name]" |
| Colour palette | GTA palette | GTA palette (strategic assignment) |

**When to use which:** If the chart will appear on the GTA website, in a GTA report, or under the GTA brand → use GTA Publication template. If the chart is for SGEPT briefings, LinkedIn posts, scenario monitors, or consulting deliverables → use SGEPT Analytical Product template.

### Strategic Line Hierarchy Palette

For line charts with strategic colour assignment (e.g. scenario monitors, trend comparisons), use this sub-palette. Colours are drawn from the GTA palette but assigned by narrative weight, not data category.

| Role | Hex | Name |
|------|-----|------|
| Dominant / alarming | #B6242E | GTA Red |
| Important / hope | #1874CD | GTA Primary Blue |
| Warning / rising | #C87F0F | GTA Amber |
| Neutral / declining | #379293 | GTA Teal |
| Background / minor | #9A9A9A | GTA Grey |

The standard GTA palette (navy, light blue, intervention-type colours) remains the default for bar charts and category-based visuals.

---

## Integration with Existing Protocols

This protocol EXTENDS, not replaces, existing quality gates:

| Protocol | Focus | Knaflic Adds |
|----------|-------|--------------|
| **visualization-reviewer.md** | Is the chart TECHNICALLY correct? | Does it COMMUNICATE effectively? |
| **statistical-communication.md** | Are the statistics MEANINGFUL? | Is the visual GUIDING attention? |
| **analytical-balance.md** | Both sides presented? | Clear narrative with call to action? |

**Sequence:** First verify correctness (visualization-reviewer), then verify communication (this protocol).

---

## The Three Types of Communication

| Type | Purpose | Tools |
|------|---------|-------|
| **Live presentation** | Persuade, explain | Slides + spoken narrative |
| **Written document** | Record, reference | Report with embedded visuals |
| **Dashboard** | Monitor, explore | Interactive, self-service |

**Critical distinction:** Exploratory analysis (finding insights) requires different tools than explanatory communication (sharing insights). Don't use exploratory dashboards for explanatory presentations.

---

## References

- Knaflic, C.N. (2015). *Storytelling with Data: A Data Visualization Guide for Business Professionals*. Wiley.
- Tufte, E. (1983). *The Visual Display of Quantitative Information*. Graphics Press.
- Few, S. (2012). *Show Me the Numbers*. Analytics Press.
