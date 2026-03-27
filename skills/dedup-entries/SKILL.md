---
name: dedup-entries
description: Deduplicate extracted entries within each country-theme pair. Merges entries that describe the same underlying trade concern. Use after extract-classify (and optionally after audit-entries) to consolidate the dataset.
user-invocable: true
---

# Deduplicate Extracted Entries

You are a trade policy analyst deduplicating a catalogue of trade concerns. Multiple extraction passes or overlapping document sections may produce entries that describe the same underlying barrier. Your job is to identify and merge these.

## Input

Read the extraction output file (JSON). Process one country-theme pair at a time.

## Merging Rules

For entries within a SINGLE COUNTRY under a SINGLE THEME:

| Condition | Decision |
|-----------|----------|
| Entries from the same document section about the same topic | **MERGE** |
| Entries quoting consecutive sentences about the same policy | **MERGE** |
| Different aspects of one law or regulation | **MERGE** |
| Same policy described at different levels of detail | **MERGE** (keep the more detailed version) |
| Genuinely different policies or sectors | **KEEP SEPARATE** |
| Same named law under different themes | **KEEP SEPARATE** (each theme gets its own entry) |

**When in doubt, merge.** It is better to consolidate than to double-count.

## Process

For each country-theme pair:

1. **Read all entries** for this country-theme combination.
2. **Identify clusters** of entries describing the same underlying concern.
3. **For each cluster**, select a representative entry and merge information from the others:
   - Keep the most detailed `barrier_description`
   - Combine all unique `exact_quote` passages
   - Union all `state_acts` (deduplicate named acts by name)
   - Union all `intervention_types`
   - Keep the strongest `match_strength`
   - Keep the highest `relevance_score`
4. **Record the merge** for transparency.

## Output Format

For each cluster, produce:

```json
{
  "cluster_id": 0,
  "representative_entry_id": "the entry ID to keep",
  "merged_entry_ids": ["entry_1", "entry_2", "entry_3"],
  "consolidated_barrier": "brief description of the consolidated barrier",
  "reasoning": "why these entries describe the same concern"
}
```

Then update the extraction file:
- Replace merged entries with a single consolidated entry
- Add a `_merged_from` field listing the original entry IDs
- Combine `exact_quote` fields from all merged entries into a `passages` array

## Named Act Deduplication

Within each country-theme pair, named state acts are deduplicated by instrument name:
- If "Cybersecurity Law" appears in two separate entries for China under tech_discrimination, it counts once in the consolidated entry.
- Unnamed acts are NOT deduplicated (no unique identifier exists).

After dedup, recalculate:
- `unique_named`: count of distinct named act names
- `unnamed`: count of unnamed act instances
- `total_state_acts`: unique_named + unnamed

## Summary Report

After processing all country-theme pairs, report:
- Total entries before dedup
- Total entries after dedup
- Number of merges performed
- Country-theme pairs affected
- Largest cluster (most entries merged)
