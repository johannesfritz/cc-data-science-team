#!/usr/bin/env bash
# cc-data-science-team — Claude Code install script (standalone)
# Symlinks agents/rules (as data-science dir)/protocols/commands/skills/hooks/templates/examples into .claude/.

set -euo pipefail
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLUGIN_ROOT="$SCRIPT_DIR"
WORKSPACE_DIR="${CLAUDE_WORKSPACE_DIR:-$PWD}"
CLAUDE_DIR="$WORKSPACE_DIR/.claude"

echo "cc-data-science-team installer"
echo "  plugin root:  $PLUGIN_ROOT"
echo "  target:       $CLAUDE_DIR"
[ -d "$WORKSPACE_DIR" ] || { echo "ERROR: workspace not found" >&2; exit 1; }

mkdir -p "$CLAUDE_DIR"/{agents,rules,protocols,commands,skills,hooks}
shopt -s nullglob

for f in "$PLUGIN_ROOT/agents/"*.md;     do ln -sfn "$f" "$CLAUDE_DIR/agents/$(basename "$f")";    echo "  agent:    $(basename "$f")"; done
# rules/ as a directory link (matches the canonical jf-private sync convention)
[ -d "$PLUGIN_ROOT/rules" ] && ln -sfn "$PLUGIN_ROOT/rules" "$CLAUDE_DIR/rules/data-science" && echo "  rule-dir: data-science"
for f in "$PLUGIN_ROOT/protocols/"*.md;  do ln -sfn "$f" "$CLAUDE_DIR/protocols/$(basename "$f")"; echo "  protocol: $(basename "$f")"; done
for f in "$PLUGIN_ROOT/commands/"*.md;   do ln -sfn "$f" "$CLAUDE_DIR/commands/$(basename "$f")";  echo "  command:  $(basename "$f")"; done
for d in "$PLUGIN_ROOT/skills/"*/;       do ln -sfn "$d" "$CLAUDE_DIR/skills/$(basename "$d")"  && echo "  skill:    $(basename "$d")"; done
for f in "$PLUGIN_ROOT/hooks/"*;         do [ -f "$f" ] && ln -sfn "$f" "$CLAUDE_DIR/hooks/$(basename "$f")" && echo "  hook:     $(basename "$f")"; done

echo ""
echo "Install complete. Restart Claude Code (or /init); /query-gta, /analytics-ready, /red-team appear."
echo "cc-os is an optional companion for richer behaviour: provides the web-fetch primitive that web-extract wraps."
