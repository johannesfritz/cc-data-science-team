---
description: "Adversarial verification of analytical deliverables before publication"
---

Adversarial verification of analytical deliverables before publication.

Usage: /red-team <project-folder>
Example: /red-team countermeasures
Example: /red-team sgept-analytics/eu-tariff-barrier-estimates/results/countermeasures

## What This Command Does

Invoke the `red-team-analysis` skill to aggressively verify analytical work:

1. **Quantitative Attack (❌ BLOCKING)** - Recalculate headline metrics from source data
2. **Consistency Tests (❌ BLOCKING)** - Verify component sums match totals
3. **Code Audit (⚠️/❌)** - Search for silent failure patterns
4. **Interpretation Review (⚠️ WARNING)** - Identify tenuous claims

## Attack Philosophy

> "Assume the analysis contains errors until proven otherwise."

This is NOT a friendly review. The red-team:
- Finds what's wrong, not what's right
- Breaks the analysis, doesn't validate it
- Questions every number, doesn't accept them
- Challenges interpretations, doesn't rubber-stamp

## Verification Process

### Phase 1: Recalculate Headline Metrics

For each published number:
1. Load raw data
2. Re-run aggregation logic
3. Compare to published value
4. Flag if difference >0.1%

### Phase 2: Internal Consistency

| Test | Pass Criteria |
|------|---------------|
| Member state totals = EU total | ±1% |
| Wave totals = Grand total | ±1% |
| Sector totals = Grand total | ±1% |
| Affected + Unaffected = 100% | ±0.5% |

### Phase 3: Code Audit

Search for these anti-patterns:
```r
coalesce(x, 0)      # Hiding NA with zeros
left_join(a, b)     # Without row count check
x / y               # Without zero guard
filter(condition)   # Without validation
```

### Phase 4: Interpretation Review

Flag tenuous claims:
- Estimates presented as facts
- Static analysis without behavioural response caveat
- Correlation implied as causation

## Output Format

```
🔴 Red-Team Report: EU Countermeasures Chartbook

Date: 2026-01-26
Status: ✅ APPROVED / ⚠️ CONDITIONAL / ❌ BLOCKED

Quantitative Verification:
| Metric | Published | Verified | Status |
| Total products | 6,458 | 6,458 | ✅ |
| Affected value | 110.0 bn | 110.02 bn | ✅ |
| TW rate | 24.04% | 24.04% | ✅ |

Consistency Tests:
| Test | Diff | Status |
| MS sum = EU | 0.02% | ✅ |
| Waves = Total | 0.00% | ✅ |

Code Audit: 2 findings (0 HIGH, 2 LOW)
Tenuous Claims: 1 identified

Overall: APPROVED
- 0 blocking issues
- 2 warnings addressed
```

## When to Use

- **MANDATORY** before publishing high-stakes deliverables
- Before chartbook/report finalisation
- After major methodology changes
- When analyst-orchestrator marks "complete"

## Implementation

1. Use the red-team-analytics agent for coordinated attacks
2. Run R verification scripts in sandbox
3. Generate red_team_report.md in results folder
4. Escalate blocking issues to analyst

## Escalation Rules

| Finding | Action |
|---------|--------|
| Arithmetic error | ❌ BLOCK - must fix |
| Consistency >1% | ❌ BLOCK - must investigate |
| HIGH severity code issue | ❌ BLOCK - must fix |
| Missing caveat | ⚠️ Add caveat |
| Tenuous claim | ⚠️ Soften language |
