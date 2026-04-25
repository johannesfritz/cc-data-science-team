# CSS design patterns for structured diagrams

Reference snippets for the diagram-generator skill. Pull what you need; you don't have to use the whole catalogue. The goal is CSS-only diagrams (no SVG) — easier to edit, render reliably across browsers, and re-style for different colour schemes.

## Layouts

### Vertical spine with horizontal exits (decision trees)

3-column CSS Grid where the decision node is centred and exits branch to one side:

```css
.row {
  display: grid;
  grid-template-columns: 1fr 320px 1fr;
  align-items: center;
}
/* Column 1: empty | Column 2: decision node | Column 3: exit outcome */
```

## Connectors (CSS-only, no SVG)

### Vertical line

```css
.v-line { width: 2.5px; height: 20px; background: #003366; border-radius: 1px; }
```

### Arrow head (down)

```css
.arrow-down {
  width: 0; height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 7px solid #003366;
}
```

### Horizontal arm with right-pointing arrow

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

### Fork/split (inverted T)

```css
.split-fork { display: flex; flex-direction: column; align-items: center; }
.v-stem { width: 2.5px; height: 14px; background: #003366; }
.h-bar { height: 2.5px; background: #003366; align-self: stretch; margin: 0 160px; }
```

## Node styles

### Decision node (white bg, navy border, rounded, shadow)

```css
.decision-box {
  background: white; border: 2.5px solid #003366; border-radius: 10px;
  padding: 12px 20px; text-align: center; font-size: 15px; font-weight: 500;
  color: #1a1a2e; box-shadow: 0 2px 8px rgba(0,51,102,0.08);
}
```

### Outcome node (solid colour bg, white text)

```css
.outcome {
  padding: 8px 16px; border-radius: 10px; color: white; font-weight: 700;
  font-size: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
```

### Badge/label (pill shape)

```css
.annex-badge {
  background: #003366; color: white; padding: 5px 18px; border-radius: 20px;
  font-size: 12px; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase;
}
```

## Colour semantics for outcome nodes

| Severity | Hex | Use |
|---|---|---|
| Extreme (e.g. +200%) | `#9B1B30` | Deep red |
| High (e.g. +50%) | `#C0392B` | Red |
| Medium-high (e.g. +25%) | `#D4880F` | Amber |
| Medium (e.g. +15%) | `#B8860B` | Dark amber |
| Standard (e.g. +10%) | `#1874CD` | GTA blue |
| Special/complex | `#003366` | Navy |
| Exempt/none | `#1E8449` | Dark green (WCAG-safe with white text) |

Each colour variant needs matching: line colour, arrow border colour, tag text colour, and tag background (8% opacity version).

## Height estimation

Use these to pre-calculate the card height before rendering — saves an iteration when content overflows.

| Element | Height (approx.) |
|---|---|
| Header (GTA branded) | 90-110px |
| Decision node + vertical connector | 80-100px per step |
| Branch section (fork + sub-tree) | 150-300px depending on depth |
| Notes section | 40-60px |
| Footer | 50-70px |

If content exceeds the format height, either compress spacing or increase the card height (accepting a non-standard aspect ratio).
