---
name: discover-themes
description: Read a policy document and propose classification themes based on its own internal taxonomy. Use when user says "what themes does this document use", "propose categories", "identify the taxonomy", "what should I classify against", or before starting extract-classify when the right themes are unknown. Not for documents where themes are already defined.
---

# Discover Themes

Analyse a policy document to identify its internal taxonomy and propose classification themes before extraction begins.

## Why This Matters

Documents often have their own analytical framework that differs from what an analyst would assume. The S301 overcapacity investigation used a two-layer taxonomy (evidentiary indicators vs policy interventions) that wasn't obvious until the document's Background section was read carefully. Starting extraction with wrong themes wastes time and produces unreliable results.

## Process

### Step 1: Read the document structure

Read the table of contents, executive summary, background/methodology sections, and introduction. These typically reveal the document's own categories.

Look for:
- **Explicit taxonomy** — numbered lists of investigation themes, policy areas, or allegation types
- **Implicit structure** — recurring section headings across country chapters
- **Nested layers** — some documents have two levels (e.g., evidence types vs policy causes, or policy areas vs instrument types)

### Step 2: Extract candidate themes

For each category the document uses, extract:
- A proposed `theme_key` (snake_case)
- A `label` (human-readable)
- The document's own description of the category scope (verbatim if possible)
- Whether the category is hierarchical (parent → child)

### Step 3: Assess classification feasibility

For each candidate theme, assess:
- **Coverage** — does the document discuss this theme for multiple countries/entities? (If only mentioned once, it may not warrant a separate theme)
- **Distinctness** — is this theme clearly separable from other themes? (Overlapping themes cause double-counting)
- **Specificity** — is the boundary clear enough to code reliably? (Vague themes produce inconsistent results)

### Step 4: Propose a themes file

Write a draft `themes.json` following the template at `${CLAUDE_PLUGIN_ROOT}/templates/themes-template.json`.

For each theme, the `domain` field is critical — it must explicitly state what is IN scope and OUT of scope. Use the document's own language where possible.

### Step 5: Present to the user for review

Show the proposed themes and ask:
- Do these match what you expect?
- Should any be merged, split, or removed?
- Is the level of granularity right?

Do NOT proceed to extraction until the user approves the themes.

## Example

User provides a USTR S301 overcapacity investigation PDF.

1. Read Background section (pp. 3-8) → discover two-layer taxonomy:
   - **Layer 1 (evidence indicators):** trade surplus, capacity utilisation, sector overcapacity, zombie firms
   - **Layer 2 (policy interventions):** production/export promotion, wage suppression, SOE activities, market access barriers, lax standards, subsidised lending, currency practices
2. Propose 11 themes (4 evidence + 7 policy), noting that Layer 2 themes are causes while Layer 1 are symptoms
3. User approves, but merges zombie firms into capacity utilisation → 10 final themes

## Common Patterns

| Document Type | Typical Taxonomy |
|---|---|
| NTE Report | Country chapters × policy areas (trade barriers, IP, services, investment) |
| S301 Investigation | Allegation categories (two layers: evidence + policy) |
| WTO Trade Policy Review | Sectors × instrument types |
| EU TBR Complaint | Barrier types × affected products |
| Subsidy catalogue | Sectors × subsidy instruments |

## Troubleshooting

**Document has no clear taxonomy:** Some documents are narrative, not structured. In this case, propose themes based on the recurring topics you observe across sections. Flag this to the user — analyst-derived themes need more validation than document-derived ones.

**Taxonomy is too granular:** If the document has 30+ categories, group them into 8-12 broader themes for practical classification. Note which sub-categories map to each theme.

**Two-layer taxonomy:** When the document separates symptoms from causes (or effects from instruments), keep both layers. They answer different questions.
