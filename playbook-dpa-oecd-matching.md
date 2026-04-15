# Playbook: DPA-OECD Policy Database Matching

How to use the data-science-team plugin in Claude Coworker to review, modify, and re-run the DPA-OECD policy matching pipeline.

**Project folder:** `data-queries/260212-dpa-oecd-matching/`

**Prerequisites:**
- Plugin installed: `claude plugin add ./cc-data-science-team`
- Python environment with: `pymysql python-dotenv openai google-genai pandas openpyxl rapidfuzz scikit-learn numpy`
- `.env` file with: `GTA_HOST`, `GTA_PORT`, `GTA_DB`, `GTA_USER_READONLY`, `GTA_DB_KEY_READONLY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`
- Source data: `data/DPA-OECD-DUPLICATION-CHECK.xlsx`

**Important:** The scripts contain hardcoded `.env` paths pointing to the original analyst's machine. Before running, update lines 24-29 in `code/v2_2_llm_matching.py` (and equivalent lines in `v2_0`, `v2_3`, `v2_4`) to point to your `.env` location, or place the `.env` file at the project root.

---

## Exercise 1: Review Existing Results

**Goal:** Understand the current match results and make accept/reject decisions on flagged pairs.

**Estimated time:** 1-2 hours

### What you prompt

**Step 1 — Understand the output**

> Load the file `results/v2_manual_review.xlsx` from the DPA-OECD matching project. This contains 74 match pairs flagged for manual review. Explain the columns and show me a summary: how many are flagged for low GPT confidence, how many because Gemini disagrees, and how many were rescued from the excluded metadata pool?

**Step 2 — Review by country**

> Show me the flagged pairs for [COUNTRY], grouped by review reason. For each pair, show the OECD title, DPA title, GPT confidence, GPT rationale, and Gemini verdict. I want to decide which are genuine matches.

Repeat for each country of interest.

**Step 3 — Record decisions**

> Add a column `referee_decision` to the manual review file. Set it to "accept" for pairs [list IDs] and "reject" for pairs [list IDs]. Save as `results/v2_manual_review_decided.xlsx`.

**Step 4 — Update the master table**

> Update `results/v2_correspondence.xlsx` to reflect my decisions: remove rejected pairs (change status to `only_oecd` / `only_dpa` as appropriate) and mark accepted pairs as confirmed. Recalculate the match summary statistics and save an updated `results/v2_match_summary.xlsx`.

### What you get

- `v2_manual_review_decided.xlsx` — your decisions recorded
- Updated `v2_correspondence.xlsx` and `v2_match_summary.xlsx`

---

## Exercise 2: Re-Run with Modified Filters

**Goal:** Change the DPA metadata filters that determine which entries are candidates for matching.

**Estimated time:** 30-45 minutes (mostly LLM API calls)

### Background

The V2 pipeline uses two filters to select DPA entries for matching:

- **F1 (Economic Activity):** IDs `{1, 9}` — Cross-cutting and ML/AI development
- **F2 (Policy Area):** IDs `{2, 4, 5, 16}` — Competition, Data governance, Subsidies/industrial policy, Design/testing standards

Pool D = F1 OR F2 (the union). Entries outside Pool D are excluded from matching (except in Sweep B, which rescues miscoded entries).

The V1/V2 comparison showed that 60 valid matches were lost because V2's filters excluded them. You may want to widen the filters.

### What you prompt

**Step 1 — See what's excluded**

> In the DPA-OECD matching project, load `data/dpa_enriched.json` and show me the distribution of economic_activity_name and policy_area_names across all 823 DPA entries. Also show me specifically the metadata of the 59 entries that are NOT in Pool D (excluded by current filters F1 and F2).

Review the excluded entries. Decide which additional filter IDs to include.

**Step 2 — Modify filters**

> In `code/v2_1_filter_candidates.py`, change the filter definitions:
> - Line 30: change `F1_ECONOMIC_ACTIVITY_IDS` from `{1, 9}` to `{1, 9, [YOUR_IDS]}`
> - Line 37: change `F2_POLICY_AREA_IDS` from `{2, 4, 5, 16}` to `{2, 4, 5, 16, [YOUR_IDS]}`
>
> Then re-run the full V2 pipeline: execute scripts `v2_1_filter_candidates.py` through `v2_6_compile.py` in order. After each script, report the key output statistics.

**Step 3 — Compare to previous V2**

> Compare the new results against the previous V2 run. How many match pairs changed? How many new matches were gained? How many were lost? Show the set difference.

### What to change

| What | File | Line | Current |
|------|------|------|---------|
| Economic activity filter | `code/v2_1_filter_candidates.py` | 30 | `{1, 9}` |
| Policy area filter | `code/v2_1_filter_candidates.py` | 37 | `{2, 4, 5, 16}` |

### What you get

- Updated `data/v2_candidate_pools.json` with new pool sizes
- New match results through the full pipeline
- Comparison against previous run

---

## Exercise 3: Re-Run with Different LLM or Prompts

**Goal:** Test sensitivity to the matching model or modify the matching criteria.

**Estimated time:** 30-60 minutes

### What you prompt

**Option A — Change the model**

> In the DPA-OECD matching project, I want to re-run the LLM matching with a different model. In `code/v2_2_llm_matching.py`, change line 32 from `MODEL = "gpt-5-mini-2025-08-07"` to `MODEL = "[YOUR_MODEL]"`. Make the same change in `code/v2_3_false_negative_sweep.py` line 35. Then run scripts `v2_2` through `v2_6` in order. Report results after each step.

