---
name: extract-classify
description: Classify a structured document against a user-defined tagging schema. Extracts labelled passages section by section, with self-audit and deterministic verification. Use when user says "classify this document", "tag these sections", "extract and label", "parse this report against my schema", or "run the extraction". Not for general summarisation.
---

# Document Classification

## Critical: Before Starting

1. Locate the **tagging schema** (`themes.json`) — defines what categories to look for and how to recognise them
2. Locate the **project config** (`project-config.json`) — defines inclusion/exclusion criteria, output fields, and audit dimensions
3. If either is missing, help the user create them from `${CLAUDE_PLUGIN_ROOT}/templates/`
4. For a working trade-policy example, see `${CLAUDE_PLUGIN_ROOT}/examples/nte-2025-themes.json`

## Workflow

### Step 1: Load Configuration

- Read `themes.json` for category definitions (theme_key, label, domain, keywords)
- Read `project-config.json` for:
  - **Inclusion criteria** — what qualifies as a match
  - **Exclusion criteria** — what to filter out
  - **Output fields** — what to extract per entry (the schema is user-defined, not fixed)
  - **Audit dimensions** — what to self-check before writing each entry

### Step 2: Process Section by Section

For each document section:

1. Read the section text carefully
2. For each theme/category, identify passages matching the category's `domain` definition
3. Apply inclusion criteria from project config
4. Apply exclusion criteria from project config
5. One entry = one distinct item matching the unit of analysis defined in the config. Consolidate multiple passages about the same item. Different items = separate entries.

### Step 3: For Each Finding, Output

Write entries using the field structure defined in `project-config.json`. The minimum required fields are:

```json
{
  "entry_id": "[SECTION]__[theme_key]__[NNN]",
  "theme_key": "category key from themes.json",
  "section": "document section this came from",
  "exact_quote": "verbatim from source text",
  "description": "what was found (1-2 sentences)",
  "match_strength": "DIRECT|STRONG|MODERATE|WEAK|TENUOUS"
}
```

Additional fields (e.g., named entities, sub-classifications, actor identification) are defined per-project in the config. Consult the project config's `output_fields` section and any referenced taxonomy files.

### Step 4: Self-Audit Each Entry

Before writing, verify each entry against the audit dimensions defined in `project-config.json`. Common dimensions include:

- **Category match** — does this entry fall within the theme's specific domain?
- **Actor/direction** — is the correct actor or direction identified? (configurable per project)
- **Currency** — is the finding still current/valid? (configurable per project)
- **Quote fidelity** — is the exact_quote truly verbatim?

Flag entries with match_strength WEAK or TENUOUS for later review.

### Step 5: Validate Output

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/extract-classify/scripts/validate_output.py --input extractions.json`

If validation fails, fix the errors before proceeding.

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/extract-classify/scripts/count_entries.py --input extractions.json`

Report the summary to the user.

### Step 6: Verify Quotes Against Source

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/extract-classify/scripts/verify_quotes.py --extractions extractions.json --source data/document.md`

This checks every extracted quote against the source text using 5-tier fuzzy matching (EXACT → PHRASE_ALL → PHRASE_PARTIAL → PHRASE_WEAK → NOT_FOUND). Fix any NOT_FOUND quotes before proceeding.

### Step 7: Verify Aggregation Integrity

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/extract-classify/scripts/verify_aggregations.py --input extractions.json`

This checks that counts are consistent across hierarchy levels. Fix any failures before delivering results.

## Example

User provides a trade policy report with 10 themes defined in `themes.json`:

1. Read themes (10 categories loaded)
2. Read the China chapter from the source document
3. Process: find 50 entries across 4 themes
4. Write entries to `extractions.json`
5. Run validation → VALID
6. Run quote verification → all 50 quotes matched
7. Report: "Processed China: 50 entries across 4 themes."

## Troubleshooting

**Empty results for a section:** Check that your themes cover the document's topics. Categories defined for one domain won't match content from another.

**Too many WEAK entries:** The category `domain` descriptions may be too broad. Tighten the `domain` field in `themes.json` to be more specific about what's in/out.

**Quote verification failures:** Ensure exact_quote is truly verbatim. Do not paraphrase, truncate, or edit quotes from the source document.

## Performance Notes

- Process one section at a time, not the whole document at once
- Quality is more important than speed — read every sentence
- Do not skip validation steps
