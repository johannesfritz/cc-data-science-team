---
name: extract-hs-codes
description: Extract HS/HTSUS product code tables from PDF documents into CSVs using dual-method verification. Use when user provides a PDF containing tariff schedules, product scope lists, annex tables, or any document with HS code tables. Covers Section 232, Section 301, Section 122, WTO schedules, and similar formats.
---

# Extract HS Codes from PDF

Extract product classification code tables (HS, HTSUS, HTS) from PDF documents into structured CSVs with dual-method cross-validation.

## When to Use

- User provides a PDF with HS/HTSUS code tables (tariff proclamations, annex lists, product scope documents)
- Tables have a code column (4 to 10+ digits) and a description column
- May be a single table, or multiple tables within one document

## Core Principles

### 1. Read the PDF first, design second

Every PDF is different. Before writing extraction code, read the entire document (20 pages at a time) and record:

- How many tables exist and what distinguishes them (separate pages? header rows? different column structures?)
- What HS code formats appear (4-digit chapters? 8-digit? 10-digit? mixed?)
- How many columns each table has (code + description? code + description + scope? more?)
- What the first and last code per table are (anchor codes for verification)
- Any structural quirks (note text before tables, multi-line descriptions, out-of-order entries)

This mapping is the spec for the extraction script. Do not skip it.

### 2. Always use two independent extraction methods

Confidence comes from agreement between methods that share no code path:

- **Method A — pdfplumber table extraction:** `page.extract_tables()` returns structured rows. Good at preserving column separation but can merge cells or miss rows.
- **Method B — independent verification:** Choose the best alternative based on the document's structure (see Method B selection below). The point is independence — if both methods produce the same codes, the extraction is correct.

### 3. Always normalise to 8-digit HS codes

Official documents mix code lengths freely. Always produce an `hs_8digit` column:

```python
HTSUS_PATTERN = re.compile(r"^\d{4}(\.\d{2}(\.\d{2,4}(\.\d{2,4})?)?)?$")

def htsus_to_hs8(code: str) -> str:
    digits = code.replace(".", "")
    return digits[:8] if len(digits) >= 8 else digits.ljust(8, "0")
```

| Input | Output |
|-------|--------|
| `7206` | `72060000` |
| `7302.10` | `73021000` |
| `7216.10.00` | `72161000` |
| `7216.91.00.10` | `72169100` |

### 4. Descriptions embed HS codes — never extract from raw text alone

Descriptions frequently reference other codes: "of heading 8471", "of subheading 9014.80.50". Method A handles this naturally (column separation). Method B must also isolate first-column content — see below.

### 5. Continuation rows need merging

Multi-line descriptions have the code only on the first row. Subsequent rows have an empty code cell. Merge by appending description text to the previous row.

### 6. Monotonicity is a warning, not a constraint

Official documents sometimes list codes out of order. Flag for review but do not reject the data.

## Choosing Method B

Select based on the document's structure. The goal is an extraction path independent of Method A.

| Document Structure | Best Method B | Why |
|--------------------|---------------|-----|
| **Single table, clean layout** | Regex on `page.extract_text()` with `^` line-start anchoring | Simple and effective when text extraction preserves line boundaries |
| **Multiple tables, or descriptions containing HS codes** | Word-level bbox extraction via `page.extract_words()` with x-coordinate threshold | Reliably separates first-column codes from description-embedded mentions |
| **OCR'd or scanned PDF** | Regex on text with aggressive false-positive filtering | Table extraction may fail; text extraction with post-hoc validation is more robust |
| **Well-structured table with scope/notes columns** | Regex on text, then reconcile column count against Method A | Extra columns make table extraction the primary method; regex serves as code-count check |

### Word-level bbox extraction (when needed)

Use `page.extract_words()` to get each word's x-coordinate. Set a threshold between the code column and description column:

```python
# Determine threshold by inspecting a sample page:
for w in page.extract_words()[:30]:
    print(f'x={w["x0"]:6.1f} text={w["text"]}')

# Typically: codes at x < 120, descriptions at x > 150
# Set threshold conservatively BELOW the minimum description x
FIRST_COL_MAX = 140.0  # adjust per document
```

This is NOT always needed. For single-table PDFs where `extract_text()` puts codes on their own lines, a simple regex is sufficient and preferred.

## Step-by-Step Process

### Step 1: Read and map the PDF

Read all pages. Produce a table inventory:

```
Document: S232 Metals Proclamation (42 pages, Annex IV ignored)

Table 1: Annex I-A Steel (pp.1-2)
  Columns: code | description
  First: 7206, Last: 7306, ~35 rows

Table 2: Annex I-A Steel Derivatives (pp.2-8)
  Columns: code | description
  First: 7216.91.00.10, Last: 7614.10.10, ~139 rows
  ...
```

### Step 2: Build the extraction script

Create `code/parse_{document_name}.py` with:

1. **Constants:** PDF path, output directory, date prefix, page ranges per section
2. **TableSpec:** dataclass with section name, category, expected first/last codes
3. **Method A:** pdfplumber table extraction with continuation row merging
4. **Method B:** chosen verification method (see selection table above)
5. **Verification checks:** 7 checks per table
6. **CSV writer:** semicolon-delimited output

Adapt the architecture to the document. A single-table PDF needs no section detection. A multi-table PDF with header rows needs header detection logic. Do not blindly copy the S232 parser's multi-row header state machine if the document has simpler structure.

