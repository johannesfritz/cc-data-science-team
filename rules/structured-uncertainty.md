# Structured Uncertainty Taxonomy (analytical claims)

**Applies to:** `analyst`, `extractor`, `comparator`, `matcher`, and `red-team-analytics` agents. Skills that emit analytical claims (`extract-classify`, `match-external`, `compare-versions`).

**Origin:** DRIL methodology (NBER w35188, §3.2 — "Data Quality Mechanisms"). Adapted from `cc-gta-monitoring/rules/structured-uncertainty.md` for the analytical-claim surface. JCC-972.

**Relationship to existing rules.** This rule is orthogonal to the existing `match_strength ∈ {DIRECT, STRONG, MODERATE, WEAK, TENUOUS}` taxonomy in `extract-classify` and `match-external`. `match_strength` measures *match quality* (how well the extraction fits the source); this rule measures *epistemic provenance* (how the value was derived in the first place). A claim may be `match_strength=STRONG` and `status=inferred` simultaneously: the value was inferred from indirect evidence, and the inference is well-supported by the source.

## Why a taxonomy

The data-science team's published outputs (chartbooks, reports, policy briefs) carry analytical claims that range from "directly observed in the data" to "inferred from a model" to "could not be determined." Today, the analyst agent's rule that "every claim cites a row" answers WHERE the claim came from but not HOW it was derived. A claim that "Brazil's tariff equivalent rose 4.2 percentage points between 2020 and 2024" reads identically whether the 4.2 number is (a) directly computed from clean trade data, (b) imputed from a partial year, (c) inferred via a model with assumed parameters, or (d) a proxy because the underlying series is missing for one of the years.

The DRIL taxonomy makes those four cases legible to the reader.

## The enum

Every non-trivial analytical claim emitted to a published artifact (Excel results, PNG charts, markdown narrative) MUST carry a `status` from:

| Status | Meaning | Analytical example |
|---|---|---|
| `answered` | Value was directly computed from observed data using a documented method. | Sum of HS-6 tariff coverage across all jurisdictions, computed from the canonical join in `code/03_aggregate.R`. |
| `not_found_after_search` | The agent searched for the data and could not assemble it from qualifying inputs. | A country's industrial-policy spending number where no qualifying source publishes it, despite a documented check of the gov budget annex and OECD reporting. |
| `not_applicable` | The variable does not apply to this unit. | Subsidy-tier classification for a country with no subsidy interventions in the period. |
| `proxy_used` | The reported value is a substitute measure for the variable of interest. | Coding GDP-weighted tariff rates when trade-weighted are not available for the jurisdiction-year. |
| `inferred` | The value is derived from indirect evidence or model output rather than direct observation. | A counterfactual trade flow under a removed measure; a year-end imputation from quarterly data; a model-estimated price elasticity. |
| `conflict_unresolved` | Two qualifying sources disagree and the conflict has not been adjudicated. | A budget figure where the ministry annual report and the OECD data report different numbers, and the methodology note does not pick one. |

The status applies to *the claim*, not to the row, the dataset, or the chart. A single chart may aggregate `answered` values for some countries and `proxy_used` values for others; the legend should declare the mix.

## How agents apply it

### analyst (claim-writing)

Every empirical claim in narrative prose must point to a row + carry a status. Pattern:

```markdown
Brazil's tariff coverage rose 4.2pp between 2020 and 2024
[row: results/brazil-tariffs.csv:23 | status: answered].
```

For shorthand in publication-ready prose where the bracketed reference is too noisy, move the status references to a footnote and keep narrative clean. The audit trail must still resolve every empirical claim to a row-status pair.

### extractor (LLM-extracted entries)

When `extract-classify` produces structured entries, each non-trivial extracted field carries a `field_status` (separate from `match_strength`):

```jsonc
{
  "doc_id": "EU-2024-001",
  "scope": "data protection",
  "amount_usd": 50000000,
  "field_status": {
    "amount_usd": "inferred",
    "scope": "answered"
  },
  "match_strength": "STRONG"
}
```

Omitted fields are implicit `answered`.

### matcher (external-DB linking)

When `match-external` returns a link verdict, the matcher records the status of the linked value as well as the existing match-strength:

```jsonc
{
  "entry_id": "...",
  "external_id": "ISIC-1234",
  "match_strength": "MODERATE",
  "field_status": "proxy_used",   // the matched code is the closest broader category
  "note": "ISIC-1234 is the parent of the desired sub-class; no sub-class available"
}
```

### red-team-analytics (audit)

The red-team agent's existing Layer 1 (extraction audit) and Layer 5 (LLM verification) extend to status discipline. Findings:

- A claim tagged `answered` whose row does not contain the value → critical finding.
- A claim tagged `inferred` without an analyst comment explaining the inference → important finding.
- A claim tagged `conflict_unresolved` not flagged in the prose to the reader → critical finding.
- A claim missing a status (silent absence) → important finding.

## What this is NOT

- Not a replacement for `match_strength`. The two coexist. `match_strength` describes the quality of an extraction; `status` describes the epistemology of the resulting value.
- Not a confidence interval. `inferred` is "derived from indirect evidence", not "uncertain at 50% confidence." If a claim has a confidence interval, that's a separate field; the status taxonomy is categorical.
- Not applied to trivial structural fields. Row IDs, ISO codes, schema scaffolding — these are populated by the schema, not by interpretive work.
- Not applied to intermediate calculations. The status is on the *published claim*, not every line of intermediate R code.

## Downstream uses

- **Publication-readiness review** (`/analytics-ready`) filters on `status != answered` to surface claims needing extra scrutiny.
- **Chart legends** declare the mix of statuses across data points where the mix is material to interpretation.
- **Replication packages** preserve the status map so a downstream user can reproduce the analysis with knowledge of which values are direct and which are inferred.

## Verification

A passing project satisfies all of:

1. Every empirical claim in the published prose has a resolvable row + status pair.
2. Charts whose data points carry mixed statuses declare the mix in the legend.
3. Red-team-analytics Layer 1 verifies that recorded statuses match the underlying data; mismatches block publication.
