---
name: audit-entries
description: Red-team review of extracted entries against user-defined audit dimensions. Checks category match, configurable quality criteria, and flags entries for removal or review. Use when user says "audit the extractions", "review the entries", "quality check", or "red-team the results". Not for initial extraction — use extract-classify first.
---

# Audit Extracted Entries

## Critical: Read These First

1. The extraction output file (JSON)
2. The tagging schema (`themes.json`)
3. The project config (`project-config.json`) — especially `audit_dimensions`
4. The source document (for quote verification)

## Audit Dimensions

Read `project-config.json` for the project's audit dimensions. If none are defined, use these defaults:

| Dimension | Question | Fail Condition |
|-----------|----------|----------------|
| **Category match** | Is this SPECIFICALLY about this theme's domain? | WEAK or TENUOUS → recommend removal |
| **Quote fidelity** | Is the exact_quote truly verbatim from the source? | Paraphrased or truncated → fix or remove |

Projects may define additional dimensions. For trade policy projects, common additions include jurisdiction checks, currency/validity checks, and liberalisation filters. These are configured per-project, not built into this skill.

## Match Strength Ratings

- **DIRECT:** Squarely within the category domain
- **STRONG:** Clearly within, addressing a sub-area
- **MODERATE:** Within the broader domain but peripheral
- **WEAK:** Tangentially connected — likely remove
- **TENUOUS:** Misclassified — remove
- **EXCLUDE:** Does not belong at all — remove

### Specificity Rule

For narrow categories: the entry must SPECIFICALLY match that category's domain. A broad passage that mentions the category topic alongside other topics = WEAK at best, unless the passage specifically targets this category.

## Output

Write audit results as JSON:

```json
{
  "entry_id": "original ID",
  "match_strength": "DIRECT",
  "reasoning": "1-2 sentences",
  "dimension_results": {
    "category_match": true,
    "quote_fidelity": true
  },
  "recommendation": "KEEP|REVIEW|REMOVE"
}
```

The `dimension_results` object contains one boolean per audit dimension defined in the project config.

## Decision Rules (Mechanical)

- DIRECT/STRONG + all dimensions pass → **KEEP**
- MODERATE + all dimensions pass → **KEEP** (flag for review)
- WEAK → **REVIEW** (likely remove)
- TENUOUS/EXCLUDE → **REMOVE**
- Any dimension fails → **REMOVE**

Apply these rules mechanically. Do not override them with subjective judgement.

## After Auditing

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/audit-entries/scripts/audit_summary.py --input audit_results.json`

Present the summary. Ask the user to decide on REVIEW entries.

## Troubleshooting

**Too many removals (>30%):** The extraction may have been too aggressive. Check if category domain descriptions are too broad.

**Audit dimensions not defined:** If `project-config.json` has no `audit_dimensions`, default to category match + quote fidelity only. Ask the user if they want additional checks.