Run with: `uv run --with pdfplumber python3 code/parse_{name}.py`

### Step 3: Verification checks (7 per table)

| # | Check | Pass Condition | Severity |
|---|-------|----------------|----------|
| 1 | Row count agreement | Method A count == Method B count | FAIL |
| 2 | Format validation | All codes match HTSUS_PATTERN; all hs_8digit are 8 digits | FAIL |
| 3 | Monotonicity | Codes non-decreasing within table | WARNING |
| 4 | Description completeness | No empty descriptions; no header text contamination | FAIL |
| 5 | Page boundary spot checks | First/last code per page printed for manual review | INFO |
| 6 | Dual-method comparison | Positional HS8 match between Method A and B | FAIL |
| 7 | Anchor code verification | First and last code match manually observed values | FAIL |

### Step 4: Iterate until all FAIL checks pass

Common issues and fixes:

- **Method B count mismatch:** If using bbox extraction, adjust the x-threshold. Inspect word positions on the failing page.
- **Method B missing sub-tables:** Header detection not working. Check how headers render with `extract_words()` — they may span multiple rows or have unexpected x-positions.
- **Description contamination:** Header rows leaking into data. Add the header text to the filter list.
- **Anchor code mismatch:** Re-read the PDF to verify expected first/last codes.

### Step 5: Write CSVs

Output to `data/` with date prefix: `{YYMMDD}_{document}_{section}_{category}.csv`

## Output Format

```csv
htsus;description;hs_8digit
7206;Iron and nonalloy steel in ingots or other primary forms;72060000
```

- Delimiter: semicolon (`;`)
- Encoding: UTF-8
- Descriptions: collapsed to single line, multiple spaces normalised
- Additional columns (scope, notes) preserved if present in the source table

## Complexity Tiers

Not every PDF needs the full multi-method architecture. Scale the approach:

| Document Complexity | Approach |
|--------------------|----------|
| **Simple:** single table, clean formatting, <100 rows | Method A + regex Method B. Minimal script. |
| **Medium:** single table with continuation rows, 100-500 rows | Method A with row merging + regex Method B. Standard verification. |
| **Complex:** multiple tables within one PDF, mixed code formats, 500+ rows | Full architecture: page ranges, header detection, TableSpec anchors, bbox Method B. |

## Document-Specific Patterns

These patterns have been encountered in practice. Use as reference when the PDF matches the type.

### Multi-table PDFs with section headers

Some PDFs contain several tables separated by header rows (e.g. "Steel", "Aluminum"). Headers may span multiple PDF lines. Handle with a state machine that tracks the current category and updates it when header words appear.

### PDFs with scope/limitation columns

Some tables have 3+ columns (code, description, scope). Method A captures all columns. Method B should still focus on code extraction only for cross-validation.

### PDFs with note text before tables

Proclamations often have legal note paragraphs before the table starts. These contain words that look like codes but are not data. Method A naturally skips these (they are not in table elements). For Method B, use page ranges or y-coordinate filtering to skip pre-table text.

## Debugging Toolkit

**Inspect word positions on a page:**
```python
uv run --with pdfplumber python3 -c "
import pdfplumber
pdf = pdfplumber.open('path/to/file.pdf')
page = pdf.pages[PAGE_IDX]
for w in page.extract_words()[:30]:
    print(f'x={w[\"x0\"]:6.1f} top={w[\"top\"]:6.1f} text={w[\"text\"]}')
pdf.close()
"
```

**Find all code-like words in first column:**
```python
import re
HTSUS = re.compile(r'^\d{4}(\.\d{2}(\.\d{2,4}(\.\d{2,4})?)?)?$')
for w in page.extract_words():
    if w['x0'] < FIRST_COL_MAX and HTSUS.match(w['text']):
        print(f'x={w["x0"]:6.1f} top={w["top"]:6.1f} text={w["text"]}')
```

**Check how a table header renders:**
```python
# Find words in the header area (adjust y-range to area between note text and first code)
for w in page.extract_words():
    if START_Y < w['top'] < END_Y:
        print(f'x={w["x0"]:6.1f} top={w["top"]:6.1f} text={w["text"]}')
```

## Reference Implementations

| Document | Script | Complexity | Tables | Rows |
|----------|--------|-----------|--------|------|
| S122 Annex II | `parse_s122_annex2.py` | Medium (single table, 3 columns) | 1 | ~700 |
| S232 Metals Annexes | `parse_s232_metals.py` | Complex (12 tables, multi-row headers, variable column positions) | 12 | 985 |

Both are in `us-tariff-barrier-estimates/code/`. Study the one closest to your document's complexity before writing a new parser.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|-------------|------------------|
| Writing code before reading the PDF | Assumptions about structure are wrong | Always map tables, columns, code formats first |
| Trusting Method A alone without verification | Table extraction can miss rows or merge cells | Cross-validate with an independent Method B |
| Using word-level bbox when simple regex works | Over-engineering adds complexity and fragility | Match method complexity to document complexity |
| Hardcoding row counts for verification | Counts change between document versions | Use anchor codes (first/last) instead |
| Rejecting out-of-order entries as errors | Official documents have legitimate ordering quirks | Treat monotonicity as WARNING after checking PDF |
| Copy-pasting S232 parser's header state machine | Most documents have simpler or different table structure | Adapt the architecture to what the PDF actually contains |
