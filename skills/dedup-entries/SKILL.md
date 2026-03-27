---
name: dedup-entries
description: Deduplicate extracted entries within each country-theme pair. Merges entries describing the same underlying trade concern and recalculates state act counts. Use when user says "deduplicate", "merge duplicates", "consolidate entries", or after extract-classify and audit-entries are complete.
---

# Deduplicate Entries

## Process

For each country-theme pair in the extraction file:

1. Read all entries for this pair
2. Identify clusters of entries describing the same barrier:
   - Same document section + same topic → merge
   - Consecutive sentences about same policy → merge
   - Different aspects of one law → merge
   - Different policies/sectors → keep separate
   - **When in doubt, merge** (better to consolidate than double-count)
3. For each cluster, keep the most detailed entry and absorb content from others:
   - Combine unique quotes into `passages` array
   - Union state acts (deduplicate named acts by name)
   - Union intervention types
   - Keep strongest match_strength and highest relevance_score
   - Add `_merged_from` field listing absorbed entry IDs
4. Recalculate counts:
   - `unique_named` = count of distinct named act names in the pair
   - `unnamed` = count of unnamed act instances
   - `total_state_acts` = unique_named + unnamed

## Output

Write clusters as JSON, then update the extraction file:

```json
{
  "cluster_id": 0,
  "representative_entry_id": "keep this one",
  "merged_entry_ids": ["absorbed_1", "absorbed_2"],
  "consolidated_barrier": "brief description",
  "reasoning": "why these are the same concern"
}
```

## After Dedup

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/dedup-entries/scripts/dedup_counts.py --before extractions.json --after extractions_deduped.json`

This compares before/after counts and reports which country-theme pairs changed.

## Troubleshooting

**No duplicates found:** This is normal for well-structured documents where each policy appears in only one section. The NTE report sometimes discusses the same law in multiple sub-sections, which is where dedup matters.

**Over-merging:** If distinct policies got merged, the theme domain descriptions may be too broad, causing different barriers to look similar. Split the merged entry back and tighten theme definitions.
