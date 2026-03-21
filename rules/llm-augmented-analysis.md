---
paths:
  - sgept-analytics/**
  - "*/data-queries/**"
---

# LLM-Augmented Analysis

**Purpose:** Decision framework for when and how to use LLMs as analytical tools within data pipelines. LLMs are not just text generators; they are semantic reasoning engines that can outperform traditional algorithms on tasks involving meaning, context, and domain knowledge.

---

## Routing Decision Tree

Before choosing a method, classify the analytical task:

| Task Type | LLM Advantage | Traditional Advantage | Use LLM When |
|-----------|--------------|----------------------|---------------|
| **Entity matching** | Understands abbreviations, context, domain knowledge | Faster for exact/near-exact matches | Tiers 1-4 leave >20% in grey zone (score 0.30-0.70) |
| **Text classification** | Handles ambiguity, multi-label, context-dependent categories | Faster for keyword-based rules | Categories require judgement, not pattern matching |
| **Structured extraction** | Handles varied formats, implicit information | Regex works when format is fixed | Format varies or information is implicit |
| **Anomaly detection** | Explains why something is anomalous | Statistical methods with clear distributions | Anomalies require domain context to identify |
| **Semantic similarity** | Understands meaning beyond surface text | Embeddings sufficient for simple similarity | Comparison requires reasoning about equivalence |

### When NOT to use LLMs

- Exact string matching (Tier 1-2 in fuzzy matching)
- Numeric calculations or aggregations
- Tasks with deterministic algorithmic solutions
- When the full dataset fits a simple rule-based approach
- When cost exceeds the value of marginal accuracy improvement

---

## Object-of-Study Specification

Before any LLM extraction, classification, or structured analysis pipeline begins, explicitly define three things and record them in PLAN.md. **Escalate ambiguity to the user rather than resolving it by assumption.**

### 1. Inclusion/exclusion criteria

Define what counts as a valid object for this analysis. The definition must be specific enough that a reviewer can classify a borderline case.

| Element | Question to Answer |
|---------|-------------------|
| **Actor** | Who must be performing the action? |
| **Action** | What type of action qualifies? |
| **Direction** | Who is affected, and in which direction? |
| **Scope** | What is in/out of scope? |

**Test:** State one example that should be included and one that should be excluded. If the boundary is ambiguous, the definition is too vague — escalate to the user.

### 2. Unit of analysis

Define what constitutes one distinct object (one row in the output). Multiple pieces of evidence about the same real-world object should be consolidated, not counted separately.

| Granularity | Definition | When to Use |
|-------------|-----------|-------------|
| **Policy** | One government action or programme | Cataloguing interventions |
| **Concern** | One discrete complaint or issue | Cataloguing allegations |
| **Passage** | One text segment | Building a retrieval index (intermediate, not final) |

**Test:** If two extracted items refer to the same real-world policy, do they merge into one row or remain separate? Write the answer down before executing.

### 3. User acceptance before execution

Present the inclusion/exclusion criteria and unit-of-analysis definition to the user in PLAN.md before pipeline execution. If executing without user confirmation (time pressure), use conservative defaults (narrower inclusion, coarser unit) and document this assumption explicitly.

---

## Model Selection Matrix

| Model | Strengths | Use For | Cost Tier |
|-------|-----------|---------|-----------|
| **GPT-4o** | Complex reasoning, structured output (JSON mode), nuanced judgement | Entity matching adjudication, multi-factor classification, ambiguous cases | High |
| **Gemini Flash** | High throughput, large context window, cost-efficient | Batch extraction, high-volume classification, false-negative sweeps | Low |
| **Claude Haiku** | Fast, cheap, reliable for simple tasks | Simple extraction, binary classification, confidence scoring | Low |
| **Claude Sonnet** | Strong reasoning at moderate cost | Cross-model verification, quality auditing | Medium |

### Selection rules

1. **Start with the cheapest model that could work** — upgrade only if quality is insufficient
2. **Use expensive models for adjudication, cheap models for volume** — the pre-filter + adjudication pattern
3. **Cross-model verification uses a different model family** — GPT-4o primary, then Gemini or Claude for verification (never verify with the same model)

---

## Token Efficiency Patterns

### Blocking strategy

Group entities by a shared attribute (country, sector, year) before sending to LLM. This:
- Reduces the candidate space per prompt
- Provides natural context (entities in same country are more likely matches)
- Enables parallel processing by block

### Compressed summaries

Build ~60-80 token summaries per entity instead of sending raw data:

```
# Bad: sending full row (200+ tokens)
{"id": 123, "name": "Ministry of Trade and Industry", "country": "Japan",
 "address": "1-3-1 Kasumigaseki", "established": "1949", ...}

# Good: compressed summary (60 tokens)
"[ID:123] Japan - Ministry of Trade and Industry (METI). Est. 1949.
 Regulates trade policy, industrial standards, energy policy."
```

### Batch by natural groupings

- Country blocks for international entity matching
- Sector groups for industry classification
- Time periods for temporal analysis
- Skip pre-filter entirely for groups with <20 candidates

---

## Validation Requirements

### Cross-model verification

For any LLM-classified output exceeding 50 items:

1. **Stratified sample** — draw 10-15% of results, stratified by confidence level (high/medium/low) and match tier
2. **Second model** — run the same prompts through a different model family
3. **Agreement thresholds:**
   - >90%: High reliability, proceed
   - 75-90%: Review all disagreements manually, adjust prompts if systematic
   - <75%: Investigate root cause before using results

### Traditional-score cross-check

For entity matching: compute Jaro-Winkler scores for all LLM-matched pairs. Flag anomalies where:
- LLM says "match" but JW score < 0.50 (may be correct but needs documentation)
- LLM says "no match" but JW score > 0.85 (likely LLM error)

### Confidence-level logging

Every LLM decision must include a confidence level. Expect bimodal distributions for matching tasks (high confidence matches + high confidence non-matches, with few in the middle). A uniform distribution suggests the LLM is guessing.

---

## Cost Tracking

### Before execution

Estimate total token usage:
- Count entities x average tokens per prompt x number of passes
- Apply model pricing
- Set budget ceiling (abort if exceeded)

### During execution

Log per-phase costs:
```
Phase 1 (pre-filter): 45K tokens, $0.02
Phase 2 (adjudication): 120K tokens, $0.15
Phase 3 (sweep): 30K tokens, $0.01
Verification: 25K tokens, $0.03
Total: 220K tokens, $0.21
```

### After execution

Record in PLAN.md:
- Total tokens used
- Total cost
- Cost per classified item
- Comparison to manual effort estimate

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|---------------|------------------|
| Trusting LLM batch indices | LLMs return 0-based, 1-based, or absolute indices unpredictably | Flexible index resolution: absolute → relative → positional fallback |
| Single-pass retrieval + classification | Embedding search alone can miss ~87% of targeted content | Recall-first: broad retrieval, then precision filtering downstream |
| Embedding search alone for document analysis | Embeddings miss oblique references and domain-specific phrasing | Hybrid pipeline: embeddings for broad net + full-text LLM cross-check |
| Accepting LLM-extracted quotes at face value | ~40% of extracted passages are truncated or paraphrased | Multi-level fuzzy matching to verify every quote against source text |
| Single query phrasing for embedding search | One phrasing misses synonyms and alternative framings | 3-6 query variants with element-wise max scoring |

---

## Integration with Existing Pipeline

This rule extends the analyst-orchestrator pipeline. When the task type matches (entity matching, text classification, semantic similarity, structured extraction):

1. **Stage 2.8** activates LLM-augmented analysis per this framework
2. **Stage 2.9** validates LLM outputs before proceeding to visualisation
3. All prompts and responses logged to `data/llm_logs/` for auditability

See: `.claude/protocols/llm-pipeline-standards.md` for procedural standards.
