# Playbook: NTE + DPA Analytical Exercises

How to use the data-science-team plugin in Claude Coworker to complete four analytical exercises involving the USTR National Trade Estimate Report and the Digital Policy Alert.

**Prerequisites:**
- Plugin installed: `claude plugin add ./cc-data-science-team`
- NTE 2025 and NTE 2026 PDFs available
- DPA MCP server connected (for exercises 3 and 4)

---

## Exercise 1: Compare NTE26 to NTE25 — Is Digital Becoming More Important?

**Goal:** Show whether more tech discrimination / DSTs are mentioned in NTE26 vs NTE25. Provide examples.

**Estimated time:** 2-3 hours

### What you prompt

**Step 1 — Prepare both documents**

> I have the NTE 2025 report as a PDF and the NTE 2026 report as a PDF. Please use the prepare-document skill to convert both to structured markdown.

Claude reads each PDF in 20-page chunks and produces `data/nte25.md` and `data/nte26.md`.

**Step 2 — Define digital-scope themes**

> Use the discover-themes skill on the NTE26 to identify all digital-policy-related categories. Focus on tech discrimination, digital services taxes, data governance, platform regulation, and AI regulation.

Claude reads NTE26 and proposes theme definitions. You review and approve. Save as `themes.json`. Alternatively, start from the plugin's example:

> Copy the digital-related themes from the NTE example themes file and adapt for our comparison.

**Step 3 — Extract both versions**

> Use extract-classify to extract all digital-policy entries from NTE25 against our themes. Save to `nte25_extractions.json`.

Then:

> Now extract NTE26 against the same themes. Save to `nte26_extractions.json`.

Claude processes country by country, runs validation and quote verification after each batch.

**Step 4 — Compare versions**

> Use compare-versions to diff the NTE25 and NTE26 extractions.

Claude runs `diff_versions.py` and reports:
- How many NEW digital entries appeared in NTE26
- How many were REMOVED from NTE25
- Which countries gained or lost entries
- Which themes grew most

**Step 5 — Get the headline numbers**

> Give me: (1) the absolute count change in digital entries, (2) the share of digital entries among all trade-barrier entries, and (3) which countries gained digital entries. Pull 3 concrete examples of NEW entries with verbatim quotes.

Claude's analyst agent works from the diff data and produces the statistics + examples.

### What you get

- `nte25_extractions.json` and `nte26_extractions.json` — structured datasets
- `diff_results.json` — entry-level comparison
- A summary with counts, shares, country spread, and verbatim examples

---

## Exercise 2: Dissect NTE26 — Full Digital Passage Extraction

**Goal:** Create an Excel of all DPA-scope passages in NTE26. One row per policy: country | policy title | full passage.

**Estimated time:** 3-4 hours (mostly extraction + review)

### What you prompt

**Step 1 — Prepare the document** (skip if already done in Exercise 1)

> Prepare the NTE26 PDF for extraction.

**Step 2 — Define themes covering DPA scope**

> Use discover-themes on NTE26. I need categories covering all digital policy areas that the DPA tracks: data governance, platform regulation, content moderation, cybersecurity, AI regulation, digital taxation, e-commerce, digital infrastructure, telecom, and cross-cutting digital trade.

Review the proposed themes. The DPA has 17 policy areas — you may want to use all of them or consolidate.

**Step 3 — Configure for comprehensive extraction**

> Set up the project config with these rules:
> - Include every digital-policy-relevant passage, even borderline ones (mark as WEAK rather than excluding)
> - Split compound passages: if one paragraph discusses two distinct policies, create two entries
> - Extract: country, policy title, full passage, page reference
> - No minimum match strength filter — we want everything for manual review

**Step 4 — Extract all countries**

> Extract NTE26 against the digital themes. Process all countries. This will take a while — do them in batches of 5.

Claude processes 5 countries at a time, running validation after each batch. You can monitor progress.

**Step 5 — Audit and review**

> Audit the extractions. Show me all WEAK and TENUOUS entries so I can decide which to keep.

Claude runs the audit skill, presents the borderline cases. You make IN/OUT decisions.

**Step 6 — Export to Excel**

> Export the final extraction to Excel with columns: Country | Policy Title | Full Passage | Page | Theme | Match Strength. Sort by country, then by theme.

### What you get

- `nte26_digital_extractions.json` — structured dataset
- `nte26_digital_passages.xlsx` — publication-ready Excel table

---

## Exercise 3: Compare NTE26 to DPA — Coverage Analysis

**Goal:** For every NTE26 digital policy entry, add a DPA ID where coverage exists. Show that DPA covers everything the NTE mentions, and more.

**Estimated time:** 2-3 hours (requires DPA MCP connection)

### What you prompt

**Step 1 — Start from Exercise 2 output**

> Load the NTE26 extraction from Exercise 2 (`nte26_digital_extractions.json`).

**Step 2 — Match against DPA**

