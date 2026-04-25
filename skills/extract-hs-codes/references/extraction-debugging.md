# Extraction debugging toolkit + anti-patterns

Reference material extracted from `extract-hs-codes/SKILL.md` to keep the main body focused on workflow. Read this when a parse run is failing or producing suspicious output.

## Inspecting word positions on a page

When `Method B` (bbox extraction) miscounts rows, the column threshold is usually wrong. Print word positions to find the real column boundary:

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

Set `FIRST_COL_MAX` conservatively below the minimum description-column x-position observed in the output.

## Finding code-like words in the first column

Useful when the parser is missing rows — confirms whether the codes are even reachable via bbox extraction:

```python
import re
HTSUS = re.compile(r'^\d{4}(\.\d{2}(\.\d{2,4}(\.\d{2,4})?)?)?$')
for w in page.extract_words():
    if w['x0'] < FIRST_COL_MAX and HTSUS.match(w['text']):
        print(f'x={w["x0"]:6.1f} top={w["top"]:6.1f} text={w["text"]}')
```

If this prints fewer codes than the PDF visually contains, the threshold is too low or the codes render with extra leading whitespace.

## Inspecting how a table header renders

Header detection failures usually come from headers spanning multiple lines or rendering with unexpected x-positions. Check the y-range between note text and the first code row:

```python
for w in page.extract_words():
    if START_Y < w['top'] < END_Y:
        print(f'x={w["x0"]:6.1f} top={w["top"]:6.1f} text={w["text"]}')
```

## Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Method B count < Method A count | Column threshold too high; some codes filtered out | Lower `FIRST_COL_MAX` after inspecting word positions |
| Method B includes description-embedded codes | Threshold too low; description text leaks in | Raise `FIRST_COL_MAX` |
| Header rows appearing in data rows | Header detection not triggered | Check word positions in header band; add header text to filter list |
| Anchor code mismatch | Expected first/last codes wrong | Re-read the PDF to verify the ground truth |
| Empty descriptions | Continuation row merging broken | Confirm `extract_tables()` returns expected row count; merge logic may be eating rows |

## Anti-patterns observed in past runs

These come from real failures encountered in `cc-data-science-team` parses. Each rule has a *why* — apply it because the explanation matches your situation, not because the rule says so.

| Anti-pattern | Why it produces bad data | Better approach |
|--------------|--------------------------|-----------------|
| Writing the parser before reading the PDF | Structure assumptions diverge from reality; you discover them only via failed verification | Map tables, columns, and code formats first (Step 1 in SKILL.md) |
| Trusting Method A alone | `extract_tables()` can silently merge cells or skip rows when the PDF's table grid is irregular | Cross-validate with Method B; agreement between independent code paths is the confidence signal |
| Reaching for word-level bbox when regex on `extract_text()` would work | Bbox adds threshold-tuning complexity that brittles on document variations | Match method complexity to document structure (see Method B selection table) |
| Hardcoding expected row counts | Document versions add or remove rows; the parser becomes false-positive-prone | Use anchor codes (first/last per table) — they're more stable than counts |
| Rejecting out-of-order codes | Official documents legitimately list codes out of order in some sections | Treat monotonicity as WARNING; flag for review but keep the data |
| Copy-pasting the S232 multi-row header state machine | Most documents have simpler or differently-shaped headers; the state machine doesn't transfer | Adapt the architecture to what the PDF actually contains, starting from the simpler reference parsers |
