---
name: prepare-document
description: Convert a PDF policy document to structured markdown for classification. Reads the PDF directly, identifies document structure (country chapters, section headers), and outputs clean markdown with proper heading hierarchy. Use before extract-classify.
user-invocable: true
---

# Prepare Document for Classification

Convert a source PDF into structured markdown suitable for the extract-classify skill.

## Why This Step Matters

The extract-classify skill works section by section through a document. Clean markdown with consistent heading hierarchy makes extraction more accurate and lets the classifier identify country boundaries, section breaks, and content structure reliably.

## Process

### Step 1: Read the PDF

Read the source PDF file. If it is large (100+ pages), read it in page ranges (e.g., pages 1-20, then 21-40). The Read tool supports PDF files with a `pages` parameter.

### Step 2: Identify the document structure

Policy documents typically follow one of these structures:

| Structure | Example | Heading Hierarchy |
|-----------|---------|-------------------|
| **Country chapters** | NTE Report, WTO TPR | `### **COUNTRY**` → `#### **Section**` |
| **Thematic sections** | EU Trade Barriers Regulation | `### **Theme**` → `#### **Country**` |
| **Instrument catalogue** | Subsidy inventories | `### **Sector**` → `#### **Instrument**` |
| **Mixed** | OECD reviews | Varies — identify the primary organising principle |

Determine which structure applies and note it for the user.

### Step 3: Convert to markdown

Write the full document as a markdown file, preserving:

1. **Heading hierarchy** — use `###` for top-level divisions (countries or themes), `####` for sub-sections, `#####` for sub-sub-sections. Reserve `#` and `##` for document-level titles.

2. **Bold country/section names** — wrap in `**` for reliable regex matching: `### **COUNTRY NAME**`

3. **Paragraph breaks** — separate paragraphs with blank lines. Do not run paragraphs together.

4. **Quoted text** — preserve any text that appears as a direct quote or citation. These are critical for the exact_quote field in extraction.

5. **Footnotes and references** — preserve at the end of each section or at the document end.

6. **Tables** — convert to markdown tables where possible. If a table is too complex, describe its content in prose.

7. **Page numbers** — optionally add page markers (`<!-- page N -->`) at page boundaries. These help the extract-classify skill record which page a finding came from.

### Step 4: Validate the output

After writing the markdown file:

1. **Check heading count** — count `###` headings. For an NTE-style report with 50+ countries, you should see 50+ country headers.
2. **Check for truncation** — verify the last country/section is complete. Large PDFs may need multiple read passes.
3. **Spot-check a mid-document section** — read one section from the middle and compare against the PDF to verify content fidelity.
4. **Report statistics** — tell the user: total lines, total words, number of top-level sections identified, number of sub-sections.

### Step 5: Write the project configuration

If a `project-config.json` does not yet exist in the project directory, create one from the template. Pre-fill:
- `document_path`: the markdown file just created
- `document_type`: inferred from the document structure

## Output

- `data/{document_name}.md` — the structured markdown
- Optionally: `data/{document_name}_pages.json` — page-level metadata (page number → line range mapping)

## Tips for Large Documents

- The NTE Report is ~500 pages. Read in 20-page chunks and write incrementally.
- If the document has a table of contents, read that first to understand the structure before processing the body.
- Some PDFs have messy extraction (headers/footers repeated, columns merged). Clean these up during conversion — the extraction skill assumes clean text.

## Example: NTE Report Structure

The USTR National Trade Estimate Report organises as:

```
# National Trade Estimate Report on Foreign Trade Barriers 2025

## [Preamble / Executive Summary]

### **ALGERIA**
#### **Trade Barriers**
[content...]
#### **Intellectual Property Protection**
[content...]

### **ARGENTINA**
#### **Import Policies**
[content...]
```

Each `### **COUNTRY**` header marks a country chapter boundary. The extract-classify skill uses these boundaries to process one country at a time.
