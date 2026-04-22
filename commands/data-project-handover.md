---
description: "Prepare a complete handover package so a colleague can review results and iterate on the methodology using Claude Coworker with the data-"
---

Prepare a complete handover package so a colleague can review results and iterate on the methodology using Claude Coworker with the data-science-team plugin.

Usage: /data-project-handover [project-folder]
Example: /data-project-handover 260212-dpa-oecd-matching
Example: /data-project-handover .

If no project-folder is given, use the current working directory.

## What This Command Does

Creates a self-contained zip that a colleague can unpack and immediately start working with in Claude Coworker. The zip includes the full project folder, credentials, documentation, and replication prompts — everything except the plugin itself (which is already installed in their environment).

---

## Phase 1: Project Audit

### 1.1 Identify project structure

Read the project folder and catalogue:
- All scripts (Python, R) with their execution order
- All data files (input, intermediate, output)
- All result files (Excel, CSV, PNG, markdown reports)
- Existing documentation (PLAN.md, METHODOLOGY.md, STATE.md, process-log.md, progress_log.md)
- Source data files (the original input the pipeline starts from)

### 1.2 Reconstruct the pipeline

For each script, identify:
- **Imports and dependencies** (Python packages, R libraries)
- **External API calls** (OpenAI, Gemini, database connections, MCP tools)
- **Key parameters** (model names, thresholds, filter values, batch sizes, temperature settings) — record file path, line number, variable name, and current value
- **Input/output files** (what each script reads and writes)
- **LLM prompt templates** (system prompts, user prompt structures)

Build a pipeline dependency graph: which scripts must run in what order.

### 1.3 Identify credentials needed

Scan scripts for:
- `load_dotenv` / `os.getenv` calls — which env vars are required
- Database connection strings
- API client initialisations

Check which `.env` files exist in the project tree and up to the workspace root (`jf-thought/.env`, `jf-private/.env`). Collect the required variables and their current values.

### 1.4 Check for hardcoded paths

Scan all scripts for absolute paths (e.g. `/Users/<name>/...` / `$HOME/...`). These must be patched in the zip so the scripts find `.env` from the project root first.

---

## Phase 2: Plugin Coverage Check

### 2.1 Map methods to plugin capabilities

For each method used in the project, verify it is covered by the plugin:

| Method | Plugin Coverage |
|--------|----------------|
| Database queries (SQL) | `database-specialist` agent |
| Python/R data processing | `data-analyst` agent |
| LLM-augmented matching/classification | `llm-augmented-analysis.md` rule |
| Fuzzy string matching | `data-handling.md` rule (tiered matching) |
| TF-IDF / sklearn | `data-analyst` agent (Python execution) |
| Cross-model verification | `llm-augmented-analysis.md` rule |
| Excel output generation | `data-analyst` agent |
| Statistical sanity checks | `statistical-reviewer` agent + `statistical-sanity.md` protocol |

If a method is NOT covered by any existing plugin capability, flag it as a gap and report to the user before proceeding.

### 2.2 Check for existing playbook

Look in the plugin root (`cc-data-science-team/`) for a `playbook-*.md` file matching this project. If one exists, check if it is up to date with the current scripts.

### 2.3 Create or update playbook

If no playbook exists, or the existing one is stale:

1. Create `playbook-{project-name}.md` in the plugin root following the conventions of `playbook-nte-dpa-analysis.md`:
   - Prerequisites section (plugin, dependencies, credentials)
   - Note about hardcoded paths if any
   - Exercise 1: Review existing results (always)
   - Exercise 2+: One exercise per meaningful modification axis (e.g. change filters, change model, change prompts, re-run on updated data)
   - Each exercise has "What you prompt" sections with copy-paste prompts
   - Each exercise has a "What to change" table (file, line, variable, current value)
   - Tips section (efficiency, quality control, troubleshooting, pipeline dependencies)

2. Commit and push to the plugin repo (`cc-data-science-team/`).

---

## Phase 3: Generate Handover Documents

### 3.1 Referee briefing

Create `documentation/referee-briefing.md` (or update if it exists) covering:

1. **What was done** — 3-sentence summary of the project, methodology, and key result
2. **How to read the output files** — column-by-column guide for every Excel/CSV in `results/`. Explain what each column means, what values to expect, and which columns require human judgement.
3. **Key numbers** — summary table of headline metrics from QA reports or result files
4. **What the referee should do** — prioritised action list (e.g. "review 74 flagged pairs", "check countries with 0% match rate")
5. **How to iterate** — pointer to the playbook and replication prompts

