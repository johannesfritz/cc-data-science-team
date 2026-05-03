---
name: red-team-analysis
description: Adversarial verification of analytical deliverables before publication. Recalculates headline metrics from source data, tests internal consistency, audits code for silent failures, and identifies tenuous claims. Use before publishing any chartbook, report, or policy brief; after major changes to data or methodology; when stakes are high (press release, client delivery, academic submission); or when analyst-orchestrator marks "complete".
allowed-tools: Read, Grep, Glob, Bash, Task
model: sonnet
---

# Red-Team Analysis Skill

Aggressively verify analytical deliverables before publication.

## Usage

```
/red-team <project-folder>
/red-team eu-tariff-barrier-estimates/results/countermeasures
/red-team sgept-analytics/data-queries/240115-trade-analysis
```

## What It Does

### Phase 1: Quantitative Attack (BLOCKING)

Recalculates headline metrics from source data:
1. Load raw data files
2. Re-run aggregation logic
3. Compare to published figures
4. Flag any discrepancy >0.1%

### Phase 2: Consistency Tests (BLOCKING)

Verifies internal consistency:
1. Component sums = totals (±1%)
2. Category sums = 100% (±0.5%)
3. Cross-checks between tables

### Phase 3: Code Audit (WARNING/BLOCKING)

Searches for failure patterns:
- `coalesce(x, 0)` hiding missing data
- Joins without row count validation
- Division without zero guards
- Filters without validation

### Phase 4: Interpretation Review (WARNING)

Identifies tenuous claims:
- Overclaiming (evidence vs claim strength)
- Missing caveats (static analysis, data limitations)
- Alternative interpretations not acknowledged

## Implementation

### Step 1: Identify Project Files

```bash
# Find analysis code
Glob: {project}/code/*.R

# Find results
Glob: {project}/results/*.csv
Glob: {project}/results/*.xlsx

# Find data
Glob: {project}/data/*.csv
Glob: {project}/data/*.Rdata
```

### Step 2: Extract Headline Metrics

Read the analysis output files and identify:
- Total counts (products, interventions, etc.)
- Value totals (trade value, revenue, etc.)
- Calculated rates (trade-weighted, effective, etc.)
- Percentage shares

### Step 3: Recalculate from Source

For each headline metric:
1. Read the source data
2. Apply the calculation logic
3. Compare to published value
4. Log PASS/FAIL

Example verification:
```r
# Verify trade-weighted rate
tw_rate_check <- raw_data %>%
  filter(cn8 %in% countermeasures$cn8) %>%
  summarise(
    tw_rate = sum(value * rate, na.rm = TRUE) / sum(value, na.rm = TRUE)
  )

# Compare to published
published_rate <- 24.04
calculated_rate <- tw_rate_check$tw_rate * 100
diff_pct <- abs(published_rate - calculated_rate) / published_rate * 100

if (diff_pct > 0.1) {
  stop(paste("FAIL: TW rate mismatch:", published_rate, "vs", round(calculated_rate, 2)))
}
```

### Step 4: Run Consistency Tests

```r
# Test: Member state totals = EU total
ms_sum <- sum(ms_data$affected_value)
eu_total <- exec_summary$total_affected
diff <- abs(ms_sum - eu_total) / eu_total * 100

if (diff > 1) {
  stop(paste("FAIL: MS sum differs from EU total by", round(diff, 2), "%"))
}
```

### Step 5: Audit Code Patterns

```bash
# Search for dangerous patterns
Grep: "coalesce.*0" -g "*.R" {project}/code/
Grep: "left_join" -g "*.R" {project}/code/
Grep: "\\s/\\s" -g "*.R" {project}/code/
```

### Step 6: Generate Report

Save to: `{project}/results/red_team_report.md`

```markdown
## Red-Team Report: [Project Name]

**Date:** YYYY-MM-DD
**Status:** ✅ APPROVED / ⚠️ CONDITIONAL / ❌ BLOCKED

### Quantitative Verification

| Metric | Published | Verified | Diff | Status |
|--------|-----------|----------|------|--------|
| Total products | 6,458 | 6,458 | 0.0% | ✅ |
| Affected value (bn) | 110.0 | 110.02 | 0.02% | ✅ |
| Trade-weighted rate | 24.04% | 24.04% | 0.0% | ✅ |

### Consistency Tests

| Test | Expected | Actual | Diff | Status |
|------|----------|--------|------|--------|
| MS sum = EU | 110.0 | 109.98 | 0.02% | ✅ |
| Waves sum = Total | 110.0 | 110.0 | 0.0% | ✅ |

### Code Audit

| Pattern | Location | Severity | Action |
|---------|----------|----------|--------|
| coalesce(x, 0) | data_prep.R:136 | LOW | Documented |

### Tenuous Claims

| Claim | Issue | Recommendation |
|-------|-------|----------------|
| "Effective tariff hike of 8.1%" | Static analysis | Add caveat about behavioral response |

### Approval Status

- [x] All arithmetic checks pass
- [x] All consistency checks pass
- [ ] Code audit issues addressed
- [ ] Tenuous claims have caveats
```

## Gate Severity

| Gate | Failure Action |
|------|----------------|
| Quantitative (>0.1% diff) | ❌ BLOCK |
| Consistency (>1% diff) | ❌ BLOCK |
| Code audit (HIGH severity) | ❌ BLOCK |
| Code audit (MED severity) | ⚠️ Document |
| Tenuous claims | ⚠️ Add caveat |

## Integration

- **analyst-orchestrator**: Invoke before Stage 4 (Output)
- **analytics-readiness-check**: Run red-team first, then readiness check
- **statistical-reviewer**: Coordinate for magnitude/direction checks

## Files Generated

- `results/red_team_report.md` - Full red-team report
- Console output with PASS/FAIL for each check

## Error Prevention

This skill prevents:
- Publishing incorrect headline numbers
- Internal inconsistencies that destroy credibility
- Silent data quality issues
- Overclaiming without caveats
