---
name: compare-documents
description: Compare claims in one policy document against evidence in another. Maps allegations, themes, or categories from a source document to a reference dataset. Use when user says "cross-check against NTE", "compare S301 to NTE", "does the NTE support these claims", "verify against the baseline", or when checking whether one document's framing is novel or repackaged.
---

# Compare Documents

Map claims from one document (source) against evidence in another (reference) to identify what is genuinely novel, what is repackaged, and what gaps exist.

## When to Use

- A new trade investigation references themes already documented elsewhere
- You need to verify whether allegations have a prior evidence base
- You want to identify definitional expansion (same countries, new framing)
- You need to find gaps between what a document claims and what prior evidence supports

## Process

### Step 1: Define the comparison frame

Identify:
- **Source document** — the newer document making claims (e.g., S301 investigation)
- **Reference document/dataset** — the baseline evidence (e.g., NTE extraction output, a prior analysis)
- **Comparison dimensions** — what you're comparing (countries? themes? specific allegations?)
- **Question** — what are you trying to answer? (Novel framing? Evidence gaps? Repackaging?)

### Step 2: Extract claims from source

For each claim in the source document, record:
- Country/entity it applies to
- Category/theme of the claim
- Specific allegation (what is being claimed?)
- Evidence cited (if any)
- Whether the claim is binary (yes/no) or graded

### Step 3: Search the reference

For each source claim, search the reference for:
1. **Direct match** — the reference explicitly discusses the same issue for the same country
2. **Indirect match** — the reference discusses a related issue that could support or contradict the claim
3. **No match** — the reference contains nothing relevant to this claim for this country

Record the match type and the specific reference evidence found (or its absence).

### Step 4: Classify the comparison

For each source claim × reference evidence pair:

| Source claims X | Reference has evidence | Reference lacks evidence |
|---|---|---|
| **Strong claim** (specific, named) | **Repackaged** — prior evidence exists | **Novel** — new framing, no prior basis |
| **Weak claim** (general, unnamed) | **Supported** — evidence exists but claim is vague | **Unsubstantiated** — vague claim with no prior evidence |

### Step 5: Produce a comparison matrix

Output a structured comparison:

```json
{
  "comparison": {
    "source": "S301 investigation",
    "reference": "NTE 2025 extraction",
    "question": "Is the S301 framing novel or repackaged?"
  },
  "results": [
    {
      "country": "JAPAN",
      "source_claim": "zombie firms / unprofitable firms continuing to operate",
      "reference_match": "NONE",
      "reference_evidence": "",
      "classification": "NOVEL",
      "notes": "NTE contains no zombie firm language for Japan"
    }
  ],
  "summary": {
    "total_claims": 38,
    "direct_match": 4,
    "indirect_match": 12,
    "no_match": 22,
    "novel_framing_pct": 57.9
  }
}
```

### Step 6: Analytical findings

Summarise:
- What proportion of source claims are genuinely novel?
- What proportion repackage prior evidence?
- Where are the biggest gaps between source framing and reference evidence?
- Are there structural patterns? (e.g., "evidence-only economies" vs "policy-cited economies")

## Example

User says: "Compare the S301 overcapacity allegations against the NTE extraction for the same 16 economies."

1. Load S301 structured data (16 economies × 11 categories)
2. Load NTE extractions.json (filtered to same 16 economies)
3. For each S301 allegation, search NTE entries for matching barriers
4. Find: only China + Indonesia have NTE overcapacity entries; 14 other economies are novel framing
5. Discover: NTE documents 40 policy instances for these 16 economies, but S301 cites only 7 — gap of 33
6. Report: "S301 is primarily novel framing applied to known trading partners, not repackaging of NTE evidence"

## Troubleshooting

**Reference dataset is too large to process at once:** Work country by country. Load one country's reference entries, compare against all source claims for that country, then move on.

**Claims and reference use different categories:** Map source categories to reference categories first. If they don't align (as in S301 vs NTE), document the mapping and its limitations.

**No structured reference dataset:** If the reference is a raw document (not extracted), run extract-classify on it first to produce a structured dataset for comparison.
