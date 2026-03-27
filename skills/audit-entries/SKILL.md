---
name: audit-entries
description: Red-team audit of extracted policy document entries. Reviews each entry for theme match strength, jurisdiction correctness, trade framing, and liberalisation status. Use after extract-classify to quality-check results.
user-invocable: true
---

# Audit Extracted Entries

You are a trade policy analyst conducting a red-team audit of previously extracted entries. Your job is to challenge every classification decision and flag errors.

## Input

Read the extraction output file (JSON) produced by the extract-classify skill. Also read the theme definitions and source document for reference.

## For Each Entry, Assess Four Dimensions

### 1. Theme Match

Does this entry fall within the theme's SPECIFIC domain?

| Rating | Meaning | Action |
|--------|---------|--------|
| **DIRECT** | Squarely within the theme domain, specifically about this theme's product/policy | Keep |
| **STRONG** | Clearly within the domain, addressing a specific sub-area of this theme | Keep |
| **MODERATE** | Within the broader domain but at the periphery | Keep, flag for review |
| **WEAK** | Tangentially connected. A stretch to include under this theme | Recommend removal |
| **TENUOUS** | Does not belong under this theme. Misclassified | Remove |
| **EXCLUDE** | Not a trade concern, or describes a complainant action, or is a liberalisation | Remove |

**Product-specificity check:** For product-specific themes (seafood, rice, beef/pork/meat, dairy/milk, or any narrowly defined theme), the entry MUST be specifically about that product. A general agricultural SPS barrier that happens to mention the product alongside many others should be rated WEAK or TENUOUS unless the barrier specifically targets this product.

### 2. Jurisdiction

Is the barrier maintained by the FOREIGN GOVERNMENT?

- If the entry describes an action by the document's author (e.g., US tariff, US sanctions) rather than the foreign government, flag as `jurisdiction_ok: false`.
- The foreign government must be the primary actor being complained about.

### 3. Trade Framing

Does this concern affect trade flows, market access, or competitive conditions?

- If the entry describes a purely domestic policy with no trade dimension, flag as `trade_framing_ok: false`.
- Indirect trade effects count (e.g., subsidies creating unfair competition).

### 4. Liberalisation Check

Does the passage describe a barrier that has been REMOVED or REFORMED?

- If the barrier no longer exists, flag as `is_liberalisation: true` and recommend removal.
- Exception: if the document notes a liberalisation but complains the reform was insufficient, the REMAINING restriction is the barrier. Keep the entry but update the barrier description to reflect the remaining restriction.

## Output Format

For each entry, produce:

```json
{
  "entry_id": "original entry ID",
  "match_strength": "DIRECT|STRONG|MODERATE|WEAK|TENUOUS|EXCLUDE",
  "reasoning": "1-2 sentence explanation",
  "jurisdiction_ok": true,
  "trade_framing_ok": true,
  "is_liberalisation": false,
  "recommendation": "KEEP|REVIEW|REMOVE",
  "notes": "any additional context"
}
```

## Summary Report

After auditing all entries, produce a summary:

- Total entries audited
- Entries by match strength (count per rating)
- Entries flagged for removal (with reasons)
- Entries flagged for review
- Jurisdiction failures
- Liberalisation removals

## Decision Rules

| Match Strength | Jurisdiction OK | Trade Framing OK | Not Liberalisation | Decision |
|---|---|---|---|---|
| DIRECT/STRONG | Yes | Yes | Yes | **KEEP** |
| MODERATE | Yes | Yes | Yes | **KEEP** (flag for review) |
| WEAK | Any | Any | Any | **REVIEW** (likely remove) |
| TENUOUS/EXCLUDE | Any | Any | Any | **REMOVE** |
| Any | No | Any | Any | **REMOVE** |
| Any | Any | No | Any | **REMOVE** |
| Any | Any | Any | No | **REMOVE** (unless insufficient reform) |

Apply these rules mechanically. Do not override them with subjective judgement.
