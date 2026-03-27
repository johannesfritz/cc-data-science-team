# cc-data-science-team — Data Science Configs (Claude Code + Coworker)

Team configuration for data science workflows: policy document classification, analytics orchestration, R code standards, applied econometrics, causal inference, and statistical review.

This repo works as both a **Claude Code** config (via symlinks) and a **Claude Coworker** plugin (via `.claude-plugin/` manifest).

## Contents

| Directory | Count | Purpose |
|-----------|-------|---------|
| `skills/` | 4 | **Coworker skills:** prepare-document, extract-classify, audit-entries, dedup-entries |
| `agents/` | 7 | analytics-manager, data-analyst, statistical-reviewer, etc. |
| `rules/` | 5 | r-code-standards, data-handling, chart-creation, etc. |
| `protocols/` | 5 | applied-econometrics, causal-inference, data-visualization, etc. |
| `commands/` | 3 | `/query-gta`, `/analytics-ready`, `/red-team` |
| `templates/` | 3 | Configurable project templates for document classification |
| `examples/` | 1 | NTE 2025 Section 301 themes (working example) |

## Installation — Claude Coworker (Plugin)

```bash
git clone git@github.com:global-trade-alert/cc-data-science-team.git
claude plugin add ./cc-data-science-team
```

Available skills:
- `/data-science-team:prepare-document` — Convert a PDF to structured markdown for classification
- `/data-science-team:extract-classify` — Classify a policy document against configurable themes
- `/data-science-team:audit-entries` — Red-team review of extracted entries
- `/data-science-team:dedup-entries` — Deduplicate entries within country-theme pairs

## Installation — Claude Code (Symlinks)

```bash
git clone git@github.com:global-trade-alert/cc-data-science-team.git .claude-ds
mkdir -p .claude/agents .claude/rules .claude/protocols .claude/commands
for f in .claude-ds/agents/*.md; do ln -s "../../$f" .claude/agents/; done
ln -s ../../.claude-ds/rules .claude/rules/data-science
for f in .claude-ds/protocols/*.md; do ln -s "../../$f" .claude/protocols/; done
for f in .claude-ds/commands/*.md; do ln -s "../../$f" .claude/commands/; done
```

## Policy Document Classification Workflow

The extraction skills port a proven methodology for systematically classifying policy documents against analytical themes. Originally developed for the USTR National Trade Estimate report, it generalises to any structured policy document.

### Quick start

1. Run `/data-science-team:prepare-document` to convert your PDF to structured markdown
2. Copy `templates/themes-template.json` and define your themes (or use `examples/nte-2025-themes.json` as a starting point)
3. Copy `templates/project-config.json` and set your inclusion/exclusion criteria
4. Run `/data-science-team:extract-classify` to classify the document section by section
5. Run `/data-science-team:audit-entries` to quality-check the extractions
6. Run `/data-science-team:dedup-entries` to consolidate duplicate entries

### Output

A structured JSON dataset with entries classified by theme, country, match strength, named/unnamed state acts, and MAST intervention types. See `templates/output-schema.json` for the full schema.

## License

Private — shared within team only.
