---
name: extract-classify
description: Classify a policy document against configurable themes, extracting trade barriers, state acts, and intervention types. Use when user says "classify this document", "extract trade barriers", "parse the NTE report", "map this report against themes", or "run the extraction". Not for general text analysis or summarisation.
---

# Policy Document Classification

## Critical: Before Starting

1. Locate the theme definitions file (`themes.json`) in the project directory
2. Locate the project config (`project-config.json`) — if missing, create from `${CLAUDE_PLUGIN_ROOT}/templates/`
3. Read both files before extracting anything

## Workflow

### Step 1: Load Configuration

- Read `themes.json` for theme definitions (theme_key, label, domain, keywords)
- Read `project-config.json` for inclusion/exclusion criteria and counting rules
- Confirm document path with the user

### Step 2: Process Section by Section

For each section (typically one country chapter):

1. Read the section text carefully
2. For each theme, identify passages describing barriers maintained by a foreign government
3. Apply inclusion criteria: barrier still in force, affects trade, foreign government is actor
4. Apply exclusion criteria: no complainant actions, no liberalisations (unless reform was insufficient), no keyword-only mentions
5. One entry = one distinct policy. Consolidate multiple quotes about the same policy. Different policies = separate entries.

### Step 3: For Each Finding, Output

```json
{
  "entry_id": "[COUNTRY]__[theme_key]__[NNN]",
  "theme_key": "...",
  "country": "...",
  "section": "document section name",
  "relevance_score": 1-5,
  "exact_quote": "verbatim from source (most informative passage)",
  "barrier_description": "what the barrier is (1-2 sentences)",
  "specific_measures": "laws, policies, regulations mentioned",
  "acting_government": "the foreign government",
  "state_acts": [
    {"name": "Named Law", "type": "named"},
    {"name": "unnamed practice description", "type": "unnamed"}
  ],
  "intervention_types": [
    {"mast": "I", "label": "Local content requirement", "confidence": "HIGH"}
  ],
  "match_strength": "DIRECT|STRONG|MODERATE|WEAK|TENUOUS",
  "notes": ""
}
```

For MAST classification, consult `${CLAUDE_PLUGIN_ROOT}/skills/extract-classify/references/mast-taxonomy.md`.
For counting methodology, consult `${CLAUDE_PLUGIN_ROOT}/skills/extract-classify/references/counting-rules.md`.

### Step 4: Self-Audit Each Entry

Before writing, verify each entry passes:
- **Theme match:** Is this SPECIFICALLY about this theme's domain? Product-specific themes require product-specific barriers.
- **Jurisdiction:** Is the foreign government the actor? Not the document's author.
- **Still in force:** Has this barrier been removed? Exclude unless reform was insufficient.
- **Quote exists:** Is the exact_quote actually verbatim from the source?

Flag entries with match_strength WEAK or TENUOUS for later review.

### Step 5: Validate Output

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/extract-classify/scripts/validate_output.py --input extractions.json`

If validation fails, fix the errors before proceeding.

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/extract-classify/scripts/count_entries.py --input extractions.json`

Report the summary to the user.

## Example

User says: "Classify the China section of the NTE against the 10 themes"

1. Read `themes.json` (10 themes loaded)
2. Read the China chapter from the source document
3. Process: find 50 entries across 4 themes (tech_discrimination, pharmaceutical_pricing, industrial_excess_capacity, forced_labor)
4. Write entries to `extractions.json`
5. Run `python ${CLAUDE_PLUGIN_ROOT}/skills/extract-classify/scripts/validate_output.py --input extractions.json` → VALID
6. Run `python ${CLAUDE_PLUGIN_ROOT}/skills/extract-classify/scripts/count_entries.py --input extractions.json` → report stats
7. Tell user: "Processed China: 50 entries across 4 themes. 29 named state acts, 21 unnamed."

## Troubleshooting

**Empty results for a section:** Check that your themes cover the document's topics. A report on digital governance won't match agricultural themes.

**Too many WEAK entries:** The theme domain descriptions may be too broad. Tighten the `domain` field in `themes.json` to be more specific about what's in/out.

**Quote verification failures:** Ensure exact_quote is truly verbatim. Do not paraphrase, truncate, or edit quotes from the source document.

## Performance Notes

- Process one country/section at a time, not the whole document at once
- Quality is more important than speed — read every sentence
- Do not skip validation steps
