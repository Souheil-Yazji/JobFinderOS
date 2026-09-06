#!/usr/bin/env bash
# Preflight for local Claude Code skill automation.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0
echo "=== JobScoutOS local runner preflight ==="

CLAUDE_BIN="${CLAUDE_BIN:-$(command -v claude || true)}"
if [[ -z "$CLAUDE_BIN" || ! -x "$CLAUDE_BIN" ]]; then
  echo "FAIL: claude CLI not in PATH (install Claude Code CLI or set CLAUDE_BIN)"
  fail=1
else
  echo "OK: claude at $CLAUDE_BIN ($("$CLAUDE_BIN" --version 2>/dev/null | head -1))"
fi

if [[ ! -d "$ROOT/vault" ]]; then
  echo "FAIL: vault/ missing under $ROOT"
  fail=1
else
  echo "OK: vault/ present"
fi

for skill in jobs-daily mark-weekly jobs-priority-watch; do
  if [[ -f "$ROOT/.claude/commands/${skill}.md" ]]; then
    echo "OK: skill .claude/commands/${skill}.md"
  else
    echo "WARN: missing .claude/commands/${skill}.md"
  fi
done

if [[ -x "$ROOT/scripts/JobScoutOS_run_skill.sh" ]]; then
  echo "OK: JobScoutOS_run_skill.sh executable"
else
  echo "FAIL: scripts/JobScoutOS_run_skill.sh missing or not executable"
  fail=1
fi

if [[ "$fail" -eq 0 && -n "${CLAUDE_BIN:-}" ]]; then
  echo
  echo "--- claude auth status ---"
  if ! "$CLAUDE_BIN" auth status 2>&1; then
    echo "FAIL: claude auth status (run: claude auth login)"
    fail=1
  fi
fi

exit "$fail"
