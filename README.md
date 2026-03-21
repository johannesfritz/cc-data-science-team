# cc-data-science-team — Claude Code Data Science Configs

Team configuration for data science workflows: analytics orchestration, R code standards, applied econometrics, causal inference, and statistical review.

## Contents

| Directory | Count | Examples |
|-----------|-------|---------|
| `agents/` | 7 | analytics-manager, data-analyst, statistical-reviewer |
| `rules/` | 5 | r-code-standards, data-handling, chart-creation |
| `protocols/` | 5 | applied-econometrics, causal-inference, data-visualization |
| `commands/` | 3 | `/query-gta`, `/analytics-ready`, `/red-team` |

## Installation

```bash
git clone git@github.com:global-trade-alert/cc-data-science-team.git .claude-ds
mkdir -p .claude/agents .claude/rules .claude/protocols .claude/commands
for f in .claude-ds/agents/*.md; do ln -s "../../$f" .claude/agents/; done
ln -s ../../.claude-ds/rules .claude/rules/data-science
for f in .claude-ds/protocols/*.md; do ln -s "../../$f" .claude/protocols/; done
for f in .claude-ds/commands/*.md; do ln -s "../../$f" .claude/commands/; done
```

## License

Private — shared within team only.
