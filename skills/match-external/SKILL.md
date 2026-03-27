---
name: match-external
description: Match extracted entries against an external database to attach IDs and flag coverage gaps. Works with any MCP-accessible source or a local reference file. Use when user says "match against DPA", "attach GTA IDs", "link to our database", "find coverage gaps", or "which entries are already in our system". Not for comparing two documents — use compare-documents instead.
---

# Match External

Match extracted entries against an external reference source to attach identifiers, assess coverage, and flag gaps.

## Critical: Never Invent IDs

If uncertain about a match, return candidates with rationale. Never fabricate an external ID. Mark uncertain matches as PROBABLE and queue them for human review.

## Process

### Step 1: Configure the External Source

The user must specify one of:
- **MCP server** — name of a connected MCP server with search/lookup tools
- **Reference file** — a local CSV/JSON file with the reference dataset

Read the project config for source details. If not specified, ask the user.

### Step 2: For Each Entry, Search and Match

For each extracted entry:

1. Construct a search query from the entry's description, section, and category
2. Query the external source (MCP tool or file search)
3. Evaluate candidates against the entry

### Step 3: Classify Match Quality

| Match Type | Condition | Action |
|---|---|---|
| **EXACT** | Single candidate clearly matches. Same entity, same scope. | Attach ID. |
| **PROBABLE** | Best candidate is likely correct but not certain. | Attach ID + flag for review. |
| **AMBIGUOUS** | Multiple plausible candidates, can't determine best. | List top 3 candidates with rationale. Queue for human review. |
| **NO_MATCH** | No relevant candidates found in external source. | Mark as coverage gap. |
| **RETRIEVAL_FAILURE** | Query failed (MCP error, timeout, rate limit). | Mark as failed. Retry later. |

### Step 4: Separate Gap Types

When an entry has NO_MATCH, distinguish:
- **Genuine gap** — the topic exists but the external DB doesn't cover it → queue for DB expansion
- **Out of scope** — the topic is outside the external DB's domain → expected, not a gap
- **Phrasing mismatch** — the topic may exist under different terminology → try alternative queries

### Step 5: Run Match Statistics

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/match-external/scripts/match_summary.py --input match_results.json`

Report match rates by section, category, and match type.

## Output Format

```json
{
  "entry_id": "original entry ID",
  "external_id": "matched ID or null",
  "match_type": "EXACT|PROBABLE|AMBIGUOUS|NO_MATCH|RETRIEVAL_FAILURE",
  "confidence": 0.0-1.0,
  "rationale": "why this match was chosen",
  "candidates": [
    {"id": "candidate_1", "score": 0.95, "title": "..."},
    {"id": "candidate_2", "score": 0.72, "title": "..."}
  ],
  "gap_type": "genuine_gap|out_of_scope|phrasing_mismatch|null"
}
```

## Troubleshooting

**Low match rates (<50%):** Check that the external source covers the same domain. If the extraction covers digital policy but the DB focuses on tariffs, low match rates are expected.

**Many AMBIGUOUS matches:** The search queries may be too broad. Use more specific terms from the entry's description. Or the external source may have overlapping entries.

**RETRIEVAL_FAILURE spikes:** Check MCP server connectivity. Rate limits may require batching with pauses.
