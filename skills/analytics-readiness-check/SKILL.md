---
name: analytics-readiness-check
description: Run quality gates for analytical deliverables before delivery. Use when analyst-orchestrator marks analysis complete, before generating Word/PDF documents, or when user asks to review a deliverable. Verifies chart-text consistency, statistical sanity, data source documentation, terminology precision, and visual quality.
allowed-tools: Read, Grep, Glob, Bash
model: haiku
---

# Analytics Readiness Check Skill

Run quality gates for analytical deliverables before delivery.

## Usage

```
/analytics-ready <project-folder>
/analytics-ready 2601-fittings
/analytics-ready "251117 AAL TD/2601-fittings"
```

## Quality Gates

### Gate 1: Chart-Text Verification (CRITICAL - BLOCKING)

**The most important gate.** Text that contradicts its chart destroys credibility.

For EVERY chart with accompanying text:

1. **Identify all claims** in captions and surrounding text:
   - Rankings ("X is the dominant supplier")
   - Numbers ("grew 27% year-over-year")
   - Comparisons ("followed by Y and Z")

2. **Query the underlying data** to verify:
```r
# Verification query template
data %>%
  group_by(category) %>%
  summarise(total = sum(value, na.rm = TRUE)) %>%
  arrange(desc(total)) %>%
  head(10)
```

3. **Compare text to data and chart visual**:
   - Text claim matches data? ✓/✗
   - Chart visual matches data? ✓/✗
   - Text matches chart visual? ✓/✗

4. **Multi-product check**: For analyses covering multiple products, verify EACH product separately. NEVER assume patterns are the same across products.

**Failure example:**
- Chart shows: Switzerland #1, China #4
- Text says: "China is the dominant supplier"
- Status: ❌ BLOCKING - must fix before delivery

### Gate 2: Statistical Sanity (BLOCKING)

- [ ] Magnitudes plausible (billions not trillions)
- [ ] Signs/directions correct
- [ ] Percentages between 0-100%
- [ ] Year-over-year calculations make sense

### Gate 3: Data Source Documentation (WARNING)

- [ ] HS code digit level stated (6-digit for international comparisons)
- [ ] Data source cited (Trade Data Monitor, GTA)
- [ ] Time period clearly stated
- [ ] Caveats noted (data limitations, classification uncertainty)

### Gate 4: Terminology Precision (WARNING)

- [ ] "EU imports" vs "EU member state imports" - use correct terminology
- [ ] Value/quantity/price specified for every quantitative claim
- [ ] British English spelling

### Gate 5: Visual Quality (WARNING)

- [ ] All axes labeled with units
- [ ] Legends present where needed
- [ ] Charts readable at document size
- [ ] No orphaned captions

## Gate Severity

| Gate | Severity | Action |
|------|----------|--------|
| Chart-Text Verification | ❌ BLOCKING | Must fix before delivery |
| Statistical Sanity | ❌ BLOCKING | Must fix before delivery |
| Data Source Documentation | ⚠️ WARNING | Should fix, not blocking |
| Terminology Precision | ⚠️ WARNING | Should fix, not blocking |
| Visual Quality | ⚠️ WARNING | Should fix, not blocking |

## Implementation

### Step 1: Load Project Context

```bash
# Read the deliverable markdown file
Read: {project}/results/*.md

# List all charts
Glob: {project}/pics/*.png
```

### Step 2: Extract Claims from Text

For each chart reference in the markdown:
1. Find the caption/surrounding text
2. Extract quantitative claims
3. Log claims for verification

### Step 3: Verify Each Claim

For each claim:
1. Identify the data source (which CSV/Excel file?)
2. Run verification query
3. Compare result to claim
4. Log pass/fail

### Step 4: Generate Report

```markdown
## Analytics Readiness Report

**Project:** {project_name}
**Date:** {date}

### Gate Results

❌ Chart-Text Verification: FAILED
   - Plastic fittings chart: Text claims "China dominates" but Switzerland is #1
   - Action: Rewrite caption to match data

✅ Statistical Sanity: PASSED
   - All magnitudes plausible
   - Directions correct

⚠️ Data Source Documentation: WARNING
   - HS digit level not stated in methodology
   - Add: "Data collected at 6-digit HS level"

✅ Terminology Precision: PASSED
✅ Visual Quality: PASSED

### Overall Status

**NOT READY** - 1 blocking issue (Chart-Text Verification)

### Required Actions

1. Fix caption for plastic fittings chart (BLOCKING)
2. Add HS digit level to methodology (recommended)

### Verification Queries Run

| Chart | Claim | Data Result | Status |
|-------|-------|-------------|--------|
| extra_eu_plastic.png | "China dominates" | Switzerland #1 ($863M), China #4 ($418M) | ❌ FAIL |
| extra_eu_copper.png | "China dominates" | China #1 ($1,264M) | ✅ PASS |
```

## Error Prevention

This skill prevents the **most embarrassing class of errors**:
- Text saying one thing, chart showing another
- Rankings that don't match the data
- Copy-paste errors from previous analyses

## Integration

- **analyst-orchestrator**: Invoke this skill before Stage 4 (Output)
- **statistical-reviewer**: Uses this skill's verification protocol
- **fact-checker**: Treats charts as internal sources to verify

## Files to Check

For each project:
1. `results/*.md` - Deliverable text
2. `pics/*.png` - Charts
3. `data/*.csv` or `data/*.xlsx` - Source data
4. `code/*.R` - Scripts that generated outputs

## Proactive Invocation

Suggest this skill when:
1. User says "analysis is complete" or "ready to deliver"
2. Word/PDF document is about to be generated
3. analyst-orchestrator reaches Stage 4
4. User asks to review the deliverable
