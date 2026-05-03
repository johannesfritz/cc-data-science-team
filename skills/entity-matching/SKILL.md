---
name: entity-matching
description: LLM-augmented entity matching between two datasets. Use when user asks to match, deduplicate, or link entities across datasets — especially when names differ in format, language, or abbreviation.
---

# Entity Matching Skill

**Trigger:** User asks to match, deduplicate, reconcile, or link entities between two datasets.

**Output:** Correspondence table with confidence levels and review flags.

---

## Workflow

### Step 1: Profile both datasets

Before choosing a strategy, understand what you're working with:

- **Column inventory:** What fields are available? (name, country, sector, ID codes, descriptions)
- **Cardinality:** How many unique entities in each dataset? (50 vs 50? 200 vs 5,000?)
- **Text richness:** Are names short codes or full descriptions? Is there supporting context?
- **Overlap estimate:** What percentage of source entities are expected to exist in the target?
- **Language:** Are names in the same language? Mixed scripts?

Report findings before proceeding. The user should confirm expectations.

### Step 2: Identify blocking variable

Find the **necessary condition** for a match — the attribute that must be identical for two entities to possibly refer to the same thing:

| Domain | Typical Blocking Variable |
|--------|--------------------------|
| International organisations | Country |
| Companies | Country + Sector |
| Academic papers | Year + Field |
| Products | HS code prefix / category |
| People | Organisation + Role |

Blocking reduces the comparison space from N x M to sum of (n_i x m_i) per block.

**Rule:** If any block has <20 target candidates, skip pre-filter and send all to LLM.

### Step 3: Choose strategy by group size

| Blocked Group Size | Strategy | Rationale |
|-------------------|----------|-----------|
| **<20 targets** | All-to-LLM | Small enough to compare all pairs directly |
| **20-100 targets** | Top-K pre-filter (K=5) + LLM | Pre-filter reduces noise without losing matches |
| **>100 targets** | Batched top-K (K=10) + LLM | Wider net needed; batch to manage token costs |

### Step 4: Build compressed summaries

Create ~60-80 token summaries for each entity. Include:
- Official name and common abbreviations
- Country/jurisdiction
- Primary function or sector
- Key distinguishing attributes

```
[ID:DPA-142] Japan - Personal Information Protection Commission (PPC).
Data protection authority. Est. 2016. Regulates Act on Protection of
Personal Information (APPI).
```

**Do not include:** Full addresses, phone numbers, raw database IDs, or any field that doesn't help distinguish the entity.

### Step 5: Execute three-pass matching

Follow the three-pass architecture from `.claude/protocols/llm-pipeline-standards.md`:

**Pass 1 — Pre-filter:**
- Compute Jaro-Winkler similarity between all source-target pairs within each block
- Also compute token overlap score
- Select top-K candidates per source entity (by max of JW and token scores)

**Pass 2 — LLM adjudication:**
- For each source entity, present its top-K candidates to GPT-4o (or selected model)
- Request: match ID (or null), confidence (high/medium/low), reasoning
- Temperature 0, JSON mode

**Pass 3 — False-negative sweep:**
- Take unmatched source entities (top 20% by importance/size)
- Run broader search against all targets in their block using Gemini Flash
- Different prompt framing: "Could any of these be the same entity under a different name?"

### Step 6: Cross-model verification

Mandatory when total matches exceed 50.

1. Draw stratified sample (10% high-confidence, 25% medium, 50% low)
2. Run verification through different model family (blind — second model doesn't see first answer)
3. Report agreement rate
4. Review all disagreements manually

### Step 7: Output correspondence table

Produce final output with:

| Column | Description |
|--------|-------------|
| `source_id` | ID from source dataset |
| `source_name` | Original name from source |
| `target_id` | Matched ID from target (or NA) |
| `target_name` | Matched name from target (or NA) |
| `confidence` | high / medium / low / unmatched |
| `match_tier` | exact / normalised / fuzzy / token / llm |
| `jw_score` | Jaro-Winkler score for the matched pair |
| `llm_reasoning` | LLM's explanation (for LLM-matched pairs) |
| `review_flag` | TRUE if confidence=low or JW-LLM disagreement |
| `verified` | TRUE if included in cross-model verification sample |

Save to `results/` as both CSV and Excel (with conditional formatting on confidence and review_flag).

---

## Quality Checklist

Before delivering results:

- [ ] All source entities have a status (matched or documented as unmatched)
- [ ] Cross-model verification completed (if >50 matches)
- [ ] Agreement rate reported and above 75%
- [ ] Traditional-score cross-check completed (JW vs LLM anomalies flagged)
- [ ] All prompts and responses logged to `data/llm_logs/`
- [ ] Correspondence table saved to `results/` with review flags
- [ ] PLAN.md updated with match statistics and cost summary
- [ ] Unmatched entities documented with explanation (no target exists / ambiguous / data quality)

---

## References

- Decision framework: `.claude/rules/data-science/llm-augmented-analysis.md`
- Pipeline standards: `.claude/protocols/llm-pipeline-standards.md`
- Traditional matching tiers: `.claude/rules/data-science/data-handling.md` (Fuzzy Matching Protocol)
