---
name: analytics
description: "Coordinate analytical projects: data preparation, R/Python analysis, statistical validation, and visualization. Use when user requests data analysis, chart creation, or statistical work on GTA/trade policy data."
---

# /analytics Skill

Show the analytics portfolio dashboard with all project statuses.

## Usage

```
/analytics
/analytics --active      # Show only active projects
/analytics --stale       # Show only stale projects (>7 days inactive)
/analytics --completed   # Show recently completed projects
```

## Behavior

When invoked, this skill:

1. **Scans project folders** in `jf-thought/sgept-analytics/data-queries/` for `*/PLAN.md` files
2. **Extracts project status** from each PLAN.md
3. **Detects stale projects** (no git activity >7 days)
4. **Generates dashboard** in markdown format

## Dashboard Format

```markdown
# Analytics Portfolio Dashboard

**Generated:** YYYY-MM-DD HH:MM

## Active Projects
| ID | Project | Status | Assigned | Started | Priority |
|----|---------|--------|----------|---------|----------|
| 1 | 260108 Trade Analysis | In Progress | Claude | 2026-01-08 | High |
| 2 | 260107 Subsidy Query | Review | Johannes | 2026-01-07 | Medium |

## Queued Projects
- 260108 ECB Request (awaiting data)

## Recently Completed (Last 7 Days)
- 260105 GTA Intervention Map (completed 2026-01-06)

## Stale Projects (>7 Days Inactive)
| Project | Last Activity | Status | Action Needed |
|---------|---------------|--------|---------------|
| 251215 GTA intermediary firms | 2025-12-20 | In Progress | Resume or archive |

## Summary
- **Active:** 2 projects
- **Queued:** 1 project
- **Completed (7d):** 1 project
- **Stale:** 1 project (needs attention)
```

## Implementation

### Step 1: Find All Projects

```bash
# Find all PLAN.md files in data-queries project folders
find data-queries -maxdepth 2 -name "PLAN.md" -type f
```

### Step 2: Parse PLAN.md Files

Extract from each PLAN.md:
- Status field (Queued | In Progress | Review | Complete)
- Created date (from ID or Created field)
- Assigned to (analyst name)
- Priority (Critical | High | Medium | Low)

### Step 3: Detect Stale Projects

```bash
# Get last git commit date for each project folder
cd data-queries
for dir in */; do
  last_commit=$(git log -1 --format="%ai" -- "$dir" 2>/dev/null)
  echo "$dir: $last_commit"
done
```

Project is stale if:
- Status is NOT "Complete"
- Last git activity >7 days ago

### Step 4: Generate Dashboard

Sort projects by:
1. Status (Active > Queued > Complete)
2. Priority (Critical > High > Medium > Low)
3. Last activity (most recent first)

## Status Detection

Parse status from PLAN.md frontmatter:

```markdown
**Status:** In Progress
```

Valid statuses:
- `Queued` - Created but not started
- `In Progress` - Actively being worked on
- `Review` - Analysis complete, awaiting review
- `Complete` - Finished and delivered

## Output Modes

### Default (Full Dashboard)

Shows all sections: Active, Queued, Completed, Stale

### --active Flag

Only shows projects with status "In Progress" or "Review"

### --stale Flag

Only shows projects needing attention:
- Not complete AND last activity >7 days ago

### --completed Flag

Shows projects completed in last 30 days

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No projects found | Empty repository or wrong directory | Verify data-queries directory exists |
| PLAN.md parse error | Malformed frontmatter | Fix PLAN.md format |
| Git history unavailable | Not a git repo | Fall back to file modification date |

## Integration

The dashboard informs:
- **analytics-manager** - For prioritization decisions
- **analyst-orchestrator** - To pick next project
- **User** - For oversight and planning

## Proactive Invocation

This skill should be suggested when:
1. User asks about project status
2. User starts a new session working with data-queries
3. analytics-manager needs portfolio overview
4. Planning which project to work on next
