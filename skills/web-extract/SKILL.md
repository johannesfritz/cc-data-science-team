---
name: web-extract
description: Stub. Reserved Layer-3 orchestrator for the data-science framing of web ingestion — URL list → fetch → schema-validated structured output for downstream analysis pipelines. Build when first concrete consumer arrives.
allowed-tools: Bash, Read, Write
---

# web-extract (stub)

**Status:** v1 stub. Build when a concrete data-science consumer materialises (analytics pipeline, monitoring feed, dataset enrichment, etc.).

This is a placeholder for the data-science framing of the web-fetch + schema-validated extraction loop. It mirrors `cc-writing-team/skills/web-research` (optional companion — research framing) on the opposite side of the same primitive.

## What it will do

- Accept a list of URLs (or a query that produces them via WebSearch)
- Invoke the cc-os Layer-1 primitive (required companion — `cc-os/scripts/fetch-source.py`) for each
- Run a schema-validated extraction pass (Pydantic / Gemini structured output) against the fetched markdown
- Emit a tabular dataset (CSV / Parquet / JSON-Lines) for downstream analysis pipelines
- Cache fetched markdown and extracted records on disk; deduplicate URLs

## Provenance

Reserved 2026-05-03 in JCC-731 (Bucket B+C capability extensions plan). Plan rationale (required companion: cc-os): URL → markdown is the same primitive for writing-research and data-extraction, but the orchestrators are framed differently — research = quotes/credibility/sources; extraction = schema/validation/dataset rows. Two distinct skills, one shared cc-os primitive.

## How to invoke today

Until this is built, agents that need URL → structured data should:

1. Use the cc-os `web-fetch` skill directly (required companion):
   ```bash
   # When cc-os is installed in the workspace (canonical jf-private layout):
   python3 ${CLAUDE_PROJECT_DIR}/.claude/shared-scripts/fetch-source.py "<url>"
   ```
2. Run an LLM extraction pass against the resulting markdown using whatever schema fits the task (typically Pydantic + Gemini `gemini-3.1-pro-preview` per `cc-os/rules/environment-and-models.md` — required companion).
3. Validate and write to your own dataset.

## When to build

Triggered when **any** of these surface a concrete need:

- A monitoring pipeline ingests URLs that don't fit the `gta-submit` / `dpa-submit` shapes
- An analytics project needs per-row enrichment from web sources
- A dataset task asks "given these URLs, extract structured fields X, Y, Z"

When the trigger arrives: replace this stub with a real SKILL.md, add the schema definition file, and wire the cache + dedup logic.
