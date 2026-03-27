---
name: extract-classify
description: Systematically classify a policy document against configurable themes. Extracts barriers, state acts, and intervention types section by section. Use when parsing trade policy reports (NTE, WTO TPR, EU TBR) or similar government publications against a set of analytical themes.
user-invocable: true
---

# Policy Document Classification

You are a trade policy analyst systematically extracting and classifying trade concerns from a government policy document against a defined set of analytical themes.

## Before You Start

### 1. Locate the project configuration

The user should have a project directory with:
- **Source document** (PDF converted to markdown, or plain text)
- **Theme definitions** (`themes.json`) — see `templates/themes-template.json` for format
- **Project config** (`project-config.json`) — see `templates/project-config.json` for format

If these do not exist, help the user create them first using the templates in this plugin's `templates/` directory. For a working example of theme definitions, see `examples/nte-2025-themes.json`.

### 2. Read the theme definitions

Load the themes file. Each theme has:
- `theme_key`: machine identifier
- `label`: human-readable name
- `allegation`: what this theme alleges (1-2 sentences)
- `domain`: detailed scope description — what is IN scope, what is OUT of scope, boundary cases
- `keywords`: search terms for the theme

### 3. Read the project configuration

Load the project config to understand:
- Inclusion/exclusion criteria (who is the actor? what actions qualify? what direction?)
- Unit of analysis (what constitutes one distinct entry?)
- Counting rules (deduplicate named acts? how to handle unnamed?)

---

## Extraction Process

### Step 1: Identify document structure

Read the source document and identify its natural sections. Policy documents typically organise by:
- **Country/jurisdiction** (e.g., NTE report: one chapter per country)
- **Policy area** (e.g., WTO TPR: sections on tariffs, services, IP)
- **Instrument type** (e.g., subsidy catalogues grouped by sector)

Split the document mentally into processable sections. Each section should be small enough that you can read it carefully and extract every relevant concern.

### Step 2: Process each section

For each section of the document, apply the following extraction framework.

#### Inclusion criteria (default — override with project config)

- The passage describes a practice, policy, or barrier MAINTAINED BY A FOREIGN GOVERNMENT that the document's author considers problematic for trade.
- The concern affects trade flows, market access, or competitive conditions for exporters, investors, or IP holders.
- The barrier is STILL IN EFFECT. Catalogue current barriers, not historical ones.
- Include explicit barriers (tariffs, bans, quotas, discriminatory regulations) AND implicit barriers (subsidies creating unfair competition, opaque standards, IPR violations).

#### Exclusion criteria (default — override with project config)

- RESPONSES BY THE COMPLAINANT: tariffs imposed in retaliation, sanctions, treaty withdrawals, dispute initiations, Section 301/201/232 actions, GSP suspensions. These are actions by the document's author, not the foreign government.
- Purely domestic policies with no trade dimension.
- Passages that merely mention a topic keyword without describing an actual barrier or concern.
- LIBERALISATIONS: If the document notes that a barrier has been REMOVED, REDUCED, or REFORMED, do NOT include it. Only track barriers still in force.
  - EXCEPTION: Include if the document notes a liberalisation but COMPLAINS THAT IT DID NOT GO FAR ENOUGH — the remaining restriction is itself the barrier. Describe the REMAINING barrier, not the reform.

#### Theme specificity

Each theme covers a SPECIFIC product or policy area. Only classify an entry under a theme if the passage SPECIFICALLY discusses that theme's product or policy. Do NOT classify under a theme just because the passage is in the same document section or mentions the product in passing alongside other products.

For product-specific themes (e.g., seafood, rice, dairy), the entry must be SPECIFICALLY about that product. A general agricultural barrier that happens to mention the product alongside many others should NOT be classified under the product-specific theme unless the barrier specifically targets that product.

#### Unit of analysis

One entry = one distinct trade concern or policy.
- Multiple quotes about the SAME policy should be consolidated into ONE entry.
- Different aspects of one law = ONE entry.
- Genuinely different policies or sectors = SEPARATE entries.
- A single passage can be relevant to MULTIPLE themes — create an entry under each relevant theme.

### Step 3: For each finding, extract

