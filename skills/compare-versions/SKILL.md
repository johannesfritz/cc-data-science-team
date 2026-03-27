---
name: compare-versions
description: Compare two editions of the same document to find additions, removals, and changes at the entry level. Use when user says "compare NTE25 to NTE26", "what changed between versions", "diff these reports", "is digital becoming more important", or when tracking evolution of a recurring publication. Not for comparing different documents — use compare-documents instead.
---

# Compare Versions

Compare two extraction datasets from different editions of the same document to identify what is new, removed, changed, or unchanged.

## Critical: Requirements

Both versions must be extracted using the same tagging schema (same `themes.json`). If schemas differ, align them first.

Input:
- `v1_extractions.json` — earlier version
- `v2_extractions.json` — later version
- Both must follow the same output structure

## Process

### Step 1: Align Entry Keys

For each entry, construct a normalisation key from:
- `section` (country/chapter name, normalised to uppercase)
- `theme_key`
- First 100 characters of `description` (or `barrier_description`), normalised

Entries with identical keys across versions are candidates for UNCHANGED or CHANGED. Entries in v2 only are NEW. Entries in v1 only are REMOVED.

### Step 2: Classify Each Entry

| Status | Condition |
|--------|-----------|
| **NEW** | Entry key exists in v2 but not v1 |
| **REMOVED** | Entry key exists in v1 but not v2 |
| **CHANGED** | Key matches but content differs (description, quote, or sub-classifications) |
| **UNCHANGED** | Key matches and content is substantively identical |

For CHANGED entries, summarise:
- What specifically changed (wording, scope, severity, new details)
- Whether the change represents strengthening, weakening, or neutral rewording

### Step 3: Produce Statistics

Report:
- Total entries: v1 count vs v2 count
- NEW / REMOVED / CHANGED / UNCHANGED counts
- By category: which themes gained or lost entries?
- By section: which sections changed most?
- For "is X becoming more important?": compare absolute counts AND share of total

### Step 4: Run Deterministic Diff

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/compare-versions/scripts/diff_versions.py --v1 v1_extractions.json --v2 v2_extractions.json`

This produces a structured diff table and summary.

## Example

User says: "Compare NTE25 digital entries to NTE26 — is digital becoming more important?"

1. Load NTE25 extraction (filtered to digital themes) and NTE26 extraction (same themes)
2. Align by country + theme_key
3. Find: 45 entries in NTE25, 62 in NTE26. 17 NEW, 3 REMOVED, 8 CHANGED, 37 UNCHANGED.
4. Report: "Digital entries grew 38%. tech_discrimination expanded from 18 to 27 countries. DSTs stable. 3 countries dropped (liberalisation)."

## Troubleshooting

**Different schemas:** If v1 used different theme definitions than v2, alignment will fail. Extract both versions with the same schema, or map themes explicitly before comparing.

**Key collisions:** If normalisation is too aggressive, distinct entries may appear to match. Tighten the key (use more characters from description) if false UNCHANGED rates are high.
