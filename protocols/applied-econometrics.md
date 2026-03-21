# Applied Econometrics Protocol

**Source:** Peter Kennedy, *A Guide to Econometrics*, 6th ed. (2008), Chapter 22

**Purpose:** Ensure regression analyses are methodologically sound. The existing statistical-sanity.md checks whether numbers are *correct*; this protocol checks whether the *analysis itself* is well-designed.

---

## The Core Problem

> "Don't do econometrics as thou sayest thy prayers. Think about what you're doing."

Even correct calculations can produce meaningless results if:
- The model is poorly specified
- Data quality is ignored
- Results are mined for significance
- Statistical and economic significance are confused
- Sensitivity is hidden rather than reported

---

## The Ten Commandments

### 1. Use common sense and economic theory

**Corollary:** Don't do econometrics as thou sayest thy prayers.

**In practice:**
- Match per capita with per capita, real with real
- Use appropriate functional forms (log-log for elasticities)
- Let theory guide specification, not fishing expeditions
- If theory says X should affect Y positively, a negative coefficient needs explanation

**Ask:**
- Does this specification make theoretical sense?
- Are units consistent across variables?
- Would an economist in the field recognise this model?

---

### 2. Ask the right questions

**Corollary:** Place relevance before mathematical elegance.

**In practice:**
- Avoid Type III errors (the right answer to the wrong question)
- Start with "What do we want to know?" not "What can we estimate?"
- Distinguish between questions of interest and questions we can answer

**Ask:**
- Is this the question the reader actually cares about?
- Could I answer this question more directly?
- Am I estimating what I think I'm estimating?

---

### 3. Know the context

**Corollary:** Don't perform ignorant statistical analyses.

**In practice:**
- Understand how data was collected
- Know measurement limitations
- Consider institutional constraints
- Recognise period-specific factors (COVID, financial crisis)

**Ask:**
- How was this data generated?
- What measurement issues might affect results?
- Are there institutional features I should know about?

---

### 4. Inspect the data

**Corollary:** Place data cleanliness ahead of econometric godliness.

**In practice:**
- Summary statistics before estimation
- Graphs and scatter plots
- Residual plots after estimation
- Look for anomalies, outliers, coding errors

**Checklist:**
- [ ] Summary statistics produced
- [ ] Key variables plotted
- [ ] Outliers identified and investigated
- [ ] Missing data patterns examined

---

### 5. Keep it sensibly simple

**Corollary:** Don't apply asymptotic approximations in vain.

**In practice:**
- Start with simple models
- Add complexity only when failures identified
- More variables ≠ better model
- Parsimony is a virtue

**Ask:**
- Could I drop variables with little explanatory power?
- Is this complexity justified by the data?
- Am I overfitting?

---

### 6. Use the interocular trauma test

**Corollary:** Apply the laugh test.

**In practice:**
- Look until results hit you between the eyes
- If it doesn't look right, it probably isn't
- Trust your intuition, then verify
- Results should make sense to domain experts

**Ask:**
- Does this pass the "smell test"?
- Would an expert laugh at these results?
- Can I explain this to a non-specialist?

---

### 7. Beware the costs of data mining

**Corollary:** Don't worship R-squared, don't hunt significance with a shotgun.

**In practice:**
- Distinguish exploratory from confirmatory analysis
- Report all specifications, not just "winning" ones
- Pre-specify hypotheses where possible
- High R-squared with no theoretical basis is suspect

**Red flags:**
- Hundreds of regressions, one reported
- Only significant results shown
- Theory constructed to fit results

---

### 8. Be willing to compromise

**Corollary:** Don't worship textbook prescriptions.

**In practice:**
- Real problems rarely match textbook assumptions
- Perfect is the enemy of good
- Document compromises made
- Proxies, aggregation, and simplifications are often necessary

**Ask:**
- What compromises have I made?
- Are they documented?
- Do they materially affect conclusions?

---

### 9. Don't confuse significance with substance

**Corollary:** Don't ignore power, don't test sharp hypotheses.

**In practice:**
- Statistical significance ≠ economic importance
- Report confidence intervals, not just p-values
- Large samples make everything "significant"
- Small effects can be precisely estimated but unimportant

**Ask:**
- Is this effect economically meaningful?
- Would a policymaker care about this magnitude?
- Am I confusing precision with importance?

---

### 10. Confess in the presence of sensitivity

**Corollary:** Anticipate criticism.

**In practice:**
- Report how results change with different specifications
- Test robustness to outliers, functional form, sample period
- Disclose fragility rather than hide it
- Reviewers will find it anyway

**Checklist:**
- [ ] Alternative specifications tested
- [ ] Results across subsamples compared
- [ ] Outlier influence checked
- [ ] Functional form sensitivity examined

---

## Common Mistakes

| Mistake | Example | Kennedy Fix |
|---------|---------|-------------|
| **Theory-free fishing** | Run 100 regressions, report best | Pre-specify based on theory |
| **Ignoring data quality** | Estimate before exploring | Summary stats and plots first |
| **Over-complexity** | Kitchen-sink regressions | Start simple, add with justification |
| **Significance worship** | "p < 0.05 therefore important" | Report economic magnitude |
| **Hidden sensitivity** | Only show "main" results | Report robustness across specs |
| **Inconsistent units** | Mix nominal and real | Ensure like-with-like |
| **Ignoring context** | Treat COVID year as normal | Know period-specific factors |

---

## Quality Checklist

### Pre-Analysis
- [ ] **Commandment 1:** Theory guides specification (not fishing)
- [ ] **Commandment 2:** Research question is clearly stated
- [ ] **Commandment 3:** Context understood (data collection, institutions)

### Data Quality
- [ ] **Commandment 4:** Data inspected (summary stats, graphs, residuals)
- [ ] Missing values, outliers, and anomalies documented

### Model Design
- [ ] **Commandment 5:** Started simple, complexity justified
- [ ] **Commandment 7:** Data mining costs acknowledged
- [ ] **Commandment 8:** Compromises documented (proxies, aggregation)

### Results Interpretation
- [ ] **Commandment 6:** Laugh test passed (results make intuitive sense)
- [ ] **Commandment 9:** Economic magnitude assessed, not just p-values
- [ ] **Commandment 10:** Sensitivity analysis reported

---

## Integration with Existing Protocols

This protocol EXTENDS, not replaces, existing quality gates:

| Protocol | Focus | Kennedy Adds |
|----------|-------|--------------|
| **statistical-sanity.md** | Is the number CORRECT? | Is the ANALYSIS sound? |
| **statistical-communication.md** | Is it MEANINGFUL? | Is it WELL-DESIGNED? |
| **data-handling.md** | Are calculations valid? | Is the model appropriate? |

**Sequence:** First verify analysis design (this protocol), then verify correctness (statistical-sanity), then verify communication (statistical-communication).

---

## When to Apply

Apply this protocol when:
- Any regression analysis is being conducted
- Causal or predictive claims are being made from data
- Statistical models are being estimated and interpreted

Skip this protocol when:
- Pure descriptive statistics (no modelling)
- Simple counts and tabulations
- Data exploration without inference

---

## References

- Kennedy, P. (2008). *A Guide to Econometrics*, 6th ed. Wiley-Blackwell. Chapter 22: Applied Econometrics.
- Angrist, J.D. & Pischke, J-S. (2010). The Credibility Revolution in Empirical Economics. *Journal of Economic Perspectives*, 24(2), 3-30.