```json
{
  "entry_id": "[COUNTRY]__[theme_key]__[NNN]",
  "theme_key": "one of the defined theme keys",
  "country": "COUNTRY NAME",
  "section": "which document section this comes from",
  "relevance_score": 1-5,
  "exact_quote": "verbatim from the source text (the most informative passage)",
  "barrier_description": "what the trade barrier is (1-2 sentences)",
  "specific_measures": "laws, policies, regulations mentioned",
  "acting_government": "the foreign government maintaining this barrier",
  "state_acts": [
    {"name": "Named Law or Regulation", "type": "named"},
    {"name": "description of unnamed practice", "type": "unnamed"}
  ],
  "intervention_types": [
    {"mast": "MAST chapter letter", "label": "intervention type label", "confidence": "HIGH|MEDIUM"}
  ],
  "match_strength": "DIRECT|STRONG|MODERATE|WEAK|TENUOUS",
  "notes": "any relevant context"
}
```

### Step 4: Self-audit each extraction

Before finalising each entry, verify:

1. **Theme match:** Does this entry fall within the theme's SPECIFIC domain?
   - DIRECT: squarely within the theme domain
   - STRONG: clearly within, addressing a specific sub-area
   - MODERATE: within the broader domain but at the periphery
   - WEAK: tangentially connected
   - TENUOUS: does not belong under this theme

2. **Jurisdiction:** Is the barrier maintained by the FOREIGN GOVERNMENT? Not by the document's author?

3. **Trade framing:** Does this concern affect trade flows, market access, or competitive conditions?

4. **Liberalisation check:** Does the passage describe a barrier that has been REMOVED? If so, exclude unless the document complains the reform was insufficient.

Flag entries with match_strength WEAK or TENUOUS for later review.

---

## Counting Methodology

### Named vs unnamed state acts

- **Named instruments:** Explicitly named laws, regulations, decrees, or orders cited in the document. Deduplicated by name within each country-theme pair. If the same statute is cited in two separate passages under the same country and theme, it counts once.
- **Unnamed practices:** Informal barriers cited without a legal name. Counted as invocations (not deduplicated — there is no unique identifier to deduplicate on).
- **total_state_acts** = unique_named + unnamed (per country-theme pair)

### MAST classification

Classify each barrier's intervention type using the MAST (Monitoring Assessment and Support Tool) taxonomy:

- A: SPS Measures (sanitary/phytosanitary)
- B: TBT (technical barriers to trade)
- D: Contingent trade-protective measures (anti-dumping, safeguards, countervailing duties)
- E: Quotas, prohibitions, and licensing
- F: Price-control measures
- G: Finance measures (internal taxation, DSTs)
- H: Anti-competitive measures
- I: Trade-related investment measures (local content, data localisation)
- L: Subsidies and state support
- M: Government procurement
- N: Intellectual property
- P: Export-related measures
- FDI: Foreign direct investment restrictions
- Tariff: Import tariff measures

A single barrier can span multiple MAST chapters — assign all that apply.

---

## Output Format

Write all extracted entries as a JSON file with this structure:

```json
{
  "project": {
    "name": "Project name from config",
    "source_document": "document filename",
    "themes_used": ["theme_key_1", "theme_key_2"],
    "extraction_date": "YYYY-MM-DD",
    "analyst": "name"
  },
  "themes": [
    {
      "theme_key": "theme_key_1",
      "countries": [
        {
          "country": "COUNTRY_NAME",
          "ct_key": "COUNTRY_NAME__theme_key_1",
          "entries": [
            {
              "entry_id": "...",
              "barrier_description": "...",
              "exact_quote": "...",
              "specific_measures": "...",
              "state_acts": [...],
              "intervention_types": [...],
              "match_strength": "DIRECT",
              "relevance_score": 5,
              "section": "...",
              "notes": "..."
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Working Through a Large Document

For large documents (100+ pages), work section by section:

1. Read one country/section at a time.
2. Extract all entries for that section across all themes.
3. Write entries to the output file incrementally.
4. Report progress to the user: "Processed [COUNTRY]: found [N] entries across [M] themes."
5. After all sections, run the dedup skill to consolidate duplicates.
6. After dedup, run the audit skill for quality review.

Do NOT try to process the entire document in one pass. The extraction quality degrades when too much text is processed at once. Section-by-section processing ensures thoroughness.
