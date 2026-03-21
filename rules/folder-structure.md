---
paths:
  - sgept-analytics/**
  - "*/data-queries/**"
---

# Folder Structure Standards

**Purpose:** Maintain tidy, clearly understandable folder structures across all analytical projects. This rule applies to both data query projects and publication projects.

---

## Core Principles

1. **Self-documenting structure** - A new team member should understand the project from folder names alone
2. **Version control at folder level** - Use prefixes (`v0-`, `v1-`) not date suffixes
3. **Deliverables separate from drafts** - Final outputs distinct from working materials
4. **Supporting materials grouped** - Verification, prior art, data dictionaries together
5. **README explains structure** - Every complex folder gets a README.md

---

## Standard Data Query Project

Created by `/new-analysis`, suitable for straightforward data requests:

```
YYMMDD-project-title/
├── code/              # R/Python scripts (numbered: 0_, 1_, 2_)
│   ├── PIPELINE.md        ← How to reproduce the full pipeline (MANDATORY for production projects)
│   ├── progress_log.md    ← Step-by-step execution log (MANDATORY)
│   └── run_pipeline.sh    ← Single-command executor (required if pipeline has 3+ scripts)
├── data/              # Input datasets
│   └── versions/      # Versioned dataset snapshots (when re-running)
├── results/           # Final outputs (Excel, PNG, CSV)
├── documentation/     # Methodology notes, original request
└── PLAN.md            # Project plan and progress tracking
```

**When to use:** Single-output projects, data extraction requests, chart generation.

---

## Extended Publication Project

For projects producing multiple analytical pieces (blog series, reports, papers):

```
YYMMDD-project-title/
├── code/                          # Scripts (unchanged)
├── data/                          # Input datasets (unchanged)
├── analysis/                      # Analytical outputs
│   ├── README.md                  # Documents the structure
│   ├── 01-[first-deliverable]/    # Numbered for logical order
│   │   ├── v0-original.md         # First draft
│   │   └── v1-revised.md          # Current working version
│   ├── 02-[second-deliverable]/
│   │   ├── [current-version].md   # No prefix = current
│   │   └── drafts/                # Earlier versions
│   └── supporting/                # Background materials
│       ├── DATA_DICTIONARY.md
│       ├── EMPIRICAL_QUESTIONS.md
│       ├── PRIOR_ART_REPORT.md
│       └── verification/          # Verification work
├── SERIES_STRATEGY.md             # Master planning (root level)
└── PLAN.md                        # Project plan
```

**When to use:** Blog series, multi-piece reports, academic papers, any project with multiple distinct deliverables.

---

## Naming Conventions

### Folders

| Type | Convention | Example |
|------|------------|---------|
| Project root | `YYMMDD-title` | `260126-sc-launch-pieces` |
| Deliverable subfolders | `NN-kebab-case` | `01-methodological-explainer` |
| Supporting folders | Lowercase, descriptive | `supporting`, `verification`, `drafts` |

### Files

| Type | Convention | Example |
|------|------------|---------|
| Current working version | Descriptive, no prefix | `piece1-transparency.md` |
| Versioned drafts | `vN-descriptor.md` | `v0-original.md`, `v1-revised.md` |
| Archived drafts | Move to `drafts/` or `drafts/archive/` | `drafts/option_A_standalone.md` |
| R scripts | Numbered prefix | `0_data_prep.R`, `1_analysis.R` |

### Version Control

```
Version prefixes:
  v0- = Original/first draft
  v1- = First revision
  v2- = Second revision
  (no prefix) = Current working version (for files past initial drafting)

Draft management:
  - Active drafts: In deliverable folder with version prefix
  - Superseded drafts: Move to drafts/ subfolder
  - Abandoned approaches: Move to drafts/archive/
```

---

## Progress Log (`code/progress_log.md`) — MANDATORY

Every analytical project must maintain a `progress_log.md` in the `code/` folder. This is the single source of truth for what happened during the project.

### Format

```markdown
# Progress Log — [Project Title]

## Steps

| # | Timestamp | Script | Summary |
|:-:|-----------|--------|---------|
| 1 | 2026-02-25 10:00 | `0_data_prep.R` | Loaded 15,234 rows from GTA. Filtered to 2020-2025. |
| 2 | 2026-02-25 10:15 | `1_analysis.R` | Computed growth rates. 3 outliers flagged and documented. |
| — | — | — | **v1 dataset archived to `data/versions/v1-initial/`** |
| 3 | 2026-02-25 14:00 | `1_analysis.R` | Re-ran with corrected methodology. v2 output. |

## Key Decisions

- [Date]: [Decision and rationale]
```

### Rules

1. **Update after every script execution** — not at the end of the session
2. **Include row counts, file counts, error counts** — quantitative, not just "ran script"
3. **Mark version snapshots** when re-running produces new outputs
4. **Record key decisions** — methodology changes, model choices, parameter selections
5. **Review at session start** — read the log to understand where the project left off

### Agent responsibility

The analyst-orchestrator and data-analyst agents MUST:
- Create `code/progress_log.md` at project start, or when entering a project that doesn't have one (legacy initialization — see `project-folder-structure.md`)
- Append a row after each script execution
- Review the log when resuming a project across sessions
- If the log is missing: create it immediately from observed state before proceeding with any analysis work. Do not proceed without a log.

---

## PIPELINE.md — Pipeline Playbook

Every analytical project with a multi-script pipeline must have `code/PIPELINE.md`.
This is the document a cold-start session reads to reproduce the full analysis.

### Required sections

1. **One-command execution** → `./code/run_pipeline.sh` (if applicable)
2. **Pipeline steps table** → Script | Outputs | Notes, in execution order
3. **Data sources** → File | What it is | How produced
4. **Published outputs** → Asset | S3 URL for every public-facing file
5. **Archive convention** → Where/how to archive before overwriting
6. **Environment** → Dependencies, credentials location, working directory

### When to create

Production projects (multi-script pipeline, S3 uploads). Create BEFORE the first script run.

### When to update

- New script added to pipeline
- New S3 upload target added (every public URL must appear here)
- Dependencies or credentials change

### Agent responsibility

Before executing any script: verify `code/PIPELINE.md` exists. If missing — create it from
observed state immediately. Never add an S3 upload without adding it to the published outputs table.

---

## Dataset Versioning (`data/versions/`)

When a pipeline is re-run with different parameters, models, or methodology, the previous output must be preserved for comparison.

### When to version

- Re-running extraction/classification with a different model
- Changing inclusion/exclusion criteria
- Applying new filters (e.g. jurisdiction check) that remove entries
- Any change that produces a materially different output dataset

### Structure

```
data/versions/
├── README.md                  # Documents each version
├── v1-initial/                # First run
│   ├── results_by_theme.json
│   └── summary.md
└── v2-revised-criteria/       # Second run
    ├── results_by_theme.json
    └── summary.md
```

### README.md format

Each version entry must record:
- **Date** of the run
- **Method** (pipeline steps, model used)
- **Key parameters** (inclusion criteria, filters applied)
- **Result summary** (row counts, key metrics)
- **What changed** from the previous version

### Rules

1. **Version before overwriting** — copy current outputs to `data/versions/vN-descriptor/` before re-running
2. **Name descriptively** — `v1-initial`, `v2-strict-criteria`, not `v1`, `v2`
3. **Include both data and results** — the version should be self-contained for comparison
4. **Never delete versions** — they are the audit trail

---

## When to Upgrade to Extended Structure

Upgrade from standard to extended structure when:

1. **Multiple distinct outputs** - More than one report, blog post, or paper
2. **Parallel workstreams** - Different pieces targeting different audiences
3. **Complex versioning needs** - Multiple drafts requiring comparison
4. **Supporting materials accumulate** - Prior art reports, verification work, data dictionaries

**How to upgrade:**
1. Create `analysis/` folder
2. Create numbered subfolders for each deliverable
3. Move existing drafts into appropriate subfolders with version prefixes
4. Create `analysis/supporting/` for background materials
5. Create `analysis/README.md` documenting the structure

---

## Quality Gate: Folder Hygiene

Before marking a project complete, verify:

### Standard Projects
- [ ] All scripts in `code/` with numbered prefixes
- [ ] All outputs in `results/`
- [ ] No loose files in project root (except PLAN.md)
- [ ] PLAN.md updated with completion status
- [ ] PIPELINE.md exists and covers all pipeline steps (production projects only)
- [ ] PIPELINE.md lists all S3 URLs for published outputs

### Extended Projects (Additional Checks)
- [ ] `analysis/README.md` exists and documents structure
- [ ] Deliverable folders use numbered prefixes (`01-`, `02-`)
- [ ] Current versions clearly identifiable (either no prefix or highest `vN-`)
- [ ] Superseded drafts in `drafts/` subfolders, not cluttering main folders
- [ ] Supporting materials grouped in `analysis/supporting/`
- [ ] No broken relative paths in moved code files

---

## Autonomous Reorganisation

Agents MAY reorganise folder structures autonomously when:

1. **Files are misplaced** - Drafts mixed with finals, supporting materials scattered
2. **Version control is unclear** - Multiple versions without clear current version
3. **Structure is undocumented** - Complex folder lacks README
4. **Upgrade is warranted** - Project has grown to need extended structure

**Autonomous reorganisation protocol:**

1. **Assess current state** - List all files, identify misplacements
2. **Plan reorganisation** - Map current → target structure
3. **Create new folders** - Build target structure
4. **Move files** - Relocate with clear version naming
5. **Fix relative paths** - Update any code referencing moved files
6. **Create README** - Document the new structure
7. **Report changes** - Summarise what was moved and why

**Do NOT reorganise when:**
- User is actively editing files (check recent modification times)
- Project has uncommitted git changes that might be lost
- Reorganisation would break external references (published URLs, shared paths)

---

## Integration with Agents

### analyst-orchestrator

At project completion, verify folder hygiene as final quality gate:
- Standard structure checklist (above)
- Extended structure checklist if `analysis/` folder present

### new-analysis skill

When creating projects, ask:
- "Will this project have multiple distinct deliverables?" → If yes, create extended structure
- Otherwise → Create standard structure

### research-director / writing-lead

When working on publication projects:
- Verify `analysis/` folder exists and is properly structured
- Create deliverable subfolders for new pieces
- Move drafts to appropriate version locations

---

## Examples

### Good: Clear structure, self-documenting

```
260126-sc-launch-pieces/
├── analysis/
│   ├── README.md
│   ├── 01-methodological-explainer/
│   │   ├── v0-original.md
│   │   └── v1-revised.md
│   ├── 02-analytical-series/
│   │   ├── piece1-transparency.md
│   │   └── drafts/archive/
│   └── supporting/
│       └── verification/
├── code/
├── data/
└── PLAN.md
```

### Bad: Cluttered, unclear versioning

```
260126-sc-launch-pieces/
├── DRAFT_piece0_release.md
├── DRAFT_piece0_release_v2.md
├── DRAFT_piece0_release_v3.md
├── FINAL_piece1_transparency.md
├── analysis/
│   ├── DATA_DICTIONARY.md
│   ├── VERIFICATION_REPORT.md
│   ├── archive/
│   │   └── (6 files mixed together)
│   └── verification_code.R
├── prior-art-report.md (duplicate!)
└── inbox/
    └── Explainer.md (orphaned)
```

---

## Enforcement

This rule is enforced through:

1. **SubagentStart hooks** - Remind agents of folder structure standards
2. **Quality gates** - Folder hygiene check before project completion
3. **Autonomous reorganisation** - Agents can tidy up autonomously
4. **Review prompts** - Ask "Is the folder structure clear?" at milestones
