---
name: prepare-document
description: Convert a PDF policy document to structured markdown for classification. Identifies country chapters, section headers, and preserves quoted text. Use when user says "prepare the document", "convert this PDF", "set up the NTE for extraction", or provides a PDF to classify. Must run before extract-classify.
---

# Prepare Document

Convert a source PDF into structured markdown for the extract-classify skill.

## Steps

### 1. Read the PDF

Read in 20-page chunks using the Read tool with `pages` parameter. Start with the table of contents to understand structure.

### 2. Identify Structure

| Document Type | Heading Pattern |
|---------------|----------------|
| Country chapters (NTE, TPR) | `### **COUNTRY**` → `#### **Section**` |
| Thematic sections | `### **Theme**` → `#### **Country**` |
| Instrument catalogue | `### **Sector**` → `#### **Instrument**` |

### 3. Write Markdown

Output to `data/{document_name}.md` with:
- `###` for top-level divisions (countries/themes)
- `####` for sub-sections
- Bold names: `### **COUNTRY NAME**`
- Paragraph breaks between paragraphs
- Verbatim preservation of quoted text
- Optional page markers: `<!-- page N -->`

### 4. Validate

Run: `python scripts/check_structure.py --input data/output.md`

Report to user: total lines, word count, number of top-level sections, number of sub-sections.

### 5. Create Project Config

If `project-config.json` doesn't exist, create from `templates/project-config.json` with the document path pre-filled.

## Example

User provides `NTE-Report-2025.pdf`:

1. Read pages 1-5 (table of contents) → identify 57 country chapters
2. Read pages 6-25, write Algeria through Cambodia
3. Continue in 20-page chunks until complete
4. Validate: "22,000 lines, 380,000 words, 57 country sections, 285 sub-sections"
5. Create `project-config.json` with `document_path: "data/nte_2025_full.md"`

## Troubleshooting

**Headers/footers repeated in text:** Clean these during conversion — remove running headers, page numbers, and repeated document titles.

**Columns merged:** Some PDFs have two-column layout. If text from columns is interleaved, read page by page and manually reconstruct paragraph order.

**Truncated output:** For 500+ page PDFs, write incrementally after each 20-page chunk. Verify the last section is complete.