**Option B — Change the matching prompt**

> In `code/v2_2_llm_matching.py`, I want to modify the system prompt (lines 100-109). Change it to:
>
> [YOUR MODIFIED PROMPT]
>
> Make the equivalent change in `code/v2_3_false_negative_sweep.py`. Then re-run from `v2_2` through `v2_6`.

**Option C — Change the Gemini verification model**

> In `code/v2_4_verification.py`, change line 33 from `MODEL = "gemini-3.1-pro-preview"` to `MODEL = "[YOUR_MODEL]"`. Re-run `v2_4` through `v2_6`.

### What to change

| What | File | Line | Current |
|------|------|------|---------|
| GPT model | `code/v2_2_llm_matching.py` | 32 | `gpt-5-mini-2025-08-07` |
| GPT model (sweep) | `code/v2_3_false_negative_sweep.py` | 35 | `gpt-5-mini-2025-08-07` |
| System prompt | `code/v2_2_llm_matching.py` | 100-109 | AI policy matching instructions |
| Gemini model | `code/v2_4_verification.py` | 33 | `gemini-3.1-pro-preview` |
| Batch size | `code/v2_2_llm_matching.py` | 34 | `MAX_OECD_PER_BATCH = 8` |
| Verification sample sizes | `code/v2_4_verification.py` | ~70-90 | 20/15/10/15 stratified |

### What you get

- New match results with the modified model/prompt
- QA report with updated cross-model agreement rate

---

## Exercise 4: Run from Scratch on Updated Data

**Goal:** Re-run the entire pipeline when either the OECD or DPA source data is updated.

**Estimated time:** 1-2 hours

### What you prompt

**Step 1 — Replace source data**

> Replace `data/DPA-OECD-DUPLICATION-CHECK.xlsx` with the updated version. Then run the full V2 pipeline from scratch. Start with `code/v2_0_enrich_dpa.py` — this requires database access to enrich DPA entries with metadata. After it runs, confirm: how many DPA entries were enriched? What is the distribution of economic activities?

**Step 2 — Run the pipeline**

> Now run the full pipeline in order:
> 1. `python code/v2_0_enrich_dpa.py` — enrich DPA metadata from database
> 2. `python code/v2_1_filter_candidates.py` — build candidate pools
> 3. `python code/v2_2_llm_matching.py` — GPT matching on Pool D
> 4. `python code/v2_3_false_negative_sweep.py` — false-negative sweeps (A + B)
> 5. `python code/v2_4_verification.py` — Gemini cross-model verification
> 6. `python code/v2_6_compile.py` — compile results and QA report
>
> After each script, report: row counts, match counts, any errors. If a script fails, diagnose and fix before continuing.

**Step 3 — If the source data structure changed**

> The data prep script (`code/0_data_prep.py`) parses specific column names from the Excel. If the column names or sheet names changed, update the script accordingly. Then re-run from `0_data_prep.py` through the full V2 pipeline.

### Prerequisites

- Database access (for `v2_0_enrich_dpa.py`) — needs `GTA_HOST`, `GTA_PORT`, `GTA_DB`, `GTA_USER_READONLY`, `GTA_DB_KEY_READONLY` in `.env`
- OpenAI API key (for `v2_2` and `v2_3`)
- Gemini API key (for `v2_4`)

### What you get

- Complete fresh run with updated data
- All output files regenerated in `results/`

---

## Tips

### Working efficiently

- **LLM calls are the bottleneck.** Steps 2 and 3 make 50-100 API calls each. Allow 10-15 minutes per step.
- **Scripts are resumable.** If a script fails mid-run, the LLM logs in `data/llm_logs/` preserve what was already processed. You can modify the script to skip completed countries.
- **Archive before re-running.** Copy current `results/` and `data/v2_*.json` files to `data/versions/` before overwriting.

### Quality control

- **Check the QA report.** After `v2_6_compile.py`, read `results/v2_qa_report.md`. Key metrics: match pair count, cross-model agreement rate, confidence distribution, countries with 0% match rates.
- **Cross-model agreement below 75% is a warning.** It means the matching criteria are producing genuinely ambiguous results. Focus your review on the disagreements.
- **Pool D should cover 85%+ of DPA entries.** If it drops much below that, the filters are too aggressive.

### Troubleshooting

| Problem | Fix |
|---|---|
| `v2_0_enrich_dpa.py` fails with connection error | Check `.env` database credentials. The `lux_*` tables must be accessible. |
| LLM returns invalid JSON | The script has error handling and retries. If persistent, check the model name is valid. |
| 0% match rate for a country | Check `data/country_mapping.json` — the country name may not be harmonised between OECD and DPA. |
| Cross-model agreement very low (<50%) | The matching prompt may be too loose. Tighten the system prompt to require stronger evidence for a match. |
| Many sweep_b rescues | The metadata filters may be too aggressive. Consider widening F1/F2 (Exercise 2). |

### Pipeline dependencies

```
v2_0_enrich_dpa.py (DB access)
    ↓
v2_1_filter_candidates.py
    ↓
v2_2_llm_matching.py (OpenAI)
    ↓
v2_3_false_negative_sweep.py (OpenAI)
    ↓
v2_4_verification.py (Gemini)
    ↓
v2_5_compare.py (only if comparing V1 vs V2)
    ↓
v2_6_compile.py → results/*.xlsx + results/v2_qa_report.md
```

You can re-run from any step — each script reads its inputs from the `data/` folder. To re-run from step N, ensure steps 0 through N-1 have valid outputs in `data/`.
