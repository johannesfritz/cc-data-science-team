# Counting Rules

## Named vs Unnamed State Acts

- **Named instruments:** Explicitly named laws, regulations, decrees, or orders cited in the document. Deduplicated by name within each country-theme pair. If the same statute appears in two passages under the same country and theme, it counts once.
- **Unnamed practices:** Informal barriers cited without a legal name. Counted as invocations — not deduplicated (no unique identifier).
- **total_state_acts** = unique_named + unnamed (per country-theme pair)

## Why This Matters

Named measures are directly actionable in trade investigations — a specific statute can be challenged. Unnamed practices require further investigation to identify the legal instrument. The distinction between "named" and "unnamed" is a proxy for legal readiness.

## Deduplication Scope

Deduplication happens WITHIN each country-theme pair, not across them. The same law appearing under two different themes for the same country counts once per theme.

## MAST Intervention Invocations

Intervention types are a property of the barrier, not the state act. One entry can have multiple MAST chapters. Count intervention_types as invocations (not deduplicated), since the same MAST chapter applied to different barriers represents distinct trade concerns.
