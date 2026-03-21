# Statistical Sanity Protocol

**Purpose:** Mandatory quality checks before approving analytical results from `jf-thought/sgept-analytics/data-queries/` projects.

---

## The "Laugh Test"

Before approving any analysis, apply these checks:

### 1. MAGNITUDE
Does this number make sense?
- Trade values should be in billions (not trillions)
- Country interventions typically 10-500/year
- Global trade ~$20-25 trillion/year

### 2. SIGN
Is the direction correct?
- Tariff increase → imports decrease
- Subsidy → exports increase
- Ban → trade volume → 0

### 3. PROPORTION
Are percentages reasonable?
- All values 0-100% (unless growth rates)
- Shares sum to 100%
- No negative percentages (unless declines)

### 4. HISTORICAL
Does this align with known patterns?
- 2020 = COVID disruption (not normal)
- 2018-2019 = US-China trade war
- 2008-2009 = Financial crisis

### 5. BENCHMARK
How does this compare to official sources?
- WTO trade statistics
- IMF Direction of Trade
- UN Comtrade
- Accept ±10% variance as normal

---

## Required Data Checks

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Row count | ±10% of expected | Investigate source |
| Missing values | >20% in key columns | Document or impute |
| Duplicate keys | 0 duplicates | Deduplicate with logic |
| Date ranges | No unexpected gaps | Document gaps |
| Outliers | >3× IQR | Review individually |

---

## Review Verdict Options

- **✅ APPROVED** - All checks pass, results are plausible
- **⚠️ CONCERNS** - Minor issues, document and proceed with caution
- **❌ REJECTED** - Major issues, must fix before delivery

---

## Remember

> "If the results don't pass the laugh test, they're wrong—even if the code runs perfectly."

Reject any analysis that:
- Has implausible magnitudes
- Shows wrong directional effects
- Contains unexplained outliers
- Contradicts known historical patterns
