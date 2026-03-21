# Causal Inference Protocol

**Source:** Joshua Angrist & Jorn-Steffen Pischke, *Mostly Harmless Econometrics* (2008)

**Purpose:** Ensure causal claims are justified by appropriate identification strategies. The applied-econometrics.md protocol checks whether analysis is well-designed; this protocol checks whether *causal claims* have credible identification.

---

## The Core Principle

> "Empirical research is most valuable when it uses data to answer specific causal questions."

The experimentalist paradigm: In the absence of real experiments, seek well-controlled comparisons and natural "quasi-experiments." The goal is to construct comparisons that mimic random assignment.

---

## The Fundamental Problem

Causal inference requires knowing what would have happened in the absence of treatment. We never observe both outcomes for the same unit:

```
Causal Effect = Y(treated) - Y(untreated)
                    ↑            ↑
               observed      never observed
```

All identification strategies are attempts to construct credible counterfactuals.

---

## The Four Core Methods

### 1. OLS with Controls (Selection on Observables)

**When to use:** When you believe all confounders are observed and can be controlled for.

**Key assumption:** Conditional Independence Assumption (CIA)
- Treatment assignment is independent of potential outcomes, conditional on observables
- No omitted variable bias

**Diagnostic:**
- Coefficient stability as controls added
- If coefficient changes dramatically, selection on unobservables likely

**Checklist:**
- [ ] All plausible confounders identified
- [ ] Controls added systematically
- [ ] Coefficient stability demonstrated
- [ ] Remaining omitted variable bias assessed

**Warning signs:**
- Coefficient changes sign when controls added
- No theoretical basis for CIA
- Obvious unobserved confounders

---

### 2. Instrumental Variables (IV)

**When to use:** When you have a variable that affects treatment but affects the outcome only through treatment.

**Key assumptions:**
1. **Relevance:** Instrument predicts treatment (testable)
2. **Exclusion restriction:** Instrument affects Y only through X (not testable)
3. **Monotonicity:** Instrument affects treatment in same direction for everyone

**Diagnostic:**
- First stage F-statistic > 10 (Staiger-Stock rule)
- Overidentification test (if multiple instruments)

**Checklist:**
- [ ] **Relevance:** First stage F > 10
- [ ] **Exclusion restriction:** Argued why instrument only affects Y through X
- [ ] **LATE interpretation:** Who are the compliers?
- [ ] Overidentification test (if multiple instruments)

**Warning signs:**
- Weak first stage (F < 10)
- Obvious violations of exclusion restriction
- Unclear complier population

---

### 3. Difference-in-Differences (DiD)

**When to use:** When a policy or treatment affects some units but not others, and you have pre- and post-treatment data.

**Key assumption:** Parallel trends
- Treatment and control groups would have followed the same trajectory absent treatment

**Diagnostic:**
- Visual pre-trend check (plot outcomes over time)
- Placebo tests (fake treatment timing)
- Event study specification

**Checklist:**
- [ ] **Parallel trends:** Pre-treatment trends visualised
- [ ] **No anticipation:** Treatment timing is sharp
- [ ] Placebo tests (fake treatment timing)
- [ ] Event study specification shows effect timing

**Warning signs:**
- Divergent pre-trends
- Treatment timing is fuzzy
- Composition changes in treatment/control groups

---

### 4. Regression Discontinuity (RD)

**When to use:** When treatment is determined by a cutoff on a continuous running variable.

**Key assumption:** No manipulation at cutoff
- Units cannot precisely sort around the threshold
- Potential outcomes are continuous at the cutoff

**Diagnostic:**
- McCrary density test (bunching at cutoff)
- Bandwidth sensitivity analysis
- Covariate balance at cutoff

**Checklist:**
- [ ] **Running variable defined** (sharp vs. fuzzy)
- [ ] **McCrary test:** No bunching at cutoff
- [ ] Bandwidth sensitivity analysis
- [ ] Donut RD (exclude observations near cutoff)
- [ ] Covariate balance at cutoff

**Warning signs:**
- Bunching at cutoff (manipulation)
- Discontinuous covariates at cutoff
- Results sensitive to bandwidth choice

---

## LATE: Local Average Treatment Effect

When using IV, you estimate the **Local Average Treatment Effect (LATE)**, not the Average Treatment Effect (ATE).

### Who is in LATE?

| Type | Definition | In LATE? |
|------|------------|----------|
| **Compliers** | Change treatment status because of instrument | Yes |
| **Always-takers** | Would take treatment regardless of instrument | No |
| **Never-takers** | Would never take treatment regardless of instrument | No |
| **Defiers** | Do opposite of instrument (assumed away) | No |

**Interpretation:** LATE is the effect on compliers only. This may differ from the effect on the whole population.

