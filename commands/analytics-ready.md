Run quality gates for analytical deliverables before delivery.

Usage: /analytics-ready <project-folder>
Example: /analytics-ready 2601-fittings
Example: /analytics-ready "251117 AAL TD/2601-fittings"

## What This Command Does

Invoke the `analytics-readiness-check` skill to run 5 quality gates:

1. **Chart-Text Verification (❌ BLOCKING)** - Every chart caption verified against underlying data
2. **Statistical Sanity (❌ BLOCKING)** - Magnitudes, signs, percentages plausible
3. **Data Source Documentation (⚠️ WARNING)** - HS digit level, sources, caveats stated
4. **Terminology Precision (⚠️ WARNING)** - EU member state imports, value/qty/price specified
5. **Visual Quality (⚠️ WARNING)** - Labels, legends, readability

## Critical Gate: Chart-Text Verification

This gate catches the most embarrassing class of errors: **text that contradicts its chart**.

For multi-product analyses, EACH product must be verified separately. Never assume patterns are the same.

### Verification Process

1. Extract all quantitative claims from text
2. Run data queries to verify actual rankings/values
3. Compare text claims to data results
4. Flag any discrepancies as BLOCKING

### Example Failure

```
Chart shows: Switzerland #1 ($863M), China #4 ($418M)
Text says: "China is the dominant supplier"
Status: ❌ BLOCKING - must fix before delivery
```

## Output Format

```
📊 Analytics Readiness Report

Project: 2601-fittings
Date: 2026-01-15

Gate Results:
❌ Chart-Text Verification: FAILED (1 discrepancy)
✅ Statistical Sanity: PASSED
⚠️ Data Source Documentation: Missing HS digit level
✅ Terminology Precision: PASSED
✅ Visual Quality: PASSED

Overall: NOT READY
- 1 blocking issue (Chart-Text)
- 1 warning (Data Source)

Required Actions:
1. Fix plastic fittings caption (BLOCKING)
2. Add HS digit level to methodology
```

## When to Use

- Before delivering any analytical report
- After generating charts and writing captions
- Before generating final Word/PDF documents
- When analyst-orchestrator marks "Analysis complete"

## Implementation

Use the Task tool with the statistical-reviewer agent to run verification queries, then generate the report.
