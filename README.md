# cc-data-science-team — Data Science Plugin (Claude Code + Coworker)

Structured document classification, version comparison, external database matching, and analytical workflows. Works as both a Claude Code config (via symlinks) and a Claude Coworker plugin (via `.claude-plugin/` manifest).

## Contents

| Directory | Count | Purpose |
|-----------|-------|---------|
| `skills/` | 8 | Document preparation, theme discovery, extraction, audit, dedup, version comparison, external matching, cross-document comparison |
| `agents/` | 5 (plugin) + 7 (CC) | Plugin: orchestrator, extractor, comparator, matcher, analyst. CC: analytics-manager, data-analyst, etc. |
| `hooks/` | 1 | Guardrails: source span validation on extraction writes |
| `rules/` | 5 | CC: r-code-standards, data-handling, chart-creation, etc. |
| `protocols/` | 5 | CC: applied-econometrics, causal-inference, data-visualization, etc. |
| `commands/` | 3 | CC: `/query-gta`, `/analytics-ready`, `/red-team` |
| `templates/` | 3 | Configurable project templates (themes, config, output schema) |
| `examples/` | 4 | NTE themes, NTE project config, MAST taxonomy, counting rules |

## Installation — Claude Coworker (Plugin)

```bash
git clone git@github.com:global-trade-alert/cc-data-science-team.git
claude plugin add ./cc-data-science-team
```

## Installation — Claude Code (Symlinks)

```bash
git clone git@github.com:global-trade-alert/cc-data-science-team.git .claude-ds
mkdir -p .claude/agents .claude/rules .claude/protocols .claude/commands
for f in .claude-ds/agents/*.md; do ln -s "../../$f" .claude/agents/; done
ln -s ../../.claude-ds/rules .claude/rules/data-science
for f in .claude-ds/protocols/*.md; do ln -s "../../$f" .claude/protocols/; done
for f in .claude-ds/commands/*.md; do ln -s "../../$f" .claude/commands/; done
```

## Skills

| Skill | What It Does |
|---|---|
| `prepare-document` | Convert PDF to structured markdown |
| `discover-themes` | Identify a document's internal taxonomy and propose categories |
| `extract-classify` | Classify document sections against a user-defined tagging schema |
| `audit-entries` | Red-team review against configurable audit dimensions |
| `dedup-entries` | Deduplicate entries within section-category pairs |
| `compare-versions` | Diff two editions of the same document (NEW/REMOVED/CHANGED/UNCHANGED) |
| `match-external` | Match entries against an external database, attach IDs, flag coverage gaps |
| `compare-documents` | Cross-check claims in one document against evidence in another |

## Agents

| Agent | Role |
|---|---|
| `orchestrator` | Plans workflow, checks inputs, delegates to specialists. Read-only. |
| `extractor` | Executes extraction and classification. Runs validation scripts after each batch. |
| `comparator` | Compares versions or cross-references. Produces diffs and statistics. |
| `matcher` | Queries external databases. Attaches IDs, flags gaps. |
| `analyst` | Produces summaries and memos from completed data. Every claim cites a row. |

## Quick Start

1. `/data-science-team:prepare-document` — convert PDF to markdown
2. `/data-science-team:discover-themes` — identify or define categories
3. Configure `project-config.json` with your inclusion criteria, output fields, and audit dimensions
4. `/data-science-team:extract-classify` — extract and tag section by section
5. `/data-science-team:audit-entries` — quality review
6. `/data-science-team:dedup-entries` — consolidate duplicates
7. `/data-science-team:compare-versions` — diff against a prior edition (optional)
8. `/data-science-team:match-external` — link to an external database (optional)
9. `/data-science-team:compare-documents` — cross-check against a different source (optional)

## Examples

`examples/` contains a complete NTE trade-policy configuration:
- `nte-2025-themes.json` — 10 Section 301 investigation themes
- `nte-project-config.json` — trade-policy-specific inclusion criteria, audit dimensions, and custom fields
- `mast-taxonomy.md` — MAST intervention type reference
- `counting-rules.md` — named vs unnamed state act methodology

These show how to fill in the generic templates for a specific domain.

## License

Private — shared within team only.