**Ask:**
- Who are the compliers?
- Are compliers representative of the population of interest?
- Could the effect differ for always-takers or never-takers?

---

## Standard Errors

### Clustering

**Rule:** Cluster at the level of treatment assignment.

| Design | Cluster Level |
|--------|---------------|
| Individual randomisation | No clustering needed |
| School-level policy | Cluster at school |
| State-level policy | Cluster at state |
| DiD with state variation | Cluster at state |

### Few Clusters Problem

If fewer than 50 clusters:
- Wild bootstrap (Cameron, Gelbach, Miller)
- Aggregation to cluster level
- Be conservative in interpretation

**Checklist:**
- [ ] Clustering level matches treatment assignment
- [ ] Heteroskedasticity-robust if needed
- [ ] Few clusters addressed (wild bootstrap)

---

## Red Flags in Causal Claims

| Claim | Red Flag | Question to Ask |
|-------|----------|-----------------|
| "X causes Y" | No identification strategy stated | How do we know this isn't correlation? |
| "Controlling for Z" | Large coefficient change | What other unobservables might matter? |
| IV used | Weak first stage | Is F > 10? |
| IV used | No exclusion restriction argument | Why does instrument only affect Y through X? |
| DiD used | No pre-trends shown | Were groups parallel before treatment? |
| RD used | No McCrary test | Could units manipulate around cutoff? |
| "Significant effect" | No magnitude discussion | Is this economically meaningful? |

---

## The Credibility Hierarchy

From strongest to weakest identification:

1. **Randomised Controlled Trial** (gold standard)
2. **Natural experiment with RD** (sharp cutoff, no manipulation)
3. **DiD with clear parallel trends** (visual evidence compelling)
4. **IV with strong first stage and defensible exclusion** (F >> 10)
5. **OLS with rich controls** (CIA plausible)
6. **OLS without controls** (correlation only)

Move down this hierarchy only when higher methods are unavailable. Always be explicit about where your analysis sits.

---

## Quality Checklist

### Research Design
- [ ] **Causal question clearly stated** (what is the treatment? what is the outcome?)
- [ ] **Identification strategy specified** (OLS, IV, DiD, RDD)
- [ ] **Comparison group defined** (who are the counterfactual?)

### For OLS with Controls
- [ ] Selection on observables defended
- [ ] Coefficient stability shown as controls added
- [ ] Remaining omitted variable bias assessed

### For Instrumental Variables
- [ ] **Relevance:** First stage F-statistic > 10
- [ ] **Exclusion restriction:** Argued why instrument only affects Y through X
- [ ] **LATE interpretation:** Who are the compliers?
- [ ] Overidentification test (if multiple instruments)

### For Difference-in-Differences
- [ ] **Parallel trends:** Pre-treatment trends visualised
- [ ] **No anticipation:** Treatment timing is sharp
- [ ] Placebo tests (fake treatment timing)
- [ ] Event study specification

### For Regression Discontinuity
- [ ] **Running variable defined** (sharp vs. fuzzy)
- [ ] **McCrary test:** No bunching at cutoff
- [ ] Bandwidth sensitivity analysis
- [ ] Donut RD (exclude observations near cutoff)

### Standard Errors
- [ ] Clustering appropriate (treatment-level)
- [ ] Heteroskedasticity-robust if needed
- [ ] Few clusters addressed (wild bootstrap)

---

## Integration with Existing Protocols

This protocol EXTENDS, not replaces, existing quality gates:

| Protocol | Focus | Angrist/Pischke Adds |
|----------|-------|----------------------|
| **applied-econometrics.md** | Is analysis WELL-DESIGNED? | Are CAUSAL CLAIMS justified? |
| **statistical-sanity.md** | Is the number CORRECT? | Is the IDENTIFICATION credible? |
| **analytical-balance.md** | Both sides presented? | Alternative explanations considered? |

**Sequence:** Applied econometrics first (good analysis design), then causal inference (credible identification), then statistical sanity (correct numbers), then communication (meaningful presentation).

---

## When to Apply

Apply this protocol when:
- Causal language is used ("X causes Y", "effect of X on Y")
- Policy evaluation is being conducted
- Treatment effects are being estimated
- Any IV, DiD, or RD method is used

Skip this protocol when:
- Pure description (no causal claims)
- Prediction without causal interpretation
- Correlation explicitly acknowledged as such

---

## References

- Angrist, J.D. & Pischke, J-S. (2008). *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton University Press.
- Angrist, J.D. & Pischke, J-S. (2014). *Mastering 'Metrics: The Path from Cause to Effect*. Princeton University Press.
- Imbens, G.W. & Rubin, D.B. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge University Press.
- [Mostly Harmless Econometrics website](https://www.mostlyharmlesseconometrics.com/)