> Use match-external to match each NTE26 entry against the DPA. For each entry:
> - Search the DPA by country + policy description
> - If a match exists, record the DPA event ID
> - If no match, mark as NO_MATCH and note whether it's a genuine gap or out of DPA scope
> - If multiple candidates, list the top 3 with rationale

Claude's matcher agent queries the DPA MCP server for each entry. This takes time — progress is reported per country.

**Step 3 — Review ambiguous matches**

> Show me all AMBIGUOUS and PROBABLE matches so I can confirm.

You review the uncertain cases and approve or correct.

**Step 4 — Produce the coverage report**

> Give me:
> (1) Match rate: what percentage of NTE26 entries have a DPA match?
> (2) Gap list: which NTE entries are NOT in the DPA? Categorise as genuine gaps vs out of scope.
> (3) DPA-only coverage: how many DPA entries exist for these countries that the NTE doesn't mention?
> (4) Three examples where DPA coverage is richer than the NTE.

**Step 5 — Export**

> Add a DPA ID column to the Exercise 2 Excel. Mark unmatched entries as "Not in DPA" with gap type.

### What you get

- `nte26_dpa_matched.json` — extraction with DPA IDs attached
- `coverage_gaps.csv` — entries DPA should add
- Updated `nte26_digital_passages.xlsx` with DPA ID column
- Coverage statistics for the memo

---

## Exercise 4: Analyse NTE26 Through DPA Taxonomy

**Goal:** For each matched DPA entry, add the DPA policy instrument and economic activity. Analyse which instruments/activities the USTR focuses on.

**Estimated time:** 1-2 hours (builds on Exercise 3)

### What you prompt

**Step 1 — Start from Exercise 3 output**

> Load the matched dataset from Exercise 3 (`nte26_dpa_matched.json`).

**Step 2 — Enrich with DPA taxonomy**

> For every entry with a DPA ID, pull the DPA policy instrument and economic activity fields. Add them as new columns.

Claude's matcher agent queries the DPA MCP server for each DPA ID's metadata.

**Step 3 — Analyse instrument distribution**

> Give me:
> (1) Count and share of NTE entries by DPA policy instrument. Which instruments does the USTR focus on?
> (2) Count and share by DPA economic activity. Which digital sectors does the USTR care about most?
> (3) Cross-tab: instrument × economic activity — where are the concentrations?
> (4) What does the USTR NOT care about? Which DPA instruments/activities have zero NTE mentions?

**Step 4 — Write the findings**

> Write a short analytical memo (600 words) summarising what the DPA taxonomy reveals about USTR priorities. Lead with findings. Include the tables. Cite specific entries as examples.

**Step 5 — Export**

> Add policy instrument and economic activity columns to the Excel. Create a summary tab with the cross-tabulation.

### What you get

- `nte26_dpa_enriched.json` — full dataset with DPA taxonomy
- Updated Excel with instrument + activity columns + summary tab
- Analytical memo

---

## Tips for All Exercises

### Working efficiently

- **Process in batches.** Don't ask Claude to do all 50+ countries at once. Batches of 5-10 give better quality and let you course-correct.
- **Check validation after each batch.** Claude runs the verification scripts automatically. If quote verification fails, fix before continuing.
- **Save intermediate outputs.** If you need to stop and resume later, the JSON files are your checkpoint. Claude can pick up where you left off.

### Quality control

- **Always review WEAK entries.** The extraction is deliberately inclusive — borderline cases are flagged, not silently dropped. You decide what's in or out.
- **Spot-check 5 quotes per batch.** Compare the `exact_quote` field against the original PDF. The verification script catches most issues, but visual spot-checks catch formatting problems.
- **For DPA matching:** if match rate is below 70%, pause and check whether the DPA search is using the right parameters. Low match rates usually mean search terms need adjusting, not that the DPA has poor coverage.

### Exercise dependencies

```
Exercise 1 (Compare NTE25 vs NTE26) — standalone
Exercise 2 (Dissect NTE26) — standalone, foundation for 3 and 4
Exercise 3 (NTE26 vs DPA) — requires Exercise 2 output
Exercise 4 (DPA taxonomy) — requires Exercise 3 output
```

Start with Exercise 2 if you plan to do all four — it's the foundation.

### When things go wrong

| Problem | Fix |
|---|---|
| Quote verification fails on many entries | Claude is paraphrasing. Remind it: "Use exact verbatim quotes from the document. Copy-paste, don't summarise." |
| Too many WEAK entries | Tighten the theme `domain` definitions. Be more specific about what's in/out of scope. |
| DPA matching returns too many AMBIGUOUS | Use more specific search terms. Include the country name and specific policy keywords in the query. |
| Claude loses context mid-extraction | Save the current extraction JSON, start a new conversation, and say "Continue extraction from where we left off. Load `extractions.json` and process the remaining countries." |
| Extraction seems to miss obvious entries | Run discover-themes again — your theme definitions may be too narrow. Or the document section may be structured differently than expected. |
