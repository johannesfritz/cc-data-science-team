---
name: dedup-entries
description: Deduplicate extracted entries within each section-category pair. Merges entries describing the same underlying item and recalculates counts. Use when user says "deduplicate", "merge duplicates", "consolidate entries", or after extract-classify and audit-entries are complete.
---

# Deduplicate Entries

## Process

For each section-category pair (e.g., country-theme, chapter-topic) in the extraction file:

1. Read all entries for this pair
2. Identify clusters of entries describing the same underlying item:
   - Same document section + same topic → merge
   - Consecutive sentences about same item → merge
   - Different aspects of one item → merge
   - Genuinely different items → keep separate
   - **When in doubt, merge** (better to consolidate than double-count)
3. For each cluster, keep the most detailed entry and absorb content from others:
   - Combine unique quotes into `passages` array
   - Union all sub-classifications and labels
   - Deduplicate named items by name within each pair
   - Keep strongest match_strength and highest relevance_score
   - Add `_merged_from` field listing absorbed entry IDs
4. Recalculate counts per the counting rules in `project-config.json`

## Output

Write clusters as JSON, then update the extraction file:

```json
{
  "cluster_id": 0,
  "representative_entry_id": "keep this one",
  "merged_entry_ids": ["absorbed_1", "absorbed_2"],
  "consolidated_description": "brief description",
  "reasoning": "why these are the same item"
}
```

## After Dedup

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/dedup-entries/scripts/dedup_counts.py --before extractions.json --after extractions_deduped.json`

This compares before/after counts and reports which section-category pairs changed.

## Troubleshooting

**No duplicates found:** Normal for well-structured documents where each item appears in only one section.

**Over-merging:** If distinct items got merged, the category domain descriptions may be too broad. Split the merged entry back and tighten category definitions.
