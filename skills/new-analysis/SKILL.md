---
name: new-analysis
description: "Scaffold a new analytical project with YYMMDD folder structure (code/, data/, results/, docs/). Use when starting a new analysis, research project, or data investigation."
---

# /new-analysis Skill

Create a new analytical project with proper folder structure and PLAN.md.

## Usage

```
/new-analysis [Project Title]
/new-analysis GTA Tariff Impact Study
/new-analysis ECB Trade Data Request
```

## Behavior

When invoked, this skill:

1. **Generates folder name** with YYMMDD prefix from current date
2. **Creates folder structure** in `jf-thought/sgept-analytics/data-queries/`:
   ```
   jf-thought/sgept-analytics/data-queries/YYMMDD-project-title/
   ├── code/
   ├── data/
   ├── results/
   ├── documentation/
   └── PLAN.md
   ```
3. **Populates PLAN.md** from template with project details
4. **Saves original request** in documentation/

## Folder Naming

Format: `YYMMDD-project-title` (lowercase, hyphens, no spaces)

Examples:
- `260108-gta-tariff-impact-study`
- `260108-ecb-trade-data-request`
- `260107-subsidy-analysis`

## PLAN.md Template

The generated PLAN.md includes:

```markdown
# Analysis Plan: [Project Title]

**ID:** PROJ-YYMMDD-NNN
**Created:** YYYY-MM-DD
**Requested by:** [To be filled]
**Assigned to:** [To be filled]
**Language:** [R / Python / Mixed]
**Status:** Queued

## Original Request
[Copy of the original request/prompt]

## Approach
1. Data sources: [To be determined]
2. Methodology: [To be determined]
3. Output format: [Excel/CSV/Charts/Report]

## Implementation Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| | | |

## Quality Checks
- [ ] Data validation passed
- [ ] Statistical sanity checks passed
- [ ] Visualization review passed
- [ ] Output verification complete

## Deliverables
- [ ] results/output.xlsx
- [ ] results/charts.png
- [ ] documentation/methodology.md

## Completion
**Completed:** N/A
**Reviewed by:** N/A
**Notes:** N/A

## Audit Trail
| Date | Action | By |
|------|--------|-----|
| YYYY-MM-DD | Project created | Claude Code |
```

## Implementation

### Step 1: Parse Arguments

Extract project title from command arguments.

### Step 2: Generate Folder Name

```python
from datetime import datetime
date_prefix = datetime.now().strftime("%y%m%d")
folder_name = f"{date_prefix}-{project_title.lower().replace(' ', '-')}"
```

### Step 3: Create Directory Structure

```bash
cd data-queries
mkdir -p "$folder_name"/{code,data,results,documentation}
```

### Step 4: Create PLAN.md

Populate template with:
- Current date
- Project title
- Sequential project ID (scan existing folders)

### Step 5: Save Original Request

If user provided context beyond title, save to:
```
documentation/original_request.txt
```

## Output

After successful creation:

```
Created new project: jf-thought/sgept-analytics/data-queries/260108-gta-tariff-impact-study

Folder structure:
  260108-gta-tariff-impact-study/
  ├── code/           (R/Python scripts)
  ├── data/           (input files)
  ├── results/        (output files)
  ├── documentation/  (notes, original request)
  └── PLAN.md         (project plan)

Next steps:
1. Edit PLAN.md to add approach and data sources
2. Place input data in data/
3. Create analysis scripts in code/
4. Run /analytics to see project in dashboard
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Folder already exists | Same title on same day | Add numeric suffix (e.g., `260108-gta-study-2`) |
| Invalid characters | Special chars in title | Sanitize title (remove /, \, :, etc.) |
| No title provided | Empty argument | Prompt user for title |

## Integration

After creation, the project appears in:
- `/analytics` dashboard as "Queued"
- analytics-manager tracking

To start work:
1. Navigate to project folder
2. Run analyst-orchestrator agent
3. Or manually execute scripts