Source material: read PLAN.md, METHODOLOGY.md, any QA reports in `results/`, comparison reports, and result summary files. Do NOT fabricate numbers — extract them from the actual files.

### 3.2 Replication prompts

Create `results/replication_prompts.md` with one prompt per pipeline phase:

For each script in execution order, write:
- **Phase N: [Name]** heading
- **Prompt:** — the exact text to paste into Claude Coworker (self-contained, includes the script path and what to report after)
- **What it does:** — one sentence
- **Check after:** — what to verify in the output
- **To modify:** — which file/line/variable controls the key parameters

End with a "Full Pipeline" section that chains all phases in one prompt.

Include estimated runtime and cost where LLM API calls are involved.

---

## Phase 4: Package the Zip

### 4.1 Prepare staging area

Create a staging directory in `/tmp/{project-name}-handover/` containing:
- The full project folder (code, data, results, documentation, PLAN.md, METHODOLOGY.md)
- The referee briefing and replication prompts (already inside the project folder)
- A `.env` file in the project root with the required credentials (collected in Phase 1.3)

### 4.2 Patch hardcoded paths

For every script with hardcoded `.env` paths (identified in Phase 1.4):
- In the STAGED COPY (not the original), prepend `Path(__file__).resolve().parent.parent / ".env"` to the env_path search list
- This ensures the project-root `.env` is found first; original paths are harmless fallbacks

### 4.3 Exclude unnecessary files

Exclude from the zip:
- `.git/` directories
- `__pycache__/` directories
- `.DS_Store` files
- Any `venv/` or `.venv/` directories
- Any files larger than 50MB (warn the user about these)

### 4.4 Create README.md

Write a `README.md` at the zip root covering:
- Contents of the zip
- Setup instructions (place folder, credentials, install dependencies)
- Where to start (briefing → review Excel → playbook → prompts)
- Key files table

### 4.5 Create the zip

Create `{project-name}-handover.zip` in:
1. The project folder itself
2. `~/Desktop/` for easy access

Report the zip size and warn: "This zip contains real API credentials. Do not share over insecure channels."

---

## Phase 5: Commit and Push

### 5.1 Project repo

Stage and commit the new/updated files in the project folder:
- `documentation/referee-briefing.md`
- `results/replication_prompts.md`
- PLAN.md updates (if modified)
- The zip file

Commit message: `Add handover package for referee review`

Push.

### 5.2 Plugin repo

If a playbook was created or updated in `cc-data-science-team/`:
- Stage the playbook file
- Commit: `Add/Update {project-name} playbook for Claude Coworker`
- Push

---

## Output

When complete, report:

```
Handover Package: {project-name}
=================================

Zip: {path} ({size})
Contents:
  - Project folder with {N} scripts, {N} data files, {N} result files
  - .env with {N} credentials pre-filled
  - Referee briefing: documentation/referee-briefing.md
  - Replication prompts: results/replication_prompts.md ({N} phases)

Plugin:
  - Playbook: cc-data-science-team/playbook-{name}.md ({N} exercises)
  - Pushed to: {repo URL}

Pipeline:
  {script_1} → {script_2} → ... → {script_N}

Key parameters the referee can tweak:
  - {param}: {file}:{line} = {value}
  - {param}: {file}:{line} = {value}
  ...

Gaps: {None / list of uncovered methods}

⚠️  This zip contains real API credentials. Do not share over insecure channels.
```

## When to Use

- Before handing off an analytical project to a colleague for review
- When a referee needs to replicate or iterate on your methodology
- When archiving a project with full reproducibility documentation
- Before going on leave with active projects

## Implementation Notes

- This command creates files outside the current project (in the plugin repo). Confirm with the user before pushing to `cc-data-science-team`.
- The `.env` file in the zip contains real credentials. Always warn the user.
- If the project has no scripts (pure manual analysis), skip Phases 1.2-1.4 and 3.2, and produce only the briefing + result files in the zip.
- The plugin repo location is: `${CLAUDE_PLUGIN_ROOT}` (typically `~/Documents/GitHub/jf-private/claude-setup/cc-data-science-team/` on the author's machine)
- Credential sources to check (in order): project `.env`, `jf-thought/.env`, `jf-thought/sgept-analytics/data-queries/.env`, `jf-private/.env`
