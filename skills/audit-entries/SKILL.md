---
name: audit-entries
description: Red-team review of extracted policy document entries. Checks theme match strength, jurisdiction, trade framing, and liberalisation status. Use when user says "audit the extractions", "review the entries", "quality check", or "red-team the results". Not for initial extraction — use extract-classify first.
---

# Audit Extracted Entries

## Critical: Read These First

1. The extraction output file (JSON)
2. The theme definitions file (`themes.json`)
3. The source document (for quote verification)

## For Each Entry, Assess

| Dimension | Question | Fail Condition |
|-----------|----------|----------------|
| **Theme match** | Is this SPECIFICALLY about this theme's domain? | WEAK or TENUOUS → recommend removal |
| **Jurisdiction** | Is the foreign government the actor? | Describes complainant's own action → remove |
| **Trade framing** | Does this affect trade flows or market access? | Purely domestic policy → remove |
| **Liberalisation** | Has the barrier been removed? | Barrier no longer exists → remove (unless reform insufficient) |

### Match Strength Ratings

- **DIRECT:** Squarely within the theme domain
- **STRONG:** Clearly within, addressing a sub-area
- **MODERATE:** Within the broader domain but peripheral
- **WEAK:** Tangentially connected — likely remove
- **TENUOUS:** Misclassified — remove
- **EXCLUDE:** Not a trade concern at all — remove

### Product-Specificity Rule

For narrow themes (seafood, rice, dairy, etc.): the barrier must SPECIFICALLY target that product. A general SPS barrier mentioning the product alongside others = WEAK at best.

## Output

Write audit results as JSON:

```json
{
  "entry_id": "original ID",
  "match_strength": "DIRECT",
  "reasoning": "1-2 sentences",
  "jurisdiction_ok": true,
  "trade_framing_ok": true,
  "is_liberalisation": false,
  "recommendation": "KEEP|REVIEW|REMOVE"
}
```

## Decision Rules (Mechanical)

- DIRECT/STRONG + all checks pass → **KEEP**
- MODERATE + all checks pass → **KEEP** (flag for review)
- WEAK → **REVIEW** (likely remove)
- TENUOUS/EXCLUDE → **REMOVE**
- Any check fails (jurisdiction, trade framing, liberalisation) → **REMOVE**

## After Auditing

Run: `python ${CLAUDE_PLUGIN_ROOT}/skills/audit-entries/scripts/audit_summary.py --input audit_results.json`

Present the summary. Ask the user to decide on REVIEW entries.

## Troubleshooting

**Too many removals (>30%):** The extraction may have been too aggressive. Check if theme domain descriptions are too broad.

**Jurisdiction confusion:** In bilateral trade disputes, both sides may be described. The barrier is the foreign government's action, not the document author's response.
